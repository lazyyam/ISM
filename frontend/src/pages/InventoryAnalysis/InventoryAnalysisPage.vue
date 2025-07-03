<template>
  <div class="inventory-analysis-container">
    <h1>Inventory Analysis</h1>

    <div class="periods-actions" style="margin-bottom: 24px;">
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
    </div>

    <!-- Summary Section -->
    <div class="summary-section">
      <div class="summary-card">
        <div class="summary-title">Total Sales Quantity</div>
        <div class="summary-value">
          {{ totalSalesQuantity }}
        </div>
        <div class="summary-breakdown">
          Transactions: {{ totalSalesTransactions }}
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-title">Total Restocked Quantity</div>
        <div class="summary-value">{{ totalRestockedQuantity }}</div>
        <div class="summary-breakdown">
          Transactions: {{ totalRestockTransactions }}
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-title">Total Adjusted Quantity</div>
        <div class="summary-value">{{ totalAdjustedQuantity }}</div>
        <div class="summary-breakdown">
          Transactions: {{ totalAdjustmentTransactions }}
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-section">
      <div class="chart-container">
        <div style="position:relative; width:100%; height:250px;">
          <div v-if="loadingInventory">Loading chart...</div>
          <div v-else-if="inventoryError" class="error-message">{{ inventoryError }}</div>
          <div v-else>
            <canvas id="inventoryChart" ref="chartCanvas" style="width:100% !important; height:100% !important;"></canvas>
          </div>
        </div>
        <div v-if="chartError" class="error-message">{{ chartError }}</div>
      </div>
    </div>

    <!-- Product Performance Section -->
    <div class="performance-section">
      <!-- Top Selling Products -->
      <div class="performance-card">
        <h2>Top Selling Products</h2>
        <div v-if="loadingSales">Loading...</div>
        <div v-else-if="salesError" class="error-message">{{ salesError }}</div>
        <div v-else class="product-table">
          <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Quantity Sold</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in topSellingProducts" :key="'top-' + index">
                <td>{{ product.name }}</td>
                <td>{{ product.quantity }}</td>
              </tr>
              <tr v-if="topSellingProducts.length === 0">
                <td colspan="2" style="text-align:center;">No data available.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- Least Selling Products -->
      <div class="performance-card">
        <h2>Least Selling Products</h2>
        <div v-if="loadingSales">Loading...</div>
        <div v-else-if="salesError" class="error-message">{{ salesError }}</div>
        <div v-else class="product-table">
          <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Quantity Sold</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in leastSellingProducts" :key="'least-' + index">
                <td>{{ product.name }}</td>
                <td>{{ product.quantity }}</td>
              </tr>
              <tr v-if="leastSellingProducts.length === 0">
                <td colspan="2" style="text-align:center;">No data available.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Stock Alert Section -->
    <div class="stock-alert-section">
      <div class="stock-alert-card">
        <h2>Stock Alerts</h2>
        <div v-if="loadingProducts">Loading...</div>
        <div v-else-if="productsError" class="error-message">{{ productsError }}</div>
        <div v-else class="alert-table">
          <table>
            <thead>
              <tr>
                <th>Product Code</th>
                <th>Product Name</th>
                <th>Quantity</th>
                <th>Threshold</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(alert, index) in paginatedStockAlerts" :key="'alert-' + index">
                <td>{{ alert.productId }}</td>
                <td>{{ alert.productName }}</td>
                <td>{{ alert.quantity }}</td>
                <td>{{ alert.alertAmount }}</td>
                <td>{{ alert.status }}</td>
              </tr>
              <tr v-if="stockAlerts.length === 0">
                <td colspan="5" style="text-align:center;">No stock alerts.</td>
              </tr>
            </tbody>
          </table>
          <div class="pagination">
            <button @click="stockCurrentPage--" :disabled="stockCurrentPage === 1" title="Previous">
              &lt;
            </button>
            <span>
              Page
              <input
                type="number"
                v-model.number="stockPageInput"
                @change="goToStockPage"
                :min="1"
                :max="stockTotalPages"
                style="width: 40px; text-align: center;"
              />
              of {{ stockTotalPages }}
            </span>
            <button @click="stockCurrentPage++" :disabled="stockCurrentPage === stockTotalPages" title="Next">
              &gt;
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Expiry Alert Section -->
    <div class="expiry-alert-card">
      <h2>Expiry Date Alerts</h2>
      <div v-if="loadingProducts">Loading...</div>
      <div v-else-if="productsError" class="error-message">{{ productsError }}</div>
      <div v-else class="expiry-table">
        <table>
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Batch</th>
              <th>Expiry Date</th>
              <th>Quantity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in paginatedExpiryAlerts" :key="'expiry-' + idx">
              <td>{{ item.productName }}</td>
              <td>{{ item.batchId }}</td>
              <td>{{ item.expiryDate }}</td>
              <td>{{ item.quantity }}</td>
              <td>
                <span :style="{color: item.status === 'Expired' ? '#e53e3e' : '#b7791f'}">
                  {{ item.status }}
                </span>
              </td>
            </tr>
            <tr v-if="expiryAlerts.length === 0">
              <td colspan="5" style="text-align:center;">No expiry alerts.</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination">
          <button @click="expiryCurrentPage--" :disabled="expiryCurrentPage === 1" title="Previous">
            &lt;
          </button>
          <span>
            Page
            <input
              type="number"
              v-model.number="expiryPageInput"
              @change="goToExpiryPage"
              :min="1"
              :max="expiryTotalPages"
              style="width: 40px; text-align: center;"
            />
            of {{ expiryTotalPages }}
          </span>
          <button @click="expiryCurrentPage++" :disabled="expiryCurrentPage === expiryTotalPages" title="Next">
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import Chart from 'chart.js/auto';

