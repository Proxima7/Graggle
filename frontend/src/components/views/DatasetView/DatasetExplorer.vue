<template>
    <div class="bg-white py-2 px-2 lg:px-2 w-full h-full">
        <div class="flex flex-col h-full">
            <!--
                Data Card
            -->
            <div class="m-2 border-2 shadow rounded p-4">
                <div class="mx-auto flex border-primary relative">
                <loading-overlay v-if="loading" :loading="loading" headline="Loading" subline="Data Card"></loading-overlay>

                <!-- left content-->
                <div class="lg:pr-8 lg:pt-4 w-1/2">                    
                    <!-- load skeleton-->
                    <div v-if="dataset_description === null">
                        <div role="status" class="max-w-sm animate-pulse">
                            <div class="h-6 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4 border-b-2 border-primary"></div>
                            <div class="h-3 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[250px] mb-2.5"></div>
                            <div class="h-3 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                            <div class="h-3 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                            <div class="h-3 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[150px] mb-2.5"></div>
                            <div class="h-3 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                            <span class="sr-only">Loading...</span>
                        </div>

                        
                    </div>
                    <!-- real CONTENT-->
                    <div v-else>
                        <div class="mx-auto flex  relative">
                            <div class="w-1/2">
                                <p class="text-3xl font-bold tracking-tight sm:text-4xl">{{ dataset_description.dataset_display_title }}</p>
                            </div>
                            <div class="w-1/2 flex justify-end">
                                <p class="text-3xl font-bold tracking-tight">
                                    <font-awesome-icon class="px-1" icon="fa-solid fa-share-nodes" @click='share()'/>
                                    <font-awesome-icon v-if="bookmarked==false" class="px-1" icon="fa-regular fa-bookmark" @click='bookmark()'/>
                                    <font-awesome-icon v-if="bookmarked==true" class="px-1" icon="fa-solid fa-bookmark" @click='unbookmark()'/>
                                    <font-awesome-icon class="px-1" icon="fa-solid fa-comments" @click='comments()'/>
                                    <font-awesome-icon class="px-1" icon="fa-regular fa-pen-to-square" />
                                </p>
                            </div>
                        </div>
                        
                        
                        <p class="mt-6 text-lg leading-8">{{ dataset_description.dataset_description }}</p>
                    </div>
                </div>

                <!-- right display description card-->
                <div class="w-1/2">
                    <DatasetDescriptionCard :dataset_description="dataset_description"/>
                </div>

                <!-- overlay with button to add data-->    
                <div v-if="(dataset_description === null || dataset_description.dataset_display_title === '<<Titel>>') && $store.state.selected_col != '' && loading === false" > 
                    <div class="absolute inset-0 bg-gray-700 opacity-20"></div>
                    <button class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white font-bold py-2 px-4 rounded" @click="dataset_add_dialog_show = !dataset_add_dialog_show">
                        <font-awesome-icon class="pr-2" icon="fa-solid fa-circle-plus" /> Add Description
                    </button>
                </div>
                </div>
            </div>

            <!--
                Explorer + prev/next
            -->
            <div class="grid grid-cols-6 gap-4 grid-rows-auto m-2 border-2 shadow rounded p-4">
                <div class="col-span-2 mt-4">
                    <p class="font-bold tracking-tight text-4xl flex justify-center">Explorer&nbsp;<small>({{ $store.state.selected_db }} / {{ $store.state.selected_col }})</small></p>
                    <div class="flex mt-1 p-0.5 gap-x-1 justify-center">
                        <button @click="prev" :disabled="index==0" class="w-32 bg-primary font-bold text-gray-300 rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">
                        <font-awesome-icon icon="fa-chevron-left" />
                            previous
                        </button>
                        <button @click="next" :disabled="next_disabled" class="w-32 bg-primary font-bold text-gray-300 rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_next">              
                            next 
                            <font-awesome-icon icon="fa-chevron-right" />
                        </button>
                    </div>
                </div>
                <div class="col-span-4 mt-4 border-2 shadow rounded p-1">
                    <div class="grid grid-cols-6 gap-0">
                        <div class="col-span-6 flex mx-4 justify-left">
                            <p class="text-3xl font-bold"><small>DATASET FILTER (MongoDB like)</small></p>
                        </div>
                        <div class="col-span-5 flex border-2 rounded mx-4 relative">
                            <input type="filter" name="filter" id="filter" v-model="filter" class=" block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="Type a query: { field: 'value'}"/>
                        </div>
                        <div class="col-span-1 flex p-0.5 gap-x-1 justify-center">
                            <button @click="resetFilter" class="w-32 bg-gray-300 font-bold text-gray-700 rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Reset</button>
                            <button @click="find" class="w-32 bg-green-900 font-bold text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Find</button>
                        </div>
                    </div>                    
                </div>

            <!--
                JSON viewer + Annatorious Image
            -->        
                <div class="col-span-2 flex flex-col h-full" style="min-height: 540px">
                    <div class="flex-1 overflow-y-auto border-2 shadow rounded p-4">
                        <div class=" ">
                            <p class="text-3xl font-bold"><small>JSON</small></p>
                            <JsonViewer :value="documents[index]" copyable sort theme="light" @onKeyClick="keyClick" />
                        </div>
                        <!--<JsonViewer v-for="doc in documents" :value="doc" copyable sort theme="light" @onKeyClick="keyClick" />-->
                    </div>
                </div>
                <div class="col-span-4 border-2 shadow rounded p-4">
                    <p class="text-3xl font-bold"><small>IMAGE</small></p>
                    <div class="flex" style="min-height: 410px">
                        <AnnotoriousImage :key="image" v-if="images" :img_url="image" :annotations="documents[index].annotations"  class=""/>
                    </div>
                </div>
            </div>

          
        </div>
        <DatasetAddDialog :showDialog=dataset_add_dialog_show @update:showDialog="dialog_finished"></DatasetAddDialog>
    </div>
