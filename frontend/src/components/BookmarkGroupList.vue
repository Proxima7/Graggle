<template>
    <div class="w-full">      

      <div class="grid grid-cols-1 gap-2 ">
        <div>
          <loading-overlay class="relative" v-if="is_loading" :loading="is_loading" headline="Loading" subline="Bookmark Groups"></loading-overlay>
        </div>
        

        <div v-for="group in bookmarkgroups" class="bg-gray-300 mb-2 py-2 px-2 rounded">
          <div class="text-xl laptop:text-2xl desktop:text-3xl 4k:text-3xl text-secondary w-100 leading-2 font-bold border-b-4 mb-2 border-secondary">Name: {{ group.name }}</div>
          <div v-for="bookmark in group.datasets" class="bg-secondary py-2 px-2 mb-1 rounded" @click="set_selected_collection(bookmark.database, bookmark.collection)">
            <div class="relative grid max-[1000px]:grid-cols-1 min-[1000px]:grid-cols-3 gap-2 "
              @mouseenter="overlay_db=bookmark.database, overlay_col=bookmark.collection" @mouseleave="overlay_db='', overlay_col='' ">
                <div class="flex items-center justify-center">
                  <img v-if="bookmark.image!=''" :src="bookmark.image" class="rounded mx-auto ">
                </div>
                <div class="">
                  <div class="font-semibold max-[1000px]:text:sm min-[1000px]text-lg">{{ bookmark.title }}</div>
                  <div class="text-gray-500 text-xs min-[1000px]:col-span-2">{{ bookmark.collection }}</div>
                </div> 
                
                <!-- Overlay -->
                <div v-if="overlay_db==bookmark.database && overlay_col==bookmark.collection">
                  <div class="absolute inset-0 bg-gray-700 opacity-20">
                  </div>
                  <button class="absolute top-1/2 left-1/3 transform -translate-x-1/2 -translate-y-1/2 bg-white font-bold py-2 px-4 rounded
                      text-sm laptop:text-lg desktop:text-xl 4k:text-2xl" @click="remove(group.name, overlay_db, overlay_col)">
                      <font-awesome-icon class="text-black" icon="fa-solid fa-trash" /> 
                  </button>
                  <button class="absolute top-1/2 left-2/3 transform -translate-x-1/2 -translate-y-1/2 bg-white font-bold py-2 px-4 rounded
                      text-sm laptop:text-lg desktop:text-xl 4k:text-2xl" @click="open_bookmark_dialog_on_dataset(overlay_db, overlay_col)">
                      <font-awesome-icon class="text-black" icon="fa-solid fa-pen" /> 
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
    import LoadingOverlay from "./Helpers/LoadingOverlay.vue"
    import requestHandler from "../logic/RequestHandler"

    export default {
        data() {
          return {
              is_loading: false,
              bookmarkgroups: [],
              gstore: useGeneralStore(),
              datasetstore: useDatasetStore(),
              overlay_db: "",
              overlay_col: "",

          }
        },
        computed: {
        },
        mounted() {
            this.handle_bookmark_groups(this.gstore.global_storage)

            watch(() => this.gstore.amount_bookmark_groups, (newValue, oldValue) => {
              this.handle_bookmark_groups(this.gstore.global_storage)
            });

            watch(() => this.gstore.global_storage, (newValue, oldValue) => {
              this.handle_bookmark_groups(this.gstore.global_storage)
            });
        },
        methods: {
          async handle_bookmark_groups(global){
            this.is_loading = true
            this.bookmarkgroups = []
            this.bookmarkgroups = await BookmarkGroups.getBookmarkGroups("",  "")            
              
            
            for(let i=0; i<this.bookmarkgroups.length; i++){
              for(let ds=0; ds<this.bookmarkgroups[i].datasets.length; ds++){
                  let db = this.bookmarkgroups[i].datasets[ds].db
                  let col = this.bookmarkgroups[i].datasets[ds].col
                  this.handle_bookmark(i, ds, db, col, this.bookmarkgroups)
              }
            }   
            this.is_loading=false       
          },

          async handle_bookmark(i, ds, db, col, new_bookmarkgroups){
              new_bookmarkgroups[i].datasets[ds].collection = col;
              new_bookmarkgroups[i].datasets[ds].database = db;
              new_bookmarkgroups[i].datasets[ds].title = db;

              let dataset_description = await this.datasetstore.read_dataset_description(db, col)
              new_bookmarkgroups[i].datasets[ds].image = dataset_description.image;
              new_bookmarkgroups[i].datasets[ds].title = dataset_description.dataset_display_title;
              
              
          },
          async open_bookmark_dialog_on_dataset(db, col){
            this.set_selected_collection(db,col)
            let sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
            await(100)
            this.gstore.cmd = "bookmarkgroupsdialog"

          },
          set_selected_collection(db, col){
              this.gstore.selected_db = db
              this.gstore.selected_col = col
          },
          async remove(groupname, db, col){
            await BookmarkGroups.removeBookmarkGroup(groupname, db,  col, this.gstore)
            this.handle_bookmark_groups()
          }
        },
    components: { 
        LoadingOverlay
    }
    }
  </script>
  
  <style>
  </style>