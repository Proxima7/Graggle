<template>
  <div class="flex flex-col h-screen">

    <div class="h-22">
      <Header />
    </div>

    <div class="flex-1 overflow-auto">
      <div class="flex flex-row h-full">
        <!-- sidebar -->
        <div class="w-1/6">
          <VSCodeMenu class="w-full h-full" />
        </div>
        <!-- main frame -->
        <div class="overflow-auto w-5/6">
          <DatasetContainer v-if="is_db_col_selected() == true" class="w-full"></DatasetContainer>
          <DatasetsSummary v-if="is_db_col_selected() == false" class="w-full"></DatasetsSummary>
        </div>
        
      </div>
    </div>

    <div class="h-5 fixed bottom-0 w-full">
      <Footer />
    </div>
     
  </div>
</template>



<script>
//import SideMenu from './components/SideMenu.vue'
import Header from './components/Header.vue'
import Footer from "./components/Footer.vue"
import VSCodeMenu from './components/VSCodeMenu.vue';
import DatasetContainer from './components/DatasetContainer.vue';
import DatasetsSummary from './components/views/DatasetView/DatasetsSummary.vue';
import { useGeneralStore } from '@/stores/general'


export default {
  name: 'App',
  setup() {
  },
  data () {
    return {
      gstore: useGeneralStore()
    }
  },
  mounted() {
  },
  components: {
    Header,
    Footer,
    VSCodeMenu,
    DatasetContainer,
    DatasetsSummary
  },
  methods: {
    is_db_col_selected(){
      let db = this.gstore.selected_db
      let col = this.gstore.selected_col
      let is_it = (db != "" && col != "")
      return is_it
    }
  }
}
</script>



<style>
html, body, #body2
{
    height: 100%;
    min-height: 100%;
}
</style>