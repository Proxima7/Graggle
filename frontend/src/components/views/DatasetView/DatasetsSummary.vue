<template>
    <div class="">
      <div class="grid grid-cols-1 gap-2">
        <div  v-for="database in databasestore.get_databases()">          
          <div class="font-semibold mx-2 text-3xl underline mt-4" v-if="datasets_complete[database.database_name] ">{{database.database_name}}</div>
          <div class="grid grid-cols-6 gap-2  ">        
            <DatasetOverviewCard v-for="dataset in datasets_complete[database.database_name]" :key="dataset.collection" :dataset="dataset" 
            class="flex flex-col m-2 border-2 shadow rounded"/>
          </div>
        </div>    
      </div>

    </div>
  </template>
  
  <script>
  import DatasetOverviewCard from "./DatasetOverviewCard.vue"
  import { useGeneralStore } from '@/stores/general'
  import { useDatasetStore } from '@/stores/dataset'
  import { useDatabasesStore } from '@/stores/databases'
  import { watch } from 'vue'

  export default {
    data() {
      return {
        headline: "",
        datasets_complete: [],
        datasets_queried: 0,
        query_id: 0,
        showDescription: false,
        gstore: useGeneralStore(),
        datasetstore: useDatasetStore(),
        databasestore: useDatabasesStore()
      };
    },
    mounted() {
        this.databasestore.load()
      
        this.loadDatasets("")

        watch(() => this.gstore.filter, (newValue, oldValue) => {
            this.loadDatasets(newValue)
        });
    },
    computed: {
    },
    methods: {
      async loadDatasets(filter){
        if(filter==""){
          this.headline="Latest changed datasets:"
        } else {
          this.headline="Filtered datasets for: " + filter
        }

        this.query_id = this.query_id + 1
        let query_id = this.query_id
        this.datasets_complete = {}
        this.datasets_queried = 0

        let datasets = await this.datasetstore.filter_datasets(filter)
        if(query_id == this.query_id){
          for(let i=0; i<datasets.length; i++){
            let db = datasets[i]["database"]
            let col = datasets[i]["collection"]
            this.dataset_description(db, col, this.query_id)
          }
        }    
        return this.datasets_complete        
      },
      async dataset_description(db, col, query_id) {
        if(this.datasets_queried>=200){
          return
        }
        this.datasets_queried = this.datasets_queried + 1
        let dataset_description = await this.datasetstore.read_dataset_description(db, col)

        if(query_id == this.query_id){
          if(!this.datasets_complete[db]){
            this.datasets_complete[db] = []
          } 
          this.datasets_complete[db].push(dataset_description)  
        }  
      }
    },
    components: {
      DatasetOverviewCard
    }
  };
  </script>
  