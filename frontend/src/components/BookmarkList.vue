<template>
    <div class="w-full">
      <div class="grid grid-cols-1 gap-2 ">
        <div v-for="bookmark in bookmarks" class="bg-secondary py-2 px-2 rounded" @click="set_selected_collection(bookmark.database, bookmark.collection)">
          <div class="grid grid-cols-3 gap-2 ">
            <div class="flex items-center justify-center">
              <img v-if="bookmark.image!=''" :src="bookmark.image" class="rounded mx-auto">
            </div>
            <div class="">
              <div class="font-semibold text-lg">{{ bookmark.title }}</div>
              <div class="text-gray-500 text-xs">{{ bookmark.collection }}</div>
            </div>
          </div>
        </div >
      </div>
    </div>
  </template>
  
  <script>
    import { Bookmark } from "./Helpers/Bookmarks.js"
    import { useGeneralStore } from '@/stores/general'
    import { useDatasetStore } from '@/stores/dataset'
    import { watch } from 'vue'

    export default {
        data() {
          return {
              bookmarks: [],
              gstore: useGeneralStore(),
              datasetstore: useDatasetStore()
          }
        },
        computed: {
        },
        mounted() {
            this.handle_bookmarks()
            watch(() => this.gstore.amount_bookmarks, (newValue, oldValue) => {
              this.handle_bookmarks()
          });
        },
        methods: {
          handle_bookmarks(){
              this.bookmarks = Bookmark.getBookmarksObj()
              for(let i = 0; i<this.bookmarks.length; i++){
                this.handle_bookmark(i)
              }
              
          },
          async handle_bookmark(i){
              let dataset_description = await this.datasetstore.read_dataset_description(this.bookmarks[i].database, this.bookmarks[i].collection)
              this.bookmarks[i].image = dataset_description.image;
              this.bookmarks[i].title = dataset_description.dataset_display_title;
              
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