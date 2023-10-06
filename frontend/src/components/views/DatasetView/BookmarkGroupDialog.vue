<template>
    <div  class="fixed inset-0 bg-gray-700 opacity-75 z-50" v-if="showDialog"></div>

    <!-- Popup dialog -->
    <div class=" m-4 fixed inset-0 z-50 flex items-center justify-center text-xs laptop:text-lg desktop:text-xl 4k:text-2xl" v-if="showDialog" >
        
        <div class="rounded-lg p-2" style="max-height: 800px">
            <div class="bg-white rounded-lg p-2 ">
                <div class="relative p-6 bg-secondary border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 ">

                    <div class="absolute right-2 top-2">
                        <label class="inline-flex items-center cursor-pointer">
                        <input type="checkbox" class="sr-only peer" v-model="global_checked">
                        <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-secondary peer-focus:ring-4 peer-focus:ring-secondary dark:peer-focus:ring-secondary dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-secondary after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-secondary after:border-secondary after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-secondary peer-checked:bg-green-600"></div>
                        <span class="ml-2 text-sm font-medium text-gray-300 dark:text-gray-300">GLOBAL</span>
                        </label>
                    </div>

                    <a href="#">
                        <h5 class="mb-5 text-2xl font-bold tracking-tight text-gray-900 text-white">{{headline}}</h5>
                    </a>
                    <p class="mb-1 font-normal text-white">Database: {{ gstore.selected_db }}</p>
                    <p class="mb-5 font-normal text-white">collection: {{ gstore.selected_col }}</p>

                    <p class="mb-10 font-normal text-white">Add the dataset to an existing Bookmark Group (left side) <br> 
                        or create a new Bookmark Group with this dataset as the first member (right side).</p>
                    

                    <div class="col-span-full grid grid-cols-2 gap-4">
                        <!-- LEFT SIDE -->
                        <div class="border-2 shadow rounded p-2 w-full bg-white">
                            <div class="mb-3 text-xl font-bold tracking-tight text-gray-900 dark:text-white">ADD TO GROUP</div>
                            <p class="mb-4 font-normal text-gray-700 dark:text-gray-400">Dataset is added by clicking on Group name.</p>
                    
                            <div class="text-sm font-medium text-gray-900 bg-white border-2 border-primary rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                                <div aria-current="true" class="block w-full px-4 py-2 text-white bg-primary border-b border-primary rounded-t-lg cursor-pointer dark:bg-gray-800 dark:border-gray-600">
                                    Bookmark Group Names
                                </div>

                                <div v-for="bookmarkgroup in bookmarkgroups" class="mt-2">
                                    <div class="">
                                        <div @click="add2group(bookmarkgroup.name)" 
                                                    :class="{'text-gray-900': !bookmarkgroup.mine, 'text-green-500': bookmarkgroup.mine, 'font-bold': bookmarkgroup.mine}"
                                                    class="block text-xl w-full px-4 py-2 border-b border-primary cursor-pointer hover:bg-gray-400 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white">
                                            {{ bookmarkgroup.name}}
                                        </div>
                                        <div v-for="dataset in bookmarkgroup.datasets">
                                            <!--{{ dataset.db }}-{{ dataset.col }}
                                             <img v-if="dataset.image!=''" :src="dataset.image" class="rounded mx-auto w-16 h-16"> -->
                                        </div>
                                    </div>
                                </div>
                            </div>                            
                        </div>

                        <!-- RIGHT SIDE-->
                        <div class="border-2 shadow rounded p-2 w-full bg-white">
                            <div class="mb-3 text-xl font-bold tracking-tight text-gray-900 dark:text-white">NEW GROUP</div>

                            <div class="flex flex-wrap items-center justify-center">
                                <div class="border-2 border-primary justify-center shadow rounded p-2 w-full mb-2 grid grid-cols-1 gap-2">
                                    <!-- https://flowbite.com/docs/forms/floating-label/ -->
                                    <div class="relative">
                                        <input type="text" v-model="new_group_name" ref="textInputGroupName" class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-200 dark:bg-gray-700 border-0 border-b-2 border-primary appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " />
                                        <label @click="focusInput" for="floating_filled" class="absolute text-sm tablet:text-sm laptop:text-xl desktop:text-xl 4k:text-xl text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] left-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4">new Bookmark Group Name</label>
                                    </div>                                 

                                    <button @click="createGroup" type="button" class="text-white bg-primary hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-xl px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Create + Add</button>
                                </div>
                            </div>
                            
                        </div>

                    </div>

                    <a href="#" @click="closeDialog" class="inline-flex items-center mt-6 px-3 py-2 text-xl font-medium text-center text-white bg-primary rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Exit
                        <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                        </svg>
                    </a>
                </div> 
            </div> 
        </div>
    </div>

