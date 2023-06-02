<template>
    <div class="flex flex-col justify-center items-stretch">
      <h2 class="text-lg font-semibold mb-4 mx-auto">Set-Me-Up</h2> 

      <div class="grid grid-cols-7 py-2 px-4 rounded border-2">
        <div class="col-span-1 flex items-center justify-start text-lg font-semibold">
          Installation:
        </div>
        <div class="col-span-6 items-center">
          <highlightjs language='python' code="pip install database_accessor" />
        </div>
      </div>

      <div class="grid grid-cols-7 py-2 px-4 rounded border-2">
        <div class="col-span-1 flex items-center justify-start text-lg font-semibold">
          Environment variables:
        </div>
        <div class="col-span-6 items-center">
          <highlightjs language='markdown' :code="envvar" />
        </div>
      </div>

      <div class="grid grid-cols-7 py-2 px-4 rounded border-2">
        <div class="col-span-1 flex items-center justify-start text-lg font-semibold">
          Usage:
        </div>
        <div class="col-span-6 items-center">
          <highlightjs language='python' :code="getUsage()" />
        </div>
      </div>


    </div>
  </template>
  
  <script>
  import 'highlight.js/lib/common';
  import hljs from 'highlight.js/lib/core';
  import hljsVuePlugin from "@highlightjs/vue-plugin";
  import javascript from 'highlight.js/lib/languages/javascript';
  import markdown from 'highlight.js/lib/languages/markdown';
  import python from 'highlight.js/lib/languages/python';
  import 'highlight.js/styles/vs2015.css';
  hljs.registerLanguage('javascript', javascript);
  hljs.registerLanguage('markdown', markdown);
  hljs.registerLanguage('python', python);

  import { useGeneralStore } from '@/stores/general'

  export default {
    data() {
      return {
        gstore: useGeneralStore(),
        
        envvar: `{mongo_instance}-{con_string_name} - The connection string of the database. 
Replace {mongo_instance} with the name of the instance you want to connect to (e.g. dev, prod) and {con_string_name} 
with the name of the connection string (e.g. mongodb_con_string_admin, mongodb_con_string_user). 
You set both when creating the MongoDB Accessor instance.

If you need to access the dev minio storage:
"dev_s3_access_key" - The access key of the minio dev instance
"dev_s3_secret_key" - The secret key of the minio dev instance
"dev_s3_host" - The host of the minio dev instance
If you need to access the prod minio storage:

"prod_s3_access_key" - The access key of the minio prod instance
"prod_s3_secret_key" - The secret key of the minio prod instance
"prod_s3_host" - The host of the minio prod instance
`,

      usage1: `from database_accessor import get_db_accessor

db_accessor = get_db_accessor(mongo_instance="dev", con_string_name="mongodb_con_string_admin")

list_data_entries = self.db_accessor.get_data(`,
      
      usage2: `, return_images=True, query=query)

for entry in list_data_entries:
  for key in entry:
    print(f'{key} has value {entry[key]}')
      `
      };
    },
    mounted() {
    },
    computed: {      
    },
    methods: {
      getInstall() {
        return hljs.highlightBlock("pip install database_accessor");
      },
      getUsage(){
        return this.usage1 + `"`+this.gstore.selected_db+`", "`+this.gstore.selected_col+`"` + this.usage2
      }
    },
    components: {
      highlightjs: hljsVuePlugin.component
    },
    watch: {
    }
  };
  </script>
  
<style>
</style>