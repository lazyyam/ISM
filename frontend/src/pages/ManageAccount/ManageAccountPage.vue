<template>
  <div class="account-container">
    <SuccessToast
      v-if="showSuccessToast"
      :message="toastMessage"
      @close="showSuccessToast = false"
    />
    <ErrorToast
      v-if="showErrorToast"
      :message="toastMessage"
      @close="showErrorToast = false"
    />

    <h1>Manage Account</h1>
    
    <div class="form-group">
      <label>Full Name</label>
      <input type="text" v-model="userData.full_name" :disabled="!isEditing" @input="clearFieldError('full_name')" />
      <p v-if="fullNameError" class="field-error">{{ fullNameError }}</p>
    </div>
    
    <div class="form-group">
      <label>Company Name</label>
      <input type="text" v-model="userData.company_name" :disabled="!isEditing" @input="clearFieldError('company_name')" />
      <p v-if="companyNameError" class="field-error">{{ companyNameError }}</p>
    </div>
    
    <div class="form-group">
      <label>Company Address</label>
      <input type="text" v-model="userData.company_address" :disabled="!isEditing" @input="clearFieldError('company_address')" />
      <p v-if="companyAddressError" class="field-error">{{ companyAddressError }}</p>
    </div>
    
    <div class="form-group">
      <label>Email</label>
      <input type="email" v-model="userData.email" :disabled="!isEditing" @input="clearFieldError('email')" />
      <p v-if="emailError" class="field-error">{{ emailError }}</p>
    </div>
    
    <div class="form-group">
      <label>Phone number</label>
      <input type="text" v-model="userData.phone_number" :disabled="!isEditing" @input="clearFieldError('phone_number')" />
      <p v-if="phoneNumberError" class="field-error">{{ phoneNumberError }}</p>
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
import SuccessToast from "@/components/SuccessToast.vue";
import ErrorToast from "@/components/ErrorToast.vue";

export default {
  name: 'ManageAccountPage',
  components: {
    SuccessToast,
    ErrorToast
  },
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
      originalUserData: {},
      fullNameError: "",
      companyNameError: "",
      companyAddressError: "",
      emailError: "",
      phoneNumberError: "",
      showSuccessToast: false,
      showErrorToast: false,
      toastMessage: ""
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
      
      this.originalUserData = { ...this.userData };
    } catch (error) {
      this.toastMessage = "Failed to load user data.";
      this.showErrorToast = true;
    }
  },
  
  methods: {
    clearFieldError(field) {
      if (field === "full_name") this.fullNameError = "";
      if (field === "company_name") this.companyNameError = "";
      if (field === "company_address") this.companyAddressError = "";
      if (field === "email") this.emailError = "";
      if (field === "phone_number") this.phoneNumberError = "";
    },
    toggleEdit() {
      this.isEditing = true;
      this.originalUserData = { ...this.userData };
    },
    
    cancelEdit() {
      this.userData = { ...this.originalUserData };
      this.isEditing = false;
      this.clearAllFieldErrors();
    },

    clearAllFieldErrors() {
      this.fullNameError = "";
      this.companyNameError = "";
      this.companyAddressError = "";
      this.emailError = "";
      this.phoneNumberError = "";
    },
    
    validateFields() {
      let valid = true;
      this.clearAllFieldErrors();

      if (!this.userData.full_name) {
        this.fullNameError = "Full name is required.";
        valid = false;
      } else if (!/^[A-Za-z\s]+$/.test(this.userData.full_name)) {
        this.fullNameError = "Full name must contain only letters and spaces.";
        valid = false;
      }
      if (!this.userData.company_name) {
        this.companyNameError = "Company name is required.";
        valid = false;
      }
      if (!this.userData.company_address) {
        this.companyAddressError = "Company address is required.";
        valid = false;
      }
      if (!this.userData.email) {
        this.emailError = "Email is required.";
        valid = false;
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.userData.email)) {
        this.emailError = "Please enter a valid email address.";
        valid = false;
      }
      if (!this.userData.phone_number) {
        this.phoneNumberError = "Phone number is required.";
        valid = false;
      } else if (!/^\d{9,15}$/.test(this.userData.phone_number.replace(/\D/g, ""))) {
        this.phoneNumberError = "Please enter a valid phone number (9-15 digits).";
        valid = false;
      }
      return valid;
    },
    
    async saveChanges() {
      if (!this.validateFields()) return;
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

        console.log(response.data);
        this.toastMessage = 'Account information updated successfully!';
        this.showSuccessToast = true;
        
        this.originalUserData = { ...this.userData };
        this.isEditing = false;
      } catch (error) {
        this.toastMessage = error.response?.data?.detail || 'Failed to update account information.';
        this.showErrorToast = true;
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

.field-error {
  color: #e53e3e;
  font-size: 13px;
  margin: 0 0 8px 0;
  text-align: left;
  width: 100%;
}
</style>