import threading
import time
import cv2
import numpy as np

from util.utils import average_image_size, create_random_4_3_preview_image, convert_ndarray_to_base_64
from data_access.data_transfer_objects import Datasets, DatasetDescriptor


def collection_metadata_description_updater(cron):
    """
    Main routine to update changing dataset description values in a defined circular sheduled time.
    Determines a subset of the dataset description to allow queries on dataset and collection names.

    Args:
        cron: Updater object that holds the data storage implementation
    """
    run = 0
    while True:
        datasetdescriptors = []
        database_collections = cron.dti.get_databases()

        for database_collection in database_collections.databases:
            db = database_collection.database_name
            for collection in database_collection.collection_names:
                col = collection
                print(col)
                number_of_documents, size_mb, created, last_update, preview_image = data_by_collection(cron, db, col)

                datasetdescriptor = DatasetDescriptor(database=db,
                                               collection=col,
                                               number_of_documents=number_of_documents,
                                               usability="",
                                               created_by="",
                                               annotation_types="",
                                               size_mb=size_mb,
                                               created=created,
                                               last_update=last_update,
                                               image="data:image/png;base64," + convert_ndarray_to_base_64(preview_image))
                datasetdescriptors.append(datasetdescriptor)
            if run==0:
                cron.mdti.set_datasets_details(Datasets(datasetdescriptors=datasetdescriptors))
                print("temp descriptors filled")
        if run > 0:
            cron.mdti.set_datasets_details(Datasets(datasetdescriptors=datasetdescriptors))
            print("temp descriptors filled")
        run = run + 1

        datas = cron.mdti.all_dataset_descriptions()
        for data in datas:
            db = data['database']
            col = data['collection']
            number_of_documents, size_mb, created, last_update, preview_image = data_by_collection(cron, db, col)
            cron.mdti.update_dataset_description(db, col, number_of_documents, size_mb, created, last_update)

        time.sleep(86400)

def data_by_collection(cron, db, col):
    """
    Determines per dataset informations like images für previews, timestamps, amounts and sizes
    Args:
        cron: Updater object that holds datastorage
        db: database
        col: collection

    Returns: number_of_documents, size_mb, created, last_update, preview_image

    """
    number_of_documents = cron.dti.count_documents(db, col)

    size_mb = 0
    image_field = ""
    try:
        document = cron.dti.get_document(db, col, 0, {})

        #entry = cron.dbm.db_accessor.get_data(db, col, return_images=True, query={}, doc_count=1, random_sample=True)[0]
        if "image" in document.document:
            image_field = "image"
        if "image_data" in document.document:
            image_field = "image_data"
    except Exception as e:
        pass

    try:
        size_mb_average = average_image_size([cron.dti.get_document(db, col, 0, {}).document[image_field] for i in range(5)])
        size_mb = round(number_of_documents * size_mb_average, 2)
    except Exception as e:
        pass

    preview_image = np.zeros((320, 480, 3), dtype=np.uint8)
    preview_image = cv2.putText(preview_image, 'HAS NO IMAGES', (5, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
    try:
        entries = [cron.dti.get_document(db, col, 0, {}).document for index in range(0, 12)]
        preview_image = create_random_4_3_preview_image([entry[image_field] for entry in entries])
        preview_image = cv2.resize(preview_image, (320, 240), interpolation=cv2.INTER_AREA)
    except Exception as e:
        pass

    last_update = cron.dti.last_update_date(db, col)
    created = cron.dti.create_date(db, col)

    return number_of_documents, size_mb, created, last_update, preview_image

class Updater():
    """Start fo endless running thread to hold dataset description up-to-date"""
    def __init__(self, dti, mdti):
        self.dti = dti
        self.mdti = mdti

    def cycling_updat(self):
        thread = threading.Thread(target=collection_metadata_description_updater, args=(self,))
        thread.start()

