# Graggle
![Graggle Logo!](/graggle_logo_large_dark_background.png)

Data is all you need. Graggle is a data-catalogue and warehouse with metadata management features. It makes managing, searching, governing, and sharing data easy, with seamless connections to data lake architectures. It also offers data inspection and tagging features for effective dataset management. 

Graggle is inspired by Kaggle, MongoDB Compass and FiftyOne and brings the best features to an easy accessible web tool.
Graggle is part of the GrandML ecosystem. To GrandML belongs GrandPa, GrandFlow, GrandHub and Graggle.

## Features
<ul>
<li>
Data exploration: Users can directly view datasets, collections, datapoints and media in the browser. Use queries to easily find specific datapoints. 
</li>
<li>
Metadata management: Metadata is stored in MongoDB and includes database and collection descriptions, discussions, and annotations.
</li>
<li>
Statistics: Graggle calculates statistics about collections, including number of documents, data quality, and annotation types (e.g., segmentation, classification, text).
</li>
<li>
Analytics: Find outliers in your data, inspect the quality and labels.
</li>
<li>
Annotation: Images can be annotated in the browser via Annotorious, and segmentation and other annotation types can be viewed and edited.
</li>
<li>
Bookmarks and queries: Users can have bookmarks and store queries for easy access.
</li>
<li>
Cross-referencing: Graggle enables cross-referencing to other projects that use the same data.
</li>
<li>
Data governance and roles: Graggle allows different level of access rights and uses standardized data-formats and schemas. 
</li>

    
## Technologies

Graggle is built using the following technologies. The code is modular it should be easy to integrate other file systems or databases:
    
### Frontend:
Vue.js: Frontend JavaScript framework
Annotorious: Browser-based image annotation library
Tailwind: The app is styled with tailwind. All tailwind classes can be used.
In additional we have a standard color palette which is defined in tailwind.config.cjs look here https://tailwindcss.com/docs/theme
Also other standards can be defined there like the min-h-90vh (equals minHeight: '90vh' in the config)
Icons: We use fontawesome icons. Icons can be added in the main.js
### Backend:
Python with FastAPI: Backend web framework
    
### Database:
MongoDB: NoSQL database for metadata management
Minio: Distributed file system for media storage

## Getting Started

To run Graggle locally, follow these steps:

    Clone the repository: git clone https://github.com/username/graggle.git
    Install the dependencies: cd graggle && npm install
    Start the frontend: npm run serve
    
    Install and start the backend: 
    pip install -r requirements.txt

Note: You'll need to set up a MongoDB instance and Minio for media storage before running Graggle.

## Adding data
At the moment data is added via a manual ETL and brought into the correct format. In the future a GrandML integration is foreseen with which data can be easily parsed and added to the Data Catalogue.
This will support different common formats like coco, yolo and manual process with schema check.

todo: write a good specification of the data-format.
    
## Contributing

We welcome contributions from the community! If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

## License

Graggle is licensed under the GPL license. See LICENSE for more information.
