import { defineStore } from 'pinia'

export const useGeneralStore = defineStore('general', {
  state: () => ({
      count: 0,
      selected_db: "",
      selected_col: "",
      filter: "",
      amount_bookmark_groups: 0,
      global_storage: false,
      cmd: "",
  }),
  actions: {
    increment() {
      this.count++
    },
    decrement() {
      this.count--
    },
  },
})
