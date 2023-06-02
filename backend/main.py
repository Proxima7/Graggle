from bson import json_util
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from typing import List
import uvicorn
from fastapi_models.models import *
from db_manager import DBManager
import json
import utils
from cron import Cron
from env_helper import set_env
from static import Static


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
dbm = DBManager()

@app.on_event("startup")
async def startup_event():
    cronjob = Cron(dbm)
    cronjob.updater()

@app.get("/")
def root():
    return {"Graggle root - API available under /docs"}

@app.get("/get/databases")
def get_databases() -> List[dict]:
    dbs = dbm.get_databases()
    return json.loads(json_util.dumps(dbs))

@app.post("/post/dataset/documents")
def get_dataset_documents(data: GetDataSet) -> List[dict]:
    dsc = DBManager().get_dataset_documents("fruit-recognition", "flickr")
    return json.loads(json_util.dumps(dsc[0]))

import cv2
@app.get("/data/{db}/{col}/{number}/{filter}")
def get_real_data(db: str, col: str, number: int, filter: str, low_resolution: bool = False) -> dict:
    try:
        query = json.loads(filter)
    except json.JSONDecodeError:
        query = {}

    data = dbm.get_data(db, col, number, query)
    if len(data)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if "image" in data[0]:
        image = data[0]["image"] if not  low_resolution else cv2.resize(data[0]["image"], (320, 240))
        data[0]["image"] = "data:image/png;base64," + utils.convert_ndarray_to_base_64(image)
    if "image_data" in data[0]:
        image = data[0]["image_data"] if low_resolution else cv2.resize(data[0]["image_data"], (320, 240))
        data[0]["image_data"] = "data:image/png;base64," + utils.convert_ndarray_to_base_64(image)
    return json.loads(json_util.dumps(data[0]))

@app.post("/datasets/filter")
def get_datasets(data: PostFilter) -> dict:
    datasets = dbm.get_dataset()

    if data.filter != "":
        filtered_list_database = [d for d in datasets if data.filter.lower() in d['database'].lower()]
        filtered_list_collection = [d for d in datasets if data.filter.lower() in d['collection'].lower()]
        merged_list = filtered_list_database.copy()
        merged_list.extend(filtered_list_collection)

        unique_keys = set((d['database'], d['collection']) for d in merged_list)
        #unique_dicts = [dict(zip(('database', 'collection'), k)) for k in unique_keys]

        datasets = [d for d in merged_list if (d['database'], d['collection']) in unique_keys]

    if len(datasets) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=datasets)

@app.get("/dataset/description/{db}/{col}")
def get_dataset_description(db: str, col: str) -> dict:
    dsc = dbm.get_dataset_description(db, col)
    if len(dsc)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        dsc[0]["image"] = "data:image/png;base64," + utils.convert_ndarray_to_base_64(dsc[0]["image"])
    except Exception as e:
        pass
    return json.loads(json_util.dumps(dsc[0]))

@app.post("/dataset/description")
def post_dataset_description(data: PostDataSetDesc) -> dict:
    print("post_dataset_description")
    dataset_description = {}
    dataset_description["database"] = data.database
    dataset_description["collection"] = data.collection
    dataset_description["dataset_display_title"] = data.dataset_display_title
    dataset_description["short_description"] = data.short_description
    dataset_description["dataset_description"] = data.dataset_description
    dataset_description["image"] = utils.convert_base_64_to_ndarray(data.image) if data.image != "" else ""

    descriptors = {}
    descriptors['usability'] = data.usability
    descriptors['created_by'] = data.created_by
    descriptors['created'] = "01.03.2021"
    descriptors['last_update'] = "02.03.2021"
    descriptors['size_mb'] = 0
    descriptors['number_of_documents'] = 0
    descriptors['annotation_types'] = ["dummy", "flummy"]
    dataset_description['descriptors'] = descriptors
    ids = dbm.set_dataset_description(dataset_description)
    if len(ids) != 0:
        return {"status": "created"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="creation failure")

@app.get("/dataset/comments/{db}/{col}")
def get_dataset_comments(db: str, col: str) -> dict:
    comment1 = Comment(id=1, person="Raphael Geng", text="Very good dataset!")
    comment2 = Comment(id=2, person="Raphael Geng", text="Sometimes is the image quality a little bit bad")
    comment3 = Comment(id=3, person="Pascal Iwohn", text="Used in the Object Detection Model V5 for DIJ")
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
