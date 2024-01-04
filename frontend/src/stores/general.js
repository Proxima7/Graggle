import { defineStore } from 'pinia'

export const useGeneralStore = defineStore('general', {
  state: () => ({
      count: 0,
      selected_db: "",
      selected_col: "",
      selected_dataset_id: "",
      filter: "",
      amount_bookmarks: 0,
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
