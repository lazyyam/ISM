<template>
  <div class="register-container">
    <div class="register-box">
      <font-awesome-icon 
        icon="arrow-left" 
        class="back-icon" 
        @click="goBack" 
      />
      <img src="@/assets/img/ISM_LOGO.png" alt="ISM Logo" class="logo" />
      <h2 class="title">Register</h2>
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label for="full_name">Full Name</label>
          <input type="text" id="full_name" v-model="full_name" placeholder="Enter your full name" required />
        </div>
        <div class="input-group">
          <label for="company_name">Company Name</label>
          <input type="text" id="company_name" v-model="company_name" placeholder="Enter your company name" required />
        </div>
        <div class="input-group">
          <label for="company_address">Company Address</label>
          <textarea id="company_address" v-model="company_address" placeholder="Enter your company address" required></textarea>
        </div>
        <div class="input-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
        </div>
        <div class="input-group">
          <label for="phone_number">Phone No.</label>
          <input type="text" id="phone_number" v-model="phone_number" placeholder="Enter your phone number" required />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
        </div>
        
        <p v-if="errorMessage" style="color: red; margin-top: 10px;">
          {{ errorMessage }}
        </p>

        <button type="submit" class="register-btn">Sign Up</button>
        <button type="button" class="login-btn" @click="goToLogin">
          Already have an account? Login
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";

library.add(faArrowLeft);

export default {
  components: {
    FontAwesomeIcon,
  },
  data() {
    return {
      full_name: "",
      email: "",
      phone_number: "",
      password: "",
      company_name: "",
      company_address: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await api.post("/register", {
          email: this.email,
          password: this.password,
          full_name: this.full_name,
          role: "supplier",
          phone_number: this.phone_number,
          company_name: this.company_name,
          company_address: this.company_address,
        });

        console.log(response.data);
        alert("Registration successful! Please login.");
        this.$router.push("/login");

      } catch (error) {
        console.error("Registration failed:", error.response?.data?.detail || error.message);

        this.errorMessage = error.response?.data?.detail 
          ? JSON.stringify(error.response.data.detail) 
          : "Registration failed.";
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
* {
  font-family: 'Poppins', sans-serif;
  color: #101540;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f1f3;
  padding: 1rem 0;
}

.register-box {
  position: relative;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 450px;
  text-align: center;
}

.logo {
  width: 130px;
  margin-bottom: 1rem;
}

.title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-align: left;
  padding-left: 2.2rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin-bottom: 1rem;
}

.input-group label {
  font-weight: 500;
  margin-bottom: 5px;
  width: 84%;
  text-align: left;
}

.input-group input, .input-group textarea {
  width: 80%;
  padding: 8px;
  border: 1px solid #8F8F8F;
  background-color: #EDF0F2;
  border-radius: 4px;
  font-size: 14px;
}

.input-group textarea {
  height: 80px;
  resize: vertical;
}

button {
  width: 84%;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.register-btn {
  background-color: #007bff;
  color: white;
}

.register-btn:hover {
  background-color: #0069da;
}

.login-btn {
  background-color: #6c757d;
  color: white;
}

.login-btn:hover {
  background-color: #616970;
}

.back-icon {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 24px;
  cursor: pointer;
  color: #007bff;
}

.back-icon:hover {
  color: #0056b3;
}

@media (max-width: 576px) {
  .register-box {
    width: 90%;
    padding: 1.5rem;
  }
}
</style>