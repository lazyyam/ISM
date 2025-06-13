import { createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/pages/Auth/LoginPage.vue";
import RegisterPage from "@/pages/Auth/RegisterPage.vue";
import ForgotPasswordPage from "@/pages/Auth/ForgotPasswordPage.vue";
import ResetPasswordPage from "@/pages/Auth/ResetPasswordPage.vue";

import ProductPage from "@/pages/Product/ProductPage.vue";
import PurchaseOrderManager from "@/pages/PurchaseOrder/PurchaseOrderManager.vue";
import ReportsPage from "@/pages/Reports/ReportsPage.vue";
import InventoryAnalysisPage from "@/pages/InventoryAnalysis/InventoryAnalysisPage.vue";
import SuppliersPage from "@/pages/Suppliers/SuppliersPage.vue";

import ManageAccountPage from "@/pages/ManageAccount/ManageAccountPage.vue";
import ProductCatalogPage from "@/pages/ProductCatalog/ProductCatalogPage.vue";
import PurchaseOrderSupplier from "@/pages/PurchaseOrder/PurchaseOrderSupplier.vue";


const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  { path: "/forgot-password", component: ForgotPasswordPage },
  { path: "/reset-password", component: ResetPasswordPage },

  { path:"/product-list", component: ProductPage, meta: {requiresAuth: true, role: "manager"} },
  { path:"/purchase-order-manager", component: PurchaseOrderManager, meta: {requiresAuth: true, role: "manager"} },
  { path:"/reports-list", component: ReportsPage, meta: {requiresAuth: true, role: "manager"} },
  { path:"/inventory-analysis", component: InventoryAnalysisPage, meta: {requiresAuth: true, role: "manager"} },
  { path:"/suppliers-list", component: SuppliersPage, meta: {requiresAuth: true, role: "manager"} },

  { path:"/manage-account", component: ManageAccountPage, meta: {requiresAuth: true, role: "supplier"} },
  { path:"/product-catalog", component: ProductCatalogPage, meta: {requiresAuth: true, role: "supplier"} },
  { path:"/purchase-order-supplier", component: PurchaseOrderSupplier, meta: {requiresAuth: true, role: "supplier"} },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (to.meta.requiresAuth && !token) {
    next("/login");

  } else if ((to.path === "/login" || to.path === "/register") && token) {
    if (role === "manager" && to.path !== "/inventory-analysis") {
      return next("/inventory-analysis");
    } else if (role === "supplier" && to.path !== "/manage-account") {
      return next("/manage-account");
    } else {
      return next();
    }

    } else if (to.meta.role && to.meta.role !== role) {
      next("/login"); 
    } else {
      next();
    }
});


export default router;
