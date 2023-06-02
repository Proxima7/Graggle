import { defineStore } from 'pinia'
import requestHandler from "../logic/RequestHandler"
import { useGeneralStore } from '@/stores/general'

export const useCommentsStore = defineStore('comments', {
  state: () => ({ 
    comments: [{ id: 1, person: "...", text: "Post the first comment" },], 
    gstore: useGeneralStore(),
  }),
  actions: {
    load(db, col) {
      var that = this;
      var dataset_comments_callback = function (resp) {
          that.comments = resp.data.comments;
      };          
      requestHandler.get_dataset_comments(dataset_comments_callback, db, col);
    },
    add_comment(person, text) {
      const newId = this.comments.length + 1;
      const newComment = {
        id: newId,
        person: person,
        text: text,
      };
      this.comments.push(newComment);
    }
  }
})