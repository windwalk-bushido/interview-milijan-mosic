<script setup lang="ts">
  import { ref, onMounted } from "vue";
  import type { Ref } from "vue";
  import axios from "axios";
  import Todo from "../class";

  const todo_list: Ref<Object | any> = ref([]);
  const temp_todo_item = ref("");
  const edit_index = ref(-1);
  const delete_index = ref(-1);
  const disable_control = ref(false);

  function GetUsersToken() {
    const uuid_token_session = sessionStorage.getItem("todo_app_user_uuid");
    const uuid_token_storage = localStorage.getItem("todo_app_user_uuid");

    if (uuid_token_session !== null) {
      return uuid_token_session;
    } else {
      return uuid_token_storage;
    }
  }

  async function FetchTodos() {
    const token = GetUsersToken();

    await axios
      .post(import.meta.env.VITE_API_URL + "/todos", {
        API_KEY: import.meta.env.VITE_API_KEY,
        mode: "get",
        uuid: token,
      })
      .then((response) => {
        const arrived_data = response["data"];
        for (let i in arrived_data) {
          todo_list.value.push(arrived_data[i]);
        }
      })
      .catch((error) => {
        alert(error);
      });
  }

  async function AddTodo() {
    const token = GetUsersToken();

    if (temp_todo_item.value !== "" && edit_index.value === -1) {
      const todo = new Todo(token, temp_todo_item.value, false);
      todo_list.value.push(todo);

      await axios
        .post(import.meta.env.VITE_API_URL + "/todos", {
          API_KEY: import.meta.env.VITE_API_KEY,
          mode: "post",
          todo: todo,
        })
        .then((response) => {
          console.log(response["data"]);
        })
        .catch((error) => {
          alert(error);
        });
    }

    // EditTodo()
    if (temp_todo_item.value !== "" && edit_index.value !== -1) {
      todo_list.value[edit_index.value].body = temp_todo_item.value;

      const todo = new Todo(
        token,
        todo_list.value[edit_index.value].body,
        todo_list.value[edit_index.value].done
      );

      await axios
        .put(import.meta.env.VITE_API_URL + "/todos", {
          API_KEY: import.meta.env.VITE_API_KEY,
          mode: "put",
          todo: todo,
          index: todo_list.value[edit_index.value].index,
          date_created: todo_list.value[edit_index.value].date_created,
        })
        .then((response) => {
          console.log(response["data"]);
        })
        .catch((error) => {
          alert(error);
        });
    }

    temp_todo_item.value = "";
    const input = document.getElementById("input") as HTMLFormElement;
    input.focus();
    edit_index.value = -1;
    disable_control.value = false;
  }

  async function DoneTodo(index: number) {
    todo_list.value[index].done = !todo_list.value[index].done;
    const token = GetUsersToken();

    const todo = new Todo(token, todo_list.value[index].body, todo_list.value[index].done);

    await axios
      .put(import.meta.env.VITE_API_URL + "/todos", {
        API_KEY: import.meta.env.VITE_API_KEY,
        mode: "put",
        todo: todo,
        index: todo_list.value[index].index,
        date_created: todo_list.value[index].date_created,
      })
      .then((response) => {
        console.log(response["data"]);
      })
      .catch((error) => {
        alert(error);
      });
  }

  function EditTodo(index: number) {
    temp_todo_item.value = todo_list.value[index].body;
    edit_index.value = index;
    const input = document.getElementById("input") as HTMLFormElement;
    input.focus();
  }

  async function DeleteTodo() {
    const number = todo_list.value[delete_index.value].index;

    await axios
      .put(import.meta.env.VITE_API_URL + "/todos", {
        API_KEY: import.meta.env.VITE_API_KEY,
        mode: "delete",
        target: number,
      })
      .then((response) => {
        console.log(response["data"]);
      })
      .catch((error) => {
        alert(error);
      });

    todo_list.value.splice(delete_index.value, 1);
    delete_index.value = -1;
  }

  function HandleModal(command: number) {
    const modal = document.getElementById("modal") as HTMLElement;
    if (command === 1) {
      modal.classList.remove("hidden");
    } else if (command === 0) {
      modal.classList.add("hidden");
    }
  }

  onMounted(() => {
    FetchTodos();
  });
</script>

