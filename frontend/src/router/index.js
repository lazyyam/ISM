import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/pages/Auth/LoginPage.vue";
import RegisterPage from "@/pages/Auth/RegisterPage.vue";
import ForgetPasswordPage from "@/pages/Auth/ForgetPasswordPage.vue";
import DashboardPage from "@/pages/Dashboard/DashboardPage.vue";

const routes = [
  { 
    path: "/", 
    redirect: "/login" 
  }, // Redirect root to login
  { 
    path: "/login", 
    component: LoginPage 
  },
  { 
    path: "/register", 
    component: RegisterPage 
  },
  { 
    path: "/forget-password", 
    component: ForgetPasswordPage
  },
  { 
    path:"/dashboard",
    component: DashboardPage,
    meta: {requiresAuth: true}  //add this to page tht need to be protected
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if ((to.path === "/login" || to.path === "/register") && token) {
    next("/dashboard");
  } else {
    next();
  }
});


export default router;
