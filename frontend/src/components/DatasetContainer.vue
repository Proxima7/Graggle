<template>
    <div class="bg-white py-2 px-4 h-full ">
        <!-- tabs: each one is toggable like in the vs code menu-->
        <ul class="flex flex-wrap text-sm font-medium text-center text-gray-300 border-b border-gray-300">
            <li v-for="tab in tabs" class="mr-2">
                
                <div 
                @click="activate(tab.id)" 
                :class="!tab.active ? 'text-gray-600 hover:text-gray-900' : 'bg-gray-500 text-gray-900 border-primary border-b-2 font-bold'"
                class="inline-block p-4 bg-gray-300  rounded-t-lg active cursor-pointer">
                <font-awesome-icon :icon="tab.icon" v-if="tab.id==4"/>    
                {{tab.title}}
                
                </div>
            </li>
        </ul>

        <div class="mt-2">
            <div v-if="activeTab === 1">
                <DatasetMain/>
            </div>
            <div v-if="activeTab === 2">
                <DatasetProjects/>
            </div>
            <div v-if="activeTab === 3">
                <DatasetComments/>
            </div>
            <div v-if="activeTab === 4">
                <SetMeUp/>
            </div>
        </div>

        <!-- spacer: makes some space between content and footer
        <div class="min-h-[20vh]"></div> -->
    </div>
</template>


<script>
    import SetMeUp from './views/DatasetView/SetMeUp.vue';
    import DatasetMain from './views/DatasetView/DatasetMain.vue';
    import DatasetComments from './views/DatasetView/DatasetComments.vue';
    import DatasetProjects from './views/DatasetView/DatasetProjects.vue';
    import { useGeneralStore } from '@/stores/general'
    import { watch } from 'vue'

    export default {
    name: 'DatasetContainer',
    data () {
        return {
            gstore: useGeneralStore(),
            activeTab: 1,
            tabs: [
                {icon: 'fa-database', active: true, title: 'Datacard', id: 1},
                {icon: 'fa-bookmark', active: false, title: 'Projects', id: 2},
                {icon: 'fa-comments', active: false, title: 'Comments', id: 3},
                {icon: 'fa-code', active: false, title: 'Set-Me-Up', id: 4},
            ],
        }
    },
    mounted() {
        watch(() => this.gstore.cmd, (newValue, oldValue) => {
            if(newValue=="comments"){
                this.gstore.cmd=""
                this.activate(3)
            }
        });
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
        DatasetMain,
        DatasetComments,
        DatasetProjects,
        SetMeUp
    }
    }
</script>