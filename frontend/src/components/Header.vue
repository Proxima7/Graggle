<template>
    <div class="grid grid-cols-12 bg-blue-900 text-white py-2">
        <!-- logo and left side-->
        <div class="col-span-2 p-2 flex justify-center m-auto">
            <a href="/" class="">
                <img class="h-14" src="../assets/graggle_logo_large.png" @click="resetSelectedCollection()"/>
            </a>
        </div>
        <div class="col-span-10 flex">
            <div class="grow relative justify-center m-auto ">
                <input type="text" v-model="filter" class="w-full text-3xl h-14 pl-12 bg-gray-800 text-gray-300 rounded-full focus:outline-none focus:shadow-outline" placeholder="Search...">
                <div class="absolute w-10 left-3 top-4 ">
                    <font-awesome-icon icon="fa-solid fa-xmark" class="text-gray-300 text-3xl" @click="clear()"/>
                </div>
                <div class="absolute mr-2 w-10 right-0 top-4">
                    <font-awesome-icon icon="fa-solid fa-search" class="text-gray-300 text-3xl" @click="search()"/>
                </div>
            </div>
            <div class="flex-none w-44 justify-center m-auto">
                <a href="#" class="mx-4">
                    <font-awesome-icon icon="fa-solid fa-user" class="text-3xl" />
                </a>
                <button class="right-0 bg-blue-800 text-white rounded-full px-8 py-2 hover:bg-blue-700 focus:outline-none focus:shadow-outline">
                    Sign In
                </button>
            </div>
        </div>        
    </div>
  </template>
  
  <script>
  export default {
    data(){
        return{
            filter: ""
        }
    },
    components: {
    },
    methods: {
        clear(){
            this.$store.state.selected_db = ""
            this.$store.state.selected_col = ""
            this.$store.state.filter = ""
            this.filter = ""
        },
        async search(){
            let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));   
            this.$store.state.selected_db = ""
            this.$store.state.selected_col = ""
            this.$store.state.filter = ""
            await sleep(50);
            this.$store.state.filter = this.filter
        },
        resetSelectedCollection(){
            this.$store.state.selected_db = ""
            this.$store.state.selected_col = ""
            this.$store.state.filter = ""
            this.filter = ""
        }
    }
  }
  </script>
  