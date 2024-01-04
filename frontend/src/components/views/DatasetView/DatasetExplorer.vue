<template>
    <div class="border-2 shadow rounded pb-2 px-2">
        <div class="flex p-0.5 gap-x-1 justify-center pb-2"> 
            
            <div class="grid grid-cols-12 gap-0 text-sm laptop:text-xl desktop:text-2xl 4k:text-3xl">
                <div class="justify-center col-span-12 flex mx-1 justify-left">
                    <p class="font-bold">DATASET FILTER (MongoDB like)</p>
                </div>
                <div class="col-span-12 
                    flex flex-col laptop:flex-row desktop:flex-row 4k:flex-row justify-center max-[1024px]:justify-items-stretch ">                
                    <div class="border-2 rounded m-1 relative min-w-[300px] laptop:min-w-[300px] desktop:min-w-[750px] 4k:min-w-[1000px]">
                        <input type="filter" name="filter" id="filter" v-model="filter" class="min-w-[300px] laptop:min-w-[300px] desktop:min-w-[850px] 4k:min-w-[1000px] border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="Type a query: { field: 'value'}"/>
                    </div>
                    <button @click="resetFilter()" class="min-[1024px]:w-44 bg-gray-300 font-bold text-gray-700 rounded m-1 px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Reset</button>
                    <button @click="find()" class="min-[1024px]:w-44 bg-green-900 font-bold text-white rounded m-1 px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_prev">Find next</button>
                </div>
            </div> 

        </div>
        <div class="grid grid-cols-2 tablet:grid-cols-3 laptop:grid-cols-4 desktop:grid-cols-6 4k:grid-cols-12 max-[800px]:gap-1 min-[800px]:gap-4">
            <img v-for="(document, index) in datasetstore.data_get_all_documents()" 
                    @contextmenu.prevent="showMenu($event)"
                    class="" 
                    :src="document.blobimage"
                    @click="click_select(index, document)"
                    :class="is_selected(index, document) ? 'opacity-75 border-8 border-red-600' : 'opacity-100'"/>
        </div>
        <div v-show="isMenuVisible" ref="menu" class="absolute bg-primary border-2 p-1 border-black w-48" :style="{ top: menuPosition.top + 'px', left: menuPosition.left + 'px' }">
            <ul>
                <li v-for="(menuItem, index) in menuItems" :key="menuItem.id" @click="handleMenuItemClick(menuItem)"
                    class="p-1 text-gray-300 font-bold " 
                    :class="index==(menuItems.length-1) || index==1 || index==3 || index==5 ? 'border-t-2 border-black' : ''">
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
            selectionDocuments: [],
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
                { id: 1, label: 'Details' },
                { id: 2, label: 'Delete' },
                { id: 3, label: 'Move' },
                { id: 4, label: 'Download selected' },
                { id: 5, label: 'Download all' },
                { id: 6, label: 'Export selected' },
                { id: 7, label: 'Export all' },
                { id: 8, label: 'Exit' }
            ]
        }
    },
    mounted() {
        this.visible = true
        this.reload()

        watch(() => this.gstore.selected_col, (newValue, oldValue) => {
            this.reload()
        });

        const screenWidth = window.innerWidth;
        if (screenWidth < 640) {
            this.records_max = 12
        } else if (screenWidth < 1024) {
            this.records_max = 18
        } else if (screenWidth < 1600) {
            this.records_max = 24
        }else if (screenWidth < 2500) {
            this.records_max = 36
        } else {
            this.records_max = 48
        }
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
            if(menuItem.label=="Details"){
                this.gstore.selected_dataset_id = this.selectionDocuments[0]._id
            }
            this.isMenuVisible = false;
            this.selection = []
            this.selectionDocuments = []
        },
        is_selected(index){
            return this.selection.includes(index)
        },
        click_select(index, document) {
            let selected = this.is_selected(index)
            if (selected) {
                // Remove the value from the list
                const myindex = this.selection.indexOf(index);
                if (myindex > -1) {
                    this.selection.splice(myindex, 1);
                    this.selectionDocuments.splice(myindex, 1);
                }
            } else {
                // Add the value to the list
                this.selection.push(index);
                this.selectionDocuments.push(document);
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
            // only when component is visible and current collection doesn't change
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
