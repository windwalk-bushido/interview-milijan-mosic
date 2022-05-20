<script>
  export default {
    name: "App",

    data() {
      return {
        todo_list: [],
        todo_item: "",
        index: 0,
        edit_index: null,
      };
    },

    methods: {
      AddTodo() {
        if (this.todo_item != "" && this.edit_index == null) {
          this.todo_list = [...this.todo_list, this.todo_item];
          localStorage.setItem(this.todo_list, JSON.stringify(this.todo_list));
          this.todo_item = "";
          this.$refs.input.focus();
        } else {
          this.todo_list[this.edit_index] = this.todo_item;
          this.todo_item = "";
          this.$refs.input.focus();
        }

        this.edit_index = null;
      },

      EditTodo(index) {
        this.todo_item = this.todo_list[index];
        this.edit_index = index;
        this.$refs.input.focus();
      },

      DeleteTodo(index) {
        this.todo_list.splice(index, 1);
      },
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
          v-model="todo_item"
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

        <div
          class="p-4 mb-6 rounded-3xl shadow-xl bg-amber-100"
          v-for="(todo_item, index) in todo_list"
          v-bind:key="index"
        >
          <div class="w-full mb-4 break-words">
            {{ todo_item }}
          </div>
          <div class="flex justify-end w-full">
            <Icon
              class="w-4 h-4 p-2 rounded-full shadow-xl text-xl transition-all ease-linear duration-150 hover:cursor-pointer bg-green-600 text-white hover:bg-green-300 hover:text-black"
              icon="check"
              @click="DoneTodo(index)"
            />
            <Icon
              class="w-4 h-4 p-2 ml-1 mr-1 rounded-full shadow-xl text-lg transition-all ease-linear duration-150 hover:cursor-pointer bg-yellow-600 text-white hover:bg-yellow-300 hover:text-black"
              icon="pen"
              @click="EditTodo(index)"
            />
            <Icon
              class="w-4 h-4 p-2 rounded-full shadow-xl text-lg transition-all ease-linear duration-150 hover:cursor-pointer bg-red-600 text-white hover:bg-red-300 hover:text-black"
              icon="trash"
              @click="DeleteTodo(index)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  ::selection {
    @apply bg-gray-300 text-black;
  }

  .app {
    max-width: 480px;
  }

  .input {
    min-width: 240px;
    max-width: 440px;
  }
</style>
