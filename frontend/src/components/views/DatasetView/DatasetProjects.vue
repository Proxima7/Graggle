<template>
    <div class="flex flex-col justify-center items-stretch">
      <h2 class="text-lg font-semibold mb-4 mx-auto">Projects of Dataset</h2> 
        <div v-for="project in projects" :key="project.id" class="border rounded-md p-4 mb-4 w-full ">
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
            desc: "Fruit Recognition for Carrefoure based in Dubai Data", 
            link: "https://dev.azure.com/matthiasrieger/ArtificialIntelligence/_build/results?buildId=265&view=results"
          },
          { id: 2, 
            name: "DIY Hornbach", 
            desc: "Hornbach Sanitary Article Detection", 
            link: "https://dev.azure.com/matthiasrieger/ArtificialIntelligence/_git/ai-gen-ms-model-pool?path=/models/diy/v2"
          },
          { id: 3, 
            name: "DIY Hornbach - V2", 
            desc: "Hornbach Sanitary Article Detection - new Model", 
            link: "https://dev.azure.com/matthiasrieger/ArtificialIntelligence/_git/ai-gen-ms-model-pool?path=/models/diy/v5"
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
  