<template>
  <div class="app-container">
    <SideBar
      v-if="isAuthenticated && role && !hideSideBarPages.includes($route.path)"
      :role="role"
    />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import { jwtDecode } from "jwt-decode";
import SideBar from "@/components/SideBar.vue";

export default {
  components: {
    SideBar,
  },
  data() {
    return {
      role: null,
      hideSideBarPages: [
        "/login",
        "/register",
        "/forgot-password",
        "/reset-password",
      ],
    };
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("token");
    },
  },
  methods: {
    setRoleFromToken() {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const decoded = jwtDecode(token);
          this.role = decoded.role;
          console.log("User role:", this.role);
        } catch (err) {
          console.error("Invalid token", err);
          localStorage.removeItem("token");
          this.role = null;
          this.$router.push("/login");
        }
      } else {
        this.role = null;
      }
    },
  },
  mounted() {
    this.setRoleFromToken();
  },
  watch: {
    '$route.path'() {
      this.setRoleFromToken();
    }
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Poppins', Arial, sans-serif;
  background-color: #f5f7fa;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

.app-container:not(:has(SideBar)) .main-content {
  width: 100%;
}
</style>

<!--npm install vue-->
<!--npm install vue router-->
<!--npm install @fontsource/poppins-->
<!--npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/vue-fontawesome
-->
<!--npm install axios-->
<!--npm install jwt-decode-->