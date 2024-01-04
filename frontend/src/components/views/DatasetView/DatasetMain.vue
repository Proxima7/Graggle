<template>
    <div class="bg-white  w-full h-full">
        <div class="flex flex-col h-full">
            
            <DatasetDescription/>
            <div class="bg-white py-2 h-full">
                <!-- tabs: each one is toggable like in the vs code menu-->
                <ul class="flex flex-wrap text-sm font-medium text-center text-gray-300 border-b border-gray-300">
                    <li v-for="tab in tabs" class="mr-2">
                        <div 
                        @click="activate(tab.id)" 
                        :class="!tab.active ? 'text-gray-600 hover:text-gray-900' : ' bg-gray-500 text-gray-900 border-primary border-b-2 font-bold'"
                        class="inline-block bg-gray-300  rounded-t-lg active cursor-pointer
                                text-xs laptop:text-sm desktop:text-lg 4k:text-xl
                                p-1 laptop:p-2 desktop:p-3 4k:p-3">
                            {{tab.title}}
                        
                        </div>
                    </li>
                </ul>

                <div class="mt-2">
                    <div v-if="activeTab === 1">
                        <DatasetExplorer/>
                    </div>
                    <div v-if="activeTab === 2">
                        <DatasetDetails/>
                    </div>
                    <div v-if="activeTab === 3">
                        <DatasetAnalytics/>
                    </div>
                </div>
            </div>
            
            

          
        </div>
        
    </div>
</template>

<script>
import DatasetAnalytics from "./DatasetAnalytics.vue"
import DatasetDescription from "./DatasetDescription.vue"
import DatasetDetails from "./DatasetDetails.vue"
import DatasetExplorer from "./DatasetExplorer.vue"
// if you used v1.0.5 or latster ,you should add import "vue3-json-viewer/dist/index.css"
import { useGeneralStore } from '@/stores/general'
import { useDatasetStore } from '@/stores/dataset'
import { watch } from 'vue'



export default {

    
    data () {
        return {
            activeTab: 1,
            tabs: [
                {active: true, title: 'Explorer', id: 1, comp: "DatasetExplorer"},
                {active: false, title: 'Details', id: 2, comp: "DatasetDetails"},
                {active: false, title: 'Analytics', id: 3, comp: "DatasetAnalytics"}                
            ],                        
            gstore: useGeneralStore(),
            datasetstore: useDatasetStore()
        }
    },
    mounted() {
        watch(() => this.gstore.selected_dataset_id, (newValue, oldValue) => {
            this.activate(2)
        });
    },
    computed: {
    },     
    methods: {
        activate(id){
            this.activeTab = id
            for(let i=0; i<this.tabs.length; i++){
                if(this.tabs[i]['id']==id){
                    this.tabs[i]['active'] = true
                } else {
                    this.tabs[i]['active'] = false
                }
            }
        }
    },
    components: {
        DatasetDescription,
        DatasetDetails,
        DatasetExplorer,
        DatasetAnalytics
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

.expand-enter-active {
  transition: height 0.3s;
}

.expand-leave-active {
  transition: height 0.3s;
}
</style>