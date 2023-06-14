from pydantic import BaseModel
from typing import List


class DatabaseCollections(BaseModel):
    database_name: str
    collection_names: List[str]


class Databases(BaseModel):
    databases: List[DatabaseCollections]


class Document(BaseModel):
    document: dict


class DatasetDescriptor(BaseModel):
    database: str
    collection: str
    number_of_documents: str
    size_mb: str
    created: str
    last_update: str
    image: str
    usability: str
    created_by: str
    annotation_types: str


class Datasets(BaseModel):
    datasetdescriptors: List[DatasetDescriptor]


class DatasetDescription(BaseModel):
    database: str
    collection: str
    dataset_display_title: str
    short_description: str
    dataset_description: str
    image: str
    generated: bool
    descriptors: DatasetDescriptor