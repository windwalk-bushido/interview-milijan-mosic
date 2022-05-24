import { createApp } from "vue";
import App from "./App.vue";

import "./assets/index.css";
import "./assets/global.css";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faPlus, faCheck, faPen, faTrash, faMoon, faSun } from "@fortawesome/free-solid-svg-icons";
library.add(faPlus, faCheck, faPen, faTrash, faMoon, faSun);

createApp(App).component("Icon", FontAwesomeIcon).mount("#app");
