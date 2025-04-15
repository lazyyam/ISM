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
              <label for="full_name">Full Name</label>
              <input type="text" id="full_name" v-model="full_name" placeholder="Enter your full name" required />
            </div>
          </div>
          <div class="input-row">
            <div class="input-group">
              <label for="email">Email</label>
              <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
            </div>
            <div class="input-group">
              <label for="phone_number">Phone No.</label>
              <input type="text" id="phone_number" v-model="phone_number" placeholder="Enter your phone number" required />
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
          });

          console.log(response.data);
          alert("Registration successful! Please login.");
          this.$router.push("/login");

        } catch (error) {
          console.error("Registration failed:", error.response?.data?.detail || error.message);

          const errorMessage = error.response?.data?.detail 
            ? JSON.stringify(error.response.data.detail) // Converts the error object to a readable string
            : "Registration failed.";
          
          alert(errorMessage);
        }
      },
      goBack() {
        this.$router.go(-1);
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