<template>
    <div class="product-container">
      <h1>Product</h1>
      
      <div class="product-actions">
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
              <th>Retail Price</th>
              <th>Threshold</th>
              <th>Quantity</th>
              <th class="expand-cell"></th>
              <th class="action-cell">Action</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(product, index) in filteredProducts" :key="product.id">
              <!-- Main Product Row -->
              <tr :class="{'expanded': expandedProductId === product.id}">
                <td>{{ index + 1 }}</td>
                <td>{{ product.name }}</td>
                <td>{{ product.category }}</td>
                <td>{{ product.code }}</td>
                <td>{{ product.cost }}</td>
                <td>{{ product.retail_price }}</td>
                <td>{{ product.stock_threshold }}</td>
                <td>{{ product.quantity }}</td>
                <td class="expand-cell">
                  <button 
                    class="expand-btn" 
                    @click="toggleExpand(product.id)"
                    :title="expandedProductId === product.id ? 'Collapse' : 'Expand'"
                  >
                    <i :class="['chevron-icon', expandedProductId === product.id ? 'chevron-up' : 'chevron-down']"></i>
                  </button>
                </td>
                <td class="action-cell">               
                  <div class="action-buttons">
                    <button 
                      class="sell-btn"
                      @click="openSellProductModal(product)"
                      title="Sell product"
                    >
                      <i class="sell-icon"></i>
                    </button>
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
              
              <!-- Expanded Batch Details -->
              <tr v-if="expandedProductId === product.id" class="batch-header">
                <td colspan="10">
                  <div class="batch-container">
                    <div class="batch-header-row">
                      <div class="batch-column batch-id">Batch ID</div>
                      <div class="batch-column batch-quantity">Quantity</div>
                      <div class="batch-column batch-expiry">Expiry Date</div>
                      <div class="batch-column batch-received">Received Date</div>
                      <div class="batch-column batch-actions">Action</div>
                    </div>
                    
                    <div class="batch-content">
                      <div v-if="product.batches && product.batches.length > 0">
                        <div 
                          v-for="(batch, index) in product.batches" 
                          :key="index"
                          class="batch-row"
                        >
                          <div class="batch-column batch-id">{{ batch.batch_id }}</div>
                          <div class="batch-column batch-quantity">{{ batch.quantity }}</div>
                          <div class="batch-column batch-expiry">{{ formatDate(batch.expiry_date) }}</div>
                          <div class="batch-column batch-received">{{ formatDate(batch.received_date) }}</div>
                          <div class="batch-column batch-actions">
                            <button class="batch-edit-btn" @click="openBatchEditModal(product.id, batch)">
                              <i class="edit-icon"></i>
                            </button>
                            <button class="batch-delete-btn" @click="deleteBatch(product.id, batch.batch_id)">
                              <i class="delete-icon"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                      <div v-else class="no-batches">No batch information available</div>
                    </div>
                    
                    <div class="add-batch-container">
                      <button class="add-batch-btn" @click="openAddBatchModal(product.id)">
                        <i class="plus-icon"></i>
                        Add Batch
                      </button>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
          <tr v-if="filteredProducts.length === 0">
            <td colspan="7" style="text-align: center;">No products found.</td>
          </tr>
        </table>
        <SalesModal
          v-if="isSalesModalOpen"
          :product="salesProduct"
          @close="closeSalesModal"
        />
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
            <label for="productRetailPrice">Product Retail Price:</label>
            <input 
              id="productRetailPrice" 
              type="number" 
              step="0.01" 
              v-model="formData.retail_price" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="productThreshold">Stock Threshold:</label>
            <input 
              id="productThreshold" 
              type="number" 
              v-model="formData.stock_threshold" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="productQuantity">Product Quantity:</label>
            <input 
              id="productQuantity" 
              type="number" 
              v-model="formData.quantity" 
              class="form-control"
              disabled
            />
            <small class="form-text">Total quantity is calculated from batches</small>
          </div>
        </div>
        
        <template v-slot:footer>
          <button class="submit-btn" @click="submitForm">
            {{ isEditing ? 'Update' : 'Add' }}
          </button>
        </template>
      </BaseModal>
      
      <!-- Batch Modal -->
      <BaseModal
        :isOpen="isBatchModalOpen"
        :title="batchModalTitle"
        @close="closeBatchModal"
      >
        <div class="product-form">      
          <div class="form-group">
            <label for="batchQuantity">Quantity:</label>
            <input 
              id="batchQuantity" 
              type="number" 
              v-model="batchFormData.quantity" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="expiryDate">Expiry Date:</label>
            <input 
              id="expiryDate" 
              type="date" 
              v-model="batchFormData.expiry_date" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="receivedDate">Received Date:</label>
            <input 
              id="receivedDate" 
              type="date" 
              v-model="batchFormData.received_date" 
              class="form-control"
            />
          </div>
        </div>
        
        <template v-slot:footer>
          <button class="submit-btn" @click="submitBatchForm">
            {{ isEditingBatch ? 'Update Batch' : 'Add Batch' }}
          </button>
        </template>
      </BaseModal>
      
      <!-- Sell Batch Modal -->
      <BaseModal
        :isOpen="isSellModalOpen"
        title="Sell Product"
        @close="closeSellModal"
      >
        <div class="product-form">      
          <div class="form-group">
            <label for="sellQuantity">Quantity to Sell:</label>
            <input 
              id="sellQuantity" 
              type="number" 
              v-model="sellFormData.quantity" 
              class="form-control"
              :max="sellFormData.maxQuantity"
            />
            <small class="form-text">Available: {{ sellFormData.maxQuantity }}</small>
          </div>
          
          <div class="form-group">
            <label for="sellPrice">Selling Price:</label>
            <input 
              id="sellPrice" 
              type="number" 
              step="0.01" 
              v-model="sellFormData.price" 
              class="form-control"
            />
          </div>
          
          <div class="form-group">
            <label for="sellDate">Sell Date:</label>
            <input 
              id="sellDate" 
              type="date" 
              v-model="sellFormData.sell_date" 
              class="form-control"
            />
          </div>
        </div>
        
        <template v-slot:footer>
          <button class="submit-btn" @click="submitSellForm">
            Complete Sale
          </button>
        </template>
      </BaseModal>
    </div>
  </template>
  
  <script>
  import BaseModal from '@/components/BaseModal.vue';
  import SalesModal from '@/components/SalesModal.vue';
  import api from "@/services/api";
  
  export default {
    name: 'ProductPage',
    components: {
      BaseModal,
      SalesModal
    },
    data() {
      return {
        searchQuery: '',
        isModalOpen: false,
        isBatchModalOpen: false,
        isSellModalOpen: false,
        isEditing: false,
        isEditingBatch: false,
        isSalesModalOpen: false,
        salesProduct: null,
        expandedProductId: null,
        currentProductId: null,
        currentBatchId: null,
        formData: {
          name: '',
          category: '',
          code: '',
          cost: '',
          retail_price: '',
          stock_threshold: '',
          quantity: ''
        },
        batchFormData: {
          batch_id: '',
          quantity: '',
          expiry_date: '',
          received_date: ''
        },
        sellFormData: {
          quantity: 1,
          maxQuantity: 0,
          price: '',
          sell_date: '',
          product_id: null,
          batch_id: null
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
      },
      batchModalTitle() {
        return this.isEditingBatch ? 'Edit Batch' : 'Add Batch';
      }
    },
    methods: {
      formatDate(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        return date.toLocaleDateString();
      },
      toggleExpand(product_id) {
        if (this.expandedProductId === product_id) {
          this.expandedProductId = null;
        } else {
          this.expandedProductId = product_id;
        }
      },
      resetForm() {
        this.formData = {
          name: '',
          category: '',
          code: '',
          cost: '',
          retail_price: '',
          stock_threshold: '',
          quantity: ''
        };
        this.currentProductId = null;
        this.isEditing = false;
      },
      resetBatchForm() {
        this.batchFormData = {
          batch_id: '',
          quantity: '',
          expiry_date: '',
          received_date: ''
        };
        this.currentBatchId = null;
        this.isEditingBatch = false;
      },
      resetSellForm() {
        const today = new Date();

        this.sellFormData = {
          quantity: 1,
          maxQuantity: 0,
          price: '',
          sell_date: today.toLocaleDateString('en-CA'),
          product_id: null,
          batch_id: null
        };
      },
      openAddModal() {
        this.resetForm();
        this.isModalOpen = true;
      },
      openEditModal(product) {
        this.isEditing = true;
        this.currentProductId = product.id;
        this.formData = { ...product };
        this.isModalOpen = true;
      },
      closeModal() {
        this.isModalOpen = false;
        setTimeout(this.resetForm, 300);
      },
      openAddBatchModal(product_id) {
        this.resetBatchForm();
        this.currentProductId = product_id;
        
        // Generate new batch ID
        const product = this.products.find(p => p.id === product_id);
        const batchCount = product.batches ? product.batches.length : 0;
        this.batchFormData.batch_id = `B${String(product_id).padStart(2, '0')}${String(batchCount + 1).padStart(2, '0')}`;
        
        // Set default dates
        const today = new Date();

        // Set received date to today
        this.batchFormData.received_date = today.toLocaleDateString('en-CA');
        
        // Default expiry date (6 months from today)
        const expiry_date = new Date();
        expiry_date.setMonth(expiry_date.getMonth() + 6);
        this.batchFormData.expiry_date = expiry_date.toLocaleDateString('en-CA');
        
        this.isBatchModalOpen = true;
      },
      openBatchEditModal(product_id, batch) {
        this.isEditingBatch = true;
        this.currentProductId = product_id;
        this.currentBatchId = batch.batch_id;
        this.batchFormData = { ...batch };
        this.isBatchModalOpen = true;
      },
      closeBatchModal() {
        this.isBatchModalOpen = false;
        setTimeout(this.resetBatchForm, 300);
      },
      openSellProductModal(product) {
        this.resetSellForm();
        this.salesProduct = product;
        this.isSalesModalOpen = true;
      },
      closeSalesModal() {
        this.isSalesModalOpen = false;
        this.salesProduct = null;
        this.fetchProducts(); 
      },
      closeSellModal() {
        this.isSellModalOpen = false;
        setTimeout(this.resetSellForm, 300);
      },
      async fetchProducts() {
        try {
            const response = await api.get('/api/products');
            this.products = response.data;

            this.products.forEach(product => {
                this.updateProductQuantity(product.id);
            });
        } catch (error) {
            console.error('Failed to fetch products:', error);
        }
      },
      async submitForm() {
        try {
            if (this.isEditing) {
                // Update product
                await api.put(`/api/products/${this.currentProductId}`, this.formData);
            } else {
                // Create new product
                await api.post('/api/products', this.formData);
            }
            this.closeModal();
            this.fetchProducts(); // Refresh product list
        } catch (error) {
            console.error('Failed to save product:', error);
        }
      },
      async submitBatchForm() {
        try {
            const payload = {
                product_id: this.currentProductId,
                quantity: Number(this.batchFormData.quantity), 
                expiry_date: this.batchFormData.expiry_date,
                received_date: this.batchFormData.received_date
            };
  
            if (this.isEditingBatch) {
                await api.put(`/api/products/${this.currentProductId}/batches/${this.currentBatchId}`, 
                    payload
                );
            } else {
                await api.post(`/api/products/${this.currentProductId}/batches`, 
                    payload
                );
            }
            this.closeBatchModal();
            this.fetchProducts();
        } catch (error) {
            console.error('Failed to save batch:', error);
        }
      },
      async submitSellForm() {
        try {
          const payload = {
            quantity: Number(this.sellFormData.quantity),
            price: Number(this.sellFormData.price),
            sell_date: this.sellFormData.sell_date
          };
          
          await api.post(
            `/api/products/${this.sellFormData.product_id}/batches/${this.sellFormData.batch_id}/sell`, 
            payload
          );
          
          this.closeSellModal();
          this.fetchProducts();
        } catch (error) {
          console.error('Failed to process sale:', error);
        }
      },
      async deleteProduct(product_id) {
        if (confirm('Are you sure you want to delete this product?')) {
          try {
            await api.delete(`/api/products/${product_id}`);
            this.fetchProducts();
          } catch (error) {
            console.error('Failed to delete product:', error);
          }
        }
      },
      async deleteBatch(product_id, batch_id) {
        try {
            await api.delete(`/api/products/${product_id}/batches/${batch_id}`);
            this.fetchProducts();
        } catch (error) {
            console.error('Failed to delete batch:', error);
        }
      },
      updateProductQuantity(product_id) {
        const productIndex = this.products.findIndex(p => p.id === product_id);
        
        if (productIndex === -1) return;
        
        const product = this.products[productIndex];
        
        if (!product.batches) {
          this.products[productIndex].quantity = 0;
          return;
        }
        
        // Sum up quantities from all batches
        const totalQuantity = product.batches.reduce((sum, batch) => {
            return sum + (Number(batch.quantity) || 0);
        }, 0);

        // Update the product's quantity
        this.products[productIndex].quantity = totalQuantity;
      }
    },
  };
  </script>
  
  <style scoped>
  .product-container {
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
  
  .product-actions {
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
  
  .expand-cell .chevron-down {
    margin-left: 0px;
  }
  
  .chevron-up {
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23718096'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 15l7-7 7 7' /%3E%3C/svg%3E");
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
  
  .expand-cell {
    width: 50px;
    text-align: center;
  }
  
  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 8px;
  }
  
  .edit-btn, .expand-btn, .delete-btn {
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
  
  .edit-btn:hover, .expand-btn:hover {
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
  
  .sell-icon {
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z' /%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
  }
  
  .chevron-icon {
    width: 16px;
    height: 16px;
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
    float: right;
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
  
  .form-text {
    display: block;
    margin-top: 4px;
    font-size: 12px;
    color: #718096;
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
  
  /* Expanded row styles */
  tr.expanded {
    background-color: #ebf4ff;
  }

  tr.batch-header td {
  padding: 0;
  border-bottom: none;
}

.batch-container {
  padding: 0 16px 16px 16px;
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.batch-header-row {
  display: flex;
  background-color: #edf2f7;
  border-radius: 4px 4px 0 0;
  padding: 10px 16px;
  font-weight: 500;
  font-size: 13px;
  color: #4a5568;
}

.batch-row {
  display: flex;
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.batch-row:last-child {
  border-bottom: none;
}

.batch-column {
  flex: 1;
}

.batch-id {
  flex: 0.5;
}

.batch-quantity {
  flex: 0.5;
}

.batch-expiry {
  flex: 1;
}

.batch-received {
  flex: 1;
}

.batch-actions {
  flex: 1;
  display: flex;
  justify-content: flex-start;
  gap: 8px;
}

.batch-edit-btn, .batch-delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background-color: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  cursor: pointer;
}

.batch-edit-btn:hover {
  background-color: #edf2f7;
}

.batch-delete-btn:hover {
  background-color: #fed7d7;
}

.add-batch-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.add-batch-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.add-batch-btn:hover {
  background-color: #3182ce;
}

.no-batches {
  padding: 16px;
  text-align: center;
  color: #718096;
  font-style: italic;
}

.sell-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: #38a169;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.sell-btn:hover {
  background-color: #2f855a;
}
</style>