<template>
  <div class="catalog-container">
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

    <h1>Product Catalog</h1>
    
    <div class="catalog-actions">
      <div class="search-bar">
        <i class="search-icon"></i>
        <input 
          type="text" 
          placeholder="Search product by name, code, or category" 
          v-model="searchQuery"
        />
      </div>
      
      <div class="filter-dropdown">
        <select v-model="selectedCategory" class="filter-select">
          <option value="">All Categories</option>
          <option v-for="cat in categoryOptions" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
    </div>

    <div v-if="productsError" class="error-message">{{ productsError }}</div>
    <div class="product-table">
      <table>
        <thead>
          <tr>
            <th>No.</th>
            <th>Name</th>
            <th>Category</th>
            <th>Code</th>
            <th>Cost</th>
            <th>Quantity Available</th>
            <th class="action-cell">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(product, index) in paginatedProducts" :key="product.id">
            <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.category }}</td>
            <td>{{ product.code }}</td>
            <td>{{ product.cost }}</td>
            <td>{{ product.quantity_available }}</td>
            <td class="action-cell">
              <div class="action-buttons">
                <button 
                  class="edit-btn" 
                  @click="openEditModal(product)"
                  title="Edit product"
                >
                  <i class="edit-icon"></i>
                </button>
                <button 
                  class="delete-btn" 
                  @click="confirmDeleteProduct(product.id)"
                  title="Delete product"
                >
                  <i class="delete-icon"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
        <tr v-if="filteredProducts.length === 0">
          <td colspan="7" style="text-align: center;">No products found.</td>
        </tr>
      </table>
      <div class="pagination">
        <button @click="currentPage--" :disabled="currentPage === 1" title="Previous">
          &lt;
        </button>
        <span>
          Page
          <input
            type="number"
            v-model.number="pageInput"
            @change="goToPage"
            :min="1"
            :max="totalPages"
            style="width: 40px; text-align: center;"
          />
          of {{ totalPages }}
        </span>
        <button @click="currentPage++" :disabled="currentPage === totalPages" title="Next">
          &gt;
        </button>
      </div>
    </div>
    
    <button class="add-product-btn" @click="openAddModal">
      <i class="plus-icon"></i>
      Add Product
    </button>
    
    <!-- Product Modal -->
    <BaseModal
      :isOpen="isModalOpen"
      :title="modalTitle"
      @close="closeModal"
    >
      <div class="product-form">
        <div class="form-group">
          <label for="productName">Product Name:</label>
          <input 
            id="productName" 
            type="text" 
            v-model="formData.name" 
            class="form-control"
            @input="clearFieldError('name')"
          />
          <p v-if="nameError" class="field-error">{{ nameError }}</p>
        </div>
        
        <div class="form-group">
          <label for="productCategory">Product Category:</label>
          <v-select
            id="productCategory"
            v-model="formData.category"
            :options="categoryOptions"
            placeholder="Select or search category"
            :reduce="cat => cat"
            :taggable="true"
            @new="addCategory"
            class="form-control category-vselect"
            @input="clearFieldError('category')"
          />
          <p v-if="categoryError" class="field-error">{{ categoryError }}</p>
        </div>
        
        <div class="form-group">
          <label for="productCode">Product Code:</label>
          <input 
            id="productCode" 
            type="text" 
            v-model="formData.code" 
            class="form-control"
            @input="clearFieldError('code')"
          />
          <p v-if="codeError" class="field-error">{{ codeError }}</p>
        </div>
        
        <div class="form-group">
          <label for="productCost">Product Cost:</label>
          <input 
            id="productCost" 
            type="number" 
            step="0.01" 
            v-model="formData.cost" 
            class="form-control"
            @input="clearFieldError('cost')"
          />
          <p v-if="costError" class="field-error">{{ costError }}</p>
        </div>
        
        <div class="form-group">
          <label for="productQuantity">Quantity Available:</label>
          <input 
            id="productQuantity" 
            type="number" 
            v-model="formData.quantity_available" 
            class="form-control"
            @input="clearFieldError('quantity_available')"
          />
          <p v-if="quantityError" class="field-error">{{ quantityError }}</p>
        </div>
      </div>
      
      <template v-slot:footer>
        <button class="cancel-btn" @click="closeModal">Cancel</button>
        <button class="submit-btn" @click="submitForm">
          {{ isEditing ? 'Update' : 'Add' }}
        </button>
      </template>
    </BaseModal>

    <!-- Delete Modal -->
    <DeleteModal
      :isOpen="showDeleteModal"
      @close="cancelDeleteProduct"
      @confirm="deleteProductConfirmed"
      message="Are you sure you want to delete this product?"
    />
  </div>
</template>

<script>
import BaseModal from '@/components/BaseModal.vue';
import DeleteModal from '@/components/DeleteModal.vue';
import SuccessToast from "@/components/SuccessToast.vue";
import ErrorToast from "@/components/ErrorToast.vue";
import api from "@/services/api";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

