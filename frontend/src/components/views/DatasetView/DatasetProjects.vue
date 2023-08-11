<template>
    <div class="flex flex-col justify-center items-stretch">
      <h2 class="text-lg laptop:text-xl desktop:text-2xl 4k:text-3xl font-semibold mb-4 mx-auto ">Projects of Dataset</h2> 
        <div v-for="project in projects" :key="project.id" class="border rounded-md p-4 mb-4 w-full text-sm laptop:text-lg desktop:text-xl 4k:text-xl">
          <div class="text-gray-700 font-bold">{{ project.name }}</div>
          <div class="text-gray-600">{{ project.desc }}</div>
          <div class="text-gray-600">Projekt reference: <a v-bind:href="project.link">LINK</a></div>
          

        </div>     
    </div>
  </template>
  
  <script>

  export default {
    data() {
      return {
        projects: [
        {   id: 1, 
            name: "Fruit Recognition V3", 
            desc: "Fruit Recognition for CustomerX based in CityY Data", 
            link: "https://www.google.de/"
          },
          { id: 2, 
            name: "DIY Hornbach", 
            desc: "CustomerM Sanitary Article Detection", 
            link: "https://www.google.de/"
          },
          { id: 3, 
            name: "DIY Hornbach - V2", 
            desc: "CustomerM Sanitary Article Detection - new Model", 
            link: "https://www.google.de/"
          }
        ]
      };
    },
    mounted() {
    },
    computed: {
    },
    methods: {
    },
    watch: {
    }
  };
  </script>
  