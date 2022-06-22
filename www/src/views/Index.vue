<script setup lang="ts">
  import { ref, defineEmits } from "vue";

  import { RouterLink, useRouter } from "vue-router";
  import axios from "axios";

  const emit = defineEmits(["NavBarLoggedIn"]);
  const router = useRouter();

  let is_login_username_good = ref(true);
  let login_username_error = ref("");
  let is_login_password_good = ref(true);
  let login_password_error = ref("");
  let is_data_being_sent = ref(false);

  function CheckUsersInputtedData() {
    const username_input = document.getElementById("username_input") as HTMLFormElement;
    const password_input = document.getElementById("password_input") as HTMLFormElement;

    let is_email_good: boolean = false;
    let is_password_good: boolean = false;

    if (username_input.value.length === 0) {
      is_login_username_good.value = false;
      login_username_error.value = "Don't leave this field empty.";
    } else {
      is_login_username_good.value = true;
      login_username_error.value = "";
      is_email_good = true;
    }

    if (password_input.value.length === 0) {
      is_login_password_good.value = false;
      login_password_error.value = "Don't leave this field empty.";
    } else {
      is_login_password_good.value = true;
      login_password_error.value = "";
      is_password_good = true;
    }

    if (is_email_good && is_password_good) {
      return true;
    } else {
      return false;
    }
  }

  async function LoginUser() {
    // const submit_button = document.getElementById("submit_button") as HTMLElement;
    // submit_button.classList.add("is-loading");
    // SUBMIT BUTTON'S ICON SHOULD CHANGE TO CIRCLE AND ROTATE

    if (CheckUsersInputtedData()) {
      is_login_username_good.value = true;
      login_username_error.value = "";
      is_login_password_good.value = true;
      login_password_error.value = "";
      is_data_being_sent.value = true;

      const username_input = document.getElementById("username_input") as HTMLFormElement;
      const password_input = document.getElementById("password_input") as HTMLFormElement;

      let hashed_password = "";
      // HASH PASSWORD HERE

      const { user, error } = await axios
        .get(import.meta.env.VITE_API_URL + "/login", {
          data: {
            username: username_input.value,
            password: hashed_password,
          },
        })
        .then((response) => {
          return response["data"];
        })
        .catch((error) => {
          return error;
        });

      if (user !== null && error === null) {
        // kul = Keep User Logged in
        const kul_checkbox = document.getElementById("kul_checkbox") as HTMLFormElement;

        if (kul_checkbox.checked) {
          localStorage.setItem("todo_app_user_uuid", user.id);
        } else {
          sessionStorage.setItem("todo_app_user_uuid", user.id);
        }

        emit("NavBarLoggedIn");
        router.push({ name: "dashboard" });
      } else {
        is_login_username_good.value = false;
        login_username_error.value = "Username or password is not correct.";
        is_login_password_good.value = false;
        login_password_error.value = "Username or password is not correct.";

        if (error !== null) {
          console.log(error);
        }
      }
    }

    //submit_button.classList.remove("is-loading");
    is_data_being_sent.value = false;
  }
</script>

<template>
  <div class="flex flex-col justify-center items-center">
    <div class="flex flex-col justify-center items-center w-80 rounded-xl shadow-xl p-4 mt-8 bg-white">
      <h1 class="text-2xl mb-12">Login</h1>

      <label for="username">Username</label>
      <input
        type="text"
        name="username"
        id="username_input"
        class="p-2 mb-1 rounded-xl shadow-md bg-gray-200"
        :class="is_login_username_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-200'"
        :readonly="is_data_being_sent"
      />
      <p class="text-rose-500" v-if="login_username_error !== ''">{{ login_username_error }}</p>
      <p v-else>&nbsp;</p>

      <label for="password" class="mt-4">Password</label>
      <input
        type="password"
        name="password"
        id="password_input"
        class="p-2 mb-1 rounded-xl shadow-md bg-gray-200"
        :class="is_login_password_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-200'"
        :readonly="is_data_being_sent"
      />
      <p class="text-rose-500" v-if="login_password_error !== ''">{{ login_password_error }}</p>
      <p v-else>&nbsp;</p>

      <div class="flex items-baseline mb-12 mt-4">
        <label for="checkbox">
          Keep me logged in
          <input
            type="checkbox"
            name="checkbox"
            id="kul_checkbox"
            class="ml-1"
            :readonly="is_data_being_sent"
          />
        </label>
      </div>

      <button
        type="button"
        id="submit_button"
        class="pl-4 pr-4 pt-2 pb-2 rounded-xl shadow-lg hover:shadow-md my-animation bg-yellow-400 hover:bg-yellow-100 text-black"
        @click="LoginUser()"
        :readonly="is_data_being_sent"
      >
        Submit
      </button>
    </div>
  </div>
</template>
