<template>
    <div class="login-container">
      <div class="login-box">
        <img src="@/assets/img/ISM_LOGO.png" alt="ISM Logo" class="logo" />
        <h2 class="title">Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
          </div>
          <div class="options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe" /> Remember me
            </label>
            <a href="#" class="forgot-password" @click.prevent="goToForgetPassword">Forgot password?</a>
          </div>
          <button type="submit" class="login-btn">Login</button>
          <button type="button" class="register-btn" @click="goToRegister">
            Create a new account
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: "",
        password: "",
        rememberMe: false,
      };
    },
    methods: {
      handleLogin() {
        console.log("Logging in with", this.email, this.password);
        // Add authentication logic later
      },
      goToRegister() {
        this.$router.push("/register");
      },
      goToForgetPassword() {
        this.$router.push("/forget-password");
      }
    },
  };
  </script>
  
<style scoped>
* {
  font-family: 'Poppins', sans-serif;
  color: #101540;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f1f3;
}

.login-box {
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
  align-items: center; /* Centers the inputs */
  width: 100%;
  margin-bottom: 1rem;
}

.input-group label {
  font-weight: 500;
  margin-bottom: 5px;
  width: 84%;
  text-align: left;
}

.input-group input {
  width: 80%;
  padding: 8px;
  border: 1px solid #8F8F8F;
  background-color: #EDF0F2;
  border-radius: 4px;
  font-size: 14px;
}

.options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  width: 85%;
  margin: 1rem auto;
}

.remember-me {
  display: flex;
  align-items: center;
}

.remember-me input {
  margin-right: 5px;
}

.forgot-password {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.forgot-password:hover {
  text-decoration: underline;
}

button {
  width: 84%;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.login-btn {
  background-color: #007bff;
  color: white;
  margin-bottom: 0.5rem;
}

.login-btn:hover {
  background-color: #0069da;
}

.register-btn {
  background-color: #6c757d;
  color: white;
}

.register-btn:hover {
  background-color: #616970
}
</style>
  