</template>

<script>
import AnnotoriousImage from "../../Tagging/AnnotoriousImage.vue"
import DatasetDescriptionCard from "./DatasetDescriptionCard.vue"
import DatasetAddDialog from "./DatasetAddDialog.vue"
import { JsonViewer } from "vue3-json-viewer"
// if you used v1.0.5 or latster ,you should add import "vue3-json-viewer/dist/index.css"
import "vue3-json-viewer/dist/index.css";
//import { reactive, ref } from "vue";
import requestHandler from "../../../logic/RequestHandler"
import LoadingOverlay from "../../Helpers/LoadingOverlay.vue"
import { Helper, Bookmark } from "../../Helpers/Helper.js"

import { mapState } from 'vuex'

export default {

    data () {
        return {
            loading: false,
            dataset_add_dialog_show: false,
            dataset_description: null,
            images: null,
            image: null,
            index: 0,
            next_disabled: true,
            prev_disabled: true,
            bookmarked: false,
            filter: "",
            documents: [{
                "loading": "we are currently fetching the data from the database. Please wait a few seconds.",
            }]
        }
    },
    mounted() {
        this.reset(true)
        this.get_dataset_description()
        this.get_dataset(true)
    },
    computed: {
        ...mapState(['selected_col'])
    },     
    methods: {
        bookmark(){
            this.bookmarked=true
            Bookmark.bookmark(this.$store)
        },
        unbookmark(){
            this.bookmarked=false
            Bookmark.unbookmark(this.$store)            
        },
        isbookmarked(){
            return Bookmark.isbookmarked(this.$store) 
        },
        comments(){
            this.$emit('transferCommand', 'comments')
        },
        async share(){
            if (true) {
               
                try {
                    await navigator.share({
                        title: 'Share graggle webside!',
                        text: 'Bizerba Data Catalog',
                        url: 'http://localhost:5173/'
                    });
                } catch (error) {
                    console.log('Error sharing:', error);
                }
            }
        },
        get_dataset_description() {
            var that = this;
            this.loading = true;
            var dataset_description_callback = function (resp) {
                that.dataset_description = resp.data;
                that.loading = false;
            };

            var dataset_description_callback_error = function (error) {
                if(error.response.status == 404){
                    that.dataset_description = null
                }
                that.loading = false;
            };

            let db = this.$store.state.selected_db
            let col = this.$store.state.selected_col
            requestHandler.get_dataset_description(dataset_description_callback, dataset_description_callback_error, db, col);
        },

        async get_dataset(next) {
            var that = this;
            var data_callback = function (resp) {
                if ('loading' in that.documents[0]) {
                    that.documents = []
                    that.images = []
                } 

                // create image url usable in anatorious
                that.images.push(Helper.base64_to_url(resp.data['image']))                
                that.image = that.images[that.index]                
                
                //remove huge base64 from json
                let document = resp.data
                delete document['image']
                that.documents.push(document)

                // load next image
                if(next){
                    that.get_dataset(false)
                } else{
                    that.next_disabled = false
                }          
            };

            var data_callback_error = function (error) {
                //that.loading = false;
            };


            let db = this.$store.state.selected_db
            let col = this.$store.state.selected_col
            let number =  this.documents.length
            if ('loading' in that.documents[0]) {
                number=0
            }
            var axiosreq = requestHandler.get_dataset(data_callback, data_callback_error, db, col, number, this.filter || "{}");
        },
        
        keyClick(keyName) {
            alert(keyName);
        },
        dialog_finished(){
            this.dataset_add_dialog_show=false
            this.get_dataset_description()
        },
        reset(complete){
            this.images = null
            this.image = null
            this.index = 0
            this.documents= [{
                "loading": "",
            }]
            if(complete){
                this.dataset_description = null
                this.bookmarked = this.isbookmarked()
                this.filter = ""
            }            
        },
        next(){
            if(this.index == (this.images.length-2)){
                this.next_disabled = true
                this.get_dataset(false)
            }            
            this.index = this.index+1
            this.image = this.images[this.index]
        },
        prev(){
            this.index = this.index-1
            this.image = this.images[this.index]
        },
        resetFilter(){
            this.reset(false)
            this.get_dataset(true)
        },
        find(){
            this.reset(false)
            this.get_dataset(true)
        }
    },
    watch: {
        selected_col(newValue, oldValue) {
            this.reset(true)
            this.get_dataset_description()
            this.get_dataset(true)
        }
    },
    components: {
        AnnotoriousImage,
        DatasetDescriptionCard,
        DatasetAddDialog,
        LoadingOverlay
    }
} 
</script>

<style>
    .jv-code {
        padding: 5px 20px !important;
    }
    small {
        font-size: 60%;
    }
</style>