<template>
    <div class="flex flex-col justify-center items-stretch">
      <h2 class="text-lg font-semibold mb-4 mx-auto">Comments</h2>
      <div class="w-full">
        <div v-for="comment in comments" :key="comment.id" class="border rounded-md p-4 mb-4 w-full ">
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
  import requestHandler from "../../../logic/RequestHandler"
  import { mapState } from 'vuex'

  export default {
    data() {
      return {
        comments: [
          { id: 1, person: "...", text: "Post the first comment" },
        ],
        newComment: {
          person: '',
          text: '',
        },
        showForm: false,
      };
    },
    mounted() {
        this.loadComments()
    },
    computed: {
        ...mapState(['selected_col'])
    },
    methods: {
      loadComments(){
        var that = this;
            var dataset_comments_callback = function (resp) {
                console.log(that.comments)
                that.comments = resp.data.comments;
                console.log(that.comments)
            };          

            let db = this.$store.state.selected_db
            let col = this.$store.state.selected_col
            requestHandler.get_dataset_comments(dataset_comments_callback, db, col);
        
      },
      addComment() {
        const newId = this.comments.length + 1;
        const newComment = {
          id: newId,
          person: this.newComment.person,
          text: this.newComment.text,
        };
        this.comments.push(newComment);
        this.newComment.person = '';
        this.newComment.text = '';
        this.showForm = false;
      },
    },
    watch: {
        selected_col(newValue, oldValue) {
            this.loadComments()
        }
    }
  };
  </script>
  