<template>
  <div class="flex justify-center w-full pt-1 pb-1 bg-green-600 text-white" v-if="edit_index === -1">
    <p class="text-lg">Ready for using</p>
  </div>
  <div class="flex justify-center w-full pt-1 pb-1 bg-yellow-500 text-black" v-else>
    <p class="text-lg">App in editing mode!</p>
  </div>

  <div class="app flex flex-col justify-center w-full mt-4">
    <h1 class="mt-2 text-center text-4xl">Todo App</h1>

    <div class="flex justify-center items-center w-full mt-12">
      <input
        class="p-2 rounded-tl-3xl rounded-bl-3xl text-xl input bg-gray-200"
        type="text"
        placeholder="Buy 3 bottles of milk"
        v-model="temp_todo_item"
        id="input"
        @keyup.enter="AddTodo()"
      />
      <button
        class="flex justify-center items-center w-12 h-12 p-2 rounded-tr-3xl rounded-br-3xl text-2xl transition-all duration-100 ease-linear bg-blue-700 text-white hover:bg-blue-300 hover:text-black"
        @click="AddTodo()"
      >
        <Icon icon="plus" />
      </button>
    </div>

    <div class="flex flex-col justify-center w-full mt-24 mb-8 pl-2 pr-2">
      <h6 class="mb-8 text-center text-2xl">List:</h6>

      <div class="flex flex-col justify-center w-full">
        <article
          class="p-4 mb-6 rounded-3xl"
          v-for="(todo, index) in todo_list"
          :key="index"
          :class="todo.done ? 'bg-white' : 'shadow-xl bg-amber-100'"
        >
          <main class="w-full mb-4 break-words" :class="todo.done ? 'line-through' : 'no-underline'">
            <p>{{ todo.body }}</p>
          </main>

          <footer class="flex justify-end w-full">
            <button
              class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl my-animation bg-green-600 text-white hover:bg-green-300 hover:text-black"
              @click="DoneTodo(index)"
              v-if="disable_control === false"
            >
              <Icon class="text-xl" icon="check" />
            </button>
            <button
              class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl bg-gray-400 text-white"
              disabled
              v-else-if="disable_control"
            >
              <Icon class="text-lg" icon="check" />
            </button>

            <button
              class="flex justify-center items-center w-8 h-8 p-2 ml-1 mr-1 rounded-full shadow-xl my-animation bg-yellow-600 text-white hover:bg-yellow-300 hover:text-black"
              @click="
                () => {
                  EditTodo(index);
                  disable_control = true;
                }
              "
              v-if="todo.done === false"
            >
              <Icon class="text-lg" icon="pen" />
            </button>
            <button
              class="flex justify-center items-center w-8 h-8 p-2 ml-1 mr-1 rounded-full shadow-xl bg-gray-400 text-white"
              disabled
              v-else
            >
              <Icon class="text-lg" icon="pen" />
            </button>

            <button
              class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl bg-gray-400 text-white"
              disabled
              v-if="todo.done === false"
            >
              <Icon class="text-lg" icon="trash" />
            </button>
            <button
              class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl my-animation bg-red-600 text-white hover:bg-red-300 hover:text-black"
              @click="
                () => {
                  delete_index = index;
                  HandleModal(1);
                }
              "
              v-else
            >
              <Icon class="text-lg" icon="trash" />
            </button>
          </footer>
        </article>
      </div>
    </div>
  </div>

  <div
    class="w-screen h-screen justify-center items-center z-10 absolute my-padding-60"
    id="modal"
    :class="delete_index !== -1 ? 'flex' : 'hidden'"
  >
    <div class="flex flex-col justify-center items-center p-8 rounded-3xl shadow-xl bg-white">
      <p class="text-2xl mb-8">Are you sure?</p>
      <div>
        <button
          class="mr-2 p-3 rounded-full hover:shadow-xl my-animation hover:opacity-100 bg-white text-black hover:bg-gray-300 hover:text-black"
          @click="HandleModal(0)"
        >
          Cancel
        </button>
        <button
          class="ml-2 p-3 text-bold rounded-full shadow-xl my-animation hover:opacity-100 bg-red-600 text-white hover:bg-red-300 hover:text-black"
          @click="
            () => {
              DeleteTodo();
              HandleModal(0);
            }
          "
        >
          Delete
        </button>
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
