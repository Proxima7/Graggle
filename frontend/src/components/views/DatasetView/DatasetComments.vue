<template>
    <div class="flex flex-col justify-center items-stretch">
      <h2 class="text-lg font-semibold mb-4 mx-auto">Comments</h2>
      <div class="w-full">
        <div v-for="comment in commentsStore.comments" :key="comment.id" class="border rounded-md p-4 mb-4 w-full ">
          <div class="text-gray-700 font-bold">{{ comment.person }}</div>
          <div class="text-gray-600">{{ comment.text }}</div>
        </div>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="showForm = !showForm">
          Add Comment
        </button>
        <div v-if="showForm" class="mt-4">
          <form @submit.prevent="addComment">
            <div class="mb-4">
              <label class="block text-gray-700 font-bold mb-2" for="person">
                Name
              </label>
              <input
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="person"
                type="text"
                placeholder="Name"
                v-model="newComment.person"
              >
            </div>
            <div class="mb-4">
              <label class="block text-gray-700 font-bold mb-2" for="text">
                Comment
              </label>
              <textarea
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="text"
                placeholder="Write your comment here"
                rows="5"
                v-model="newComment.text"
              ></textarea>
            </div>
            <div class="flex justify-end">
              <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                type="submit"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useGeneralStore } from '@/stores/general'
  import { useCommentsStore } from '@/stores/comments'
  import { watch } from 'vue'

  export default {
    data() {
      return {
        newComment: {
          person: '',
          text: '',
        },
        showForm: false,
        gstore: useGeneralStore(),
        commentsStore: useCommentsStore()
      };
    },
    mounted() {
        this.commentsStore.load(this.gstore.selected_db, this.gstore.selected_col)
        watch(() => this.gstore.selected_col, (newValue, oldValue) => {
          this.commentsStore.load(this.gstore.selected_db, this.gstore.selected_col)
        });
    },
    computed: {
    },
    methods: {
      addComment() {
        this.commentsStore.add_comment(this.newComment.person, this.newComment.text)
        this.newComment.person = '';
        this.newComment.text = '';
        this.showForm = false;
      },
    }
  };
  </script>
  