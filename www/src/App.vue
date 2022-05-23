<script>
  import axios from "axios";
  import Todo from "./class";

  export default {
    name: "App",

    data() {
      return {
        url: "http://localhost:5000",
        todo_list: [],
        temp_todo_item: "",
        index: 0,
        edit_index: null,
      };
    },

    methods: {
      FetchTodos() {
        axios
          .get(this.url + "/todos")
          .then((response) => {
            this.todo_list = response["data"];
          })
          .catch((error) => {
            console.log(error);
          });
        axios
          .get(this.url + "/index")
          .then((response) => {
            this.index = response["data"];
          })
          .catch((error) => {
            console.log(error);
          });
      },

      AddTodo() {
        if (this.temp_todo_item != "" && this.edit_index == null) {
          let todo = new Todo(this.index, this.temp_todo_item, false);
          this.index++;
          this.todo_list.push(todo);

          axios
            .put(this.url + "/index", {
              index: this.index,
            })
            .then((response) => {
              console.log(response["data"]);
            })
            .catch((error) => {
              console.log(error);
            });
          axios
            .post(this.url + "/todos", { todo })
            .then((response) => {
              console.log(response["data"]);
            })
            .catch((error) => {
              console.log(error);
            });

          this.temp_todo_item = "";
          this.$refs.input.focus();
        }
        if (this.temp_todo_item != "" && this.edit_index != null) {
          this.todo_list[this.edit_index].body = this.temp_todo_item;

          let todo = new Todo(this.edit_index, this.temp_todo_item, this.todo_list[this.edit_index].done);
          axios
            .put(this.url + "/todos", { todo })
            .then((response) => {
              console.log(response["data"]);
            })
            .catch((error) => {
              console.log(error);
            });

          this.temp_todo_item = "";
          this.$refs.input.focus();
          this.edit_index = null;
        }
      },

      DoneTodo(index) {
        this.todo_list[index].done = !this.todo_list[index].done;

        let todo = new Todo(
          this.todo_list[index].index,
          this.todo_list[index].body,
          this.todo_list[index].done
        );
        axios
          .put(this.url + "/todos", { todo })
          .then((response) => {
            console.log(response["data"]);
          })
          .catch((error) => {
            console.log(error);
          });
      },

      EditTodo(index) {
        this.temp_todo_item = this.todo_list[index].body;
        this.edit_index = index;
        this.$refs.input.focus();
      },

      DeleteTodo(index) {
        let todo = new Todo(
          this.todo_list[index].index,
          this.todo_list[index].body,
          this.todo_list[index].done
        );
        axios
          .delete(this.url + "/todos", { todo })
          .then((response) => {
            console.log(response["data"]);
          })
          .catch((error) => {
            console.log(error);
          });

        this.todo_list.splice(index, 1);
      },
    },

    mounted() {
      //this.FetchTodos();
      console.log(this.index);
    },
  };
</script>

<template>
  <div class="flex flex-col justify-center items-center w-full">
    <div class="app flex flex-col justify-center w-full">
      <h1 class="mt-2 text-center text-4xl">Todo App</h1>

      <div class="flex justify-center items-center w-full mt-12">
        <input
          class="p-2 rounded-tl-3xl rounded-bl-3xl text-xl input bg-gray-200"
          type="text"
          placeholder="Buy 3 bottles of milk"
          v-model="temp_todo_item"
          ref="input"
          @keyup.enter="AddTodo()"
        />
        <button
          class="flex justify-center items-center w-12 h-12 p-2 rounded-tr-3xl rounded-br-3xl text-2xl transition-all duration-150 ease-linear bg-blue-700 text-white hover:bg-blue-300 hover:text-black"
          @click="AddTodo()"
        >
          <Icon icon="plus" />
        </button>
      </div>

      <div class="flex flex-col justify-center w-full mt-24 mb-8 pl-2 pr-2">
        <h6 class="mb-8 text-center text-2xl">List:</h6>

        <div class="flex flex-col justify-center w-full">
          <div
            class="p-4 mb-6 rounded-3xl"
            v-for="(todo, index) in todo_list"
            v-bind:key="index"
            :class="todo.done ? 'bg-white' : 'shadow-xl bg-amber-100'"
          >
            <div class="w-full mb-4 break-words" :class="todo.done ? 'line-through' : 'no-underline'">
              <p>{{ todo.body }}</p>
            </div>

            <div class="flex justify-end w-full">
              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl transition-all ease-linear duration-150 hover:cursor-pointer bg-green-600 text-white hover:bg-green-300 hover:text-black"
                @click="DoneTodo(index)"
                v-if="todo.done === false"
              >
                <Icon class="text-xl" icon="check" />
              </button>
              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl transition-all ease-linear duration-150 opacity-50 hover:opacity-100 hover:cursor-pointer bg-green-600 text-white hover:bg-green-300 hover:text-black"
                @click="DoneTodo(index)"
                v-else
              >
                <Icon class="text-xl" icon="check" />
              </button>

              <button
                class="flex justify-center items-center w-8 h-8 p-2 ml-1 mr-1 rounded-full shadow-xl transition-all ease-linear duration-150 hover:cursor-pointer bg-yellow-600 text-white hover:bg-yellow-300 hover:text-black"
                @click="EditTodo(index)"
                v-if="todo.done === false"
              >
                <Icon class="text-lg" icon="pen" />
              </button>
              <button
                class="flex justify-center items-center w-8 h-8 p-2 ml-1 mr-1 rounded-full shadow-xl bg-gray-400 text-white"
                @click="EditTodo(index)"
                disabled
                v-else
              >
                <Icon class="text-lg" icon="pen" />
              </button>

              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl transition-all ease-linear duration-150 hover:cursor-pointer bg-red-600 text-white hover:bg-red-300 hover:text-black"
                @click="DeleteTodo(index)"
                v-if="todo.done === false"
              >
                <Icon class="text-lg" icon="trash" />
              </button>
              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl transition-all ease-linear duration-150 opacity-50 hover:opacity-100 hover:cursor-pointer bg-red-600 text-white hover:bg-red-300 hover:text-black"
                @click="DeleteTodo(index)"
                v-else
              >
                <Icon class="text-lg" icon="trash" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  .app {
    max-width: 480px;
  }

  .input {
    min-width: 240px;
    max-width: 440px;
  }
</style>