export default {
  name: 'InventoryAnalysisPage',
  // Move chart instance outside of data to make it non-reactive
  chart: null,
  isMounted: false,
  chartInitPromise: null,
  data() {
    const today = new Date().toLocaleDateString('en-CA');
    const thisMonth = today.slice(0, 7);
    const thisYear = today.slice(0, 4);
    return {
      viewMode: "daily",
      selectedDate: today,
      selectedMonth: thisMonth,
      selectedYear: thisYear,
      stockCurrentPage: 1,
      stockPageSize: 5,
      stockPageInput: 1,
      expiryCurrentPage: 1,
      expiryPageSize: 5,
      expiryPageInput: 1,
      sales: [],
      products: [],
      inventory: [],
      stockAlerts: [],
      expiryAlerts: [],
      salesError: "",
      inventoryError: "",
      productsError: "",
      loadingSales: false,
      loadingInventory: false,
      loadingProducts: false,
      chartError: "",
    };
  },
  watch: {
    viewMode() {
      this.stockCurrentPage = 1;
      this.stockPageInput = 1;
      this.expiryCurrentPage = 1;
      this.expiryPageInput = 1;
      this.updateChart();
    },
    selectedDate() {
      this.stockCurrentPage = 1;
      this.stockPageInput = 1;
      this.expiryCurrentPage = 1;
      this.expiryPageInput = 1;
      this.updateChart();
    },
    selectedMonth() {
      this.stockCurrentPage = 1;
      this.stockPageInput = 1;
      this.expiryCurrentPage = 1;
      this.expiryPageInput = 1;
      this.updateChart();
    },
    selectedYear() {
      this.stockCurrentPage = 1;
      this.stockPageInput = 1;
      this.expiryCurrentPage = 1;
      this.expiryPageInput = 1;
      this.updateChart();
    },
    stockCurrentPage(val) {
      this.stockPageInput = val;
    },
    expiryCurrentPage(val) {
      this.expiryPageInput = val;
    },
    // Remove the deep watcher that was causing the circular reference
    inventory: {
      handler() {
        this.updateChart();
      },
      deep: false // Changed from deep: true to prevent circular references
    },
  },
  computed: {
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
    filteredStockAlerts() {
      const productIds = new Set(this.filteredInventory.map(e => e.product_id));
      return this.stockAlerts.filter(alert => productIds.has(alert.productId));
    },
    filteredExpiryAlerts() {
      const batchIds = new Set(this.filteredInventory.map(e => e.batch_id));
      return this.expiryAlerts.filter(alert => batchIds.has(alert.batchId));
    },
    paginatedStockAlerts() {
      const start = (this.stockCurrentPage - 1) * this.stockPageSize;
      const end = start + this.stockPageSize;
      return this.stockAlerts.slice(start, end);
    },
    stockTotalPages() {
      return Math.ceil(this.stockAlerts.length / this.stockPageSize) || 1;
    },
    paginatedExpiryAlerts() {
      const start = (this.expiryCurrentPage - 1) * this.expiryPageSize;
      const end = start + this.expiryPageSize;
      return this.expiryAlerts.slice(start, end);
    },
    expiryTotalPages() {
      return Math.ceil(this.expiryAlerts.length / this.expiryPageSize) || 1;
    },
    totalSalesQuantity() {
      return this.filteredInventory
        .filter(e => e.transaction_type === "sale")
        .reduce((sum, e) => sum + Math.abs(Number(e.change_amount) || 0), 0);
    },
    totalRestockedQuantity() {
      return this.filteredInventory
        .filter(e => e.transaction_type === "restock")
        .reduce((sum, e) => sum + Number(e.change_amount || 0), 0);
    },
    totalAdjustedQuantity() {
      return this.filteredInventory
        .filter(e => e.transaction_type === "manual_add" || e.transaction_type === "adjustment")
        .reduce((sum, e) => sum + Number(e.change_amount || 0), 0);
    },
    totalSalesTransactions() {
      return this.filteredInventory.filter(e => e.transaction_type === "sale").length;
    },
    totalRestockTransactions() {
      return this.filteredInventory.filter(e => e.transaction_type === "restock").length;
    },
    totalAdjustmentTransactions() {
      return this.filteredInventory.filter(e => e.transaction_type === "adjustment").length;
    },
    topSellingProducts() {
      const productSalesMap = {};
      this.filteredSales.forEach(sale => {
        if (!productSalesMap[sale.product_id]) {
          productSalesMap[sale.product_id] = {
            name: sale.product_name,
            quantity: 0
          };
        }
        productSalesMap[sale.product_id].quantity += Number(sale.quantity) || 0;
      });
      const productSalesArr = Object.values(productSalesMap);
      return [...productSalesArr].sort((a, b) => b.quantity - a.quantity).slice(0, 3);
    },
    leastSellingProducts() {
      const productSalesMap = {};
      this.filteredSales.forEach(sale => {
        if (!productSalesMap[sale.product_id]) {
          productSalesMap[sale.product_id] = {
            name: sale.product_name,
            quantity: 0
          };
        }
        productSalesMap[sale.product_id].quantity += Number(sale.quantity) || 0;
      });
      const productSalesArr = Object.values(productSalesMap);
      return [...productSalesArr].sort((a, b) => a.quantity - b.quantity).slice(0, 3);
    }
  },
  mounted() {
    this.fetchSales();
    this.fetchInventory().then(() => {
      this.$options.isMounted = true;
      this.$options.chartInitPromise = this.$nextTick().then(() => {
        if (this.$options.isMounted) {
          try {
            this.initChart();
            window.addEventListener('resize', this.handleResize);
          } catch (e) {
            this.chartError = "Failed to render chart.";
          }
        }
      });
    });
    this.fetchProducts();
  },
  beforeUnmount() {
    this.$options.isMounted = false;
    this.destroyChart();
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    goToStockPage() {
      if (this.stockPageInput < 1) this.stockPageInput = 1;
      if (this.stockPageInput > this.stockTotalPages) this.stockPageInput = this.stockTotalPages;
      this.stockCurrentPage = this.stockPageInput;
    },
    goToExpiryPage() {
      if (this.expiryPageInput < 1) this.expiryPageInput = 1;
      if (this.expiryPageInput > this.expiryTotalPages) this.expiryPageInput = this.expiryTotalPages;
      this.expiryCurrentPage = this.expiryPageInput;
    },
    handleResize() {
      if (this.$options.chart) {
        this.$options.chart.resize();
      }
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
      if (this.$options.chart) {
        this.updateChart();
      }
    },
    async fetchProducts() {
      this.loadingProducts = true;
      this.productsError = "";
      try {
        const res = await api.get("/api/products/");
        this.products = res.data;
        this.updateStockAlerts();
        this.updateExpiryAlerts(); 
      } catch (e) {
        this.products = [];
        this.stockAlerts = [];
        this.expiryAlerts = [];
        this.productsError = "Failed to load products data.";
      } finally {
        this.loadingProducts = false;
      }
    },
    updateStockAlerts() {
      this.stockAlerts = this.products
        .map(product => {
          const currentStock = (product.inventory || []).reduce(
            (sum, entry) => sum + Number(entry.change_amount || 0),
            0
          );
          return {
            productId: product.code,
            productName: product.name,
            quantity: currentStock,
            alertAmount: product.stock_threshold,
            status: currentStock <= product.stock_threshold ? (currentStock === 0 ? "Out of Stock" : "Low") : "OK"
          };
        })
        .filter(alert => alert.status !== "OK");
    },
    updateExpiryAlerts() {
      const today = new Date();
      const soon = new Date();
      soon.setDate(today.getDate() + 30); 

      const alerts = [];
      this.products.forEach(product => {
        (product.batches || []).forEach(batch => {
          if (!batch.expiry_date) return;
          const expiry = new Date(batch.expiry_date);
          if (expiry <= soon) {
            alerts.push({
              productName: product.name,
              batchId: batch.batch_id,
              expiryDate: batch.expiry_date,
              quantity: batch.quantity,
              status: expiry < today ? "Expired" : "Expiring Soon"
            });
          }
        });
      });
      alerts.sort((a, b) => new Date(a.expiryDate) - new Date(b.expiryDate));
      this.expiryAlerts = alerts;
    },
    // Create a method to generate chart data without reactivity
    getChartData() {
      const incomingTypes = ["restock", "manual_add"];
      const outgoingTypes = ["sale", "adjustment"];
      const grouped = {};

      this.filteredInventory.forEach(entry => {
        if (!entry.created_at) return;
        const date = new Date(entry.created_at);
        const month = date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, "0");
        if (!grouped[month]) {
          grouped[month] = { incoming: 0, outgoing: 0 };
        }
        if (incomingTypes.includes(entry.transaction_type)) {
          grouped[month].incoming += Number(entry.change_amount) || 0;
        }
        if (outgoingTypes.includes(entry.transaction_type)) {
          grouped[month].outgoing += Math.abs(Number(entry.change_amount) || 0);
        }
      });

      const months = Object.keys(grouped).sort();
      return {
        labels: months,
        datasets: [
          {
            label: "Incoming Stock",
            data: months.map(m => grouped[m].incoming),
            backgroundColor: "#ffda77",
            borderColor: "#ffda77",
            borderWidth: 1
          },
          {
            label: "Outgoing Stock",
            data: months.map(m => grouped[m].outgoing),
            backgroundColor: "#5b6ff9",
            borderColor: "#5b6ff9",
            borderWidth: 1
          }
        ]
      };
    },
    initChart() {
      if (!this.$refs.chartCanvas || this.$options.chart || !this.$options.isMounted) return;
      const ctx = this.$refs.chartCanvas.getContext('2d');
      
      // Use the method instead of the computed property to avoid reactivity issues
      const chartData = JSON.parse(JSON.stringify(this.getChartData()));
      
      this.$options.chart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { position: 'top' },
            title: { display: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    },
    updateChart() {
      if (this.$options.chart) {
        try {
          // Create a completely new data object to avoid reactivity
          const newData = JSON.parse(JSON.stringify(this.getChartData()));
          this.$options.chart.data.labels = newData.labels;
          this.$options.chart.data.datasets = newData.datasets;
          this.$options.chart.update('none'); // Use 'none' animation mode to prevent issues
        } catch (error) {
          console.error('Chart update error:', error);
          this.chartError = "Failed to update chart.";
        }
      }
    },
    destroyChart() {
      if (this.$options.chart) {
        try {
          this.$options.chart.destroy();
        } catch (error) {
          console.error('Chart destruction error:', error);
        } finally {
          this.$options.chart = null;
        }
      }
      this.$options.chartInitPromise = null;
    }
  }
};
</script>

