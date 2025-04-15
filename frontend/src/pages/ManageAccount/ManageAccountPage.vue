<template>
    <div class="account-container">
      <h1>Manage Account</h1>
      
      <div class="form-group">
        <label>Full Name</label>
        <input type="text" v-model="userData.fullName" :disabled="!isEditing" />
      </div>
      
      <div class="form-group">
        <label>Company Name</label>
        <input type="text" v-model="userData.companyName" :disabled="!isEditing" />
      </div>
      
      <div class="form-group">
        <label>Company Address</label>
        <input type="text" v-model="userData.companyAddress" :disabled="!isEditing" />
      </div>
      
      <div class="form-group">
        <label>Email</label>
        <input type="email" v-model="userData.email" :disabled="!isEditing" />
      </div>
      
      <div class="form-group">
        <label>Phone number</label>
        <input type="text" v-model="userData.phoneNumber" :disabled="!isEditing" />
      </div>
      
      <button 
        class="edit-btn" 
        @click="toggleEdit"
      >
        {{ isEditing ? 'Save' : 'Edit' }}
      </button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isEditing: false,
        userData: {
          fullName: 'Chong Lee',
          companyName: 'Chong\'s Trading',
          companyAddress: 'Lot 13, Jalan Bukit ABC, 24000 Kemaman, Terengganu',
          email: 'chong@gmail.com',
          phoneNumber: '0123456789'
        }
      }
    },
    methods: {
      toggleEdit() {
        this.isEditing = !this.isEditing;
        
        if (!this.isEditing) {
          // Save logic would go here
          console.log('Saving user data:', this.userData);
          // You might want to call an API endpoint here
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .account-container {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    padding: 30px;
    max-width: 800px;
    margin: 30px auto;
  }
  
  h1 {
    color: #4a5568;
    margin-top: 0;
    margin-bottom: 30px;
    font-weight: 500;
    font-size: 24px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
    color: #4a5568;
    font-weight: 500;
    font-size: 14px;
  }
  
  input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    background-color: #f8f9fa;
    color: #2d3748;
    font-size: 14px;
  }
  
  input:focus {
    outline: none;
    border-color: #0066cc;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
  }
  
  input:disabled {
    background-color: #f8f9fa;
    color: #4a5568;
    cursor: not-allowed;
  }
  
  .edit-btn {
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 12px 24px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .edit-btn:hover {
    background-color: #0052a3;
  }
  </style>