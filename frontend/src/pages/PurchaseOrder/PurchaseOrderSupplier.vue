<template>
  <div class="purchase-order-container">
    <h1>Purchase Order</h1>
    
    <div class="order-actions">
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
    
    <div class="order-table">
      <table>
        <thead>
          <tr>
            <th>No.</th>
            <th>Order Date</th>
            <th>Description</th>
            <th>Total Cost</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(order, index) in filteredOrders" 
            :key="order.id"
            @click="viewOrderDetails(order)"
            class="order-row"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ formatDate(order.order_date) }}</td>
            <td>{{ order.description }}</td>
            <td>{{ formatCurrency(order.total_cost) }}</td>
            <td>
              <span 
                class="status-badge" 
                :class="{ 
                  'status-delivered': order.status === 'Delivered',
                  'status-delivering': order.status === 'Delivering',
                  'status-processing': order.status === 'Processing',
                  'status-pending': order.status === 'Pending'
                }"
              >
                {{ order.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <BaseModal
      :isOpen="isModalOpen"
      title="Purchase Order Details"
      @close="closeModal"
    >
      <div v-if="selectedOrder" class="order-details">
        <div class="detail-header">
          <div class="order-number">
            Order #{{ selectedOrder.id }}
          </div>
          <div class="order-date">
            <strong>Date:</strong> {{ formatDate(selectedOrder.order_date) }}
          </div>
        </div>
        
        <div class="detail-section">
          <h3>Order Description</h3>
          <p>{{ selectedOrder.description }}</p>
        </div>
        
        <div class="detail-section">
          <h3>Products</h3>
          <div class="products-table">
            <div class="products-header">
              <div class="product-header-name">Product</div>
              <div class="product-header-quantity">Quantity</div>
              <div class="product-header-cost">Unit Cost</div>
              <div class="product-header-total">Total</div>
            </div>
            
            <div v-for="(item, index) in orderItems" :key="index" class="product-row">
              <div class="product-name">{{ item.product_name }}</div>
              <div class="product-quantity">{{ item.quantity }}</div>
              <div class="product-cost">{{ formatCurrency(item.unit_cost) }}</div>
              <div class="product-total">{{ formatCurrency(item.subtotal) }}</div>
            </div>
          </div>
          
          <div class="order-total">
            <div class="total-label">Total Cost:</div>
            <div class="total-value">{{ formatCurrency(selectedOrder.total_cost) }}</div>
          </div>
        </div>
        
        <div class="detail-section status-section">
          <h3>Status</h3>
          <div class="status-info">
            <div class="current-status">
              <span>Current Status:</span>
              <span 
                class="status-badge" 
                :class="{ 
                  'status-delivered': selectedOrder.status === 'Delivered',
                  'status-delivering': selectedOrder.status === 'Delivering',
                  'status-processing': selectedOrder.status === 'Processing',
                  'status-pending': selectedOrder.status === 'Pending'
                }"
              >
                {{ selectedOrder.status }}
              </span>
            </div>
            
            <div v-if="selectedOrder.status === 'Pending'" class="status-update">
              <button 
                class="update-status-btn" 
                @click="updateOrderStatus(selectedOrder.id, 'Processing')"
              >
                Mark as Processing
              </button>
            </div>
            
            <div v-else-if="selectedOrder.status === 'Processing'" class="status-update">
              <button 
                class="update-status-btn" 
                @click="updateOrderStatus(selectedOrder.id, 'Delivering')"
              >
                Mark as Delivering
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <template v-slot:footer>
        <button class="close-btn" @click="closeModal">
          Close
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import BaseModal from "@/components/BaseModal.vue";
import api from "@/services/api";

export default {
  name: 'PurchaseOrderSupplier',
  components: {
    BaseModal
  },
  data() {
    return {
      searchQuery: '',
      orders: [],
      isModalOpen: false,
      selectedOrder: null,
      orderItems: []
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
               order.description.toLowerCase().includes(query) ||
               order.status.toLowerCase().includes(query);
      });
    }
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      try {
        const response = await api.get(`/api/purchase-orders/supplier`);
        this.orders = response.data;
      } catch (error) {
        console.error('Failed to fetch orders:', error);
      }
    },
    formatDate(dateString) {
      if (!dateString) return "";

      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    formatCurrency(amount) {
      return `RM ${parseFloat(amount).toFixed(2)}`;
    },
    async viewOrderDetails(order) {
      this.selectedOrder = order;
      try {
        const response = await api.get(`/api/purchase-orders/${order.id}`);
        const orderData = response.data;
        this.orderItems = orderData.items || [];
        this.isModalOpen = true;
      } catch (error) {
        console.error('Failed to fetch order details:', error);
      }
    },
    closeModal() {
      this.isModalOpen = false;
      this.selectedOrder = null;
      this.orderItems = [];
    },
    async updateOrderStatus(orderId, newStatus) {
      try {
        await api.patch(`/api/purchase-orders/${orderId}/status`, {
          status: newStatus
        });
        
        // Update local state
        if (this.selectedOrder) {
          this.selectedOrder.status = newStatus;
        }
        
        // Update in orders list
        const orderIndex = this.orders.findIndex(order => order.id === orderId);
        if (orderIndex !== -1) {
          this.orders[orderIndex].status = newStatus;
        }
        
      } catch (error) {
        console.error('Failed to update order status:', error);
      }
    }
  }
};
</script>

<style scoped>
.purchase-order-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #4a5568;
  margin-top: 0;
  margin-bottom: 24px;
  font-weight: 500;
  font-size: 24px;
}

.order-actions {
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

.order-table {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 16px;
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

.order-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.order-row:hover {
  background-color: #f7fafc;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-delivered {
  background-color: #e6fffa;
  color: #047857;
}

.status-delivering {
  background-color: #fcf3fe;
  color: #9333ea;
}

.status-processing {
  background-color: #eff6ff;
  color: #1d4ed8;
}

.status-pending {
  background-color: #fff7ed;
  color: #c2410c;
}

.order-details {
  padding: 8px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 20px;
}

.order-number {
  font-size: 18px;
  font-weight: 500;
  color: #2d3748;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  font-size: 16px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 12px;
}

.products-table {
  margin-bottom: 16px;
}

.products-header {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid #e2e8f0;
  font-weight: 500;
  font-size: 14px;
  color: #4a5568;
}

.product-row {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #edf2f7;
}

.product-header-name, .product-name {
  flex: 3;
}

.product-header-quantity, .product-quantity,
.product-header-cost, .product-cost,
.product-header-total, .product-total {
  flex: 1;
  text-align: right;
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

.status-section {
  padding: 16px;
  background-color: #f7fafc;
  border-radius: 6px;
}

.status-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.current-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.update-status-btn {
  padding: 8px 16px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.update-status-btn:hover {
  background-color: #0052a3;
}

.close-btn {
  padding: 10px 24px;
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #cbd5e0;
}
</style>