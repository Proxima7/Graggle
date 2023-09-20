<template>
    <div class="w-full">
      <div class="grid grid-cols-1 gap-2 ">
        <div v-for="group in bookmarkgroups" class="bg-gray-300 mb-2 py-2 px-2 rounded">
          <div class="text-xl laptop:text-2xl desktop:text-3xl 4k:text-3xl text-secondary w-100 leading-2 font-bold border-b-4 mb-2 border-secondary">Name: {{ group.name }}</div>
          <div v-for="bookmark in group.datasets" class="bg-secondary py-2 px-2 mb-1 rounded" @click="set_selected_collection(bookmark.database, bookmark.collection)">
            <div class="relative grid max-[1000px]:grid-cols-1 min-[1000px]:grid-cols-3 gap-2 ">
                <div class="flex items-center justify-center">
                  <img v-if="bookmark.image!=''" :src="bookmark.image" class="rounded mx-auto ">
                </div>
                <div class="">
                  <div class="font-semibold max-[1000px]:text:sm min-[1000px]text-lg">{{ bookmark.title }}</div>
                  <div class="text-gray-500 text-xs min-[1000px]:col-span-2">{{ bookmark.collection }}</div>
                </div> 
                
                <!-- Overlay -->
                <div>
                  <div class="absolute inset-0 bg-gray-700 opacity-20">
                  </div>
                  <button class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white font-bold py-2 px-4 rounded
                      text-sm laptop:text-lg desktop:text-xl 4k:text-2xl" @click="dataset_add_dialog_show = !dataset_add_dialog_show">
                      <font-awesome-icon class="text-black" icon="fa-solid fa-circle-plus" /> 
                  </button>
                </div>
            </div> 
          </div>  
        </div >
      </div>
    </div>
  </template>
  
  <script>
    import { BookmarkGroups } from "./Helpers/BookmarkGroups.js"
    import { useGeneralStore } from '@/stores/general'
    import { useDatasetStore } from '@/stores/dataset'
    import { watch } from 'vue'

    export default {
        data() {
          return {
              bookmarkgroups: [],
              gstore: useGeneralStore(),
              datasetstore: useDatasetStore()
          }
        },
        computed: {
        },
        mounted() {
            this.handle_bookmark_groups()
            watch(() => this.gstore.amount_bookmark_groups, (newValue, oldValue) => {
              this.handle_bookmark_groups()
          });
        },
        methods: {
          handle_bookmark_groups(){
              this.bookmarkgroups = BookmarkGroups.getBookmarkGroups("",  "")
              for(let i=0; i<this.bookmarkgroups.length; i++){
                for(let ds=0; ds<this.bookmarkgroups[i].datasets.length; ds++){
                    let db = this.bookmarkgroups[i].datasets[ds].db
                    let col = this.bookmarkgroups[i].datasets[ds].col
                    this.handle_bookmark(i, ds, db, col)
                }
              }
             
              
          },
          async handle_bookmark(i, ds, db, col){
              let dataset_description = await this.datasetstore.read_dataset_description(db, col)
              this.bookmarkgroups[i].datasets[ds].image = dataset_description.image;
              this.bookmarkgroups[i].datasets[ds].title = dataset_description.dataset_display_title;
              this.bookmarkgroups[i].datasets[ds].collection = col;
              this.bookmarkgroups[i].datasets[ds].database = db;
              
          },
          set_selected_collection(db, col){
              this.gstore.selected_db = db
              this.gstore.selected_col = col
          }
        }
    }
  </script>
  
  <style>
  </style>