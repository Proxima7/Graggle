import { defineStore } from 'pinia'
import requestHandler from "../logic/RequestHandler"
import { useGeneralStore } from '@/stores/general'
import { Helper } from "../Components/Helpers/Helper.js"

export const useDatasetStore = defineStore('dataset', {
  state: () => ({ 
    global_counter: 0,
    low_resolution: false, 
    dataset_description: null, 
    dataset_loading: false, 

    documents_filter: "{}",
    documents_images: [],
    documents: [{
      "loading": "we are currently fetching the data from the database. Please wait a few seconds.",
    }],
    current_index: 0,
    gstore: useGeneralStore(),
  }),
  actions: {
    
    reset() {
      this.global_counter = this.global_counter + 1
      this.documents_filter="{}"
      this.current_index=0
      this.documents_images = []
      this.documents= [{
          "loading": "",
      }]
    },
    reset_dataset_description() {
      this.dataset_description= null
    },
    set_filter(documents_filter){
      this.documents_filter = documents_filter
    },

    load() {
      this.load_dataset_description()
      this.get_data(true)
    },

    // --
    // Data
    // --
    data_get_all_documents(){
      return this.documents
    },
    data_get_all_image(){
      return this.documents_images
    },
    data_get_current_documents(){
      return this.documents[this.current_index]
    },
    data_get_current_image(){
      return this.documents_images[this.current_index]
    },
    data_has_data(){
      const data_has_data = 0 < this.documents_images.length
      return data_has_data
    },
    data_has_next(){
      const data_has_next = this.current_index < (this.documents_images.length-1)
      return data_has_next
    },
    data_has_prev(){
      const data_has_prev = this.current_index>0
      return data_has_prev
    },
    data_next(){
      if(this.current_index == (this.documents_images.length-2)){
         this.get_data(false)
      }            
      this.current_index = this.current_index+1
      this.current_image = this.documents_images[this.current_index]
    },
    data_prev(){
      this.current_index = this.current_index-1
      this.current_image = this.documents_images[this.current_index]
    },
    async get_data(preload_next){
      let start_counter = this.global_counter
      var that = this;
      var data_callback = function (resp) {
          
        // verwerfen von request aus anderem context
          if (that.global_counter != start_counter){
             return 
          }

          if ('loading' in that.documents[0]) {
              that.documents = []
              that.documents_images = []
          } 

          let document = resp.data.document

          // create image url usable in anatorious
          if ('image' in document){
              that.documents_images.push(Helper.base64_to_url(document['image']))                
              document['blobimage'] = document['image']
          }
          if ('image_data' in document){
              that.documents_images.push(Helper.base64_to_url(document['image_data']))    
              document['blobimage'] = document['image_data']
              delete document['image_data']            
          }           
          
          that.documents.push(document)

          // load next image
          if(preload_next){
              that.get_data(false)
          } else{
              that.next_disabled = false
          }          
      };

      var data_callback_error = function (error) {
          that.documents= [{
            "empty result or wrong filter": "",
          }]
      };


      let db = this.gstore.selected_db
      let col = this.gstore.selected_col
      let number =  this.documents.length
      if ('loading' in that.documents[0]) {
          number=0
      }
      requestHandler.get_dataset_document(data_callback, data_callback_error, db, col, number, this.documents_filter || "{}", this.low_resolution);       
    },

    // --
    // description for datacard
    // --
    is_dataset_loading(){
      return this.dataset_loading
    },
    get_dataset_description(){
      return this.dataset_description
    },
    async filter_datasets(filter) {
      var datasets = null

      var dataset_overview_callback = function (resp) {
        datasets = resp.data.datasetdescriptors;              
      }
      await requestHandler.get_datasets_filtered(dataset_overview_callback, filter);
      return datasets
    },
    
    async read_dataset_description(db, col) {
      var dataset_description = null

      var dataset_description_callback = function (resp) {
          dataset_description = resp.data;
      };

      var dataset_description_callback_error = function (error) {
      };
      await requestHandler.get_dataset_description(dataset_description_callback, dataset_description_callback_error, db, col);
      return dataset_description
    },
    load_dataset_description() {
      var that = this;
      this.dataset_loading = true;
      var dataset_description_callback = function (resp) {
          that.dataset_description = resp.data;
          that.dataset_loading = false;
      };

      var dataset_description_callback_error = function (error) {
          if(error.response.status == 404){
              that.dataset_description = null
          }
          that.dataset_loading = false;
      };
      let db = this.gstore.selected_db
      let col = this.gstore.selected_col
      requestHandler.get_dataset_description(dataset_description_callback, dataset_description_callback_error, db, col);
    },
    async post_dataset_description(body) {
      let success = true
      var dataset_description_post_callback = function (resp) {
          success = true;
      };
      var dataset_description_post_callback_error = function (error) {
          success = false;
      };
      await requestHandler.post_dataset_description(dataset_description_post_callback, dataset_description_post_callback_error, body);
      return success
    }
  }
})