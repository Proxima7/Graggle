<template>
    <div class="border-2 shadow rounded pb-2 px-2">
        <div class="flex p-0.5 gap-x-1 justify-center pb-2">
            <button v-if="false" @click="reload()" :disabled="records_queried>datasetstore.documents.lenght" 
                class="w-48 text-gray-600 bg-gray-300 font-bold rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">
            <font-awesome-icon icon="fa-shuffle" />
                reload
            </button>   
            
            <div class="grid grid-cols-11 gap-0">
                <div class="col-span-2 "></div>
                <div class="col-span-7 flex mx-1 justify-left">
                    <p class="text-3xl font-bold"><small>DATASET FILTER (MongoDB like)</small></p>
                </div>
                <div class="col-span-2 "></div>

                <div class="col-span-2 "></div>
                <div class="col-span-5 flex border-2 rounded mx-1 relative">
                    <input type="filter" name="filter" id="filter" v-model="filter" class=" block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="Type a query: { field: 'value'}"/>
                </div>
                <div class="col-span-2 flex p-0.5 gap-x-1 justify-center">
                    <button @click="resetFilter()" class="w-44 bg-gray-300 font-bold text-gray-700 rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Reset</button>
                    <button @click="find()" class="w-44 bg-green-900 font-bold text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Find next</button>
                </div>
                <div class="col-span-2 "></div>

            </div> 

        </div>
        <div class="grid grid-cols-6 gap-4">
            <img v-for="(dataset_img, index) in datasetstore.data_get_all_image()" 
                    @contextmenu.prevent="showMenu($event)"
                    class="h-44" 
                    :src="dataset_img"
                    @click="click_select(index)"
                    :class="is_selected(index) ? 'opacity-75 border-8 border-red-600' : 'opacity-100'"/>
        </div>
        <div v-show="isMenuVisible" ref="menu" class="absolute bg-primary border-2 p-1 border-black w-48" :style="{ top: menuPosition.top + 'px', left: menuPosition.left + 'px' }">
            <ul>
                <li v-for="(menuItem, index) in menuItems" :key="menuItem.id" @click="handleMenuItemClick(menuItem)"
                    class="p-1 text-gray-300 font-bold " 
                    :class="index==(menuItems.length-1) || index==2 || index==4 ? 'border-t-2 border-black' : ''">
                    {{ menuItem.label }}
                </li>
            </ul>
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
            selection: [],
            visible: true,
            records_max: 24,
            records_queried: 0,          
            gstore: useGeneralStore(),
            datasetstore: useDatasetStore(),

            isMenuVisible: false,
            menuPosition: {
                top: 0,
                left: 0
            },
            menuItems: [
                { id: 1, label: 'Delete' },
                { id: 2, label: 'Move' },
                { id: 3, label: 'Download selected' },
                { id: 4, label: 'Download all' },
                { id: 5, label: 'Export selected' },
                { id: 6, label: 'Export all' },
                { id: 7, label: 'Exit' }
            ]
        }
    },
    mounted() {
        this.visible = true
        this.reload()

        watch(() => this.gstore.selected_col, (newValue, oldValue) => {
            this.reload()
        });
    },   
    unmounted() {
        this.visible = false
    },
    methods: { 
        showMenu(event) {
            if(this.selection.length>0){
                this.isMenuVisible = true;
                this.menuPosition = {
                    top: event.clientY,
                    left: event.clientX
                };
                // Listen for click events on the document to close the menu
                document.addEventListener('click', this.handleOutsideClick);
            }            
        },
        handleOutsideClick(event) {
            // Check if the click event target is outside the menu
            const menu = this.$refs.menu;
            if (!menu.contains(event.target)) {
                this.isMenuVisible = false;
                document.removeEventListener('click', this.handleOutsideClick);
            }
        },
        handleMenuItemClick(menuItem) {
            // Perform actions based on the clicked menu item
            this.isMenuVisible = false;
            this.selection = []
        },
        is_selected(index){
            return this.selection.includes(index)
        },
        click_select(index) {
            let selected = this.is_selected(index)
            if (selected) {
                // Remove the value from the list
                const myindex = this.selection.indexOf(index);
                if (myindex > -1) {
                    this.selection.splice(myindex, 1);
                }
            } else {
                // Add the value to the list
                this.selection.push(index);
            }
        },
        reload(){
            this.reset()
            this.load()
        },
        reset(){      
            this.records_queried = 0
            this.selection = []
            this.datasetstore.reset()      
            this.datasetstore.load_dataset_description()
        },
        async load(){
            this.datasetstore.low_resolution = true
            let col = this.gstore.selected_col
            while(this.records_queried<this.records_max && col == this.gstore.selected_col && this.visible){
                await this.datasetstore.get_data(false)
                this.records_queried = this.records_queried + 1
            }
            this.datasetstore.low_resolution = false
        },
        resetFilter(){
            this.reset()  
            this.filter = ""
            this.datasetstore.set_filter("")          
            this.load()
        },
        find(){            
            this.reset()
            this.datasetstore.set_filter(this.filter)
            this.load()
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
