from bson import json_util
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import copy
import uvicorn
from fastapi_models.models import *
import json
import utils
from cron import Cron
from env_helper import set_env
from static import Static
from data_access import data_transfer_impl_mongoDB_minioS3
from data_access.data_transfer_objects import DatasetDescription, DatasetDescriptor

# Start Service
app = FastAPI(
    title="ProductText",
    description="Text based classification of products",
    version="0.0.1",
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
Static.configureStatic(app)

set_env()
dti = data_transfer_impl_mongoDB_minioS3.DataTransferMongoDBMinioS3()
mdti = data_transfer_impl_mongoDB_minioS3.MetadataTransferMongoDBMinioS3()

@app.on_event("startup")
async def startup_event():
    cronjob = Cron(dti, mdti)
    cronjob.updater()

@app.get("/")
def root():
    return {"Graggle root - API available under /docs"}

@app.get("/databases")
def get_databases_with_collections() -> dict:
    databases = dti.get_databases()
    return databases

@app.post("/datasets/filter")
def get_databases_filtered(data: PostFilter) -> dict:
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

import cv2
@app.get("/dataset/document/{db}/{col}/{number}/{filter}")
def get_document_of_database_and_collection_with_filter(db: str, col: str, number: int, filter: str, low_resolution: bool = False) -> dict:
    filtered_document = dti.get_document(db, col, number, filter)
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
    dsc = mdti.get_dataset_description(db, col)
    if dsc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return dsc

@app.post("/dataset/description")
def create_dataset_description(data: PostDataSetDesc) -> dict:
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
                                             image=utils.convert_base_64_to_ndarray(data.image) if data.image != "" else "",
                                             generated=False,
                                             descriptors=dataset_descriptor)

    ids = mdti.create_dataset_description(dataset_description)
    if len(ids) != 0:
        return {"status": "created"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="creation failure")

@app.get("/dataset/comments/{db}/{col}")
def get_dataset_comments(db: str, col: str) -> dict:
    comment1 = Comment(id=1, person="Mr. Lorem Ipsum", text="Very good dataset!")
    comment2 = Comment(id=2, person="Mr. Lorem Ipsum", text="Sometimes is the image quality a little bit bad")
    comment3 = Comment(id=3, person="Mr. Lorem Ipsum", text="Used in the Object Detection Model V5 for SpecialCases")
    return Comments(comments=[comment1, comment2, comment3])




import os
if __name__ == "__main__":
    my_port = int(os.getenv("APP_PORT"))
    my_root_path = os.getenv("ENDPOINT_PREFIX")
    if my_root_path and len(my_root_path) > 0:
        uvicorn.run(app, host="0.0.0.0", port=my_port, root_path=my_root_path)
    else:
        uvicorn.run(app, host="0.0.0.0", port=my_port, root_path="")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
