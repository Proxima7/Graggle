from pydantic import BaseModel
from typing import List
from numpy import ndarray


class DatabaseCollections(BaseModel):
    """Dataset keys"""
    database_name: str
    collection_names: List[str]


class Databases(BaseModel):
    """List of datasets"""
    databases: List[DatabaseCollections]


class Document(BaseModel):
    """Container for documents with different format"""
    document: dict


class DatasetDescriptor(BaseModel):
    """Dataset detail informations"""
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
    """List of dataset details for update job"""
    datasetdescriptors: List[DatasetDescriptor]


class DatasetDescription(BaseModel):
    """Description for a single dataset incl. detailed descriptors"""
    database: str
    collection: str
    dataset_display_title: str
    short_description: str
    dataset_description: str
    image: str
    generated: bool
    descriptors: DatasetDescriptor