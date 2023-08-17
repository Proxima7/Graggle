# Common
The Graggle backend is the component controlling data in and output for the frontend. It controles which images and image metadata are available to the user. Further functionality/storage options such as comments, bookmarks, user data, filters or queries will/should also be provided via the backend in the future.

# Design
## RESTful API
The RESTful api is hosted by Uvicorn which is an ASGI web server implementation for Python.

The endpoints are created and automatically documented with openapi v3 by FastAPI which is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

The endpoints implementation is in ```main.py``` together with additional openapi information, CORS settings and the choosen persistence implementation.

The api response models are stored in **/fastapi_modesl/models.py**.

## Frontend
The frontend is from the **/frontend** project withing this Graggle project. After the frontend build the output in the **dist** needs to be copied into the **public** folder. This files are hosted static by the uvicorn webserver under **/graggle-frontend** and is accessible by ```http://localhost:8101/graggle-backend/graggle-frontend/index.html```. The subpath **/graggle-backend** is coming from the static file hosting. The additional mount entries come from cloud hosting where a reverse proxy is always involved that replaces **/graggle-backend** but the browser always includes that path. 

## Storage
### MongoDB + Minio (S3)
By default the Graggle backend implements a architecture where the images are stored in a Minio Storage (fully compatible with Amazon S3) and the image metadata with the link to the Minio destination are stored in a MongoDB database.  

It is necessary to set the following environment variables for a valid data access.
```
prod_mongodb_con_string_admin=mongodb-con-string-with-write-rights
prod_s3_host=url-to-minio
prod_s3_access_key=access-key-for-minio
prod_s3_secret_key=secret-for-acces-minio
```

The fundamental storage schema requirements are:
- Image should be stored in Minio and the image-link is part of the MongoDB entry.
- Minio image-link is stored in a MongoDB field with the name **image**.
- Annotations stored in the MongoDB field with the name **annotations** and the following style ...
```
{
  "_id": {
    "$oid": "a5c6f6"
  },
  "image": "https://s3.company.com/cars/6c2d6a.png",
  "meta": {
    "width": 768,
    "height": 1024,
    "created": "2020-12-18 10:30:46.449348",
    "uploader": "uploader_component",
    "dataset": "cars"
  },
  "annotations": [
    {
      "type": "word",
      "id": 0,
      "box": [[452,444],[462,446],[473,446],[485,446]],
      "meta": {
        "illegibility": false,
        "text": "OPEN",
        "annotator": "dataset",
        "confidence": 1
      }
    },
    {
      "type": "char",
      "id": 1,
      "box": [[467,463],[467,449],[474,449],[474,463]],
      "meta": {
        "text": "O",
        "annotator": "approx_decide_legibel",
        "confidence": 1
      }
    }
  ]
}
```

### Custom implementation
It is possible to use a different storage technology (e.g. RDMS, Filesystem, DocumentDatabase only) but this requires the implementation of data and metadata access.  

 - For your custom storage access your need to implement the interface **DataTransferInterface.py** to access the the database, datasets, documents and some document related metadata.

 - The second interface that needs to be implemented is **MetadataTransferInterface.py** to store, query and provide dataset metadata like descriptions, preview images, dataset size, image counter, usability ration, aso.

- The custom implementation has to be used in the ```main.py``` by replacing the existing with your implementation with your created. 
```
dti = data_transfer_impl_mongoDB_minioS3.DataTransferMongoDBMinioS3()
mdti = data_transfer_impl_mongoDB_minioS3.MetadataTransferMongoDBMinioS3()
```

# Build & Deploy
The deployment can easily made by docker technology.  

**ATTENTION** - Builded frontend has to be copied to the 'public' folder.    
  
 
 Run a docker build command similar to this:
 ```
 $name = "graggle-backend-service"
 $version = "0.1.2"
docker build -t graggle/$name`:$version -f containerization/Dockerfile .
 ```
 Deploy it with a cloud technology like kubernetes or run the docker directly.