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
              @input="clearError('password')"
            />
            <p v-if="passwordError" class="field-error">{{ passwordError }}</p>
          </div>
  
          <div class="input-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              required
              placeholder="Confirm new password"
              @input="clearError('confirmPassword')"
            />
            <p v-if="confirmPasswordError" class="field-error">{{ confirmPasswordError }}</p>
          </div>
  
          <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? "Resetting..." : "Reset Password" }}
          </button>
        </form>
  
        <p v-if="message" :class="isSuccess ? 'success-message' : 'field-error'">{{ message }}</p>
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
      passwordError: "",
      confirmPasswordError: "",
      message: "",
      isSuccess: false,
      isLoading: false,
    };
  },
  methods: {
    clearError(field) {
      if (field === "password") this.passwordError = "";
      if (field === "confirmPassword") this.confirmPasswordError = "";
      this.message = "";
      this.isSuccess = false;
    },
    async submitReset() {
      this.passwordError = "";
      this.confirmPasswordError = "";
      this.message = "";
      this.isSuccess = false;

      if (!this.password) {
        this.passwordError = "Password is required.";
        return;
      }
      if (this.password.length < 8) {
        this.passwordError = "Password must be at least 8 characters.";
        return;
      }

      if (!this.confirmPassword) {
        this.confirmPasswordError = "Please confirm your password.";
        return;
      }
      if (this.password !== this.confirmPassword) {
        this.confirmPasswordError = "Passwords do not match.";
        return;
      }

      const token = this.$route.query.token;
      if (!token) {
        this.message = "Invalid or missing token.";
        return;
      }

      this.isLoading = true;

      try {
        await api.post("/api/reset-password", {
          token: token,
          new_password: this.password,
        });

        this.message = "Password has been reset successfully. You can now log in.";
        this.isSuccess = true;
        this.password = "";
        this.confirmPassword = "";
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.detail || "Reset failed.";
        } else {
          this.message = "An error occurred. Please try again.";
        }
        this.isSuccess = false;
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
  padding-left: 2.0rem;
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
  width: 84%;
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

.submit-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.submit-btn:hover:enabled {
  background-color: #0069da;
}

.field-error {
  color: #e53e3e;
  font-size: 14px;
  margin-top: 6px;
  margin-bottom: 0;
  text-align: left;
  width: 84%;
  padding-left: 2.0rem;
}

.success-message {
  color: green;
  font-size: 14px;
  margin-top: 10px;
  text-align: left;
  width: 84%;
  padding-left: 2.0rem;
}
</style>