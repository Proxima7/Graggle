<template>
    <div class="">
      <div class="font-semibold mx-2 text-3xl underline">Latest</div>
      <div class="grid grid-cols-4 gap-4  ">        
        <DatasetOverviewCard v-for="dataset in datasets_complete" :key="dataset.collection" :dataset="dataset" 
        class="flex flex-col m-2 border-2 shadow rounded"/>
      </div>
    </div>
  </template>
  
  <script>
  import requestHandler from "../../../logic/RequestHandler"
  import DatasetOverviewCard from "./DatasetOverviewCard.vue"
  import { mapState } from 'vuex'

  export default {
    data() {
      return {
        datasets: "",
        datasets_complete: [],
        datasets_queried: 0,
        query_id: 0,
        showDescription: false
      };
    },
    mounted() {
        this.loadDatasets("")
    },
    computed: {
        ...mapState(['filter'])
    },
    methods: {
      async loadDatasets(filter){
        var that = this;
        this.query_id = this.query_id + 1
        let query_id = this.query_id
        this.datasets_complete = []
        this.datasets_queried = 0
        var dataset_overview_callback = function (resp) {
            that.datasets = resp.data;
            if(query_id == that.query_id){
              for(let i=0; i<that.datasets.length; i++){
                let db = that.datasets[i]["database"]
                let col = that.datasets[i]["collection"]
                that.loadDataset(db, col, that.query_id)
              }
            }            
        };      
        requestHandler.get_datasets(dataset_overview_callback, filter);
      },
      async loadDataset(db, col, query_id) {
            if(this.datasets_queried>=24){
              return
            }
            this.datasets_queried = this.datasets_queried + 1
            var that = this;
            this.loading = true;
            var dataset_description_callback = function (resp) {
                if(query_id == that.query_id){
                  that.datasets_complete.push(resp.data) 
                }
            };

            var dataset_description_callback_error = function (error) {
                if(error.response.status == 404){
                    that.dataset_description = null
                }
                that.loading = false;
            };
            if(query_id != that.query_id){
              return
            }
            requestHandler.get_dataset_description(dataset_description_callback, dataset_description_callback_error, db, col);
      }
    },
    watch: {
        filter(newValue, oldValue) {
            this.loadDatasets(newValue)
        }
    },
    components: {
      DatasetOverviewCard
    }
  };
  </script>
  