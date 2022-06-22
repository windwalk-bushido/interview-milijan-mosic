<script setup lang="ts">
  import { ref } from "vue";
  import { RouterLink, RouterView, useRouter } from "vue-router";

  const router = useRouter();

  let is_user_logged_in = ref(true);

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
    <nav class="" v-if="is_user_logged_in === false">
      <RouterLink to="/">Home</RouterLink>
    </nav>

    <nav class="" v-if="is_user_logged_in">
      <RouterLink to="/user/dashboard">Dashboard</RouterLink>
      <RouterLink to="/user/settings">Settings</RouterLink>
      <button @click="LogoutUser()">Logout</button>
    </nav>
  </header>

  <main class="flex flex-col justify-start items-center w-screen h-screen">
    <RouterView @NavBarLoggedIn="NavBarLoggedIn" />
  </main>

  <footer class="">
    <div class="">
      <p>By:</p>
      <a href="https://github.com/windwalk-bushido">Windwalk</a>
    </div>
    <p>2022.</p>
  </footer>
</template>
