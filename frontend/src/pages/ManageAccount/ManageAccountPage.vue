<template>
  <div class="account-container">
    <h1>Manage Account</h1>
    
    <div class="form-group">
      <label>Full Name</label>
      <input type="text" v-model="userData.full_name" :disabled="!isEditing" />
    </div>
    
    <div class="form-group">
      <label>Company Name</label>
      <input type="text" v-model="userData.company_name" :disabled="!isEditing" />
    </div>
    
    <div class="form-group">
      <label>Company Address</label>
      <input type="text" v-model="userData.company_address" :disabled="!isEditing" />
    </div>
    
    <div class="form-group">
      <label>Email</label>
      <input type="email" v-model="userData.email" :disabled="!isEditing" />
    </div>
    
    <div class="form-group">
      <label>Phone number</label>
      <input type="text" v-model="userData.phone_number" :disabled="!isEditing" />
    </div>
    
    <div class="buttons-container">
      <button 
        class="edit-btn" 
        @click="isEditing ? saveChanges() : toggleEdit()"
      >
        {{ isEditing ? 'Save' : 'Edit' }}
      </button>
      
      <button 
        v-if="isEditing"
        class="cancel-btn" 
        @click="cancelEdit"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      isEditing: false,
      userData: {
        full_name: "",
        company_name: "",
        company_address: "",
        email: "",
        phone_number: ""
      },
      originalUserData: {}
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('token');
      const response = await api.get('/api/user-info', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });   

      this.userData = {
        full_name: response.data.full_name,
        company_name: response.data.company_name,
        company_address: response.data.company_address,
        email: response.data.email,
        phone_number: response.data.phone_number
      };
      
      // Store a copy of the original data
      this.originalUserData = { ...this.userData };
    } catch (error) {
      console.error('Failed to load user data:', error.response?.data || error.message);
    }
  },
  
  methods: {
    toggleEdit() {
      this.isEditing = true;
      this.originalUserData = { ...this.userData };
    },
    
    cancelEdit() {
      this.userData = { ...this.originalUserData };
      this.isEditing = false;
    },
    
    async saveChanges() {
      try {
        const token = localStorage.getItem('token');

        const response = await api.put('/api/manage-account', {
          full_name: this.userData.full_name,
          company_name: this.userData.company_name,
          company_address: this.userData.company_address,
          email: this.userData.email,
          phone_number: this.userData.phone_number,
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        console.log('User updated:', response.data);
        alert('Account information updated successfully!');
        
        // Update original data after successful save
        this.originalUserData = { ...this.userData };
        this.isEditing = false;
      } catch (error) {
        console.error('Error updating account:', error.response?.data || error.message);
        alert('Failed to update account information.');
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
  margin: 10px auto;
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

.buttons-container {
  display: flex;
  gap: 10px;
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

.cancel-btn {
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-btn:hover {
  background-color: #cbd5e0;
}
</style>