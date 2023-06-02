import pymongo
import settings
from database_accessor import get_db_accessor
from database_accessor.utils import vault_reader
import random
import os
import utils
from bson.objectid import ObjectId
import pickle
import cv2



class DBManager:

    def __init__(self):
        mongodb_con_string = vault_reader.read_value(f"prod_mongodb_con_string_admin", vault="prod")
        self.my_mongo_client = pymongo.MongoClient(mongodb_con_string)
        self.db_graggle = self.my_mongo_client.graggle
        self.temp_descriptors = []
        self.db_accessor = get_db_accessor(mongo_instance="prod", con_string_name="mongodb_con_string_admin")


    def set_temp_descriptors(self, temp_descriptors):
        try:
            os.remove('temp_descriptors.pickle')
        except OSError:
            pass
        with open('temp_descriptors.pickle', 'wb') as f:
            pickle.dump(temp_descriptors, f)
        self.temp_descriptors = temp_descriptors
    def get_temp_descriptors(self):
        if self.temp_descriptors == []:
            #load pickle
            with open('temp_descriptors.pickle', 'rb') as f:
                self.temp_descriptors = pickle.load(f)
        return self.temp_descriptors

    def get_dataset_documents(self, database, collection_name, page_size: int = 10, last_id=None):
        """Function returns `page_size` number of documents after last_id
        and the new last_id.
        """
        db = self.my_mongo_client.get_database(database)
        coll = db[collection_name]
        if last_id is None:
            # When it is first page
            cursor = coll.find().limit(page_size)
        else:
            cursor = coll.find({'_id': {'$gt': last_id}}).limit(page_size)

        # Get the data
        data = [x for x in cursor]

        if not data:
            # No documents left
            return None, None

        # Since documents are naturally ordered with _id, last document will
        # have max id.
        last_id = data[-1]['_id']

        # Return data and last_id
        return data, last_id

    def get_databases(self) -> list[dict]:
        # databases
        databases = list(self.my_mongo_client.list_database_names())
        # remove system databases
        databases = [db for db in databases if db not in ['admin', 'config', 'local', 'garbage_collector']]

        # remove gragggle
        databases.remove('graggle')
        databases.remove('org')
        databases.remove('dev2')
        databases.remove('test')
        databases.remove('request_log')
        databases.remove('test-customer-root-id-test-customer-id')

        # bring into sendable json notation
        database_collections = [{
                "name": db_name,
                "collections": self.my_mongo_client.get_database(db_name).list_collection_names()
            }
            for db_name in databases
        ]

        return database_collections

    def get_data(self, database: str, collection: str, number: int, query: str = ""):
        #query = {"database": database, "collection": collection}
        datas = self.db_accessor.get_data(database, collection, return_images=True, query=query, doc_count=1, skip_count=number, random_sample=True)
        return datas

    def get_collection_creation_update_time(self, database: str, collection: str):
        try:
            db = self.my_mongo_client[database]
            coll = db[collection]
            documents = list(coll.find().limit(1))
            creation_time = ObjectId(documents[0]["_id"]).generation_time
            creation_time = creation_time.strftime("%d.%m.%Y")
        except Exception as e:
            creation_time = "??.??.????"

        #indexes = db["system.indexes"].find({"ns": coll.full_name}).sort([("lastmod", pymongo.DESCENDING)]).limit(1)
        #last_update_time = next(indexes, None)["lastmod"]

        return creation_time, creation_time

    def get_dataset_descriptions(self):
        query = {}
        datas = self.db_accessor.get_data("graggle", "dataset_descriptions", return_images=True, query=query)
        return datas

    def update_dataset_description(self, database: str, collection: str, number_of_documents: int, size_mb: float, created: str, last_update: str):
        db = self.my_mongo_client["graggle"]
        coll = db["dataset_descriptions"]
        query = {"database": database, "collection": collection}
        new_value = {"$set": {"descriptors.number_of_documents": number_of_documents, "descriptors.size_mb": size_mb, "descriptors.created": created, "descriptors.last_update": last_update}}
        try:
            coll.update_one(query, new_value)
        except Exception as e:
            print(e)

    def get_dataset(self):
        temp_descriptors = self.get_temp_descriptors()
        sorted_temp_descriptors = sorted(temp_descriptors, key=lambda x: x['created'], reverse=True)
        return sorted_temp_descriptors

    def get_dataset_description(self, database: str, collection: str):
        query = {"database": database, "collection": collection}
        datas = self.db_accessor.get_data("graggle", "dataset_descriptions", return_images=True, query=query)

        # fill with dummy if not existing
        if len(datas)==0:
            # filter
            filtered_temp_descriptor = None
            for temp_descriptor in self.get_temp_descriptors():
                if temp_descriptor["database"] == database and temp_descriptor["collection"] == collection:
                    filtered_temp_descriptor = temp_descriptor

            dataset_description = {}
            dataset_description["database"] = database
            dataset_description["collection"] = collection
            dataset_description["dataset_display_title"] = '<<Titel>>'
            dataset_description["short_description"] = "<<Description>>"
            dataset_description["dataset_description"] = "<<Description>>"
            dataset_description["image"] = "" if filtered_temp_descriptor is None else filtered_temp_descriptor["image"]
            dataset_description["generated"] = True



            descriptors = {}
            descriptors['usability'] = "calc.."
            descriptors['created_by'] = "calc.."
            descriptors['created'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor["created"]
            descriptors['last_update'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor["last_update"]
            descriptors['size_mb'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor["size_mb"]
            descriptors['number_of_documents'] = "calc.." if filtered_temp_descriptor is None else filtered_temp_descriptor["number_of_documents"]
            descriptors['annotation_types'] = "[ ... calculating ]"
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
        return datas

    def set_dataset_description(self, dataset_description: dict):
        # generate image if empty
        db = dataset_description["database"]
        col = dataset_description["collection"]
        if dataset_description["image"] == "":
            try:
                entries = [ self.db_accessor.get_data(db, col, return_images=True, query={}, doc_count=1, random_sample=True) for index in range(0,12)]
                preview_image = utils.create_random_4_3_preview_image([entry[0]["image"] for entry in entries])
                dataset_description["image"] = preview_image
            except Exception as e:
                return []

        inserted_ids = self.db_accessor.insert_data(dataset_description, "graggle", "dataset_descriptions")
        return inserted_ids