</template>

<script>
import { useGeneralStore } from '@/stores/general'
import { useDatasetStore } from '@/stores/dataset'
import { BookmarkGroups } from "../../Helpers/BookmarkGroups.js"
import { watch } from 'vue'


export default {
  props: {
    showDialog: {
      type: Boolean,
      required: true
    },
  },
  computed: {
  },
  components: { 
  }, 
  mounted() {
    this.global_checked =this.gstore.global_storage
    watch(() => this.showDialog, (newValue, oldValue) => {
        this.readBookmarkGroups()
    });
    watch(() => this.global_checked, (newValue, oldValue) => {
        this.gstore.global_storage = newValue
        this.readBookmarkGroups()
    });
    watch(() => this.gstore.global_storage, (newValue, oldValue) => {
        this.global_checked =this.gstore.global_storage
        this.readBookmarkGroups()
    });
  },
  data() {
    return {
      headline: "Bookmark Group Assignment", 
      gstore: useGeneralStore(),
      datasetstore: useDatasetStore(),
      bookmarkgroups: null,
      new_group_name: "",
      global_checked: false,
    };
  },
  methods: {
    async readBookmarkGroups(){
        this.bookmarkgroups = await BookmarkGroups.getBookmarkGroups(this.gstore.selected_db,  this.gstore.selected_col)
        for(let i=0; i<this.bookmarkgroups.length; i++){
            for(let ds=0; ds<this.bookmarkgroups[i].datasets.length; ds++){
                let db = this.bookmarkgroups[i].datasets[ds].db
                let col = this.bookmarkgroups[i].datasets[ds].col

                if(db==this.gstore.selected_db && col==this.gstore.selected_col){
                    this.bookmarkgroups[i].mine=true
                }

                // let dataset_description = await this.datasetstore.read_dataset_description(db, col)
                // this.bookmarkgroups[i].datasets[ds].image = dataset_description.image;
            }
        }
    },
    async createGroup(){
        if(this.new_group_name==""){
            console.log("missing new group name")
        } else {
            await BookmarkGroups.setBookmarkGroup(this.new_group_name, this.gstore.selected_db,  this.gstore.selected_col, this.gstore)
            console.log("create group done")
            this.readBookmarkGroups()

            //this.closeDialog()
        }
        
    },
    async add2group(groupname){
        // check if in group
        let is_in_group = false
        for(let i=0; i<this.bookmarkgroups.length; i++){
            for(let ds=0; ds<this.bookmarkgroups[i].datasets.length; ds++){
                if(this.bookmarkgroups[i].name==groupname){
                    let db = this.bookmarkgroups[i].datasets[ds].db
                    let col = this.bookmarkgroups[i].datasets[ds].col

                    if(db==this.gstore.selected_db && col==this.gstore.selected_col){
                        is_in_group=true
                    }
                }                
            }
        }
        if(is_in_group){
            await BookmarkGroups.removeBookmarkGroup(groupname, this.gstore.selected_db,  this.gstore.selected_col, this.gstore)
        } else {    
            await BookmarkGroups.addBookmarkGroup(groupname, this.gstore.selected_db,  this.gstore.selected_col, this.gstore)
        }        
        this.readBookmarkGroups()
        //this.closeDialog()
    },
    closeDialog() {
        this.$emit('update:showDialog')
    },
    focusInput() {
      this.$refs.textInputGroupName.focus();
    }
  }
};
</script>
