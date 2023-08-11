<template>
    <div class="">
      <div class="grid grid-cols-1 gap-2 overflow-x-hidden">
        <div v-for="database in databasestore.get_databases()" 
              class="bg-secondary py-2 px-4 rounded font-semibold text-xs laptop:text-base desktop:text-lg 4k:text-xl" 
              :class="{ 'bg-tertiary-900': is_active_database(database.database_name) }" @click="set_selected_database(database.database_name)">{{database.database_name}}
            <ul v-if="is_active_database(database.database_name)" class="mt-2 border-l-4 border-secondary overflow-y-auto max-h-80 overflow-x-hidden">
                <li v-for="col in database.collection_names" class="py-2 px-2 cursor-pointer text-m text-gray-300" :class="{ 'bg-tertiary-900': isActive(1, 1) }" @click="set_selected_collection(database.database_name, col)">{{ col.slice(0, 22) }} 
                </li>
            </ul>
          </div>
        
    </div>
  </div>
  </template>
  
  <script>
    import { useGeneralStore } from '@/stores/general'
    import { useDatabasesStore } from '@/stores/databases'
    
    export default {
        data() {
          return {
              activeIndex: null,
              datasets: ["loading"],
              active_database: null,
              collection_overwrite: false,
              gstore: useGeneralStore(),
              databasestore: useDatabasesStore()
          }
        },
        computed: {
        },
        mounted() {
            this.databasestore.load()
        },
        methods: {
            is_active_database(database){
                if(this.active_database == database){
                    return true
                } else {
                    return false
                }
            },
            isActive(menuIndex, submenuIndex) {
                if (Array.isArray(this.activeIndex)) {
                if (this.activeIndex[0] === menuIndex) {
                    if (submenuIndex) {
                    return this.activeIndex[1] === submenuIndex;
                    }
                    return true;
                }
                return false;
                }
                return this.activeIndex === menuIndex;
            },
            async set_selected_database(db){
              let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
              await sleep(50)
              if(!this.collection_overwrite){
                this.active_database = db
                this.gstore.selected_db = ""
                this.gstore.selected_col = ""
                this.gstore.filter = ""
                await sleep(50)
                this.gstore.filter = this.active_database
              }
            },
            async set_selected_collection(db, col){
                this.gstore.selected_db = db
                this.gstore.selected_col = col

                // avoid trigger of method "set_selected_database"
                this.collection_overwrite = true
                let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
                await sleep(500)
                this.collection_overwrite = false
            }
        }
    }
  </script>
  
  <style>
    /* Set font family and font size */
body {
  font-size: 16px;
}

/* Set max width and center content */
.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Style the menu */
.menu li:hover {
  background-color: #eee;
}

/* Set active menu and submenu items */
.menu li.active {
  background-color: #ddd;
}

.menu li.active-submenu {
  background-color: #ccc;
}

/* Style the submenu */
.submenu li:hover {
  background-color: #ddd;
}

/* Add borders to menu and submenu items */
.menu li,
.submenu li {
  border-top: 1px solid #ccc;
}

.submenu li:last-child {
  border-bottom: 1px solid #ccc;
}

 </style>