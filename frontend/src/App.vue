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
          <ViewContainer v-if="is_db_col_selected() == true" class="w-full"></ViewContainer>
          <DatasetOverview v-if="is_db_col_selected() == false" class="w-full"></DatasetOverview>
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
import ViewContainer from './components/ViewContainer.vue';
import DatasetOverview from './components/views/DatasetView/DatasetOverview.vue';

export default {
  name: 'App',
  data () {
    return {
    }
  },
  components: {
    Header,
    Footer,
    VSCodeMenu,
    ViewContainer,
    DatasetOverview
  },
  methods: {
    is_db_col_selected(){
      let db = this.$store.state.selected_db
      let col = this.$store.state.selected_col
      return (db != "" && col != "")
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