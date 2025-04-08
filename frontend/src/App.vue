<template>
  <div>
    <nav>
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link> |
      <router-link to="/dashboard" v-if="isAuthenticated">Dashboard</router-link> |
      <button @click="logout" v-if="isAuthenticated">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("token");
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
  },
};
</script>

<!--npm install vue-->
<!--npm install vue router-->
<!--npm install @fontsource/poppins-->
<!--npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/vue-fontawesome
-->
<!--npm install axios-->