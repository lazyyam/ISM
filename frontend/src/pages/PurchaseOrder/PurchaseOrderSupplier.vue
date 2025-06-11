<template>
  <div class="purchase-order-container">
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

    <h1>Purchase Order</h1>
    
    <div class="order-actions">
      <div class="search-bar">
        <i class="search-icon"></i>
        <input 
          type="text" 
          placeholder="Search Order" 
          v-model="searchQuery"
        />
      </div>
      <div class="filter-dropdown">
        <select v-model="selectedStatus" class="filter-select">
          <option value="">All Statuses</option>
          <option v-for="status in statusOptions" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="ordersError" class="error-message">{{ ordersError }}</div>
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
          <tr v-if="filteredOrders.length === 0 && !ordersError">
            <td colspan="5" style="text-align:center;">No orders found.</td>
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
          <input id="bankName" v-model="bankForm.bank_name" class="form-control" @input="clearBankFieldError('bank_name')" />
          <p v-if="bankNameError" class="field-error">{{ bankNameError }}</p>
        </div>
        <div class="form-group">
          <label for="accountNumber">Account Number:</label>
          <input id="accountNumber" v-model="bankForm.account_number" class="form-control" @input="clearBankFieldError('account_number')" />
          <p v-if="accountNumberError" class="field-error">{{ accountNumberError }}</p>
        </div>
        <div class="form-group">
          <label for="accountHolder">Account Holder:</label>
          <input id="accountHolder" v-model="bankForm.account_holder" class="form-control" @input="clearBankFieldError('account_holder')" />
          <p v-if="accountHolderError" class="field-error">{{ accountHolderError }}</p>
        </div>
        <div v-if="bankError" class="error-message">{{ bankError }}</div>
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
              <div class="button-group">
                <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Accepted')">
                  Accept Order
                </button>
                <button class="decline-btn" @click="showDecline = true">
                  Decline Order
                </button>
              </div>
              <div v-if="showDecline" class="decline-reason-box">
                <textarea v-model="declineMessage" placeholder="Enter reason for declining"></textarea>
                <div class="decline-actions">
                  <button class="decline-btn" @click="declineOrder(selectedOrder.id)">Submit Decline</button>
                  <button class="cancel-btn" @click="cancelDecline">Cancel</button>
                </div>
                <p v-if="declineError" class="field-error">{{ declineError }}</p>
              </div>
            </div>
            <div v-else-if="selectedOrder.status === 'Paid'" class="status-update">
              <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Processing')">
                Mark as Processing
              </button>
            </div>
            <div v-else-if="selectedOrder.status === 'Processing'" class="status-update">
              <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Delivering')">
                Mark as Delivering
              </button>
            </div>                            
          </div>
          <div v-if="['Paid', 'Processing', 'Delivering', 'Delivered'].includes(selectedOrder.status)" class="receipt-section" style="margin-top: 16px;">
            <label><strong>Payment Receipt:</strong></label>
            <a
              :href="receiptUrl(selectedOrder.payment_receipt_url)"
              target="_blank"
              rel="noopener"
              class="receipt-link"
              v-if="selectedOrder.payment_receipt_url"
            >
              View Receipt
            </a>
            <em v-else>No payment receipt uploaded yet.</em>
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
        <div class="invoice-section" v-if="showInvoiceButton(selectedOrder)">
          <button class="invoice-btn" @click="downloadInvoice(selectedOrder)">
            <i class="invoice-icon"></i>
            Download Invoice
          </button>
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
import SuccessToast from "@/components/SuccessToast.vue";
import ErrorToast from "@/components/ErrorToast.vue";
import api from "@/services/api";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default {
  name: 'PurchaseOrderSupplier',
  components: {
    BaseModal,
    SuccessToast,
    ErrorToast
  },
  data() {
    return {
      searchQuery: '',
      selectedStatus: '',
      statusOptions: [
        "Pending", "Accepted", "Paid", "Processing", "Delivering", "Delivered", "Declined"
      ],
      orders: [],
      ordersError: "",
      isDetailModalOpen: false, 
      selectedOrder: null,
      orderItems: [],
      showDecline: false,
      declineMessage: "",
      declineError: "",
      isBankModalOpen: false,
      bankAccountId: null,
      bankForm: {
        bank_name: "",
        account_number: "",
        account_holder: ""
      },
      bankNameError: "",
      accountNumberError: "",
      accountHolderError: "",
      bankError: "",
      showSuccessToast: false,
      showErrorToast: false,
      toastMessage: ""
    };
  },
  computed: {
    filteredOrders() {
      let filtered = this.orders;
      if (this.selectedStatus) {
        filtered = filtered.filter(order => order.status === this.selectedStatus);
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(order => {
          return order.id.toString().includes(query) ||
                 order.description.toLowerCase().includes(query) ||
                 order.status.toLowerCase().includes(query);
        });
      }
      return filtered;
    }
  },
  mounted() {
    this.fetchOrders();
    this.fetchBankInfo();
  },
  methods: {
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
    async fetchOrders() {
      this.ordersError = "";
      try {
        const response = await api.get(`/api/purchase-orders/supplier`);
        this.orders = response.data;
      } catch (error) {
        this.orders = [];
        this.ordersError = "Failed to fetch orders.";
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
      this.declineError = "";
      try {
        const response = await api.get(`/api/purchase-orders/${order.id}`);
        const orderData = response.data;
        this.orderItems = orderData.items || [];
        this.selectedOrder.status_history = orderData.status_history || [];
        this.selectedOrder.status = orderData.status;
        this.selectedOrder.total_cost = orderData.total_cost;
        this.selectedOrder.description = orderData.description;
        this.selectedOrder.order_date = orderData.order_date;
        this.isDetailModalOpen = true;
      } catch (error) {
        this.showToast("Failed to fetch order details.", "error");
      }
    },
    closeModal() {
      this.isDetailModalOpen = false;
      this.selectedOrder = null;
      this.orderItems = [];
      this.showDecline = false;
      this.declineMessage = "";
      this.declineError = "";
    },
    async updateOrderStatus(orderId, newStatus) {
      try {
        await api.patch(`/api/purchase-orders/${orderId}/status`, {
          status: newStatus
        });
        await this.viewOrderDetails({ id: orderId });
        await this.fetchOrders();
        this.showToast("Order status updated!", "success");
      } catch (error) {
        this.showToast("Failed to update order status.", "error");
      }
    },
    async declineOrder(orderId) {
      this.declineError = "";
      if (!this.declineMessage.trim()) {
        this.declineError = "Please enter a reason for declining.";
        return;
      }
      try {
        await api.patch(`/api/purchase-orders/${orderId}/status`, {
          status: "Declined",
          message: this.declineMessage
        });
        this.showDecline = false;
        this.declineMessage = "";
        this.declineError = "";
        await this.viewOrderDetails({ id: orderId });
        await this.fetchOrders();
        this.showToast("Order declined.", "success");
      } catch (error) {
        this.showToast("Failed to decline order.", "error");
      }
    },
    cancelDecline() {
      this.showDecline = false;
      this.declineMessage = "";
      this.declineError = "";
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
      this.bankError = "";
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
        this.bankAccountId = null;
        this.bankError = "Failed to fetch bank info.";
      }
    },
    clearBankFieldError(field) {
      if (field === "bank_name") this.bankNameError = "";
      if (field === "account_number") this.accountNumberError = "";
      if (field === "account_holder") this.accountHolderError = "";
      this.bankError = "";
    },
    async submitBankInfo() {
      this.bankNameError = "";
      this.accountNumberError = "";
      this.accountHolderError = "";
      this.bankError = "";
      let valid = true;
      
      if (!this.bankForm.bank_name) {
        this.bankNameError = "Bank name is required.";
        valid = false;
      } else if (!/^[A-Za-z\s]+$/.test(this.bankForm.bank_name)) {
        this.bankNameError = "Bank name must contain only letters and spaces.";
        valid = false;
      }
      if (!this.bankForm.account_number) {
        this.accountNumberError = "Account number is required.";
        valid = false;
      } else if (!/^\d{6,20}$/.test(this.bankForm.account_number)) {
        this.accountNumberError = "Account number must be 6-20 digits and contain only numbers.";
        valid = false;
      }
      if (!this.bankForm.account_holder) {
        this.accountHolderError = "Account holder is required.";
        valid = false;
      } else if (!/^[A-Za-z\s]+$/.test(this.bankForm.account_holder)) {
        this.accountHolderError = "Account holder must contain only letters and spaces.";
        valid = false;
      }
      
      if (!valid) return;
      try {
        if (this.bankAccountId) {
          await api.delete(`/api/supplier-bank-accounts/${this.bankAccountId}`);
        }
        await api.post("/api/supplier-bank-accounts/", {
          ...this.bankForm,
          supplier_id: null 
        });
        this.isBankModalOpen = false;
        this.fetchBankInfo();
        this.showToast("Bank info updated!", "success");
      } catch (e) {
        this.bankError = "Failed to update bank info.";
      }
    },
    receiptUrl(path) {
      if (!path) return "#";
      if (path.startsWith("http")) return path;
      return `${process.env.VUE_APP_API_BASE_URL || ""}/${path.replace(/^\/+/, "")}`;
    },
    showInvoiceButton(order) {
      return order && !['Pending', 'Declined'].includes(order.status);
    },
    downloadInvoice(order) {
      if (!order || !this.orderItems || this.orderItems.length === 0) {
        this.showToast("No invoice data to export!", "error");
        return;
      }
      const doc = new jsPDF();
      doc.setFontSize(20);
      doc.text("INVOICE", 14, 18);

      doc.setFontSize(12);
      doc.text(`Invoice #: ${order.id}`, 14, 28);
      doc.text(`Order Date: ${this.formatDate(order.order_date)}`, 14, 36);
      doc.text(`Supplier: ${order.supplier_name || ''}`, 14, 44);
      doc.text(`Company: ${order.company_name || ''}`, 14, 52);
      doc.text(`Status: ${order.status}`, 14, 60);

      doc.text("Order Description:", 14, 70);
      doc.text(order.description || '', 14, 78);

      autoTable(doc, {
        startY: 88,
        head: [["Product", "Quantity", "Unit Cost", "Subtotal"]],
        body: (this.orderItems || []).map(item => [
          item.product_name,
          item.quantity,
          this.formatCurrency(item.unit_cost),
          this.formatCurrency(item.subtotal)
        ]),
        theme: 'grid',
        headStyles: { fillColor: [0, 102, 204] },
        styles: { fontSize: 11 }
      });

      const finalY = doc.lastAutoTable ? doc.lastAutoTable.finalY : 88 + 8 * (this.orderItems?.length || 1);
      doc.setFontSize(13);
      doc.text(`Total: ${this.formatCurrency(order.total_cost)}`, 14, finalY + 12);

      doc.setFontSize(10);
      doc.text("Thank you for your business!", 14, finalY + 24);

      doc.save(`invoice_order_${order.id}.pdf`);
      this.showToast("Invoice downloaded!", "success");
    },
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

.button-group {
  display: flex;
  align-items: center;
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
  white-space: nowrap;
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
  white-space: nowrap;
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

.invoice-section {
  margin-top: 24px;
  text-align: right;
}
.invoice-btn {
  display: inline-flex;
  align-items: center;
  padding: 10px 18px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.invoice-btn:hover {
  background-color: #0052a3;
}
.invoice-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 17v-2a2 2 0 012-2h2a2 2 0 012 2v2m-6 4h6a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v12a2 2 0 002 2z' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}
.filter-select {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
  background: white;
  margin-left: 8px;
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
</style>