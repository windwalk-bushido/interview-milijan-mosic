import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "./assets/global.css";
import "./assets/index.css";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faPlus, faCheck, faPen, faTrash, faMoon, faSun } from "@fortawesome/free-solid-svg-icons";

library.add(faPlus, faCheck, faPen, faTrash, faMoon, faSun);

const app = createApp(App);

app.use(router);
app.component("Icon", FontAwesomeIcon);
app.mount("#app");
