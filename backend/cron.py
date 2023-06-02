import threading
import time
import cv2

import numpy as np

from utils import average_image_size, create_random_4_3_preview_image, convert_ndarray_to_base_64
def collection_metadata_description_updater(cron):
    run = 0
    while True:
        temp_descriptors = []
        database_collections = cron.dbm.get_databases()
        for database_collection in database_collections:
            db = database_collection['name']
            for collection in database_collection["collections"]:
                col = collection
                print(col)
                number_of_documents, size_mb, created, last_update, preview_image = data_by_collection(cron, db, col)

                descriptor = {}
                descriptor["database"] = db
                descriptor["collection"] = col
                descriptor["number_of_documents"] = number_of_documents
                descriptor["size_mb"] = size_mb
                descriptor["created"] = created
                descriptor["last_update"] = last_update
                descriptor["image"] = "data:image/png;base64," + convert_ndarray_to_base_64(preview_image)
                temp_descriptors.append(descriptor)
            if run==0:
                cron.dbm.set_temp_descriptors(temp_descriptors)
                print("temp descriptors filled")
        if run > 0:
            cron.dbm.set_temp_descriptors(temp_descriptors)
            print("temp descriptors filled")
        run = run + 1

        datas = cron.dbm.get_dataset_descriptions()
        for data in datas:
            db = data['database']
            col = data['collection']
            number_of_documents, size_mb, created, last_update, preview_image = data_by_collection(cron, db, col)
            cron.dbm.update_dataset_description(db, col, number_of_documents, size_mb, created, last_update)





        time.sleep(8640)

def data_by_collection(cron, db, col):
    number_of_documents = cron.dbm.my_mongo_client[db][col].count_documents({})

    size_mb = 0
    image_field = ""
    try:
        entry = cron.dbm.db_accessor.get_data(db, col, return_images=True, query={}, doc_count=1, random_sample=True)[0]
        if "image" in entry:
            image_field = "image"
        if "image_data" in entry:
            image_field = "image_data"
    except Exception as e:
        pass

    try:
        size_mb_average = average_image_size([cron.dbm.db_accessor.get_data(db, col, return_images=True, query={}, doc_count=1, random_sample=True)[0][image_field] for i in range(5)])
        size_mb = round(number_of_documents * size_mb_average, 2)
    except Exception as e:
        pass

    preview_image = np.zeros((320, 480, 3), dtype=np.uint8)
    preview_image = cv2.putText(preview_image, 'HAS NO IMAGES', (5, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
    try:
        entries = [cron.dbm.db_accessor.get_data(db, col, return_images=True, query={}, doc_count=1, random_sample=True) for index in range(0, 12)]
        preview_image = create_random_4_3_preview_image([entry[0][image_field] for entry in entries])
        preview_image = cv2.resize(preview_image, (320, 240), interpolation=cv2.INTER_AREA)
    except Exception as e:
        pass

    created, last_update = cron.dbm.get_collection_creation_update_time(db, col)
    return number_of_documents, size_mb, created, last_update, preview_image

class Cron():
    def __init__(self, dbm):
        self.name = "hello my name is"
        self.dbm = dbm

    def updater(self):
        thread = threading.Thread(target=collection_metadata_description_updater, args=(self,))
        thread.start()

