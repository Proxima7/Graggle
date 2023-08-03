<template>
  <div class="flex flex-col min-h-screen mainer">

    <div class="h-22 w-full " >
      <Header />
    </div>

    <main class="wrapper overflow-y-hidden overflow-x-hidden h-full">
      <!-- sidebar -->
      <div class="sidebar overflow-y-auto">
          <div class="flex flex-col h-full">
            <VSCodeMenu class="flex-1 "/>
          </div>
          
        </div>
        <!-- main frame -->
        <div class="content overflow-y-auto  overflow-x-hidden">
          <DatasetContainer v-if="is_db_col_selected() == true" class="w-full"></DatasetContainer>
          <DatasetsSummary v-if="is_db_col_selected() == false" class="w-full"></DatasetsSummary>
        </div>
    </main >

    <div class="h-8 w-full">
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
.wrapper {
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 5fr;
  grid-gap: 50px;
}

.sidebar {
  grid-column: 1;
  color: #fff;
}

.content {
  grid-column: 2;
}

  .mainer {
    overflow: hidden;
    height: 100vh;
  }
</style>