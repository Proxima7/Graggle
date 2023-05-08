# Graggle
Data is all you need. Graggle is a data-catalogue and warehouse with metadata management features. It makes managing, searching, governing, and sharing data easy, with seamless connections to data lake architectures. It also offers data inspection and tagging features for effective dataset management.

## Features
<ul>
<li>
Data exploration: Users can directly view collections, databases, and images in the browser. Use queries to easily find specific datapoints. 
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
Data governance: Graggle allows different level of access rights and uses standardized data-formats. 
</li>

    
## Technologies

Graggle is built using the following technologies:
**Frontend**:
Vue.js: Frontend JavaScript framework
Annotorious: Browser-based image annotation library
**Backend**:
Python with FastAPI: Backend web framework
**Database**:
MongoDB: NoSQL database for metadata management
Minio: Distributed file system for media storage

The code is modular it should be easy to integrate other file systems or databases. 

## Ecosystem

Graggle is part of the GrandML ecosystem. To GrandML belongs GrandPa, GrandFlow, GrandHub and Graggle.

## Getting Started

To run Graggle locally, follow these steps:

    Clone the repository: git clone https://github.com/username/graggle.git
    Install the dependencies: cd graggle && npm install
    Start the frontend: npm run serve
    
    Install and start the backend: 
    pip install -r requirements.txt

Note: You'll need to set up a MongoDB instance and Minio for media storage before running Graggle.

## Contributing

We welcome contributions from the community! If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

## License

Graggle is licensed under the GPL license. See LICENSE for more information.