export default {
  name: 'ProductCatalog',
  components: {
    BaseModal,
    DeleteModal,
    SuccessToast,
    ErrorToast,
    vSelect
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      pageInput: 1,
      searchQuery: '',
      selectedCategory: '',
      isModalOpen: false,
      isEditing: false,
      currentProductId: null,
      showDeleteModal: false,
      productIdToDelete: null,
      formData: {
        name: '',
        category: '',
        code: '',
        cost: '',
        quantity_available: ''
      },
      products: [],
      categoryOptions: [
        "Vegetables", "Fruits", "Herbs & Spices", "Poultry", "Beef & Lamb", "Fish & Seafood", "Frozen Meat",
        "Milk", "Cheese", "Eggs", "Yogurt", "Bread", "Cakes & Pastries", "Buns & Rolls", "Canned Food",
        "Instant Noodles", "Rice & Grains", "Cooking Oil", "Flour & Baking Supplies", "Sugar & Salt",
        "Pasta & Spaghetti", "Soy Sauce", "Chili Sauce", "Curry Paste", "Seasoning Powders", "Bottled Water",
        "Soft Drinks", "Coffee & Tea", "Juice", "Instant Beverages", "Biscuits & Cookies", "Chocolates & Candy",
        "Chips & Crackers", "Traditional Snacks", "Detergents", "Cleaning Supplies", "Tissues & Towels",
        "Trash Bags", "Soap & Body Wash", "Shampoo & Hair Care", "Toothpaste", "Sanitary Products", "Diapers",
        "Baby Food", "Baby Wipes", "Pet Food", "Pet Grooming", "Others"
      ],
      productsError: "",
      nameError: "",
      categoryError: "",
      codeError: "",
      costError: "",
      quantityError: "",
      showSuccessToast: false,
      showErrorToast: false,
      toastMessage: ""
    };
  },
  mounted() {
    this.fetchProducts();
  },
  watch: {
    currentPage(val) {
      this.pageInput = val;
    },
    searchQuery() {
      this.currentPage = 1;
    },
    selectedCategory() {
      this.currentPage = 1;
    }
  },
  computed: {
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredProducts.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredProducts.length / this.pageSize) || 1;
    },
    filteredProducts() {
      let filtered = this.products;
      if (this.selectedCategory) {
        filtered = filtered.filter(product => product.category === this.selectedCategory);
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(product => {
          return (
            (product.name && product.name.toLowerCase().includes(query)) ||
            (product.code && product.code.toLowerCase().includes(query)) ||
            (product.category && product.category.toLowerCase().includes(query))
          );
        });
      }
      return filtered;
    },
    modalTitle() {
      return this.isEditing ? 'Edit Product' : 'Add Product';
    }
  },
  methods: {
    goToPage() {
      if (this.pageInput < 1) this.pageInput = 1;
      if (this.pageInput > this.totalPages) this.pageInput = this.totalPages;
      this.currentPage = this.pageInput;
    },
    showToast(msg, type = "success") {
      this.toastMessage = msg;
      this.showSuccessToast = type === "success";
      this.showErrorToast = type === "error";
      setTimeout(() => {
        this.showSuccessToast = false;
        this.showErrorToast = false;
        this.toastMessage = "";
      }, 2500);
    },
    addCategory(newCategory) {
      if (!this.categoryOptions.includes(newCategory)) {
        this.categoryOptions.push(newCategory);
      }
      this.formData.category = newCategory;
    },
    resetForm() {
      this.formData = {
        name: '',
        category: '',
        code: '',
        cost: '',
        quantity_available: ''
      };
      this.currentProductId = null;
      this.isEditing = false;
      this.clearAllFieldErrors();
    },
    openAddModal() {
      this.resetForm();
      this.isModalOpen = true;
    },
    openEditModal(product) {
      this.isEditing = true;
      this.currentProductId = product.id;
      this.formData = { 
        name: product.name,
        category: product.category,
        code: product.code,
        cost: product.cost,
        quantity_available: product.quantity_available
      };
      this.isModalOpen = true;
      this.clearAllFieldErrors();
    },
    closeModal() {
      this.isModalOpen = false;
      setTimeout(this.resetForm, 300);
    },
    async fetchProducts() {
      this.productsError = "";
      try {
        const response = await api.get('/api/supplier-products');
        this.products = response.data;
      } catch (error) {
        this.products = [];
        this.productsError = "Failed to fetch products.";
      }
    },
    clearFieldError(field) {
      if (field === "name") this.nameError = "";
      if (field === "category") this.categoryError = "";
      if (field === "code") this.codeError = "";
      if (field === "cost") this.costError = "";
      if (field === "quantity_available") this.quantityError = "";
    },
    clearAllFieldErrors() {
      this.nameError = "";
      this.categoryError = "";
      this.codeError = "";
      this.costError = "";
      this.quantityError = "";
    },
    validateForm() {
      let valid = true;
      this.clearAllFieldErrors();

      if (!this.formData.name) {
        this.nameError = "Product name is required.";
        valid = false;
      } else if (
        this.products.some(
          p =>
            p.name.trim().toLowerCase() === this.formData.name.trim().toLowerCase() &&
            (!this.isEditing || p.id !== this.currentProductId)
        )
      ) {
        this.nameError = "Product name must be unique.";
        valid = false;
      }

      if (!this.formData.category) {
        this.categoryError = "Category is required.";
        valid = false;
      }

      if (!this.formData.code) {
        this.codeError = "Product code is required.";
        valid = false;
      } else if (
        this.products.some(
          p =>
            p.code.trim().toLowerCase() === this.formData.code.trim().toLowerCase() &&
            (!this.isEditing || p.id !== this.currentProductId)
        )
      ) {
        this.codeError = "Product code must be unique.";
        valid = false;
      }

      if (!this.formData.cost && this.formData.cost !== 0) {
        this.costError = "Cost is required.";
        valid = false;
      } else if (isNaN(this.formData.cost) || Number(this.formData.cost) < 0) {
        this.costError = "Cost must be a non-negative number.";
        valid = false;
      }

      if (
        this.formData.quantity_available === "" ||
        this.formData.quantity_available === null
      ) {
        this.quantityError = "Quantity is required.";
        valid = false;
      } else if (
        isNaN(this.formData.quantity_available) ||
        Number(this.formData.quantity_available) < 0
      ) {
        this.quantityError = "Quantity must be a non-negative number.";
        valid = false;
      }
      return valid;
    },
    async submitForm() {
      if (!this.validateForm()) return;
      try {
        if (this.isEditing) {
          await api.put(`/api/supplier-products/${this.currentProductId}`, this.formData);
          this.showToast("Product updated successfully!", "success");
        } else {
          await api.post('/api/supplier-products', this.formData);
          this.showToast("Product added successfully!", "success");
        }
        this.closeModal();
        this.fetchProducts();
      } catch (error) {
        this.showToast("Failed to save product.", "error");
      }
    },
    confirmDeleteProduct(productId) {
      this.productIdToDelete = productId;
      this.showDeleteModal = true;
    },
    async deleteProductConfirmed() {
      try {
        await api.delete(`/api/supplier-products/${this.productIdToDelete}`);
        this.fetchProducts();
        this.showToast("Product deleted.", "success");
      } catch (error) {
        this.showToast("Failed to delete product.", "error");
      } finally {
        this.showDeleteModal = false;
        this.productIdToDelete = null;
      }
    },
    cancelDeleteProduct() {
      this.showDeleteModal = false;
      this.productIdToDelete = null;
    }
  }
};
</script>

