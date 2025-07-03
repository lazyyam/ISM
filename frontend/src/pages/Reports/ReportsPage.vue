<template>
  <div class="reports-container">
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

    <h1>Reports</h1>

    <div class="reports-actions">
      <div class="controls-group">
        <div class="view-mode">
          <label>
            <input type="radio" value="daily" v-model="viewMode" /> Daily
          </label>
          <label>
            <input type="radio" value="monthly" v-model="viewMode" /> Monthly
          </label>
          <label>
            <input type="radio" value="yearly" v-model="viewMode" /> Yearly
          </label>
        </div>
        <div class="date-picker">
          <input
            v-if="viewMode === 'daily'"
            type="date"
            v-model="selectedDate"
            class="date-input"
          />
          <input
            v-if="viewMode === 'monthly'"
            type="month"
            v-model="selectedMonth"
            class="date-input"
          />
          <input
            v-if="viewMode === 'yearly'"
            type="number"
            min="2000"
            max="2100"
            v-model="selectedYear"
            class="date-input year-input"
            placeholder="Year"
          />
        </div>
      </div>
      <div class="button-group">
        <button class="generate-report-btn" @click="downloadSalesPDF">
          <span class="download-icon"></span>
          Download Sales PDF
        </button>
        <button class="generate-report-btn" @click="downloadInventoryPDF">
          <span class="download-icon"></span>
          Download Restock/Adjustment PDF
        </button>
      </div>
    </div>

    <p v-if="yearError" class="field-error">{{ yearError }}</p>

    <!-- Sales History Section -->
    <div class="report-section" ref="salesSection">
      <h2>Sales History</h2>
      <div v-if="loadingSales" class="loading-message">Loading sales...</div>
      <div v-if="salesError" class="error-message">{{ salesError }}</div>
      <div class="report-table">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Product</th>
              <th>Quantity</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sale in paginatedSales" :key="sale.id">
              <td>{{ sale.sell_date }}</td>
              <td>{{ sale.product_name }}</td>
              <td>{{ sale.quantity }}</td>
              <td>{{ sale.remarks || '-' }}</td>
            </tr>
            <tr v-if="!loadingSales && !salesError && filteredSales.length === 0">
              <td colspan="4" style="text-align:center;">No sales data found.</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <button @click="salesCurrentPage--" :disabled="salesCurrentPage === 1" title="Previous">
            &lt;
          </button>
          <span>
            Page
            <input
              type="number"
              v-model.number="salesPageInput"
              @change="goToSalesPage"
              :min="1"
              :max="salesTotalPages"
              style="width: 40px; text-align: center;"
            />
            of {{ salesTotalPages }}
          </span>
          <button @click="salesCurrentPage++" :disabled="salesCurrentPage === salesTotalPages" title="Next">
            &gt;
          </button>
        </div>
      </div>
    </div>

    <!-- Restock/Adjustment History Section -->
    <div class="report-section" ref="restockSection">
      <h2>Restock & Adjustment History</h2>
      <div v-if="loadingInventory" class="loading-message">Loading inventory...</div>
      <div v-if="inventoryError" class="error-message">{{ inventoryError }}</div>
      <div class="report-table">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Product</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Batch</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in paginatedInventory" :key="entry.id">
              <td>{{ entry.created_at ? entry.created_at.split('T')[0] : '-' }}</td>
              <td>{{ entry.product_name }}</td>
              <td>{{ entry.transaction_type }}</td>
              <td>{{ entry.change_amount }}</td>
              <td>{{ entry.batch_id || '-' }}</td>
            </tr>
            <tr v-if="!loadingInventory && !inventoryError && filteredInventory.length === 0">
              <td colspan="5" style="text-align:center;">No inventory data found.</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <button @click="inventoryCurrentPage--" :disabled="inventoryCurrentPage === 1" title="Previous">
            &lt;
          </button>
          <span>
            Page
            <input
              type="number"
              v-model.number="inventoryPageInput"
              @change="goToInventoryPage"
              :min="1"
              :max="inventoryTotalPages"
              style="width: 40px; text-align: center;"
            />
            of {{ inventoryTotalPages }}
          </span>
          <button @click="inventoryCurrentPage++" :disabled="inventoryCurrentPage === inventoryTotalPages" title="Next">
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import SuccessToast from "@/components/SuccessToast.vue";
import ErrorToast from "@/components/ErrorToast.vue";

