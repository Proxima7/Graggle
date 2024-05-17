from data_access.data_transfer_interface import DataTransferInterface
from data_access.data_transfer_interface import MetadataTransferInterface
from data_access.data_transfer_interface import UserSessionInterface
from data_access.data_transfer_objects import Databases, DatabaseCollections, Bookmarkgroups, Bookmarkgroup, Dataset
from data_access.data_transfer_objects import Document
from data_access.data_transfer_objects import DatasetDescription, DatasetDescriptor

from database_accessor.utils import vault_reader
from database_accessor import get_collection_interface


import pymongo
import json
import ast
from globals import logger
from bson.objectid import ObjectId
import cv2
from util import utils
import numpy as np

mongodb_con_string = vault_reader.read_value(f"prod_mongodb_con_string_admin".upper(), vault="prod")
my_mongo_client = pymongo.MongoClient(mongodb_con_string)
temp_descriptors = []
#db_accessor = get_db_accessor(mongo_instance="prod", con_string_name="mongodb_con_string_admin")

DB_KEY_SEPARATOR = "###"
INSTANCE = "prod"
class DBC:
    interface_pool = {}

    def get_interface(self, db, col):
        db_key = f"{db}{DB_KEY_SEPARATOR}{col}"  
        
        if db_key not in self.interface_pool:
            # create new interface, first access
            db_accessor_new = get_collection_interface(db, col, INSTANCE)
            self.interface_pool[db_key] = db_accessor_new

        return self.interface_pool[db_key]
    

class UserdataMongoDBMinioS3(UserSessionInterface):

    def __init__(self):
        self.dbc = DBC()
        self.interface = self.dbc.get_interface("graggle", "bookmarkgroups")
    
    def get_bookmark_groups(self) -> Bookmarkgroups:
        dbgroups = self.interface.get_data(return_images=False, query={})
        if len(dbgroups)!=0:
            bookmarkgroups = []
            for dbgroup in dbgroups[0]["groups"]:
                datasets = []
                for dbdataset in dbgroup["datasets"]:
                    datasets.append(Dataset(db=dbdataset["db"], col=dbdataset["col"]))
                bookmarkgroups.append(Bookmarkgroup(name=dbgroup["name"], datasets=datasets))
            return Bookmarkgroups(groups=bookmarkgroups)
        else:
            return Bookmarkgroups(groups=[])

    def set_bookmark_groups(self, bookmarkgroups):
        self.interface.delete_many({})
        result = self.interface.insert_one(bookmarkgroups.dict())
        if result.acknowledged:
            return True
        else:
            return False

    def get_username(self) -> str:
        return "global"
    
