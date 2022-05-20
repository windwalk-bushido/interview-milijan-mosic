import { createApp } from "vue";
import App from "./App.vue";

import "./assets/index.css";
import "./assets/global.css";

import axios from "axios";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faPlus, faCheck, faPen, faTrash } from "@fortawesome/free-solid-svg-icons";
library.add(faPlus, faCheck, faPen, faTrash);

createApp(App).component("Icon", FontAwesomeIcon).mount("#app");
