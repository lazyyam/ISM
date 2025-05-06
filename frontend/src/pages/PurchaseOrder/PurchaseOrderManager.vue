<template>
  <div class="purchase-order-container">
    <h1>Purchase Order</h1>
    
    <div class="purchase-order-actions">
      <div class="search-bar">
        <i class="search-icon"></i>
        <input 
          type="text" 
          placeholder="Search order ID" 
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
    
    <div class="purchase-order-table">
      <table>
        <thead>
          <tr>
            <th class="action-cell">Action</th>
            <th>No.</th>
            <th>Order Date</th>
            <th>Supplier</th>
            <th>Company</th>
            <th>Description</th>
            <th>Total Cost</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(order, index) in filteredOrders" :key="order.id">
            <td class="action-cell">
              <button 
                class="edit-btn" 
                @click="editOrder(order)"
                title="Edit order"
              >
                <i class="edit-icon"></i>
              </button>
            </td>
            <td>{{ index + 1 }}</td>
            <td>{{ formatDate(order.orderDate) }}</td>
            <td>{{ order.supplier }}</td>
            <td>{{ order.company }}</td>
            <td>{{ order.description }}</td>
            <td>{{ formatCurrency(order.totalCost) }}</td>
            <td>
              <span :class="getStatusClass(order.status)">{{ order.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <button class="add-purchase-btn" @click="openAddModal">
      <i class="plus-icon"></i>
      Add Purchase
    </button>
    
    <!-- Purchase Order Modal -->
    <BaseModal
      :isOpen="isModalOpen"
      :title="modalTitle"
      @close="closeModal"
    >
      <div class="purchase-form">
        <div class="form-group">
          <label for="orderDate">Order Date:</label>
          <input 
            id="orderDate" 
            type="date" 
            v-model="formData.orderDate" 
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="supplier">Supplier:</label>
          <select 
            id="supplier" 
            v-model="formData.supplierId" 
            class="form-control"
            @change="supplierChanged"
          >
            <option value="">Select Supplier</option>
            <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
              {{ supplier.name }} ({{ supplier.company }})
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Description:</label>
          <input 
            type="text" 
            v-model="formData.description" 
            class="form-control"
            placeholder="Brief description of order"
          />
        </div>
        
        <div class="form-divider">Products</div>
        
        <div v-if="formData.supplierId" class="product-selection">
          <div class="products-header">
            <div class="product-header-name">Product</div>
            <div class="product-header-quantity">Quantity</div>
            <div class="product-header-cost">Cost</div>
            <div class="product-header-action"></div>
          </div>
          
          <div v-for="(item, index) in formData.orderItems" :key="index" class="product-row">
            <div class="product-name">
              <select 
                v-model="item.productId" 
                class="form-control"
                @change="productChanged(index)"
              >
                <option value="">Select Product</option>
                <option 
                  v-for="product in supplierProducts" 
                  :key="product.id" 
                  :value="product.id"
                >
                  {{ product.name }} ({{ formatCurrency(product.cost) }})
                </option>
              </select>
            </div>
            <div class="product-quantity">
              <input 
                type="number" 
                min="1" 
                v-model.number="item.quantity" 
                class="form-control"
                @input="updateItemTotal(index)"
              />
            </div>
            <div class="product-cost">
              {{ formatCurrency(item.total) }}
            </div>
            <div class="product-action">
              <button 
                v-if="formData.orderItems.length > 1" 
                class="remove-item-btn"
                @click="removeOrderItem(index)"
                title="Remove item"
              >
                <i class="delete-icon"></i>
              </button>
            </div>
          </div>
          
          <div class="add-product-row">
            <button class="add-item-btn" @click="addOrderItem">
              <i class="plus-icon"></i>
              Add Product
            </button>
          </div>
          
          <div class="order-total">
            <div class="total-label">Total Cost:</div>
            <div class="total-value">{{ formatCurrency(calculateTotalCost()) }}</div>
          </div>
        </div>
        
        <!-- Status field only shown when editing an existing order -->
        <div v-if="formData.supplierId && isEditing" class="form-group">
          <label for="status">Status:</label>
          <select 
            id="status" 
            v-model="formData.status" 
            class="form-control"
          >
            <option value="Pending">Pending</option>
            <option value="Processing">Processing</option>
            <option value="Delivered">Delivered</option>
          </select>
        </div>
        
        <!-- Show status info text when adding a new order -->
        <div v-if="formData.supplierId && !isEditing" class="status-info">
          <p>New orders will be created with status: <span class="status-pending">Pending</span></p>
        </div>
      </div>
      
      <template v-slot:footer>
        <button 
          class="submit-btn" 
          @click="submitForm"
          :disabled="!isFormValid"
        >
          {{ isEditing ? 'Update Order' : 'Create Order' }}
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import BaseModal from "@/components/BaseModal.vue";

export default {
  name: 'PurchaseOrderManager',
  components: {
    BaseModal
  },
  data() {
    return {
      searchQuery: '',
      isModalOpen: false,
      isEditing: false,
      currentOrderId: null,
      orders: [
        {
          id: 1,
          orderDate: '2024-05-06',
          supplier: 'Chong',
          company: 'Chong\'s Trading',
          description: 'Canned Foods',
          totalCost: 300.00,
          status: 'Delivered'
        },
        {
          id: 2,
          orderDate: '2024-05-15',
          supplier: 'Ali',
          company: 'Ali Enterprise Sdn. Bhd.',
          description: 'Bread and drinks',
          totalCost: 220.00,
          status: 'Delivered'
        },
        {
          id: 3,
          orderDate: '2024-06-15',
          supplier: 'Chong',
          company: 'Chong\'s Trading',
          description: 'Canned Foods',
          totalCost: 300.00,
          status: 'Processing'
        },
        {
          id: 4,
          orderDate: '2024-06-18',
          supplier: 'Chong',
          company: 'Chong\'s Trading',
          description: 'Canned Foods',
          totalCost: 300.00,
          status: 'Pending'
        }
      ],
      suppliers: [
        { id: 1, name: 'Chong', company: 'Chong\'s Trading' },
        { id: 2, name: 'Ali', company: 'Ali Enterprise Sdn. Bhd.' },
        { id: 3, name: 'Kumar', company: 'Kumar Wholesales' }
      ],
      products: [
        { id: 1, name: 'Canned Tuna', supplierId: 1, cost: 5.50 },
        { id: 2, name: 'Canned Corn', supplierId: 1, cost: 4.20 },
        { id: 3, name: 'Canned Beans', supplierId: 1, cost: 3.80 },
        { id: 4, name: 'White Bread', supplierId: 2, cost: 3.00 },
        { id: 5, name: 'Whole Wheat Bread', supplierId: 2, cost: 4.50 },
        { id: 6, name: 'Soda', supplierId: 2, cost: 1.50 },
        { id: 7, name: 'Rice', supplierId: 3, cost: 25.00 },
        { id: 8, name: 'Flour', supplierId: 3, cost: 12.50 }
      ],
      formData: {
        orderDate: '',
        supplierId: '',
        description: '',
        status: 'Pending', // Default status is always Pending
        orderItems: [
          { productId: '', quantity: 1, cost: 0, total: 0 }
        ]
      },
      supplierProducts: []
    };
  },
  computed: {
    filteredOrders() {
      if (!this.searchQuery) {
        return this.orders;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.orders.filter(order => {
        return order.id.toString().includes(query) ||
               order.supplier.toLowerCase().includes(query) ||
               order.company.toLowerCase().includes(query) ||
               order.description.toLowerCase().includes(query) ||
               order.status.toLowerCase().includes(query);
      });
    },
    modalTitle() {
      return this.isEditing ? 'Edit Purchase Order' : 'Add Purchase Order';
    },
    isFormValid() {
      if (!this.formData.orderDate || !this.formData.supplierId || !this.formData.description) {
        return false;
      }
      
      // Check if at least one item is selected and has quantity
      return this.formData.orderItems.some(item => item.productId && item.quantity > 0);
    }
  },
  mounted() {
    // You can fetch real data from your API here
    // this.fetchOrders();
    // this.fetchSuppliers();
    // this.fetchProducts();
    
    // Set current date as default for new orders
    const today = new Date();
    this.formData.orderDate = today.toISOString().split('T')[0];
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    formatCurrency(amount) {
      return `RM ${parseFloat(amount).toFixed(2)}`;
    },
    openAddModal() {
      this.isEditing = false;
      this.currentOrderId = null;
      this.resetForm();
      this.isModalOpen = true;
    },
    editOrder(order) {
      this.isEditing = true;
      this.currentOrderId = order.id;
      
      // Find the supplier id based on supplier name
      const supplier = this.suppliers.find(s => s.name === order.supplier);
      const supplierId = supplier ? supplier.id : '';
      
      // Reset the form and then set values
      this.resetForm();
      
      this.formData = {
        orderDate: order.orderDate,
        supplierId: supplierId,
        description: order.description,
        status: order.status, // Keep the existing status for edits
        orderItems: []
      };
      
      // Here you would typically fetch order items from API
      // For demo purposes, adding a dummy item
      this.formData.orderItems = [
        { productId: '', quantity: 1, cost: 0, total: 0 }
      ];
      
      if (supplierId) {
        this.supplierChanged();
      }
      
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    resetForm() {
      const today = new Date();
      this.formData = {
        orderDate: today.toISOString().split('T')[0],
        supplierId: '',
        description: '',
        status: 'Pending', // Always default to Pending
        orderItems: [
          { productId: '', quantity: 1, cost: 0, total: 0 }
        ]
      };
      this.supplierProducts = [];
    },
    supplierChanged() {
      // Filter products by selected supplier
      if (this.formData.supplierId) {
        this.supplierProducts = this.products.filter(
          p => p.supplierId === this.formData.supplierId
        );
        
        // Reset order items when supplier changes
        this.formData.orderItems = [
          { productId: '', quantity: 1, cost: 0, total: 0 }
        ];
      } else {
        this.supplierProducts = [];
      }
    },
    productChanged(index) {
      const item = this.formData.orderItems[index];
      if (item.productId) {
        const product = this.products.find(p => p.id === item.productId);
        if (product) {
          item.cost = product.cost;
          this.updateItemTotal(index);
        }
      } else {
        item.cost = 0;
        item.total = 0;
      }
    },
    updateItemTotal(index) {
      const item = this.formData.orderItems[index];
      item.total = item.quantity * item.cost;
    },
    addOrderItem() {
      this.formData.orderItems.push({ 
        productId: '', 
        quantity: 1, 
        cost: 0, 
        total: 0 
      });
    },
    removeOrderItem(index) {
      if (this.formData.orderItems.length > 1) {
        this.formData.orderItems.splice(index, 1);
      }
    },
    calculateTotalCost() {
      return this.formData.orderItems.reduce((total, item) => {
        return total + (item.total || 0);
      }, 0);
    },
    getStatusClass(status) {
      switch(status.toLowerCase()) {
        case 'delivered':
          return 'status-delivered';
        case 'processing':
          return 'status-processing';
        case 'pending':
          return 'status-pending';
        default:
          return '';
      }
    },
    async submitForm() {
      if (!this.isFormValid) return;
      
      try {
        // Find supplier information
        const supplier = this.suppliers.find(s => s.id === this.formData.supplierId);
        
        const orderData = {
          orderDate: this.formData.orderDate,
          supplier: supplier ? supplier.name : '',
          company: supplier ? supplier.company : '',
          description: this.formData.description,
          totalCost: this.calculateTotalCost(),
          status: this.formData.status, // For new orders, this will always be 'Pending'
          items: this.formData.orderItems.map(item => {
            const product = this.products.find(p => p.id === item.productId);
            return {
              productId: item.productId,
              productName: product ? product.name : '',
              quantity: item.quantity,
              cost: item.cost,
              total: item.total
            };
          })
        };
        
        if (this.isEditing) {
          // Update existing order
          // await api.put(`/api/purchase-orders/${this.currentOrderId}`, orderData);
          
          // For demo purposes, update local order
          const index = this.orders.findIndex(o => o.id === this.currentOrderId);
          if (index !== -1) {
            this.orders[index] = {
              ...this.orders[index],
              ...orderData
            };
          }
        } else {
          // Create new order (status will always be 'Pending')
          // const response = await api.post('/api/purchase-orders', orderData);
          
          // For demo purposes, add to local orders
          const newOrder = {
            id: this.orders.length + 1,
            ...orderData
          };
          this.orders.push(newOrder);
        }
        
        this.closeModal();
      } catch (error) {
        console.error('Failed to save purchase order:', error);
      }
    }
  }
};
</script>

<style scoped>
.purchase-order-container {
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

.purchase-order-actions {
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

.purchase-order-table {
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
  width: 60px;
  text-align: center;
}

.edit-btn {
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

.add-purchase-btn {
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

.add-purchase-btn:hover {
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

.status-delivered {
  color: #2f855a;
}

.status-processing {
  color: #dd6b20;
}

.status-pending {
  color: #3182ce;
}

/* Form Styles */
.purchase-form {
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

.form-divider {
  font-weight: 500;
  color: #4a5568;
  margin: 20px 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.product-selection {
  margin-bottom: 20px;
}

.products-header {
  display: flex;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 14px;
  color: #4a5568;
}

.product-row {
  display: flex;
  margin-bottom: 8px;
}

.product-header-name, .product-name {
  flex: 3;
  padding-right: 8px;
}

.product-header-quantity, .product-quantity {
  flex: 1;
  padding-right: 8px;
}

.product-header-cost, .product-cost {
  flex: 1;
  padding-right: 8px;
}

.product-header-action, .product-action {
  width: 40px;
  display: flex;
  justify-content: center;
}

.add-product-row {
  margin-top: 12px;
}

.add-item-btn {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: #edf2f7;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 13px;
  color: #4a5568;
  cursor: pointer;
}

.add-item-btn:hover {
  background-color: #e2e8f0;
}

.remove-item-btn {
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

.remove-item-btn:hover {
  background-color: #fed7d7;
}

.order-total {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.total-label {
  font-weight: 500;
  margin-right: 16px;
}

.total-value {
  font-weight: 500;
  font-size: 18px;
  color: #4a5568;
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

.submit-btn:hover:not(:disabled) {
  background-color: #0052a3;
}

.submit-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

/* New status info styling */
.status-info {
  margin-top: 16px;
  padding: 10px;
  background-color: #f7fafc;
  border-radius: 4px;
  border-left: 4px solid #3182ce;
}

.status-info p {
  margin: 0;
  font-size: 14px;
  color: #4a5568;
}
</style>