<style scoped>
.catalog-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #4a5568;
  margin-top: 0;
  margin-bottom: 24px;
  font-weight: 500;
  font-size: 24px;
}

.catalog-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-bar {
  position: relative;
  flex: 1;
  max-width: 500px;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23718096'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.search-bar input {
  width: 100%;
  padding: 10px 10px 10px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
}

.filter-dropdown {
  margin-left: 15px;
}

.filter-btn {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.chevron-down {
  width: 16px;
  height: 16px;
  margin-left: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23718096'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.product-table {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #edf2f7;
}

th {
  background-color: #f8fafc;
  color: #4a5568;
  font-weight: 500;
  font-size: 14px;
}

td {
  color: #2d3748;
  font-size: 14px;
}

.action-cell {
  width: 100px;
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.edit-btn, .delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background-color: #edf2f7;
}

.delete-btn:hover {
  background-color: #fed7d7;
}

.edit-icon {
  width: 16px;
  height: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.delete-icon {
  width: 16px;
  height: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23e53e3e'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.add-product-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-left: auto;
  transition: background-color 0.2s;
}

.add-product-btn:hover {
  background-color: #0052a3;
}

.plus-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 6v6m0 0v6m0-6h6m-6 0H6' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.product-form {
  width: 100%;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 6px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
}

.cancel-btn {
  padding: 10px 16px;
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.2s;
}

.cancel-btn:hover {
  background-color: #cbd5e0;
}

.submit-btn {
  padding: 10px 24px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #0052a3;
}

.filter-select {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
  background: white;
  min-width: 180px;
}

.error-message {
  color: #e53e3e;
  font-size: 15px;
  padding: 12px 16px;
}
.field-error {
  color: #e53e3e;
  font-size: 13px;
  margin: 0 0 8px 0;
  text-align: left;
  width: 100%;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin: 16px 0;
}
.pagination button {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  background: #e2e8f0;
  cursor: not-allowed;
}
</style>