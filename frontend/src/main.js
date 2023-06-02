/* Set up using Vue 3 */
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia, setActivePinia } from "pinia" 

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { 
    faUser, faDatabase, faSearch, faBars, faTimes, faChevronDown, faChevronUp, faLeaf, faBookmark, 
    faHome, faChevronLeft, faChevronRight, faChevronCircleRight, faChevronCircleLeft, faPlusCircle, faMinusCircle,
    faStar, faHardDrive, faFile, faVectorSquare, faCalendarCheck, faCalendarPlus, faCirclePlus, faImage, faCheck, 
    faComments, faShareNodes, faXmark, faFilter, faMaximize, faMinimize, faShuffle,
    faSliders, faCodePullRequest, faFileImport, faCode, faLanguage, faBookOpen
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
library.add(faMaximize)
library.add(faMinimize)
library.add(faShuffle)
library.add(faSliders)
library.add(faCodePullRequest)
library.add(faFileImport, faCode, faLanguage, faBookOpen)


const pinia = createPinia()
setActivePinia(pinia);




const myapp = createApp(App)
.component('font-awesome-icon', FontAwesomeIcon)
.use(pinia)

myapp.mount('#app')



