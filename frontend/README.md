# Graggle
![Getting Started](./src/assets/graggle_logo_large.png)

This will become an open source data catalogue ready to use for any company.
The style will be a mixture of mongoDB compass, Kraggle and FiftyOne.
The platform goes hand in hand with GrandML and GrandHub.

The platform supports:
Viewing any dataset prepared in our data structure formats (for MongoDB). This includes metadata data management for datasets. Where's a dataset from, what type of data is inside, formats, and an advanced semantic search like in Kaggle.
Secondly it supports viewing single documents (example MongoDB Atlas), images, and referenced data.
Thirdly we provide simple tagging tools (example fiftyone).

It has integrations to GrandHub.
Supporting references to workflows which use a specific dataset.

Further use-cases:
- Blockchain integration to share data accross companies for example via the Ocean Protocol and SingularityNet


# Setup:
open terminal
1. npm install 
2. npm run dev (now the browser should start in localhost)

## Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

# Coding

 and vue3.js. The server is vite.


## Styling
The app is styled with tailwind. All tailwind classes can be used.
In additional we have a standard color palette which is defined in tailwind.config.cjs look here https://tailwindcss.com/docs/theme
Also other standards can be defined there like the min-h-90vh (equals minHeight: '90vh' in the config)

### icons
We use fontawesome icons. Icons can be added in the main.js

# App features

## Role management
There are predefined roles for the granularity of accessability. The admin can configure read rights for a consumer.
-- this is work in progress ---

## Adding data
At the moment data is added via a manual ETL and brought into the correct format. In the future a GrandML integration is foreseen with which data can be easily parsed and added to the Data Catalogue.
This will support different common formats like coco, yolo and manual process with schema check.
