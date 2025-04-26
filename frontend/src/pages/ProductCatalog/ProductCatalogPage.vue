<template>
  <div class="catalog-container">
    <h1>Product Catalog</h1>
    
    <div class="catalog-actions">
      <div class="search-bar">
        <i class="search-icon"></i>
        <input 
          type="text" 
          placeholder="Search product ID" 
          v-model="searchQuery"
        />
      </div>
      
      <div class="filter-dropdown">
        <button class="filter-btn">
          Filter
          <i class="chevron-down"></i>
        </button>
      </div>
    </div>
    
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
          <tr v-for="(product, index) in filteredProducts" :key="product.id">
            <td>{{ index + 1 }}</td>
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
                  @click="deleteProduct(product.id)"
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
          />
        </div>
        
        <div class="form-group">
          <label for="productCategory">Product Category:</label>
          <input 
            id="productCategory" 
            type="text" 
            v-model="formData.category" 
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="productCode">Product Code:</label>
          <input 
            id="productCode" 
            type="text" 
            v-model="formData.code" 
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="productCost">Product Cost:</label>
          <input 
            id="productCost" 
            type="number" 
            step="0.01" 
            v-model="formData.cost" 
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="productQuantity">Quantity Available:</label>
          <input 
            id="productQuantity" 
            type="number" 
            v-model="formData.quantity_available" 
            class="form-control"
          />
        </div>
      </div>
      
      <template v-slot:footer>
        <button class="cancel-btn" @click="closeModal">Cancel</button>
        <button class="submit-btn" @click="submitForm">
          {{ isEditing ? 'Update' : 'Add' }}
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import BaseModal from '@/components/BaseModal.vue';
import api from "@/services/api";

export default {
  name: 'ProductCatalog',
  components: {
    BaseModal
  },
  data() {
    return {
      searchQuery: '',
      isModalOpen: false,
      isEditing: false,
      currentProductId: null,
      formData: {
        name: '',
        category: '',
        code: '',
        cost: '',
        quantity_available: ''
      },
      products: []
    };
  },
  mounted() {
    this.fetchProducts();
  },
  computed: {
    filteredProducts() {
      if (!this.searchQuery) {
        return this.products;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.products.filter(product => {
        return product.name.toLowerCase().includes(query) ||
               product.code.includes(query);
      });
    },
    modalTitle() {
      return this.isEditing ? 'Edit Product' : 'Add Product';
    }
  },
  methods: {
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
    },
    closeModal() {
      this.isModalOpen = false;
      setTimeout(this.resetForm, 300);
    },
    async fetchProducts() {
      try {
        const response = await api.get('/api/supplier-products');
        this.products = response.data;
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    },
    async submitForm() {
      try {
        if (this.isEditing) {
          // Update product
          await api.put(`/api/supplier-products/${this.currentProductId}`, this.formData);
        } else {
          // Create new product
          await api.post('/api/supplier-products', this.formData);
        }
        this.closeModal();
        this.fetchProducts();
      } catch (error) {
        console.error('Failed to save product:', error);
      } 
    },
    async deleteProduct(product_id) {
      if (confirm('Are you sure you want to delete this product?')) {
        try {
          await api.delete(`/api/supplier-products/${product_id}`);
          this.fetchProducts();
        } catch (error) {
          console.error('Failed to delete product:', error);
        }
      }
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

/* Form Styles */
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
</style>