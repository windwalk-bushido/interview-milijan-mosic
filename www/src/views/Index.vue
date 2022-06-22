<script setup lang="ts">
  import { ref, defineEmits } from "vue";

  import { RouterLink, useRouter } from "vue-router";
  import axios from "axios";

  const emit = defineEmits(["NavBarLoggedIn"]);
  const router = useRouter();

  let is_register_username_good = ref(true);
  let register_username_error = ref("");
  let is_register_password1_good = ref(true);
  let register_password1_error = ref("");
  let is_register_password2_good = ref(true);
  let register_password2_error = ref("");

  let is_login_username_good = ref(true);
  let login_username_error = ref("");
  let is_login_password_good = ref(true);
  let login_password_error = ref("");

  let is_data_being_sent = ref(false);
  let is_modal_raised = ref(true);

  function HandleModal(command: boolean) {
    is_modal_raised.value = command;
  }

  function CheckUsersInputDataForRegister() {
    const register_username_input = document.getElementById("register_username_input") as HTMLFormElement;
    const register_password1_input = document.getElementById("register_password1_input") as HTMLFormElement;
    const register_password2_input = document.getElementById("register_password2_input") as HTMLFormElement;

    let is_username_good: boolean = false;
    let is_password1_good: boolean = false;
    let is_password2_good: boolean = false;

    const username_regex: RegExp = /^[a-z0-9_-]{5,33}$/;
    const username_regex_testing = username_regex.exec(register_username_input.value);

    if (register_username_input.value.length === 0) {
      is_register_username_good.value = false;
      register_username_error.value = "Don't leave this field empty.";
    } else if (register_username_input.value.length < 5) {
      is_register_username_good.value = false;
      register_username_error.value = "Username's length must be greater than or equal to 5.";
    } else if (register_username_input.value.length > 33) {
      is_register_username_good.value = false;
      register_username_error.value = "Username's length must be lower than or equal to 32.";
    } else if (!username_regex_testing) {
      is_register_username_good.value = false;
      register_username_error.value =
        "Only uppercase, lowercase, hiphen (-) and underscore(_) characters are allowed.";
    } else {
      is_register_username_good.value = true;
      register_username_error.value = "";
      is_username_good = true;
    }

    const password_regex: RegExp = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$/;
    const password_regex_testing = password_regex.exec(register_password1_input.value);

    if (register_password1_input.value.length === 0) {
      is_register_password1_good.value = false;
      register_password1_error.value = "Don't leave this field empty.";
    } else if (register_password1_input.value.length < 7) {
      is_register_password1_good.value = false;
      register_password1_error.value = "Password's length must be greater than or egual to 8.";
    } else if (register_password1_input.value.length > 65) {
      is_register_password1_good.value = false;
      register_password1_error.value = "Password's length must be lower than or egual to 64.";
    } else if (!password_regex_testing) {
      is_register_password1_good.value = false;
      register_password1_error.value =
        "Type in at least one uppercase letter, one lowercase letter, one number and one special character.";
    } else {
      is_register_password1_good.value = true;
      register_password1_error.value = "";
      is_password1_good = true;
    }

    if (register_password2_input.value.length === 0) {
      is_register_password2_good.value = false;
      register_password2_error.value = "Don't leave this field empty.";
    } else if (register_password2_input.value !== register_password1_input.value) {
      is_register_password2_good.value = false;
      register_password2_error.value = "Passwords don't match.";
    } else {
      is_register_password2_good.value = true;
      register_password2_error.value = "";
      is_password2_good = true;
    }

    if (is_username_good && is_password1_good && is_password2_good) {
      return true;
    } else {
      return false;
    }
  }

  async function RegisterUser() {
    // const submit_button = document.getElementById("submit_button") as HTMLElement;
    // submit_button.classList.add("is-loading");
    // SUBMIT BUTTON'S ICON SHOULD CHANGE TO CIRCLE AND ROTATE

    if (CheckUsersInputDataForRegister()) {
      is_data_being_sent.value = true;

      const register_username_input = document.getElementById("register_username_input") as HTMLFormElement;
      const register_password1_input = document.getElementById("register_password1_input") as HTMLFormElement;

      let hashed_password = "";
      // HASH PASSWORD HERE

      const { user, error } = await axios
        .get(import.meta.env.VITE_API_URL + "/register", {
          data: {
            username: register_username_input.value,
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
        HandleModal(true);
      } else {
        if (error !== null) {
          alert(error);
        }
      }
    }

    //submit_button.classList.remove("is-loading");
    is_data_being_sent.value = false;
  }

  function CheckUsersInputDataForLogin() {
    const login_username_input = document.getElementById("login_username_input") as HTMLFormElement;
    const login_password_input = document.getElementById("login_password_input") as HTMLFormElement;

    let is_username_good: boolean = false;
    let is_password_good: boolean = false;

    if (login_username_input.value.length === 0) {
      is_login_username_good.value = false;
      login_username_error.value = "Don't leave this field empty.";
    } else {
      is_login_username_good.value = true;
      login_username_error.value = "";
      is_username_good = true;
    }

    if (login_password_input.value.length === 0) {
      is_login_password_good.value = false;
      login_password_error.value = "Don't leave this field empty.";
    } else {
      is_login_password_good.value = true;
      login_password_error.value = "";
      is_password_good = true;
    }

    if (is_username_good && is_password_good) {
      return true;
    } else {
      return false;
    }
  }

  async function LoginUser() {
    // const submit_button = document.getElementById("submit_button") as HTMLElement;
    // submit_button.classList.add("is-loading");
    // SUBMIT BUTTON'S ICON SHOULD CHANGE TO CIRCLE AND ROTATE

    if (CheckUsersInputDataForLogin()) {
      is_data_being_sent.value = true;

      const login_username_input = document.getElementById("login_username_input") as HTMLFormElement;
      const login_password_input = document.getElementById("login_password_input") as HTMLFormElement;

      let hashed_password = "";
      // HASH PASSWORD HERE

      const { user, error } = await axios
        .get(import.meta.env.VITE_API_URL + "/login", {
          data: {
            username: login_username_input.value,
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
  <div class="flex flex-wrap justify-center items-center mt-32 mb-16">
    <div class="flex flex-col justify-center items-center w-80 m-4 rounded-xl shadow-xl p-6 mt-8 bg-gray-100">
      <h1 class="text-2xl mb-12">Register</h1>

      <label for="username">Username</label>
      <input
        type="text"
        name="username"
        id="register_username_input"
        class="w-full p-2 mb-1 rounded-xl shadow-md bg-gray-300"
        :class="is_register_username_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-300'"
        :readonly="is_data_being_sent"
      />
      <p class="text-rose-500" v-if="register_username_error !== ''">{{ register_username_error }}</p>
      <p v-else>&nbsp;</p>

      <label for="password" class="mt-4">Password</label>
      <input
        type="password"
        name="password"
        id="register_password1_input"
        class="w-full p-2 mb-1 rounded-xl shadow-md bg-gray-300"
        :class="is_register_password1_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-300'"
        :readonly="is_data_being_sent"
      />
      <p class="text-rose-500" v-if="register_password1_error !== ''">{{ register_password1_error }}</p>
      <p v-else>&nbsp;</p>

      <label for="password" class="mt-4">Password again</label>
      <input
        type="password"
        name="password"
        id="register_password2_input"
        class="w-full p-2 mb-1 rounded-xl shadow-md bg-gray-300"
        :class="is_register_password2_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-300'"
        :readonly="is_data_being_sent"
      />
      <p class="text-rose-500" v-if="register_password2_error !== ''">{{ register_password2_error }}</p>
      <p v-else>&nbsp;</p>

      <button
        type="button"
        id="register_submit_button"
        class="mt-6 pl-4 pr-4 pt-2 pb-2 rounded-xl shadow-lg hover:shadow-md my-animation bg-yellow-400 hover:bg-yellow-100 text-black"
        @click="RegisterUser()"
        :readonly="is_data_being_sent"
      >
        Submit
      </button>
    </div>

    <div class="flex flex-col justify-center items-center w-80 m-4 rounded-xl shadow-xl p-6 mt-8 bg-gray-100">
      <h1 class="text-2xl mb-12">Login</h1>

      <label for="username">Username</label>
      <input
        type="text"
        name="username"
        id="login_username_input"
        class="w-full p-2 mb-1 rounded-xl shadow-md bg-gray-300"
        :class="is_login_username_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-300'"
        :readonly="is_data_being_sent"
      />
      <p class="text-rose-500" v-if="login_username_error !== ''">{{ login_username_error }}</p>
      <p v-else>&nbsp;</p>

      <label for="password" class="mt-4">Password</label>
      <input
        type="password"
        name="password"
        id="login_password_input"
        class="w-full p-2 mb-1 rounded-xl shadow-md bg-gray-300"
        :class="is_login_password_good === false ? 'border-2 border-rose-500' : 'border-2 border-gray-300'"
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
        id="login_submit_button"
        class="pl-4 pr-4 pt-2 pb-2 rounded-xl shadow-lg hover:shadow-md my-animation bg-yellow-400 hover:bg-yellow-100 text-black"
        @click="LoginUser()"
        :readonly="is_data_being_sent"
      >
        Submit
      </button>
    </div>
  </div>

  <div
    class="w-screen h-screen justify-center items-center z-10 absolute my-padding-60"
    :class="is_modal_raised ? 'flex' : 'hidden'"
  >
    <div class="flex flex-col justify-center items-center p-8 rounded-3xl shadow-xl bg-white">
      <p class="text-2xl">Account created successfully.</p>
      <p class="text-2xl mb-8">You can now log in.</p>
      <div>
        <button
          class="ml-2 p-3 text-bold rounded-full shadow-xl my-animation hover:opacity-100 bg-green-600 text-white hover:bg-green-300 hover:text-black"
          @click="HandleModal(false)"
        >
          Okay
        </button>
      </div>
    </div>
  </div>
</template>
