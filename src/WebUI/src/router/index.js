import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Detector from "../views/Detector.vue";
import QueryGen from "../views/QueryGen.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/detector", component: Detector },
  { path: "/query-generator", component: QueryGen },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
