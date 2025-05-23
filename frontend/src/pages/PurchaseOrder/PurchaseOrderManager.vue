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
            <th>No.</th>
            <th>Order Date</th>
            <th>Supplier</th>
            <th>Company</th>
            <th>Description</th>
            <th>Total Cost</th>
            <th>Status</th>
            <th class="action-cell">Action</th>
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
            <td>{{ order.supplier_name }}</td>
            <td>{{ order.company_name }}</td>
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
            <td class="action-cell" @click.stop>
              <div class="action-buttons">
                <button
                  class="edit-btn"
                  :disabled="order.status !== 'Pending'"
                  @click="editOrder(order)"
                  title="Edit (only when Pending)"
                >
                  <i class="edit-icon"></i>
                </button>
                <button class="delete-btn" @click="deleteOrder(order.id)" title="Delete order">
                  <i class="delete-icon"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="bottom-buttons">
      <button class="mapping-btn" @click="showMappingModal = true">
        Product Mapping
      </button>
      <button class="add-purchase-btn" @click="openAddModal">
        <i class="plus-icon"></i>
        Add Purchase
      </button>
    </div>
    <MappingModal
      :isOpen="showMappingModal"
      @close="showMappingModal = false"
    />

    <!-- Order Details/Status Modal -->
    <BaseModal
      :isOpen="isDetailModalOpen"
      title="Purchase Order Details"
      @close="closeDetailModal"
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
            <div v-for="(item, index) in selectedOrder.items" :key="index" class="product-row">
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

            <div v-if="selectedOrder.status === 'Delivering'" class="status-update">
              <button class="accept-btn" @click="updateOrderStatus(selectedOrder.id, 'Delivered')">
                Mark as Delivered
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
        <button class="close-btn" @click="closeDetailModal">
          Close
        </button>
      </template>
    </BaseModal>

    <!-- Purchase Order Modal (Add/Edit) -->
    <BaseModal
      :isOpen="isModalOpen"
      :title="modalTitle"
      @close="closeModal"
    >
      <div class="purchase-form">
        <div>
          <div class="form-group">
            <label>Order Date</label>
            <input type="date" v-model="formData.orderDate" :disabled="isEditing" />
          </div>
          <div class="form-group">
            <label>Supplier</label>
            <select v-model="formData.supplierId" :disabled="isEditing" @change="supplierChanged">
              <option value="" disabled>Select Supplier</option>
              <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
                {{ supplier.full_name }} ({{ supplier.company_name }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="formData.description" placeholder="Description"></textarea>
          </div>
          <div class="form-group">
            <label>Order Items</label>
            <table class="items-table">
              <thead>
                <tr>
                  <th class="product-col">Product</th>
                  <th class="quantity-col">Quantity</th>
                  <th>Unit Cost</th>
                  <th>Subtotal</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in formData.orderItems" :key="idx">
                  <td class="product-col">
                    <select v-model="item.productId" @change="productChanged(idx)">
                      <option value="" disabled>Select Product</option>
                      <option v-for="prod in supplierProducts" :key="prod.id" :value="prod.id">
                        {{ prod.name }}
                      </option>
                    </select>
                  </td>
                  <td class="quantity-col">
                    <input
                      type="number"
                      min="1"
                      :max="getProductMaxQuantity(item.productId)"
                      v-model.number="item.quantity"
                      @input="updateItemTotal(idx)"
                    />
                    <span v-if="getProductMaxQuantity(item.productId)" class="available-qty">
                      / {{ getProductMaxQuantity(item.productId) }} available
                    </span>
                  </td>
                  <td>
                    {{ formatCurrency(item.cost) }}
                  </td>
                  <td>
                    {{ formatCurrency(item.total) }}
                  </td>
                  <td>
                    <button 
                      v-if="formData.orderItems.length > 1" 
                      class="remove-item-btn"
                      @click="removeOrderItem(index)"
                      title="Remove item"
                    >
                      <i class="delete-icon"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <button class="add-item-btn" @click="addOrderItem">
              <i class="plus-icon"></i>
              Add Product
            </button>
          </div>
          <div class="form-group total-cost">
            <strong>Total Cost: {{ formatCurrency(calculateTotalCost()) }}</strong>
          </div>
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
import MappingModal from "@/components/MappingModal.vue";
import api from "@/services/api";

export default {
  name: 'PurchaseOrderManager',
  components: {
    BaseModal,
    MappingModal
  },
  data() {
    return {
      isModalOpen: false,
      isDetailModalOpen: false,
      selectedOrder: null,
      isEditing: false,
      showMappingModal: false,
      currentOrderId: null,
      orders: [],
      suppliers: [],
      supplierProducts: [],
      productMappings: [],
      formData: {
        orderDate: "",
        supplierId: "",
        description: "",
        status: "Pending", 
        orderItems: [
          { productId: "", quantity: 1, cost: 0, total: 0 },
        ],
      },
      searchQuery: "",
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
               (order.supplier_name && order.supplier_name.toLowerCase().includes(query)) ||
               (order.company_name && order.company_name.toLowerCase().includes(query)) ||
               (order.description && order.description.toLowerCase().includes(query)) ||
               (order.status && order.status.toLowerCase().includes(query));
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
      return this.formData.orderItems.some(
        (item) => item.productId && item.quantity > 0
      );
    }
  },
  mounted() {
    this.fetchOrders();
    this.fetchSuppliers();
  },
  methods: {
    async fetchOrders() {
      try {
        const response = await api.get("/api/purchase-orders");
        this.orders = response.data;
      } catch (error) {
        console.error("Failed to fetch orders:", error);
      }
    },
    async fetchSuppliers() {
      try {
        const response = await api.get("/api/suppliers");
        this.suppliers = response.data;
      } catch (error) {
        console.error("Failed to fetch suppliers:", error);
      }
    },
    async fetchSupplierProducts() {
      if (!this.formData.supplierId) {
        this.supplierProducts = [];
        return;
      }
      try {
        const response = await api.get(`/api/supplier-products/by-supplier/${this.formData.supplierId}`);
        const mappedSupplierProductIds = this.productMappings.map(m => m.supplier_product_id);
        this.supplierProducts = response.data.filter(
          (product) => mappedSupplierProductIds.includes(product.id)
        );
      } catch (error) {
        this.supplierProducts = [];
      }
    },
    async fetchProductMappings() {
      if (!this.formData.supplierId) {
        this.productMappings = [];
        return;
      }
      try {
        const response = await api.get("/api/product-mappings");
        this.productMappings = response.data.filter(
          m => m.supplier_id == this.formData.supplierId
        );
      } catch (error) {
        this.productMappings = [];
      }
    },
    async viewOrderDetails(order) {
      try {
        const response = await api.get(`/api/purchase-orders/${order.id}`);
        this.selectedOrder = response.data;
        this.isDetailModalOpen = true;
      } catch (error) {
        console.error('Failed to fetch order details:', error);
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
    statusClass(status) {
      return {
        'status-delivered': status === 'Delivered',
        'status-delivering': status === 'Delivering',
        'status-processing': status === 'Processing',
        'status-accepted': status === 'Accepted',
        'status-declined': status === 'Declined',
        'status-pending': status === 'Pending'
      };
    },
    openAddModal() {
      this.isEditing = false;
      this.currentOrderId = null;
      this.resetForm();
      this.isModalOpen = true;
    },
    async editOrder(order) {
      if (order.status !== "Pending") {
        alert("You can only edit orders that are still pending.");
        return;
      }
      this.isEditing = true;
      this.currentOrderId = order.id;
      try {
        const response = await api.get(`/api/purchase-orders/${order.id}`);
        const orderData = response.data;
        this.formData = {
          orderDate: orderData.order_date,
          supplierId: orderData.supplier_id,
          description: orderData.description || "",
          status: orderData.status,
          orderItems: orderData.items.map((item) => ({
            productId: item.supplier_product_id,
            quantity: item.quantity,
            cost: item.unit_cost,
            total: item.subtotal,
          })),
        };
        await this.fetchSupplierProducts();
        this.isModalOpen = true;
      } catch (error) {
        console.error("Failed to fetch order details:", error);
      }
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
    closeModal() {
      this.isModalOpen = false;
      this.resetForm();
    },
    closeDetailModal() {
      this.isDetailModalOpen = false;
      this.selectedOrder = null;
    },
    resetForm() {
      const today = new Date();
      this.formData = {
        orderDate: today.toISOString().split("T")[0],
        supplierId: "",
        description: "",
        status: "Pending",
        orderItems: [
          { productId: "", quantity: 1, cost: 0, total: 0 },
        ],
      };
      this.supplierProducts = [];
    },
    async supplierChanged() {
      await this.fetchProductMappings();
      await this.fetchSupplierProducts();
      this.formData.orderItems = [
        { productId: "", quantity: 1, cost: 0, total: 0 },
      ];
    },
    productChanged(index) {
      const item = this.formData.orderItems[index];
      if (item.productId) {
        const product = this.supplierProducts.find(
          (p) => p.id === item.productId
        );
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
        productId: "",
        quantity: 1,
        cost: 0,
        total: 0,
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
    getProductMaxQuantity(productId) {
      const prod = this.supplierProducts.find(p => p.id === productId);
      return prod ? prod.quantity_available : 1;
    },
    async submitForm() {
      if (!this.isFormValid) return;
      for (const item of this.formData.orderItems) {
        const prod = this.supplierProducts.find(p => p.id === item.productId);
        if (prod && item.quantity > prod.quantity_available) {
          alert(`Cannot order more than available quantity for ${prod.name}`);
          return;
        }
      }
      try {
        const orderData = {
          supplier_id: this.formData.supplierId,
          status: this.formData.status,
          total_cost: this.calculateTotalCost(),
          description: this.formData.description,
          items: this.formData.orderItems.map((item) => ({
            supplier_product_id: item.productId,
            quantity: item.quantity,
            unit_cost: item.cost,
            subtotal: item.total,
          })),
        };
        if (this.isEditing) {
          await api.put(
            `/api/purchase-orders/${this.currentOrderId}`,
            orderData
          );
        } else {
          await api.post("/api/purchase-orders", orderData);
        }
        this.fetchOrders();
        this.closeModal();
      } catch (error) {
        console.error("Failed to save purchase order:", error);
      }
    },
    async deleteOrder(orderId) {
      if (confirm('Are you sure you want to delete this order?')) {
        try {
          await api.delete(`/api/purchase-orders/${orderId}`);
          this.fetchOrders();
        } catch (error) {
          console.error('Failed to delete order:', error);
        }
      }
    },
  },
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

.action-cell {
  width: 120px;
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

.edit-btn:disabled {
  background-color: #e2e8f0;
  cursor: not-allowed;
}

.edit-btn:hover:not(:disabled) {
  background-color: #edf2f7;
}

.delete-btn:hover {
  background-color: #fee2e2;
}

.edit-icon, .delete-icon, .plus-icon {
  width: 16px;
  height: 16px;
  display: inline-block;
  background-size: contain;
  background-repeat: no-repeat;
}

.edit-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z' /%3E%3C/svg%3E");
}
.delete-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23e53e3e'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16' /%3E%3C/svg%3E");
}
.plus-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 6v6m0 0v6m0-6h6m-6 0H6' /%3E%3C/svg%3E");
  margin-right: 8px;
}

.bottom-buttons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.mapping-btn {
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
  transition: background-color 0.2s;
}

.mapping-btn:hover {
  background-color: #0052a3;
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

.BaseModal .modal-content,
.base-modal .modal-content {
  background: #fff;
  border-radius: 10px;
  padding: 32px 28px 24px 28px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}

.BaseModal .modal-header,
.base-modal .modal-header {
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 18px;
  padding-bottom: 10px;
}

.BaseModal .modal-title,
.base-modal .modal-title {
  font-size: 22px;
  font-weight: 600;
  color: #2563eb;
}

.BaseModal .modal-footer,
.base-modal .modal-footer {
  border-top: 1px solid #e2e8f0;
  margin-top: 18px;
  padding-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
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

.purchase-form {
  width: 100%;
}

.purchase-form .form-group label {
  font-weight: 500;
}

.form-group label {
  display: block;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 6px;
}

.purchase-form input[type="date"],
.purchase-form select,
.purchase-form textarea {
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
  margin-top: 3px;
  margin-bottom: 8px;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.purchase-form textarea {
  min-height: 60px;
  resize: vertical;
}

.purchase-form .items-table th,
.purchase-form .items-table td {
  font-size: 13px;
  padding: 7px 8px;
}

.purchase-form .items-table th {
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 14px;
  color: #4a5568;
}

.purchase-form .items-table td {
  background: #fff;
}

.purchase-form .items-table select,
.purchase-form .items-table input {
  width: 100%;
  padding: 5px;
  font-size: 13px;
}

.purchase-form .add-item-btn {
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

.purchase-form .add-item-btn:hover {
  background-color: #e2e8f0;
}

.purchase-form .remove-item-btn {
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

.purchase-form .remove-item-btn:hover {
  background-color: #fed7d7;
}

.purchase-form .total-cost {
  text-align: right;
  margin-top: 10px;
  font-weight: 500;
}

.purchase-form .items-table .product-col {
  width: 38%;
  min-width: 180px;
}

.purchase-form .items-table .quantity-col {
  width: 12%;
  min-width: 60px;
  max-width: 80px;
}

.submit-btn, .close-btn, .accept-btn {
  min-width: 110px;
  padding: 10px 0;
  margin-left: 8px;
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