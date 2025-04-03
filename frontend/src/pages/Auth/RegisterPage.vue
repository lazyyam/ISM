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
          <div class="input-row">
            <div class="input-group">
              <label for="fullName">Full Name</label>
              <input type="text" id="fullName" v-model="fullName" placeholder="Enter your full name" required />
            </div>
          </div>
          <div class="input-row">
            <div class="input-group">
              <label for="email">Email</label>
              <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
            </div>
            <div class="input-group">
              <label for="phone">Phone No.</label>
              <input type="text" id="phone" v-model="phone" placeholder="Enter your phone number" required />
            </div>
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
          </div>
          <button type="submit" class="register-btn">Sign Up</button>
        </form>
      </div>
    </div>
  </template>
  
  
  
  <script>
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  import { library } from "@fortawesome/fontawesome-svg-core";
  import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
  
  // Add the icon to the FontAwesome library
  library.add(faArrowLeft);
  
  export default {
    components: {
      FontAwesomeIcon,
    },
    data() {
      return {
        fullName: "",
        email: "",
        phone: "",
        password: "",
      };
    },
    methods: {
      handleRegister() {
        console.log("Registering with:", this.fullName, this.email, this.phone, this.password);
        // Add registration logic later
      },
      goBack() {
        this.$router.go(-1); // Go back to the previous page
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
    height: 100vh;
    background-color: #f0f1f3;
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
  
  .input-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    width: 100%;
    flex-wrap: wrap;
  }
  
  .input-group {
    display: flex;
    flex-direction: column;
    width: 48%;
    margin-bottom: 1rem;
    align-items: center;
  }
  
  .input-group label {
    font-weight: 500;
    margin-bottom: 5px;
    text-align: left;
    width: 66%;
  }
  
  .input-group input {
    width: 58%;
    padding: 8px;
    border: 1px solid #8F8F8F;
    background-color: #EDF0F2;
    border-radius: 4px;
    font-size: 14px;
  }
  
  button {
    width: 84%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    background-color: #007bff;
    color: white;
    margin-top: 0.3rem;
  }

  button:hover{
    background-color: #0069da;
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

  </style>