from fastapi import FastAPI, status, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

import os
import cv2
import uvicorn
import base64
from globals import configure_logging, logger
from fastapi_models.models import *
from util import utils
from util.updater import Updater
from fastapi_hosting.environment_helper import set_necessary_environment
from fastapi_hosting.frontend_files_hosting import Static
from data_access import data_transfer_impl_mongoDB_minioS3
from data_access.data_transfer_objects import DatasetDescription, DatasetDescriptor, Bookmarkgroups



# Start Service + Description
app = FastAPI(
    title="Graggle Cloud Backend",
    description="Graggle Cloud Backend for frontend provision and database/data-storage connection",
    version="0.1.0",
    root_path=""
)

# CORS header
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', '*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=3600
)

# Provision of Frontend delivered by the Backend
Static.configureStatic(app)

# Environmeht configuration
set_necessary_environment()

# data-storage implementation
# minio s3 (amazon s3 like) for image data
# + mongodb for image references and metadata
dti = data_transfer_impl_mongoDB_minioS3.DataTransferMongoDBMinioS3()
mdti = data_transfer_impl_mongoDB_minioS3.MetadataTransferMongoDBMinioS3()
ud = data_transfer_impl_mongoDB_minioS3.UserdataMongoDBMinioS3()

@app.on_event("startup")
async def startup_event():
    # run the dataset metadata update job
    # at startup and then every 24 hour
    # updates e.g. number of images per dataset, calc. dataset size, provides preview image, aso.
    updater_job = Updater(dti, mdti)
    updater_job.cycling_updat()

@app.get("/")
def root():
    """
    Root endpoint of th webserver

    Returns: plain-text information the the API doc can be found
    """
    return {"Graggle root - API available under /docs"}

@app.get("/databases")
def get_databases_with_collections() -> dict:
    logger.debug(f"Endpoint: GET:/databases")
    """
    Endpoint to get all available datasets.

    Returns: List with all available datasets
    """
    databases = dti.get_databases()
    return databases

@app.post("/datasets/filter")
def get_databases_filtered(data: PostFilter) -> dict:
    logger.debug(f"Endpoint: GET:/dataset/document/ with {data}")
    """
    Endpoint to filter datasets.
    Args:
        data: PostFilter containing the filter string

    Returns: List of datasets matching to the filter criteria

    """
    datasets_details = mdti.get_datasets_details()

    if data.filter != "":
        filtered_list_database = [d for d in datasets_details.datasetdescriptors if data.filter.lower() in d.database.lower()]
        filtered_list_collection = [d for d in datasets_details.datasetdescriptors if data.filter.lower() in d.collection.lower()]
        merged_list = filtered_list_database.copy()
        merged_list.extend(filtered_list_collection)

        unique_keys = set((d.database, d.collection) for d in merged_list)
        # unique_dicts = [dict(zip(('database', 'collection'), k)) for k in unique_keys]

        filtered_datasetdescriptors = [d for d in merged_list if (d.database, d.collection) in unique_keys]
        datasets_details.datasetdescriptors = filtered_datasetdescriptors

    if len(datasets_details.datasetdescriptors) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return datasets_details

@app.get("/dataset/document/{db}/{col}/{skip_count}/{base64_filter}")
def get_document_of_database_and_collection_with_filter(db: str, col: str, skip_count: int, base64_filter: str, low_resolution: bool = False) -> dict:
    logger.debug(f"Endpoint: GET:/dataset/document/{db}/{col}/{skip_count}/{base64_filter}")
    """
    Endpoint to query/filter for a specific document based on the parameters.

    Args:
        db: database (depends on implementation)
        col: collection (depends on implementation)
        skip_count: number of documents to skip
        base64_filter: filter in collection (base64 encoded because of special chars)
        low_resolution: boolean to control if original sized or reduced sized image should be returned

    Returns: Single document that matches the incoming arguments
    """
    filter = base64.b64decode(base64_filter).decode('utf-8')
    filtered_document = dti.get_document(db, col, skip_count, filter)
    if filtered_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if "image" in filtered_document.document:
        image = filtered_document.document["image"] if not low_resolution else cv2.resize(filtered_document.document["image"], (320, 240))
        filtered_document.document["image"] = "data:image/png;base64," + utils.convert_ndarray_to_base_64(image)
    if "image_data" in filtered_document.document:
        image = filtered_document.document["image_data"] if low_resolution else cv2.resize(filtered_document.document["image_data"], (320, 240))
        filtered_document.document["image_data"] = "data:image/png;base64," + utils.convert_ndarray_to_base_64(image)

    return filtered_document




