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
                :class="statusClass(order.status)"
              >
                {{ order.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="update-bank-btn" @click="isBankModalOpen = true">
      <i class="bank-icon"></i>
      Update Bank Info
    </button>

    <BaseModal
      :isOpen="isBankModalOpen"
      title="Update Bank Info"
      @close="isBankModalOpen = false"
    >
      <div class="bank-form">
        <div class="form-group">
          <label for="bankName">Bank Name:</label>
          <input id="bankName" v-model="bankForm.bank_name" class="form-control" />
        </div>
        <div class="form-group">
          <label for="accountNumber">Account Number:</label>
          <input id="accountNumber" v-model="bankForm.account_number" class="form-control" />
        </div>
        <div class="form-group">
          <label for="accountHolder">Account Holder:</label>
          <input id="accountHolder" v-model="bankForm.account_holder" class="form-control" />
        </div>
      </div>
      <template v-slot:footer>
        <button class="cancel-btn" @click="isBankModalOpen = false">Cancel</button>
        <button class="submit-btn" @click="submitBankInfo">Save</button>
      </template>
    </BaseModal>
    
    <BaseModal
      :isOpen="isDetailModalOpen"
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
                :class="statusClass(selectedOrder.status)"
              >
                {{ selectedOrder.status }}
              </span>
            </div>
            
            <div v-if="selectedOrder.status === 'Pending'" class="status-update">
              <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Accepted')">
                Accept Order
              </button>
              <button class="decline-btn" @click="showDecline = true">
                Decline Order
              </button>
              <div v-if="showDecline" class="decline-reason-box">
                <textarea v-model="declineMessage" placeholder="Enter reason for declining"></textarea>
                <div class="decline-actions">
                  <button class="decline-btn" @click="declineOrder(selectedOrder.id)">Submit Decline</button>
                  <button class="cancel-btn" @click="cancelDecline">Cancel</button>
                </div>
              </div>
            </div>
            <div v-else-if="selectedOrder.status === 'Paid'" class="status-update">
              <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Processing')">
                Mark as Processing
              </button>
              <div v-if="selectedOrder.payment_receipt_url" class="receipt-section" style="margin-top: 16px;">
                <label><strong>Payment Receipt:</strong></label>
                <a
                  :href="receiptUrl(selectedOrder.payment_receipt_url)"
                  target="_blank"
                  rel="noopener"
                  class="receipt-link"
                >
                  View Receipt
                </a>
              </div>
              <div v-else class="receipt-section" style="margin-top: 16px;">
                <em>No payment receipt uploaded yet.</em>
              </div>
            </div>
            <div v-else-if="selectedOrder.status === 'Processing'" class="status-update">
              <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Delivering')">
                Mark as Delivering
              </button>
            </div>
          </div>
          <div class="status-history">
            <h4>Status History</h4>
            <ul>
              <li v-for="entry in selectedOrder.status_history" :key="entry.updated_at">
                <strong>{{ entry.status }}</strong> at {{ formatDateTime(entry.updated_at) }}
                <span v-if="entry.message"> — {{ entry.message }}</span>
              </li>
            </ul>
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
      isDetailModalOpen: false, 
      selectedOrder: null,
      orderItems: [],
      showDecline: false,
      declineMessage: "",
      isBankModalOpen: false,
      bankAccountId: null,
      bankForm: {
        bank_name: "",
        account_number: "",
        account_holder: ""
      },
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
    this.fetchBankInfo();
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
    formatDateTime(dt) {
      return new Date(dt).toLocaleString();
    },
    formatCurrency(amount) {
      return `RM ${parseFloat(amount).toFixed(2)}`;
    },
    async viewOrderDetails(order) {
      this.selectedOrder = order;
      this.showDecline = false;
      this.declineMessage = "";
      try {
        const response = await api.get(`/api/purchase-orders/${order.id}`);
        const orderData = response.data;
        this.orderItems = orderData.items || [];
        // Merge status history and other details
        this.selectedOrder.status_history = orderData.status_history || [];
        this.selectedOrder.status = orderData.status;
        this.selectedOrder.total_cost = orderData.total_cost;
        this.selectedOrder.description = orderData.description;
        this.selectedOrder.order_date = orderData.order_date;
        this.isDetailModalOpen = true;
      } catch (error) {
        console.error('Failed to fetch order details:', error);
      }
    },
    closeModal() {
      this.isDetailModalOpen = false;
      this.selectedOrder = null;
      this.orderItems = [];
      this.showDecline = false;
      this.declineMessage = "";
    },
    async updateOrderStatus(orderId, newStatus) {
      try {
        await api.patch(`/api/purchase-orders/${orderId}/status`, {
          status: newStatus
        });
        await this.viewOrderDetails({ id: orderId });
        await this.fetchOrders();
      } catch (error) {
        console.error('Failed to update order status:', error);
      }
    },
    async declineOrder(orderId) {
      if (!this.declineMessage.trim()) {
        alert("Please enter a reason for declining.");
        return;
      }
      try {
        await api.patch(`/api/purchase-orders/${orderId}/status`, {
          status: "Declined",
          message: this.declineMessage
        });
        this.showDecline = false;
        this.declineMessage = "";
        await this.viewOrderDetails({ id: orderId });
        await this.fetchOrders();
      } catch (error) {
        console.error('Failed to decline order:', error);
      }
    },
    cancelDecline() {
      this.showDecline = false;
      this.declineMessage = "";
    },
    statusClass(status) {
      return {
        'status-delivered': status === 'Delivered',
        'status-delivering': status === 'Delivering',
        'status-processing': status === 'Processing',
        'status-paid': status === 'Paid',
        'status-accepted': status === 'Accepted',
        'status-declined': status === 'Declined',
        'status-pending': status === 'Pending'
      };
    },
    async fetchBankInfo() {
      try {
        const res = await api.get("/api/supplier-bank-accounts/by-supplier");
        if (res.data.length > 0) {
          const bank = res.data[0];
          this.bankForm = {
            bank_name: bank.bank_name,
            account_number: bank.account_number,
            account_holder: bank.account_holder
          };
          this.bankAccountId = bank.id;
        }
      } catch (e) {
        // No bank info yet
        this.bankAccountId = null;
      }
    },
    async submitBankInfo() {
      try {
        if (this.bankAccountId) {
          // Update existing
          await api.delete(`/api/supplier-bank-accounts/${this.bankAccountId}`);
        }
        await api.post("/api/supplier-bank-accounts/", {
          ...this.bankForm,
          supplier_id: null 
        });
        this.isBankModalOpen = false;
        this.fetchBankInfo();
      } catch (e) {
        alert("Failed to update bank info.");
      }
    },
    receiptUrl(path) {
      // If your backend serves static files from /uploads, adjust as needed
      if (!path) return "#";
      if (path.startsWith("http")) return path;
      return `${process.env.VUE_APP_API_BASE_URL || ""}/${path.replace(/^\/+/, "")}`;
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
  background-color: #edf7fd;
  color: #0ea5e9;
}

.status-paid {
  background-color: #f0f4ff;
  color: #2563eb;
}

.status-processing {
  background-color: #eff6ff;
  color: #1d4ed8;
}

.status-accepted {
  background-color: #e0f2fe;
  color: #0284c7;
}

.status-declined {
  background-color: #fee2e2;
  color: #b91c1c;
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

.product-header-name, .product-name { flex: 2; }
.product-header-quantity, .product-quantity { flex: 1; text-align: center; }
.product-header-cost, .product-cost { flex: 1; text-align: right; }
.product-header-total, .product-total { flex: 1; text-align: right; }

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

.status-history h4 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
}

.status-history ul {
  padding-left: 18px;
}

.status-history li {
  font-size: 13px;
  margin-bottom: 4px;
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

.accept-btn {
  padding: 8px 16px;
  background-color: #059669;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-right: 8px;
  transition: background-color 0.2s;
}

.accept-btn:hover {
  background-color: #047857;
}

.decline-btn {
  padding: 8px 16px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-right: 8px;
  transition: background-color 0.2s;
}
.decline-btn:hover {
  background-color: #b91c1c;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.cancel-btn:hover {
  background-color: #cbd5e0;
}

.decline-reason-box {
  margin-top: 12px;
}
.decline-reason-box textarea {
  width: 100%;
  min-height: 60px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 8px;
  font-size: 14px;
  margin-bottom: 8px;
  resize: vertical;
}

.decline-actions {
  display: flex;
  gap: 8px;
}

.update-bank-btn {
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
  margin-top: 20px;
  transition: background-color 0.2s;
}
.update-bank-btn:hover {
  background-color: #0052a3;
}
.bank-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 10l9-7 9 7v7a2 2 0 01-2 2H5a2 2 0 01-2-2v-7z' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}
.bank-form {
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
.receipt-link {
  color: #2563eb;
  text-decoration: underline;
  margin-left: 8px;
}
.receipt-link:hover {
  color: #1d4ed8;
}

</style>