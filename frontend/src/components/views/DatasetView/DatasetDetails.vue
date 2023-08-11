<template>
    <!--
        Data Card
    -->
    <div class="grid grid-cols-6 gap-2 grid-rows-auto border-2 shadow rounded p-2 mt-2">
        <!--
            Explorer + prev/next
        -->
        <div class="max-[1800px]:flex max-[1800px]:col-span-6 min-[1800px]:col-span-2 mt-4 text-sm laptop:text-lg desktop:text-xl 4k:text-2xl">
            <div class="min-[1800px]:flex font-bold tracking-tight justify-center mr-8">Explorer&nbsp;({{ gstore.selected_db }} / {{ gstore.selected_col }})</div>
            <div class="min-[1800px]:flex mt-1 p-0.5 gap-x-1 justify-center text-xs laptop:text-sm desktop:text-lg 4k:text-lg">
                <button @click="datasetstore.data_prev()" :disabled="!datasetstore.data_has_prev()" class="w-32 bg-primary font-bold text-gray-300 rounded m-0.5 py-2 mr-1 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">
                <font-awesome-icon icon="fa-chevron-left" />
                    previous
                </button>
                <button @click="datasetstore.data_next()" :disabled="!datasetstore.data_has_next()" class="w-32 bg-primary font-bold text-gray-300 rounded m-0.5 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_next">              
                    next 
                    <font-awesome-icon icon="fa-chevron-right" />
                </button>
            </div>
        </div>

        <div class="max-[1800px]:col-span-6 min-[1800px]:col-span-4 mt-4 border-2 shadow rounded p-1">
            <div class="grid grid-cols-6 gap-0">
                <div class="col-span-6 flex mx-4 justify-left">
                    <p class="text-3xl font-bold"><small>DATASET FILTER (MongoDB like)</small></p>
                </div>
                <div class="col-span-6 tablet:col-span-6 laptop:col-span-4 desktop:col-span-5 k4:col-span-5 flex border-2 rounded mx-2 relative">
                    <input type="filter" name="filter" id="filter" v-model="filter" class=" block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="Type a query: { field: 'value'}"/>
                </div>
                <div class="col-span-6 tablet:col-span-6 laptop:col-span-2 desktop:col-span-1 k4:col-span-1 flex p-0.5 gap-x-1 justify-center">
                    <button @click="resetFilter()" class="w-32 bg-gray-300 font-bold text-gray-700 rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Reset</button>
                    <button @click="find()" class="w-32 bg-green-900 font-bold text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_next">Find</button>
                </div>
            </div>                    
        </div>

        <!--
            JSON viewer + Annatorious Image
        -->        
        <div class="max-[1800px]:col-span-6 min-[1800px]:col-span-2 flex flex-col  max-[1800px]:max-h-[330px] min-[1800px]:h-full" >
            <div class="flex-1 border-2 shadow rounded p-4 max-[1800px]:max-h-[330px]">
                <div class="max-[1800px]:max-h-[330px]">
                    <p class="text-3xl font-bold max-[1800px]:max-h-[35px]"><small>JSON</small></p>
                    <vue-json-pretty :data="datasetstore.data_get_current_documents()" expand=true  
                        deep="3" virtual=true editable=true height=540 showLength=true @onKeyClick="keyClick" 
                        class="max-[1800px]:max-h-[265px]"/>                    
                </div>
            </div>
        </div>

        <div class="max-[1800px]:col-span-6 min-[1800px]:col-span-4 border-2 shadow rounded ">
            <p class="text-3xl font-bold p-2"><small>IMAGE</small></p>
            <div class="flex" style="min-height: 490px">
                <AnnotoriousImage :key="datasetstore.data_get_current_image()" v-if="datasetstore.data_has_data()" :img_url="datasetstore.data_get_current_image()" :annotations="datasetstore.data_get_current_documents().annotations"  class=""/>
            </div>
        </div>
    </div>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty';
import AnnotoriousImage from "../../Tagging/AnnotoriousImage.vue"
import LoadingOverlay from "../../Helpers/LoadingOverlay.vue"
import { useGeneralStore } from '@/stores/general'
import { useDatasetStore } from '@/stores/dataset'
import { watch } from 'vue'
import 'vue-json-pretty/lib/styles.css';

export default {
    props: {
        dataset_description: null
    },
    data () {
        return {
            filter: "",            
            gstore: useGeneralStore(),
            datasetstore: useDatasetStore()
        }
    },
    mounted() {
        this.datasetstore.reset()
        this.datasetstore.low_resolution = false
        this.datasetstore.load()

        watch(() => this.gstore.selected_col, (newValue, oldValue) => {
            this.reset(true)
            this.datasetstore.load()
        });
    },     
    methods: {       
        reset(complete){
            this.datasetstore.low_resolution = false
            this.datasetstore.reset()      
            if(complete){
                this.datasetstore.reset_dataset_description()
                this.datasetstore.set_filter("")
            }       
        },
        keyClick(keyName) {
            alert(keyName);
        },
        resetFilter(){
            this.reset(false)  
            this.filter = ""
            this.datasetstore.set_filter("")          
            this.datasetstore.get_data(true)
        },
        find(){            
            this.reset(false)
            this.datasetstore.set_filter(this.filter)
            this.datasetstore.get_data(true)
        }
        
    },
    components: {
        LoadingOverlay,
        AnnotoriousImage,
        VueJsonPretty
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