<style scoped>
.inventory-analysis-container {
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
  padding: 10px 16px;
}

.summary-section {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}
.summary-card {
  flex: 1;
  background: #f8fafc;
  border-radius: 8px;
  padding: 18px 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  text-align: center;
}
.summary-title {
  color: #4a5568;
  font-size: 14px;
  margin-bottom: 8px;
}
.summary-value {
  color: #2d3748;
  font-size: 20px;
  font-weight: bold;
}
.summary-breakdown {
  color: #718096;
  font-size: 13px;
  margin-top: 6px;
}

#inventoryChart {
  width: 100% !important; 
  height: 100% !important;
  max-width: 100%;
  max-height: 100%;
}

.chart-section {
  margin-bottom: 24px;
}
.chart-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  padding: 20px;
}

.performance-section {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}
.performance-card {
  flex: 1;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.product-table, .alert-table {
  width: 100%;
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

.stock-alert-section {
  margin-bottom: 24px;
}
.stock-alert-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.expiry-alert-section {
  margin-bottom: 24px;
}

.expiry-alert-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 24px;
  padding-bottom: 8px;
}
.expiry-table {
  width: 100%;
  padding: 0 0 16px 0;
}

.periods-actions {
  display: flex;
  justify-content: flex-start;
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

.error-message {
  color: #e53e3e;
  padding: 12px 16px;
  font-size: 15px;
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

@media (max-width: 768px) {
  .performance-section {
    flex-direction: column;
  }
}
</style>