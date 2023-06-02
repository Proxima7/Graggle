<template>
    <div class="grid grid-cols-12 bg-blue-900 text-white py-2">
        <!-- logo and left side-->
        <div class="col-span-2 p-2 flex justify-center m-auto">
            <div>
                <img class="h-14" src="../assets/graggle_logo_large.png" @click="resetSelectedCollection()"/>
            </div>
        </div>
        <div class="col-span-10 flex">
            <div class="grow relative justify-center m-auto ">
                <input type="text" v-model="filter" class="w-full text-3xl h-14 pl-12 bg-gray-800 text-gray-300 rounded-full focus:outline-none focus:shadow-outline" placeholder="Search...">
                <div class="absolute w-10 left-3 top-4 ">
                    <font-awesome-icon icon="fa-solid fa-search" class="text-gray-300 text-3xl" @click="search()"/>
                </div>
                <div class="absolute mr-2 w-10 right-0 top-4">
                    <font-awesome-icon icon="fa-solid fa-xmark" class="text-gray-300 text-3xl" @click="clear()"/>
                </div>
            </div>
            <div class="flex w-44 justify-center m-auto">
                <a href="#" class="mx-4">
                    <font-awesome-icon icon="fa-solid fa-user" class="text-3xl mt-2" />
                </a>
                <button class="right-0 bg-blue-800 text-white rounded-full px-8 py-2 hover:bg-blue-700 focus:outline-none focus:shadow-outline">
                    Sign In
                </button>
            </div>
        </div>        
    </div>
  </template>
  
  <script>
  import { useGeneralStore } from '@/stores/general'


  export default {
    data(){
        return{
            filter: "",
            gstore: useGeneralStore()
        }
    },
    computed: {
    },
    components: {
    },
    methods: {
        clear(){
            this.gstore.selected_db = ""
            this.gstore.selected_col = ""
            this.gstore.filter = ""
            this.filter = ""
        },
        async search(){
            let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));   
            this.gstore.selected_db = ""
            this.gstore.selected_col = ""
            this.gstore.filter = ""
            await sleep(50);
            this.gstore.filter = this.filter
        },
        resetSelectedCollection(){
            this.gstore.selected_db = ""
            this.gstore.selected_col = ""
            this.gstore.filter = ""
            this.filter = ""
        }
    }
  }
  </script>
  