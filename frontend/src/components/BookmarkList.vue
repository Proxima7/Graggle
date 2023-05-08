<template>
    <div class="w-full">
      <div class="grid grid-cols-1 gap-2 ">
        <div v-for="bookmark in bookmarks" class="bg-secondary py-2 px-2 rounded" @click="set_selected_collection(bookmark.database, bookmark.collection)">
          <div class="grid grid-cols-3 gap-2 ">
            <div class="flex items-center justify-center">
              <img v-if="bookmark.image!=''" :src="bookmark.image" class="rounded mx-auto">
            </div>
            <div class="">
              <div class="font-semibold text-lg">{{ bookmark.database }}</div>
              <div class="text-gray-500 text-xs">{{ bookmark.collection }}</div>
            </div>
          </div>
        </div >
      </div>
    </div>
  </template>
  
  <script>
    import { Bookmark } from "./Helpers/Helper.js"
    import requestHandler from "../logic/RequestHandler"
    import { mapState } from 'vuex'

    export default {
        data() {
          return {
              bookmarks: []
          }
        },
        computed: {
            ...mapState(['amount_bookmarks'])
        },
        mounted() {
            this.handle_bookmarks()
        },
        methods: {
          handle_bookmarks(){
              this.bookmarks = Bookmark.getBookmarksObj()
              for(let i = 0; i<this.bookmarks.length; i++){
                this.get_dataset_description(i)
              }
          },
          set_selected_collection(db, col){
            this.$store.state.selected_db = db
                this.$store.state.selected_col = col
          },
          async get_dataset_description(index) {
              var that = this;
              var dataset_description_callback = function (resp) {
                  that.bookmarks[index].image = resp.data.image;
              };
              var dataset_description_callback_error = function (error) {
              };
              let db = this.bookmarks[index].database
              let col = this.bookmarks[index].collection
              requestHandler.get_dataset_description(dataset_description_callback, dataset_description_callback_error, db, col);
          }
        },
    watch: {
        amount_bookmarks(newValue, oldValue) {
            this.handle_bookmarks()
        }
    }
    }
  </script>
  
  <style>
  </style>