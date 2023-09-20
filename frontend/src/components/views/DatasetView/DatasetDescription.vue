<template>
    <!--
        Data Card
    -->
    <div class="border-2 shadow rounded p-2 w-full">
        <div v-if="!isExpanded" >
            <div class="grid grid-cols-12">
                <div class="max-[600px]:col-span-12 min-[600px]:col-span-10">             
                    <div class="font-bold tracking-tight text-lg laptop:text-2xl desktop:text-3xl 4k:text-4xl">
                        <font-awesome-icon class="px-1" icon="fa-solid fa-maximize" @click="isExpanded = true"/>
                         Datacard 
                    </div>
                    <div class="align-top">
                        Database: {{ gstore.selected_db }} <br> 
                        Collection: {{ gstore.selected_col }})
                    </div>
                </div>
                <div class="max-[600px]:col-span-6 min-[600px]:col-span-2 flex justify-end">
                    <img v-if="datasetstore.get_dataset_description() && datasetstore.get_dataset_description().image != ''" :src="datasetstore.get_dataset_description().image" 
                    class="rounded-xl shadow-xl ring-1 ring-gray-400/10 min-[1000px]:w-36"/>
                </div>
            </div>
        </div>
        <div v-if="isExpanded" class="">
            <div class="overflow-hidden transition-height duration-300 mx-auto flex border-primary relative grid grid-cols-4">
                <loading-overlay v-if="datasetstore.is_dataset_loading()" :loading="datasetstore.is_dataset_loading()" headline="Loading" subline="Data Card"></loading-overlay>

                <!-- left content-->
                <div class="col-span-4 desktop:col-span-2 4k:col-span-2">                    
                    <!-- load skeleton-->
                    <div v-if="datasetstore.get_dataset_description() === null">
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
                                
                                <p class="text-ml laptop:text-xl desktop:text-2xl 4k:text-3xl font-bold tracking-tight ">
                                    <font-awesome-icon class="px-1" icon="fa-solid fa-minimize" @click="isExpanded = false"/>
                                    {{ datasetstore.get_dataset_description().dataset_display_title }}
                                </p>
                            </div>
                            <div class="w-1/2 flex justify-end">
                                <p class="text-ml laptop:text-xl desktop:text-2xl 4k:text-3xl font-bold tracking-tight">
                                    <font-awesome-icon class="px-1" icon="fa-solid fa-share-nodes" @click='share()'/>
                                    <font-awesome-icon v-if="bookmarked==false" class="px-1" icon="fa-regular fa-bookmark" @click='bookmark()' @contextmenu="bookmarkgroups($event)"/>
                                    <font-awesome-icon v-if="bookmarked==true" class="px-1" icon="fa-solid fa-bookmark" @click='unbookmark()' @contextmenu="bookmarkgroups($event)"/>
                                    <font-awesome-icon class="px-1" icon="fa-solid fa-comments" @click='comments()'/>
                                    <font-awesome-icon class="px-1" icon="fa-regular fa-pen-to-square" />
                                </p>
                            </div>
                        </div>                        
                        <p class="mt-2 text-sm laptop:text-lg desktop:text-xl 4k:text-2xl">{{ datasetstore.get_dataset_description().dataset_description }}</p>
                    </div>
                </div>

                <!-- right display description card-->
                <div class="col-span-4 desktop:col-span-2 4k:col-span-2">
                    <DatasetDescriptionCard :dataset_description="datasetstore.get_dataset_description()"/>
                </div>

                <!-- overlay with button to add data-->    
                <div v-if="(datasetstore.get_dataset_description() === null || datasetstore.get_dataset_description().dataset_display_title === '<<Titel>>') && gstore.selected_col != '' && datasetstore.is_dataset_loading() === false" > 
                    <div class="absolute inset-0 bg-gray-700 opacity-20">

                    </div>
                    <button class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white font-bold py-2 px-4 rounded
                        text-sm laptop:text-lg desktop:text-xl 4k:text-2xl" @click="dataset_add_dialog_show = !dataset_add_dialog_show">
                        <font-awesome-icon class="pr-2" icon="fa-solid fa-circle-plus" /> Insert Description
                    </button>
                </div>
            </div>

            <DatasetAddDialog :showDialog=dataset_add_dialog_show @update:showDialog="add_dialog_finished"></DatasetAddDialog>

            <BookmarkGroupDialog :showDialog=bookmark_group_dialog_show @update:showDialog="bookmark_group_dialog_finished"></BookmarkGroupDialog>
        </div>
    </div>

</template>

<script>

import LoadingOverlay from "../../Helpers/LoadingOverlay.vue"
import DatasetDescriptionCard from "./DatasetDescriptionCard.vue"
import { useGeneralStore } from '@/stores/general'
import { useDatasetStore } from '@/stores/dataset'
import { Bookmark } from "../../Helpers/Bookmarks.js"
import { watch } from 'vue'
import DatasetAddDialog from "./DatasetAddDialog.vue"
import BookmarkGroupDialog from "./BookmarkGroupDialog.vue"

export default {
    data () {
        return {
            dataset_add_dialog_show: false,
            bookmark_group_dialog_show: false,
            bookmarked: false,
            gstore: useGeneralStore(),
            datasetstore: useDatasetStore(),
            isExpanded: true
        }
    },
    mounted() {
        this.shrink_auto()
        this.reset(true)
        this.datasetstore.load_dataset_description()

        watch(() => this.gstore.selected_col, (newValue, oldValue) => {
            this.reset(true)
            this.datasetstore.load_dataset_description()
        });
    },     
    methods: {
        
        async share(){
            if (true) {               
                try {
                    await navigator.share({
                        title: 'Share graggle webside!',
                        text: 'Bizerba Data Catalog',
                        url: window.location.href
                    });
                } catch (error) {
                    console.log('Error sharing:', error);
                }
            }
        },
        async shrink_auto(){
            let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
            await sleep(3000)
            this.isExpanded = false
        },
        bookmark(){
            this.bookmarked=true
            Bookmark.bookmark(this.gstore)
        },
        unbookmark(){
            this.bookmarked=false
            Bookmark.unbookmark(this.gstore)            
        },
        isbookmarked(){
            return Bookmark.isbookmarked(this.gstore) 
        },
        bookmarkgroups: function(e) {
            this.bookmark_group_dialog_show = !this.bookmark_group_dialog_show
            e.preventDefault();
        },
        reset(complete){
            if(complete){
                this.bookmarked = this.isbookmarked()
            }            
        },
        bookmark_group_dialog_finished(){
            this.bookmark_group_dialog_show = false
        },        
        add_dialog_finished(){
            this.dataset_add_dialog_show = false
            this.datasetstore.load_dataset_description()
        },
        comments(){
            this.gstore.cmd = "comments"
        }
    },
    components: { 
        DatasetDescriptionCard,
        DatasetAddDialog,
        LoadingOverlay,
        BookmarkGroupDialog
    }
}
</script>

<style>
.expand-enter-active {
  transition: height 0.3s;
}

.expand-leave-active {
  transition: height 0.3s;
}
</style>
