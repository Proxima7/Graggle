<template>
    <div class="relative "
            @mouseover="showDescription = true" @mouseleave="showDescription = false"
            @click="selectDataset(dataset)">
        <!-- OVERLAY -->
        <div class="absolute inset-0 bg-black opacity-80 mx-2 mt-20 mb-2" v-if="showDescription">
        <p class="text-white text-xl font-bold m-2">{{ dataset.dataset_description.slice(0, 300) }}</p>
        </div>

        <!-- DATASET -->
        <img :src="dataset.image" class=" object-cover m-0.5 rounded">
        <span v-if="dataset.generated==false" class="absolute top-5 right-5 h-5 w-5 bg-green-500 rounded-full"></span>
        <span v-else class="absolute top-5 right-5 h-5 w-5 bg-red-500 rounded-full"></span>
        <div class="bg-white p-1 min-[1000px]:p-2">
          <h3 class="font-semibold text-xs tablet:text-xs laptop:text-sm desktop:text-sm 4k:text-sm">{{ fixed_titel }}</h3>
          <p class="text-gray-500 text-xs tablet:text-xs laptop:text-sm desktop:text-sm 4k:text-sm">{{ dataset.collection }}</p>
        </div>
    </div>
  </template>
  
  <script>
  import { useGeneralStore } from '@/stores/general'

  export default {
    props: {
      dataset: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        showDescription: false,
        gstore: useGeneralStore()
      }
    },
    computed: {
      fixed_titel(){
        if(this.dataset.dataset_display_title.includes("<<Titel>>")){
          return this.dataset.database
        } 
        return this.dataset.dataset_display_title
      }
    },
    methods: {
      selectDataset(dataset){
        this.gstore.selected_db = dataset.database
        this.gstore.selected_col = dataset.collection
      }
    }
  };
  </script>
  
  <style>
  /* Optional: add styles for the content and overlay */
  </style>
  