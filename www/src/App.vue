<script setup lang="ts">
  import { ref } from "vue";
  import { RouterLink, RouterView, useRouter } from "vue-router";

  const router = useRouter();

  let is_user_logged_in = ref(false);

  function NavBarLoggedIn() {
    is_user_logged_in.value = true;
  }

  function NavBarNormal() {
    is_user_logged_in.value = false;
  }

  function LogoutUser() {
    sessionStorage.removeItem("todo_app_user_uuid");
    localStorage.removeItem("todo_app_user_uuid");

    NavBarNormal();
    router.push({ name: "index" });
  }
</script>

<template>
  <header class="">
    <nav
      class="fixed flex justify-end items-center w-full shadow-md bg-white text-black p-4"
      v-if="is_user_logged_in === false"
    >
      <RouterLink
        class="pl-4 pr-4 pt-2 pb-2 hover:rounded-xl hover:shadow-md my-animation bg-white hover:bg-yellow-100 text-black"
        to="/"
        >Home</RouterLink
      >
    </nav>

    <nav
      class="fixed flex justify-end items-center w-full shadow-md bg-white text-black p-4"
      v-if="is_user_logged_in"
    >
      <RouterLink
        class="pl-4 pr-4 pt-2 pb-2 hover:rounded-xl hover:shadow-md my-animation bg-white hover:bg-yellow-100 text-black"
        to="/user/dashboard"
        >Dashboard</RouterLink
      >
      <RouterLink
        class="mr-4 ml-4 pl-4 pr-4 pt-2 pb-2 hover:rounded-xl hover:shadow-md my-animation bg-white hover:bg-yellow-100 text-black"
        to="/user/settings"
        >Settings</RouterLink
      >
      <button
        class="pl-4 pr-4 pt-2 pb-2 rounded-xl shadow-lg hover:shadow-md my-animation bg-yellow-400 hover:bg-yellow-100 text-black"
        @click="LogoutUser()"
      >
        Logout
      </button>
    </nav>
  </header>

  <main class="flex flex-col justify-start items-center w-screen h-screen bg-gray-100">
    <RouterView class="mt-20" @NavBarLoggedIn="NavBarLoggedIn" />
  </main>

  <footer class="flex justify-between items-center p-4">
    <div class="flex">
      <p class="mr-2">By:</p>
      <a
        class="underline hover:decoration-double my-animation text-blue-500 hover:text-blue-800"
        href="https://github.com/windwalk-bushido"
        >Windwalk</a
      >
    </div>
    <p>2022.</p>
  </footer>
</template>