class MetadataTransferMongoDBMinioS3(MetadataTransferInterface):

    def __init__(self):
        self.dbc = DBC()

    def all_dataset_descriptions(self) -> DatasetDescription:
        query = {}
        datas = self.dbc.get_interface("graggle", "dataset_descriptions").get_data(return_images=True, query=query)
        return datas

    def get_dataset_description(self, database: str, collection: str) -> DatasetDescription:
        query = {"database": database, "collection": collection}
        datas = self.dbc.get_interface("graggle", "dataset_descriptions").get_data(return_images=True, query=query)

        # fill with dummy if not existing
        if len(datas) == 0:
            # filter
            filtered_temp_descriptor = None
            for temp_descriptor in self.get_datasets_details().datasetdescriptors:
                if temp_descriptor.database == database and temp_descriptor.collection == collection:
                    filtered_temp_descriptor = temp_descriptor

            dataset_description = {}
            dataset_description["database"] = database
            dataset_description["collection"] = collection
            dataset_description["dataset_display_title"] = '<<Titel>>'
            dataset_description["short_description"] = "<<Description>>"
            dataset_description["dataset_description"] = "<<Description>>"
            dataset_description["image"] = "" if filtered_temp_descriptor is None else filtered_temp_descriptor.image
            dataset_description["generated"] = True

            descriptors = {}
            descriptors['usability'] = "calc.."
            descriptors['created_by'] = "calc.."
            descriptors['created'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor.created
            descriptors['last_update'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor.last_update
            descriptors['size_mb'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor.size_mb
            descriptors['number_of_documents'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor.number_of_documents
            descriptors['annotation_types'] = "[ ... calculating ]"
            descriptors['image'] = "" if filtered_temp_descriptor is None else filtered_temp_descriptor.image
            dataset_description['descriptors'] = descriptors
            datas.append(dataset_description)

        for data in datas:
            data["descriptors"]["annotation_types"] = "[ ... calculating ]"
            try:
                data["image"] = cv2.resize(data["image"], (480, 320))
            except Exception as e:
                pass
            if "generated" not in data:
                data["generated"] = False

        dataset_descriptor = DatasetDescriptor(database=datas[0]["database"],
                                              collection=datas[0]["collection"],
                                              number_of_documents=str(datas[0]['descriptors']["number_of_documents"]),
                                              size_mb=str(datas[0]['descriptors']["size_mb"]),
                                              created=datas[0]['descriptors']["created"],
                                              last_update=datas[0]['descriptors']["last_update"],
                                              image="",
                                              usability=datas[0]['descriptors']["usability"],
                                              created_by=datas[0]['descriptors']["created_by"],
                                              annotation_types=datas[0]['descriptors']["annotation_types"])

        if isinstance(datas[0]["image"], np.ndarray):
            image = "data:image/png;base64," + utils.convert_ndarray_to_base_64(datas[0]["image"])
        else:
            image = datas[0]["image"]

        dataset_description = DatasetDescription(database=datas[0]["database"],
                                              collection=datas[0]["collection"],
                                              dataset_display_title=datas[0]["dataset_display_title"],
                                              short_description=datas[0]["short_description"],
                                              dataset_description=datas[0]["dataset_description"],
                                              image=image,
                                              generated=datas[0]["generated"],
                                              descriptors=dataset_descriptor)

        return dataset_description

    def update_dataset_description(self, database: str, collection: str, number_of_documents: int, size_mb: float, created: str, last_update: str):
        query = {"database": database, "collection": collection}
        new_value = {"$set": {"descriptors.number_of_documents": number_of_documents, "descriptors.size_mb": size_mb,
                              "descriptors.created": created, "descriptors.last_update": last_update}}
        try:
            self.dbc.get_interface("graggle", "dataset_descriptions").update_one(query, new_value)
        except Exception as e:
            logger.error(e)

    def insert_dataset_description(self, dataset_description: DatasetDescription):
        dataset_description = utils.object_to_dict(dataset_description)
        if "database" in dataset_description['descriptors']:
            dataset_description['descriptors'].pop('database')
        if "collection" in dataset_description['descriptors']:
            dataset_description['descriptors'].pop('collection')
        if "image" in dataset_description['descriptors']:
            dataset_description['descriptors'].pop('image')
        if "generated" in dataset_description:
            dataset_description.pop('generated')

        # generate image if empty
        db = dataset_description["database"]
        col = dataset_description["collection"]
        if dataset_description["image"] == "":
            try:
                interface = self.dbc.get_interface(db, col)
                entries = [                                        
                    interface.get_data(return_images=True, query={}, doc_count=1, random_sample=True)
                    for index in range(0, 12)]
                if "image" in entries[0][0]:
                    preview_image = utils.create_random_4_3_preview_image([entry[0]["image"] for entry in entries])
                if "image_data" in entries[0][0]:
                    preview_image = utils.create_random_4_3_preview_image([entry[0]["image_data"] for entry in entries])
                dataset_description["image"] = preview_image
            except Exception as e:
                return []
        else:
            dataset_description["image"] = utils.convert_base_64_to_ndarray(dataset_description["image"])

        result = self.dbc.get_interface("graggle", "dataset_descriptions").insert_one(dataset_description)
        if result.acknowledged:
            return True
        else:
            return False

class DataTransferMongoDBMinioS3(DataTransferInterface):
    # remove system databases
    ignore_dbs = ['admin', 'config', 'local', 'garbage_collector', 'graggle', 'org', 'test', 'request_log',
                  'test-customer-root-id-test-customer-id']

    def __init__(self):
        self.dbc = DBC()

    def count_documents(self, database: str, collection: str) -> int:
        number_of_documents = my_mongo_client[database][collection].count_documents({})
        return number_of_documents

    def get_databases(self) -> Databases:
        # databases
        databases = list(my_mongo_client.list_database_names())
        databases = [db for db in databases if db not in self.ignore_dbs]

        # bring into return format
        dbs = [DatabaseCollections(database_name=db_name,
                                   collection_names=my_mongo_client.get_database(db_name).list_collection_names())
               for db_name in databases]

        return Databases(databases=dbs)

    def get_document(self, database: str, collection: str, skip_count: int, filter: str = "") -> Document:
        #parsed_filter = json.loads(filter)
        if filter == {}:
            parsed_filter = filter
        else:
            try:
                parsed_filter = ast.literal_eval(filter)
            except Exception as e:
                logger.error(f"Exception when creating query for pymongo with error: {e}")
                parsed_filter = {}

        # manuelly create the ObjectId
        if '_id' in parsed_filter:
            parsed_filter['_id'] = ObjectId(parsed_filter['_id'])

        query = parsed_filter
        documents = self.dbc.get_interface(database, collection).get_data(return_images=True, query=query, doc_count=1,
                                         skip_count=skip_count, random_sample=True)
        if len(documents) == 0:
            return None
        else:
            documents[0]["_id"] = str(documents[0]["_id"])
            utils.remove_objects_of_type(documents[0], ObjectId)
            return Document(document=documents[0])

    def last_update_date(self, database: str, collection: str) -> str:
        try:
            db = my_mongo_client[database]
            coll = db[collection]
            documents = list(coll.find().limit(1))
            creation_time = ObjectId(documents[0]["_id"]).generation_time
            creation_time = creation_time.strftime("%d.%m.%Y")
        except Exception as e:
            creation_time = "??.??.????"

        return creation_time

    def create_date(self, database: str, collection: str) -> int:
        return self.last_update_date(database, collection)
