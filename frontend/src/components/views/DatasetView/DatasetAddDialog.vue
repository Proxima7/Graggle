<template>
    <div class="fixed inset-0 bg-gray-700 opacity-75 z-50" v-if="showDialog"></div>

    <!-- Popup dialog -->
    <div class="m-4 fixed inset-0 z-50 flex items-center justify-center text-xs laptop:text-lg desktop:text-xl 4k:text-2xl" v-if="showDialog">
        
        <div class="bg-white rounded-lg p-4">
            <form @submit.prevent class="w-full relative">
                <loading-overlay :loading="loading" headline="Inserting" subline="This will take a few seconds"></loading-overlay>
                <div class="space-y-12 ">
                    <div class="">
                        <h2 class="text-base font-semibold leading-7 text-gray-900">{{headline}}</h2>

                        <div class="border-b border-gray-900/10 mt-2 grid grid-cols-1 gap-x-6 gap-y-2 sm:grid-cols-6">
                            <div class="sm:col-span-4">
                                <label for="text" class="block font-medium leading-6 text-gray-900">Dataset titel</label>
                                <div class="mt-0">
                                <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                                    <input  required type="text" name="titel" id="titel"  v-model="titel" autocomplete="titel" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:leading-6" placeholder="meaningful titel for the dataset"/>
                                </div>
                                </div>
                            </div>

                            <div class="sm:col-span-4">
                                <label for="shortdesc" class="block font-medium leading-6 text-gray-900">Short description</label>
                                <div class="mt-0">
                                <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                                    <input required type="shortdesc" name="shortdesc" id="shortdesc" v-model="shortdesc" autocomplete="titel" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:leading-6" placeholder="short description of the dataset"/>
                                </div>
                                </div>
                            </div>

                            <div class="col-span-full">
                                <label for="desc" class="block font-medium leading-6 text-gray-900">Detail description</label>
                                <div class="mt-0">
                                <textarea required id="desc" name="desc" v-model="desc" rows="3" class="block w-full rounded-md border-0 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:py-1.5 sm:leading-6" />
                                </div>
                                <p class="mt-3 leading-6 text-gray-600">Write a few sentences what the dataset is about.</p>
                            </div>

                            <div class="col-span-full ">
                                <label for="images" class="block font-medium leading-6 text-gray-900">Preview photo</label>
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="mt-0 flex flex-col justify-between rounded-lg border border-dashed border-gray-900/25 px-6 py-10" :class="getColor(2)">
                                        <div class="text-center">
                                            <font-awesome-icon class="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" icon="fa-solid fa-image" />
                                            <div class="mt-4 text-s leading-6 text-gray-600">
                                            <label for="file-upload" class="relative cursor-pointer rounded-md font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
                                                <span>Upload a file</span>
                                                <input id="file-upload" name="file-upload" type="file" class="sr-only" ref="fileupload" @change="handleFileUpload"/>
                                            </label>
                                            </div>
                                            <p class="leading-5 text-gray-600">PNG, JPG, GIF up to 10MB</p>
                                        </div>
                                        
                                    </div>
                                    <div class="mt-0 flex flex-col justify-between rounded-lg border border-dashed border-gray-900/25 px-6 py-10 relative" :class="getColor(1)">
                                        <img src='../../../assets/gear.png' class="mx-auto h-24  text-gray-300" alt="Product screenshot">
                                        <p class="text-gray-600 text-center">automatical create from images</p>
                                        <div class="absolute inset-0 bg-gray-700 opacity-0" @click="toggleSelection() "></div>
                                    </div>
                                </div>
                            </div>

                            <div class="col-span-full">
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="p-2">
                                        <label for="usability" class="block font-medium leading-6 text-gray-900">Usability</label>
                                    </div>
                                    <div class="p-2">
                                        <div class="flex sm:max-w-md">
                                            <Slider @slider-value-updated="handleSliderValue"></Slider>
                                        </div>
                                    </div>

                                    <div class="p-2">
                                        <label for="createdby" class="block font-medium leading-6 text-gray-900">Created by</label>
                                    </div>
                                    <div class="p-2">
                                        <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                                            <input required type="createdby" name="createdby" id="createdby" v-model="createdby" autocomplete="createdby" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:leading-6" placeholder="name or service"/>
                                        </div>
                                    </div>
                                </div>
                            </div>                          
                        </div>

                        <div class="mt-2 flex items-center justify-end gap-x-6">
                            <button type="button" class="font-semibold leading-6 text-gray-900" @click="closeDialog">Cancel</button>
                            <button class="rounded-md bg-indigo-600 px-3 py-2 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="storeDB">Save</button>
                        </div>

                        <div class="mt-2 flex items-center justify-end gap-x-6" v-if="error != ''">
                            <label for="error" class="block text-l font-medium leading-6 text-red-400">{{error}}</label>
                        </div>

                    </div>
                </div>
            </form> 
        </div>
    </div>

</template>

<script>
import LoadingOverlay from "../../Helpers/LoadingOverlay.vue"
import Slider from "../../Helpers/Slider.vue"
import { useGeneralStore } from '@/stores/general'
import { useDatasetStore } from '@/stores/dataset'


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
    LoadingOverlay,
    Slider 
  }, 
  data() {
    return {
      headline: "Detailed Data Description",
      isChecked: false,
      loading: false,
      error: "",
      selection: 1,
      titel: "",
      shortdesc: "",
      desc: "",
      usability: "",
      createdby: "",
      image: "",            
      gstore: useGeneralStore(),
      datasetstore: useDatasetStore()
    };
  },
  computed: {
    formFilled() {
      return this.titel && this.shortdesc && this.desc && this.usability && this.createdby
    }
  },
  methods: {
    closeDialog() {
        this.titel = ""
        this.shortdesc = ""
        this.desc = ""
        this.usability = ""
        this.createdby = ""
        this.image = ""
        this.$emit('update:showDialog')
    },
    getColor(input) {
      return {
        'bg-green-300': input === this.selection,
        'bg-white': input != this.selection,
      };
    },
    toggleSelection(){
        if(this.selection==1){
            this.selection = 2
        } else {
            this.selection = 1
        }
    },
    handleSliderValue(value) {
      this.usability = value;
    },
    handleFileUpload() {
     let that = this
      const file = this.$refs.fileupload.files[0];
      if(file.name.endsWith(".png") || file.name.endsWith(".jpg") || file.name.endsWith(".jpeg")  ){

        // base64 encoded
        const reader = new FileReader()        
        reader.onload = () => {
            that.image= reader.result.split(',')[1]
        }
        reader.readAsDataURL(file)
        this.error = ""
        this.selection = 2
      } else {        
        this.error = "Wrong data format (only .png, .jpg and .jpeg)"
        this.selection = 1
      }    
    },


    async storeDB(){
        
        if(!this.formFilled){
            this.error = ""
        } else {
            this.loading = true;
            this.error = ""        

            var body = {
                            "database": this.gstore.selected_db, 
                            "collection": this.gstore.selected_col, 
                            "dataset_display_title": this.titel, 
                            "short_description": this.shortdesc, 
                            "dataset_description": this.desc, 
                            "usability": this.usability, 
                            "created_by": this.createdby, 
                            "image": this.image
                        }

            let success = await this.datasetstore.post_dataset_description(body)
            if(success) {
                this.closeDialog()
                this.loading = false;
            } else {
                this.loading = false;
                this.error = "Fehler beim erzeugen der Dataset Description"
            }
        }      
    }
  }
};
</script>
