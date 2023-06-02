<template>
  <div class='flex-grow'>
      <div class="flex p-0.5 gap-x-1 justify-center">
        <div class="bg-primary text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_home">
            <font-awesome-icon icon="fa-home" />
            zoom fit
          </div> 
        <div class="bg-primary text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_zoom_out">
            <font-awesome-icon icon="fa-minus-circle" />
            zoom out
          </div>
          <div class="bg-primary text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_zoom_in">
            <font-awesome-icon icon="fa-plus-circle" />
            zoom in
          </div>
          <div class="bg-primary text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_rotate_left">
            <font-awesome-icon icon="fa-chevron-circle-left" />
            rotate left
          </div>
          <div class="bg-primary text-white rounded px-4 py-2 hover:bg-secondary focus:outline-none focus:shadow-outline" id="ann_nav_btn_rotate_right">
            <font-awesome-icon icon="fa-chevron-circle-right" />
            rotate right
          </div>
      </div>
      <div class="w-full h-full"  id="annotorious_container" />
      <div>use shift+click to draw. Use shift+double click to end polygon.</div>
  </div>
</template>

<script>
import AnnotoriusEditorPopup from './AnnotoriousEditorPopup.vue'
import OpenSeadragon from 'openseadragon'
import AnnotoriousOpenSeadragon from '@recogito/annotorious-openseadragon'
import '@recogito/annotorious-openseadragon/dist/annotorious.min.css'
import { Annotations }from '../Helpers/Annoatation.js'


export default {
  props: {
    img_url: {
      type: String,
      default: '../../src/assets/banana.jpg'
    },
    default: {
      type: String,
      default: '../../src/assets/banana.jpg'
    },
    menu_items: {
      type: Array
    },
    objects: {
      type: Object
    },
    annotations: {
      type: Object
    }
  },
  methods: {
    createVueComponent: function (comp) {
      var ComponentClass = Vue.extend(comp)
      var instance = new ComponentClass()
      instance.$mount() // pass nothing
      return instance
    },
    createEditor: function (/*args*/) {
      var instance = this.createVueComponent(AnnotoriusEditorPopup)
      return instance.$el
    },
    createSelection: async function (selection) {
      this.addObjectToMenu()
      this.openObjectsMenu()
      // Tag to insert
      selection.body = [{
        type: 'TextualBody',
        purpose: 'tagging',
        value: 'MyTag'
      }]
      // Step 3: update the selection and save it
      // Remember that .updateSelected is an async function!
      // You need to wait until it completes before saving
      await window.anno.updateSelected(selection)
      window.anno.saveSelected()
    },
    openObjectsMenu: function () {
      for (let i = 0; i < this.menu_items.length; i++) {
        if (this.menu_items[i].active && this.menu_items[i].name !== 'objects') {
          this.menu_items[i].active = ''
        } else if (this.menu_items[i].name === 'objects') {
          this.menu_items[i].active = this.cl_menu_item_active
        }
      }
    },
    addObjectToMenu: function () {
      this.objects.items.push({
        name: 'Object ' + String(this.objects.items.length + 1),
        content: {
          title: 'Object ' + String(this.objects.items.length + 1),
          items: [{name: 'Class', content: 'Please select the class'}]
        }})
    },
    selectAnnotation: function (/*selection*/) {
    }
  },
  mounted: function () {
    this.createViewer()
    this.createAnnotorious()
    this.loadImage()
  },
  data () {
    return {
      cl_menu_item_active: 'border-l-8 border_l_blue',
      viewer: null,
      anno: null
    }
  },
  methods:{
    createViewer(){
      this.viewer = OpenSeadragon({
        id: 'annotorious_container',
        minZoomImageRatio: 0,
        maxZoomPixelRatio: Infinity,
        animationTime: 0.5,
        showFullPageControl: false,
        fitHorizontally: true,
        autoResize: true,
        rotationIncrement: 90,
        zoomInButton: 'ann_nav_btn_zoom_in',
        zoomOutButton: 'ann_nav_btn_zoom_out',
        homeButton: 'ann_nav_btn_home',
        nextButton: 'ann_nav_btn_next',
        previousButton: 'ann_nav_btn_prev',
        rotateLeftButton: 'ann_nav_btn_rotate_left',
        rotateRightButton: 'ann_nav_btn_rotate_right',
        showRotationControl: true,
        tileSources: {
          type: 'image',
          url: this.img_url,
          ajaxWithCredentials: false,
          fitBounds: true
        }
      })
    },
    createAnnotorious(){
      var options = {
        disableEditor: true // the default editor is disabled to implement a custom behaviour
      }
      this.anno = AnnotoriousOpenSeadragon(this.viewer, options)
      this.anno.setDrawingTool('polygon')
      this.anno.on('createSelection', this.createSelection)
      this.anno.on('selectAnnotation', this.selectAnnotation)
    },
    loadImage(){    

    if(this.annotations){
      const annos = Annotations.getAnnotoriousAnnoations(this.annotations)      
      this.anno.setAnnotations(annos);
    }
    
    
    window.viewer = this.viewer
    window.anno = this.anno
    }
  },
  watch: {
    img_url: function(newValue, oldValue) {
    }
  }
}
</script>

<style>
.r6o-editor {
top: 1em impo !important;
}
</style>
