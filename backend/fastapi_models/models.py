from pydantic import BaseModel
from typing import List

class GetDataSet(BaseModel):
    db: str
    col: str

class PostFilter(BaseModel):
    filter: str

class PostDataSetDesc(BaseModel):
    database: str
    collection: str
    dataset_display_title: str
    short_description: str
    dataset_description: str
    usability: str
    created_by: str
    image: str

class Comment(BaseModel):
    id: int
    person: str
    text: str

class Comments(BaseModel):
    comments: List[Comment] = []