export default {
  name: 'ReportsPage',
  components: {
    SuccessToast,
    ErrorToast,
  },
  data() {
    const savedViewMode = localStorage.getItem('reportsViewMode') || "daily";
    const today = new Date().toLocaleDateString('en-CA');
    const thisMonth = today.slice(0, 7);
    const thisYear = today.slice(0, 4);
    return {
      salesCurrentPage: 1,
      salesPageSize: 5,
      salesPageInput: 1,
      inventoryCurrentPage: 1,
      inventoryPageSize: 5,
      inventoryPageInput: 1,
      viewMode: savedViewMode,
      selectedDate: today,
      selectedMonth: thisMonth,
      selectedYear: thisYear,
      products: [],
      sales: [],
      inventory: [],
      loadingSales: false,
      loadingInventory: false,
      salesError: "",
      inventoryError: "",
      yearError: "",
      showSuccessToast: false,
      showErrorToast: false,
      toastMessage: "",
    };
  },
  watch: {
    viewMode(newVal) {
      localStorage.setItem('reportsViewMode', newVal);
      this.salesCurrentPage = 1;
      this.salesPageInput = 1;
      this.inventoryCurrentPage = 1;
      this.inventoryPageInput = 1;
    },
    salesCurrentPage(val) {
      this.salesPageInput = val;
    },
    inventoryCurrentPage(val) {
      this.inventoryPageInput = val;
    }
  },
  computed: {
    paginatedSales() {
      const start = (this.salesCurrentPage - 1) * this.salesPageSize;
      const end = start + this.salesPageSize;
      return this.filteredSales.slice(start, end);
    },
    salesTotalPages() {
      return Math.ceil(this.filteredSales.length / this.salesPageSize) || 1;
    },
    paginatedInventory() {
      const start = (this.inventoryCurrentPage - 1) * this.inventoryPageSize;
      const end = start + this.inventoryPageSize;
      return this.filteredInventory.slice(start, end);
    },
    inventoryTotalPages() {
      return Math.ceil(this.filteredInventory.length / this.inventoryPageSize) || 1;
    },
    filteredSales() {
      if (this.viewMode === "daily") {
        return this.sales.filter(s => s.sell_date === this.selectedDate);
      }
      if (this.viewMode === "monthly") {
        return this.sales.filter(s => s.sell_date && s.sell_date.startsWith(this.selectedMonth));
      }
      if (this.viewMode === "yearly") {
        return this.sales.filter(s => s.sell_date && s.sell_date.startsWith(this.selectedYear));
      }
      return this.sales;
    },
    filteredInventory() {
      if (this.viewMode === "daily") {
        return this.inventory.filter(e => e.created_at && e.created_at.split('T')[0] === this.selectedDate);
      }
      if (this.viewMode === "monthly") {
        return this.inventory.filter(e => e.created_at && e.created_at.startsWith(this.selectedMonth));
      }
      if (this.viewMode === "yearly") {
        return this.inventory.filter(e => e.created_at && e.created_at.startsWith(this.selectedYear));
      }
      return this.inventory;
    },
  },
  mounted() {
    this.fetchProducts();
    this.fetchSales();
    this.fetchInventory();
  },
  methods: {
    goToSalesPage() {
      if (this.salesPageInput < 1) this.salesPageInput = 1;
      if (this.salesPageInput > this.salesTotalPages) this.salesPageInput = this.salesTotalPages;
      this.salesCurrentPage = this.salesPageInput;
    },
    goToInventoryPage() {
      if (this.inventoryPageInput < 1) this.inventoryPageInput = 1;
      if (this.inventoryPageInput > this.inventoryTotalPages) this.inventoryPageInput = this.inventoryTotalPages;
      this.inventoryCurrentPage = this.inventoryPageInput;
    },
    async fetchProducts() {
      try {
        const res = await api.get("/api/products/");
        this.products = res.data;
      } catch (e) {
        this.products = [];
      }
    },
    getProductInfo(productName) {
      return this.products.find(p => p.name === productName) || {};
    },
    async fetchSales() {
      this.loadingSales = true;
      this.salesError = "";
      try {
        const res = await api.get("/api/sales/");
        this.sales = res.data;
      } catch (e) {
        this.sales = [];
        this.salesError = "Failed to load sales data.";
      } finally {
        this.loadingSales = false;
      }
    },
    async fetchInventory() {
      this.loadingInventory = true;
      this.inventoryError = "";
      try {
        const res = await api.get("/api/inventory/");
        this.inventory = res.data;
      } catch (e) {
        this.inventory = [];
        this.inventoryError = "Failed to load inventory data.";
      } finally {
        this.loadingInventory = false;
      }
    },
    validateYear() {
      if (this.viewMode === "yearly") {
        if (!this.selectedYear || isNaN(this.selectedYear) || this.selectedYear < 2000 || this.selectedYear > 2100) {
          this.yearError = "Please enter a valid year (2000-2100).";
          return false;
        }
      }
      this.yearError = "";
      return true;
    },
    showToastMessage(msg, type = "error") {
      this.toastMessage = msg;
      if (type === "success") {
        this.showSuccessToast = true;
        this.showErrorToast = false;
      } else {
        this.showErrorToast = true;
        this.showSuccessToast = false;
      }
      setTimeout(() => {
        this.showSuccessToast = false;
        this.showErrorToast = false;
        this.toastMessage = "";
      }, 2500);
    },
    downloadSalesPDF() {
      if (!this.validateYear()) return;
      if (this.filteredSales.length === 0) {
        this.showToastMessage("No sales data to export!", "error");
        return;
      }
      const doc = new jsPDF();

      // 1. Company Branding and Header
      doc.setFontSize(20);
      doc.text("OCO", 14, 18);
      doc.setFontSize(14);
      doc.text("Sales Report", 14, 28);
      doc.setFontSize(11);
      doc.text(`Period: ${this.getReportPeriod()}`, 14, 36);
      doc.text(`Generated: ${new Date().toLocaleDateString()}`, 14, 43);

      // 2. Sales Table with Product Details
      const salesRows = this.filteredSales.map(sale => {
        const info = this.getProductInfo(sale.product_name);
        return [
          sale.sell_date,
          sale.product_name,
          info.code || "-",
          info.category || "-",
          info.retail_price !== undefined ? this.formatCurrency(info.retail_price) : "-",
          sale.quantity,
          sale.remarks || "-"
        ];
      });

      autoTable(doc, {
        startY: 50,
        head: [["Date", "Product", "Code", "Category", "Unit Price", "Quantity", "Remarks"]],
        body: salesRows,
        theme: 'striped',
        headStyles: { fillColor: [0, 102, 204], textColor: 255, fontStyle: 'bold' },
        alternateRowStyles: { fillColor: [240, 240, 240] },
        styles: { fontSize: 11, cellPadding: 3 }
      });

      // 3. Totals and Summary Section
      const totalQty = this.filteredSales.reduce((sum, s) => sum + Number(s.quantity), 0);
      const totalAmount = this.filteredSales.reduce((sum, s) => {
        const info = this.getProductInfo(s.product_name);
        return sum + (Number(info.retail_price) || 0) * Number(s.quantity);
      }, 0);

      const finalY = doc.lastAutoTable ? doc.lastAutoTable.finalY : 50 + 8 * (salesRows.length || 1);
      doc.setFontSize(12);
      doc.text(`Total Quantity: ${totalQty}`, 14, finalY + 10);
      doc.text(`Total Sales: ${this.formatCurrency(totalAmount)}`, 14, finalY + 18);

      // 5. Footer with page numbers (optional)
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(10);
        doc.text(`Page ${i} of ${pageCount}`, doc.internal.pageSize.getWidth() - 40, doc.internal.pageSize.getHeight() - 10);
      }

      doc.save(`sales_report_${this.viewMode}_${this.getReportPeriod()}.pdf`);
      this.showToastMessage("PDF downloaded!", "success");
    },
    downloadInventoryPDF() {
      if (!this.validateYear()) return;
      if (this.filteredInventory.length === 0) {
        this.showToastMessage("No inventory data to export!", "error");
        return;
      }
      const doc = new jsPDF();

      // Header
      doc.setFontSize(20);
      doc.text("OCO", 14, 18);
      doc.setFontSize(14);
      doc.text("Restock & Adjustment Report", 14, 28);
      doc.setFontSize(11);
      doc.text(`Period: ${this.getReportPeriod()}`, 14, 36);
      doc.text(`Generated: ${new Date().toLocaleDateString()}`, 14, 43);

      // Table with product details
      const inventoryRows = this.filteredInventory.map(entry => {
        const info = this.getProductInfo(entry.product_name);
        return [
          entry.created_at ? entry.created_at.split('T')[0] : '-',
          entry.product_name,
          info.code || "-",
          info.category || "-",
          entry.transaction_type,
          entry.change_amount,
          entry.batch_id || '-'
        ];
      });

      autoTable(doc, {
        startY: 50,
        head: [["Date", "Product", "Code", "Category", "Type", "Quantity", "Batch"]],
        body: inventoryRows,
        theme: 'striped',
        headStyles: { fillColor: [0, 102, 204], textColor: 255, fontStyle: 'bold' },
        alternateRowStyles: { fillColor: [240, 240, 240] },
        styles: { fontSize: 11, cellPadding: 3 }
      });

      // Totals
      const totalRestock = this.filteredInventory
        .filter(e => e.transaction_type === "restock")
        .reduce((sum, e) => sum + Number(e.change_amount), 0);
      const totalAdjustment = this.filteredInventory
        .filter(e => e.transaction_type === "adjustment" || e.transaction_type === "manual_add")
        .reduce((sum, e) => sum + Number(e.change_amount), 0);

      const finalY = doc.lastAutoTable ? doc.lastAutoTable.finalY : 50 + 8 * (inventoryRows.length || 1);
      doc.setFontSize(12);
      doc.text(`Total Restocked: ${totalRestock}`, 14, finalY + 10);
      doc.text(`Total Adjusted: ${totalAdjustment}`, 14, finalY + 18);

      // Footer with page numbers
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(10);
        doc.text(`Page ${i} of ${pageCount}`, doc.internal.pageSize.getWidth() - 40, doc.internal.pageSize.getHeight() - 10);
      }

      doc.save(`restock_report_${this.viewMode}_${this.getReportPeriod()}.pdf`);
      this.showToastMessage("PDF downloaded!", "success");
    },
    formatCurrency(amount) {
      if (amount === undefined || amount === null || isNaN(amount)) return "-";
      return "RM " + Number(amount).toLocaleString("en-MY", { minimumFractionDigits: 2 });
    },
    getReportPeriod() {
      if (this.viewMode === "daily") return this.selectedDate;
      if (this.viewMode === "monthly") return this.selectedMonth;
      if (this.viewMode === "yearly") return this.selectedYear;
      return "all";
    }
  }
};
</script>
  
<style scoped>
.reports-container {
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

h2 {
  color: #2d3748;
  margin-top: 0;
  margin-bottom: 16px;
  font-weight: 500;
  font-size: 18px;
}

.reports-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}

.controls-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.view-mode {
  display: flex;
  gap: 16px;
  align-items: center;
}

.view-mode label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #4a5568;
  cursor: pointer;
}

.view-mode input[type="radio"] {
  margin: 0;
}

.date-picker {
  display: flex;
  align-items: center;
}

.date-input {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
  color: #2d3748;
  background-color: white;
  min-width: 140px;
}

.date-input:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2);
}

.year-input {
  min-width: 100px;
}

.button-group {
  display: flex;
  gap: 12px;
}

.generate-report-btn {
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
  white-space: nowrap;
}

.generate-report-btn:hover {
  background-color: #0052a3;
}

.download-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23ffffff'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.report-section {
  margin-bottom: 30px;
}

.report-table {
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

.loading-message {
  color: #2d3748;
  font-size: 15px;
  padding: 12px 16px;
}
.error-message, .field-error {
  color: #e53e3e;
  font-size: 15px;
  padding: 12px 16px;
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