import { defineStore } from 'pinia'
import requestHandler from "../logic/RequestHandler"

export const useDatabasesStore = defineStore('databases', {
  state: () => ({ 
    datasets: ["loading"],
  }),
  actions: {
    load() {
      var that = this;
      var get_databases_callback = function(resp) {
          that.datasets = resp.data.databases;
      }
      requestHandler.get_databases(get_databases_callback);
    },
    get_databases() {
      return this.datasets
    }
  }
})