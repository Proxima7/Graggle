<template>
   
    <div class="font-semibold mx-2 text-3xl underline mt-4">Analytics</div>   
    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            Data Schema Analysis:
        </div>
        <div class="col-span-4 px-2">
            Getting insights how the data is structured!
        </div>
    </div>

    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            Distinct Keys:
        </div>
        <div class="col-span-4 px-2">
            What keys are inside of the data and howto access them!
        </div>
    </div>

    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            Image:
        </div>
        <div class="col-span-4 px-2">
            How many images per class? How many images in total? Image quality?
        </div>
    </div>

    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            Metrics / Analysis:
        </div>
        <div class="col-span-4 px-2">
            Data quality? Outliers inside of the data/images? Duplicates? Special data? Abnormality?
        </div>
    </div>

    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            AI/ML:
        </div>
        <div class="col-span-4 px-2">
            Execution of models (e.g. fruit) direct on the image data.
        </div>
    </div>

    <!--
        DIVERSES
    -->
    <div class="font-semibold mx-2 text-3xl underline mt-4">Miscellaneous</div>   
    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            Filtering:
        </div>
        <div class="col-span-4 px-2">
            Advanced data filtering with drag'n'drop. Save and editing of create filters.
        </div>
    </div>

    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            Export/Import:
        </div>
        <div class="col-span-4 px-2">
            Export of filtered data in well-established format (e.g. COCO) for further processes (e.g. external annotation). 
            Import of data from well-established format for useres and external sources.
        </div>
    </div>

    <div class="grid grid-cols-5  py-2 px-4 rounded text-lg  border-2">
        <div class="col-span-1 flex items-center justify-end font-semibold">
            UI:
        </div>
        <div class="col-span-4 px-2">
            Responsive design well usable on desktop and mobile. Upload of images direct from the smartphone. 
        </div>
    </div>


</template>

<script>

import { useGeneralStore } from '@/stores/general'
import { useDatasetStore } from '@/stores/dataset'
import { watch } from 'vue'

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
        this.reset(true)
        this.datasetstore.load()

        watch(() => this.gstore.selected_col, (newValue, oldValue) => {
            this.reset(true)
            this.datasetstore.load()
        });
    },     
    methods: {       
        reset(complete){
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
