<template>
    <div class="reset-password-container">
      <div class="reset-password-box">
        <font-awesome-icon icon="arrow-left" class="back-icon" @click="goBack" />
        <h2 class="title">Create a new password</h2>
        <p class="description">Enter your new password below.</p>
  
        <form @submit.prevent="submitReset">
          <div class="input-group">
            <label for="password">New Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              required
              placeholder="Enter new password"
            />
          </div>
  
          <div class="input-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              required
              placeholder="Confirm new password"
            />
          </div>
  
          <button type="submit" class="submit-btn" :disabled="isLoading">
            Reset Password
          </button>
        </form>
  
        <p v-if="message" class="message">{{ message }}</p>
      </div>
    </div>
  </template>

<script>
import api from "@/services/api";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
library.add(faArrowLeft);

export default {
  components: {
    FontAwesomeIcon,
  },
  data() {
    return {
      password: "",
      confirmPassword: "",
      message: "",
      isLoading: false,
    };
  },
  methods: {
    async submitReset() {
      if (this.password !== this.confirmPassword) {
        this.message = "Passwords do not match.";
        return;
      }

      const token = this.$route.query.token;
      if (!token) {
        this.message = "Invalid or missing token.";
        return;
      }

      this.isLoading = true;

      try {
        await api.post("/reset-password", {
          token: token,
          new_password: this.password,
        });

        this.message = "Password has been reset successfully. You can now log in.";
        
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.detail || "Reset failed.";
        } else {
          this.message = "An error occurred. Please try again.";
        }
      } finally {
        this.isLoading = false;
      }
    },
    goBack() {
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

.reset-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f1f3;
}

.reset-password-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 450px;
  text-align: center;
  position: relative;
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

.title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: left;
  padding-left: 2.2rem;
}

.description {
  font-size: 14px;
  color: #666;
  margin-bottom: 1.5rem;
  text-align: left;
  padding-left: 2.2rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
  width: 100%;
}

.input-group label {
  font-weight: 500;
  margin-bottom: 5px;
  text-align: left;
  width: 84%;
}

.input-group input {
  width: 80%;
  padding: 8px;
  border: 1px solid #8F8F8F;
  background-color: #EDF0F2;
  border-radius: 4px;
  font-size: 14px;
}

.submit-btn {
  width: 84%;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  background-color: #007bff;
  color: white;
  margin-top: 0.5rem;
}

.submit-btn:hover {
  background-color: #0069da;
}

.message {
  margin-top: 10px;
  font-size: 14px;
  color: green;
}
</style>