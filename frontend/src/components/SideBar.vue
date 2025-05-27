<template>
  <div class="sidebar">
    <div class="logo-container">
      <img src="@/assets/img/ISM_LOGO.png" alt="ISM Logo" class="logo" />
    </div>
    
    <nav class="nav-menu">
      <div 
        v-for="item in sidebarItem" 
        :key="item.path" 
        class="nav-item"
        :class="{ active: isActive(item.path) }"
        @click="navigate(item)"
      >
        <div class="icon-wrapper">
          <img :src="require(`@/assets/icons/${item.icon}`)" :alt="item.label" />
        </div>
        <span>{{ item.label }}</span>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  props: {
    role: {
      type: String,
      required: true,
    },
  },
  computed: {
    sidebarItem() {
      const managerPage = [
        //{ path: "/dashboard-manager", icon: "dashboard.png", label: "Dashboard" },
        { path: "/inventory-analysis", icon: "inventory_analysis.png", label: "Inventory Analysis" },
        { path: "/product-list", icon: "product.png", label: "Product"},
        { path: "/purchase-order-manager", icon: "purchase_order.png", label: "Purchase Order" },
        { path: "/reports-list", icon: "reports.png", label: "Report" },
        { path: "/suppliers-list", icon: "suppliers.png", label: "Suppliers" },
      ];
      
      const supplierPage = [
        //{ path: "/dashboard-supplier", icon: "dashboard.png", label: "Dashboard" },
        { path: "/manage-account", icon: "manage_account.png", label: "Manage Account" },
        { path: "/product-catalog", icon: "product_catalog.png", label: "Product Catalog" },
        { path: "/purchase-order-supplier", icon: "purchase_order.png", label: "Purchase Order" },
      ];

      const items = [
        ...(this.role === "manager" ? managerPage : []),
        ...(this.role === "supplier" ? supplierPage : []),
      ];
      
      items.push({ path: "/login", icon: "log_out.png", label: "Log Out", logout: true });
      
      return items;
    },
  },
  methods: {
    navigate(item) {
      if (item.logout) {
        console.log("Logging out...");
        localStorage.removeItem("token");
        this.$router.push("/login");
        return;
      }
      this.$router.push(item.path);
    },
    isActive(path) {
      return this.$route.path === path;
    }
  },
};
</script>

<style scoped>
.sidebar {
  width: 240px;
  height: 100%;
  background-color: white;
  border-right: 1px solid #eaeaea;
  display: flex;
  flex-direction: column;
  color: #5c6270;
}

.logo-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.logo {
  width: 100px;
  height: auto;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.nav-item:hover {
  background-color: #f5f5f5;
}

.nav-item.active {
  color: #0066cc;
  background-color: #f0f7ff;
  border-left: 4px solid #0066cc;
}

.icon-wrapper {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.nav-item img {
  width: 20px;
  height: 20px;
  opacity: 0.7;
}

.nav-item.active img {
  opacity: 1;
}

/* Place logout at the bottom */
.nav-item:last-child {
  margin-top: auto;
  border-top: 1px solid #eaeaea;
}
</style>