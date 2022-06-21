<script setup lang="ts">
  import { ref, onMounted } from "vue";
  import type { Ref } from "vue";
  import axios from "axios";
  import Todo from "./class";

  const url = ref("http://localhost:5000");
  const todo_list: Ref<Object | any> = ref([]);
  const temp_todo_item = ref("");
  const index = ref(-1);
  const edit_index = ref(-1);

  async function FetchTodos() {
    axios
      .get(url.value + "/todos")
      .then((response) => {
        const arrived_data = response["data"];
        for (let i in arrived_data) {
          todo_list.value.push(arrived_data[i]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
    axios
      .get(url.value + "/index")
      .then((response) => {
        index.value = response["data"];
      })
      .catch((error) => {
        console.log(error);
      });
  }

  async function AddTodo() {
    if (temp_todo_item.value !== "" && edit_index.value === -1) {
      const todo = new Todo(index.value, temp_todo_item.value, false);
      index.value++;
      todo_list.value.push(todo);

      axios({
        method: "put",
        url: url.value + "/index",
        data: {
          index: index.value,
        },
      })
        .then((response) => {
          console.log(response["data"]);
        })
        .catch((error) => {
          console.log(error);
        });
      axios({
        method: "post",
        url: url.value + "/todos",
        data: {
          todo,
        },
      })
        .then((response) => {
          console.log(response["data"]);
        })
        .catch((error) => {
          console.log(error);
        });
    }
    if (temp_todo_item.value !== "" && edit_index.value !== -1) {
      todo_list.value[edit_index.value].body = temp_todo_item.value;

      const todo = new Todo(
        todo_list.value[edit_index.value].index,
        todo_list.value[edit_index.value].body,
        todo_list.value[edit_index.value].done
      );
      axios({
        method: "put",
        url: url.value + "/todos",
        data: {
          todo,
          mode: "put",
        },
      })
        .then((response) => {
          console.log(response["data"]);
        })
        .catch((error) => {
          console.log(error);
        });
    }

    temp_todo_item.value = "";
    const input = document.getElementById("input") as HTMLFormElement;
    input.focus();
    edit_index.value = -1;
  }

  async function DoneTodo(index: number) {
    todo_list.value[index].done = !todo_list.value[index].done;

    const todo = new Todo(
      todo_list.value[index].index,
      todo_list.value[index].body,
      todo_list.value[index].done
    );
    axios({
      method: "put",
      url: url.value + "/todos",
      data: {
        todo,
        mode: "put",
      },
    })
      .then((response) => {
        console.log(response["data"]);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function EditTodo(index: number) {
    temp_todo_item.value = todo_list.value[index].body;
    edit_index.value = index;
    const input = document.getElementById("input") as HTMLFormElement;
    input.focus();
  }

  async function DeleteTodo(index: number) {
    const number = todo_list.value[index].index;
    axios({
      method: "put",
      url: url.value + "/todos",
      data: {
        target: number,
        mode: "delete",
      },
    })
      .then((response) => {
        console.log(response["data"]);
      })
      .catch((error) => {
        console.log(error);
      });

    todo_list.value.splice(index, 1);
  }

  onMounted(() => {
    FetchTodos();
  });
</script>

<template>
  <div class="flex flex-col justify-center items-center w-full">
    <main class="app flex flex-col justify-center w-full">
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
          class="flex justify-center items-center w-12 h-12 p-2 rounded-tr-3xl rounded-br-3xl text-2xl transition-all duration-150 ease-linear bg-blue-700 text-white hover:bg-blue-300 hover:text-black"
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
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl transition-all ease-linear duration-150 hover:cursor-pointer bg-green-600 text-white hover:bg-green-300 hover:text-black"
                @click="DoneTodo(index)"
                v-if="todo.done === false"
              >
                <Icon class="text-xl" icon="check" />
              </button>
              <!--
              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl bg-gray-400 text-white"
                disabled
                v-else-if="edit_index === todo_list[index]"
              >
                <Icon class="text-lg" icon="check" />
              </button>
              -->
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
              <!--
              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl bg-gray-400 text-white"
                disabled
                v-else-if="temp_todo_item.value === todo_list.value[index.value.toString()].body"
              >
                <Icon class="text-lg" icon="trash" />
              </button>
              -->
              <button
                class="flex justify-center items-center w-8 h-8 p-2 rounded-full shadow-xl transition-all ease-linear duration-150 opacity-50 hover:opacity-100 hover:cursor-pointer bg-red-600 text-white hover:bg-red-300 hover:text-black"
                @click="DeleteTodo(index)"
                v-else
              >
                <Icon class="text-lg" icon="trash" />
              </button>
            </footer>
          </article>
        </div>
      </div>
    </main>
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
