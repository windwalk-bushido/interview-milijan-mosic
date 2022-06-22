import { createRouter, createWebHistory } from "vue-router";
import Index from "../views/Index.vue";
import Dashboard from "../views/Dashboard.vue";
import Settings from "../views/Settings.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "index",
      component: Index,
    },
    {
      path: "/user/dashboard",
      name: "dashboard",
      component: Dashboard,
    },
    {
      path: "/user/settings",
      name: "settings",
      component: Settings,
    },
  ],
});

let is_user_logged_in: boolean = false;

function CheckIfUserIsLoggedIn() {
  const uuid_token_session = sessionStorage.getItem("todo_app_user_uuid");
  const uuid_token_storage = localStorage.getItem("todo_app_user_uuid");

  if (uuid_token_session !== null || uuid_token_storage !== null) {
    is_user_logged_in = true;
  } else {
    is_user_logged_in = false;
  }
}

router.beforeEach(async (to, from) => {
  CheckIfUserIsLoggedIn();
  if (is_user_logged_in === false && (to.name === "dashboard" || to.name === "settings")) {
    return { name: "index" };
  }
  if (is_user_logged_in && to.name === "index") {
    return { name: "dashboard" };
  }
});

export default router;
