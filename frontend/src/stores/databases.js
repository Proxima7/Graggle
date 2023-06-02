import { defineStore } from 'pinia'
import requestHandler from "../logic/RequestHandler"

export const useDatabasesStore = defineStore('databases', {
  state: () => ({ 
    datasets: ["loading"],
  }),
  actions: {
    load() {
      var that = this;
      var get_datasets_callback = function(resp) {
          that.datasets = resp.data;
      }
      requestHandler.get_databases(get_datasets_callback);
    },
    get_datasets() {
      return this.datasets
    }
  }
})