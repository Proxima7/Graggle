<template>
  <div :class="[
      'flex flex-col bg-primary text-white', 
      p_flex_size,
      isCollapsed ? 'min-w-[50px]': 'min-w-[250px]'
    ]
      ">
    <div class="flex flex-col h-full ">
        <div class="grid grid-cols-12 p-0 h-full">
            <div :class="[buttons_col_span, 'bg-secondary min-w-[50px]']">
              <!-- left buttons -->
              <div 
                v-for="(item) in menu_items" v-bind:key="item.id" 
                class="text-2xl bg-gray cursor-pointer"
                :class="['px-3.5 py-2', 'border-1', 'border-black', item.active ? cl_menu_item_active : '']"
                @click="menu_btn_click(item)"
                >
                <font-awesome-icon :icon="item.icon" 
                :class="!item.active ? 'text-gray-600 hover:text-gray-500' : ''"
                />
              </div>
            </div>
            <!-- right side of menu -->
            <div :style="isCollapsed ? 'display: none' : ''" class="col-span-10 px-2">
                <div v-for="(item) in menu_items" v-bind:key="item.id" 
                v-show="item.active"
                >
                  <!-- title -->  
                  <div class="flex justify-center border-b-4 mb-2 border-secondary">
                    <div class="text-xl text-gray-300 w-100 leading-2 font-bold">{{ item.title }}</div>
                  </div>
                  
                  <!-- content -->
                  <component class="h-full" :is="item.comp" ></component>
                </div>
            </div>            
          </div>
        </div>

    </div>
</template>

<script>
import Options from './Options.vue';
import DatasetList from './DatasetList.vue';
import BookmarkList from './BookmarkList.vue';
import Filters from './Filters.vue';

export default {
  name: 'Tagging',
  data () {
    return {
      cl_menu_item_active: 'border-l-8 border-gray-800',
      p_flex_size: this.flex_size,
      isCollapsed: false,
      buttons_col_span: 'col-span-2',
      menu_items: [
        {icon: 'fa-database', active: true, title: 'Datasets', comp: "DatasetList"},
        {icon: 'fa-bookmark', active: false, title: 'Bookmarks', comp: "BookmarkList"},
        {icon: 'fa-filter', active: false, title: 'Filters', comp: "Filters"},
        {icon: 'fa-bars', active: false, title: 'Options', comp: "Options"},
      ],
    }
  },
  methods: {
    menu_btn_click (item) {
      // do nothing if selected item is already active
      if(item.active == true){
        return
      }

      // toggle menu if clicked on same button
      var idxClicked = this.menu_items.indexOf(item)
      var currActive = this.menu_items.findIndex(item => item.active)

      if (idxClicked === currActive && !this.isCollapsed) {
        this.collapse()
      }
      else if (idxClicked === currActive && this.isCollapsed) {
        this.uncollapse()
      }
      else {
        this.uncollapse()
      }
      // make new button active
      for (let i = 0; i < this.menu_items.length; i++) {
        this.menu_items[i].active = false
      }
      item.active = true
    },
    collapse() {
      // logic param
      this.isCollapsed = true
      // stylings
      this.p_flex_size = 'w-15'
      this.buttons_col_span = 'col-span-12'
    },
    uncollapse() {
      // logic param
      this.isCollapsed = false
      // stylings
      this.p_flex_size = this.flex_size
      this.buttons_col_span = 'col-span-2'
    }
  },
  components: {
    DatasetList,
    BookmarkList,
    Filters,
    Options
  }
}
</script>