@app.get("/dataset/description/{db}/{col}")
def get_dataset_description(db: str, col: str) -> dict:
    logger.debug(f"Endpoint: GET:/dataset/description/{db}/{col}")
    """
    Endpoint to get the dataset description based on the parameter.

    Args:
        db: database (depends on implementation)
        col: collection (depends on implementation)

    Returns: Detailed dataset description

    """
    dsc = mdti.get_dataset_description(db, col)
    if dsc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return dsc

@app.post("/dataset/description")
def insert_dataset_description(data: PostDataSetDesc) -> dict:
    logger.debug(f"Endpoint: POST:/dataset/description with {data}")
    """
    Endpoint to add a dataset description.

    Args:
        data: Dataset description information

    """
    dataset_descriptor = DatasetDescriptor(database=data.database,
                                           collection=data.collection,
                                           number_of_documents="0",
                                           size_mb="0",
                                           created="01.01.2001",
                                           last_update="01.01.2001",
                                           image="",
                                           usability=data.usability,
                                           created_by=data.created_by,
                                           annotation_types="dummy")

    dataset_description = DatasetDescription(database=data.database,
                                             collection=data.collection,
                                             dataset_display_title=data.dataset_display_title,
                                             short_description=data.short_description,
                                             dataset_description=data.dataset_description,
                                             image=data.image if data.image != "" else "",
                                             generated=False,
                                             descriptors=dataset_descriptor)

    ids = mdti.insert_dataset_description(dataset_description)
    if len(ids) != 0:
        return Response(status_code=201, content=None)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="creation failure")

@app.get("/dataset/comments/{db}/{col}")
def get_dataset_comments(db: str, col: str) -> dict:
    logger.debug(f"Endpoint: GET: /dataset/comments/{db}/{col}")
    """
    Endpoint to get the comments for a dataset
    Args:
        db: database (depends on implementation)
        col: collection (depends on implementation)

    Returns: List of comments with comment creators

    """
    comment1 = Comment(id=1, person="Mr. Lorem Ipsum", text="Comment no.1")
    comment2 = Comment(id=2, person="Mr. Lorem Ipsum", text="Comment no.2")
    comment3 = Comment(id=3, person="Mr. Lorem Ipsum", text="Comment no.3")
    return Comments(comments=[comment1, comment2, comment3])

@app.get("/bookmarkgroups")
def get_bookmark_group() -> Bookmarkgroups:
    logger.debug(f"Endpoint: GET:/bookmarkgroups")
    bookmarkgroups = ud.get_bookmark_groups()
    return bookmarkgroups

@app.post("/bookmarkgroups")
def post_bookmark_group(bookmarkgroups: Bookmarkgroups):
    logger.debug(f"Endpoint: POST:/bookmarkgroups with {bookmarkgroups}")
    ids = ud.set_bookmark_groups(bookmarkgroups)

    if len(ids) != 0:
        return Response(status_code=201, content=None)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="creation failure post_bookmark_group")


@app.get(f"/health/live")
def health():
    """
    Health endpoint for webservice lifetime check

    Returns: Is alive response
    """
    return {"status": "ok"}



if __name__ == "__main__":
    """
        Main start of webserver
    """
    configure_logging()

    my_port = int(os.getenv("APP_PORT"))
    logger.warning(f'Using PORT:{my_port}')

    my_root_path = os.getenv("ENDPOINT_PREFIX")
    logger.warning(f'Using ENDPOINT_PREFIX:{my_root_path}')

    if my_root_path and len(my_root_path) > 0:
        uvicorn.run(app, host="0.0.0.0", port=my_port, root_path=my_root_path, limit_concurrency=50, log_level="warning")
    else:
        uvicorn.run(app, host="0.0.0.0", port=my_port, root_path="", limit_concurrency=50, log_level="warning")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
