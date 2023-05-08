/* Set up using Vue 3 */
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createStore } from 'vuex'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { 
    faUser, faDatabase, faSearch, faBars, faTimes, faChevronDown, faChevronUp, faLeaf, faBookmark, 
    faHome, faChevronLeft, faChevronRight, faChevronCircleRight, faChevronCircleLeft, faPlusCircle, faMinusCircle,
    faStar, faHardDrive, faFile, faVectorSquare, faCalendarCheck, faCalendarPlus, faCirclePlus, faImage, faCheck, 
    faComments, faShareNodes, faXmark, faFilter
  } from '@fortawesome/free-solid-svg-icons'

  import { 
     faBookmark as faBookmarkRegular, faPenToSquare
  } from '@fortawesome/free-regular-svg-icons'

/* add icons to the library */
library.add(faUser)
library.add(faDatabase)
library.add(faSearch)
library.add(faBars)
library.add(faChevronDown)
library.add(faChevronUp)
library.add(faTimes)
library.add(faBookmark)
library.add(faBookmarkRegular)
library.add(faLeaf)
library.add(faHome)
library.add(faChevronLeft)
library.add(faChevronRight)
library.add(faChevronCircleRight)
library.add(faChevronCircleLeft)
library.add(faPlusCircle)
library.add(faMinusCircle)
library.add(faStar)
library.add(faHardDrive)
library.add(faFile)
library.add(faVectorSquare)
library.add(faCalendarCheck)
library.add(faCalendarPlus)
library.add(faCirclePlus)
library.add(faImage)
library.add(faCheck)
library.add(faComments)
library.add(faShareNodes)
library.add(faXmark)
library.add(faPenToSquare)
library.add(faFilter)

const store = createStore({
    state () {
      return {
        selected_db: "",
        selected_col: "",
        filter: "",
        amount_bookmarks: 0
      }
    },
    mutations: {
        print_selected_collection (state) {
            console.log(state.selected_col + " " +state.selected_db)
        }
    }
  })


/* other components like json viewer */
import JsonViewer from "vue3-json-viewer";
import "vue3-json-viewer/dist/index.css";

const myapp = createApp(App)
.component('font-awesome-icon', FontAwesomeIcon)
.use(JsonViewer)
.use(store)
.mount('#app')
