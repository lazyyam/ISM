import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/pages/Auth/LoginPage.vue";
import RegisterPage from "@/pages/Auth/RegisterPage.vue";
import ForgetPasswordPage from "@/pages/Auth/ForgetPasswordPage.vue";

const routes = [
  { path: "/", redirect: "/login" }, // Redirect root to login
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  { path: "/forget-password", component: ForgetPasswordPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
