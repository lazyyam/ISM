<template>
  <div class="inventory-analysis-container">
    <h1>Inventory Analysis</h1>

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
        <div v-if="loadingInventory">Loading chart...</div>
        <div v-else-if="inventoryError" class="error-message">{{ inventoryError }}</div>
        <div v-else>
          <canvas id="inventoryChart" ref="chartCanvas"></canvas>
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
        <h2>Stock Alert</h2>
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
              <tr v-for="(alert, index) in stockAlerts" :key="'alert-' + index">
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
            <tr v-for="(item, idx) in expiryAlerts" :key="'expiry-' + idx">
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
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import Chart from 'chart.js/auto';

export default {
  name: 'InventoryAnalysisPage',
  data() {
    return {
      chart: null,
      isMounted: false,
      chartInitPromise: null,
      sales: [],
      topSellingProducts: [],
      leastSellingProducts: [],
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
  computed: {
    totalSalesQuantity() {
      return this.inventory
        .filter(e => e.transaction_type === "sale")
        .reduce((sum, e) => sum + Math.abs(Number(e.change_amount) || 0), 0);
    },
    totalRestockedQuantity() {
      return this.inventory
        .filter(e => e.transaction_type === "restock")
        .reduce((sum, e) => sum + Number(e.change_amount || 0), 0);
    },
    totalAdjustedQuantity() {
      return this.inventory
        .filter(e => e.transaction_type === "manual_add" || e.transaction_type === "adjustment")
        .reduce((sum, e) => sum + Number(e.change_amount || 0), 0);
    },
    totalSalesTransactions() {
      return this.inventory.filter(e => e.transaction_type === "sale").length;
    },
    totalRestockTransactions() {
      return this.inventory.filter(e => e.transaction_type === "restock").length;
    },
    totalAdjustmentTransactions() {
      return this.inventory.filter(e => e.transaction_type === "adjustment").length;
    },
    chartDataFromInventory() {
      const incomingTypes = ["restock", "manual_add"];
      const outgoingTypes = ["sale", "adjustment"];
      const grouped = {};

      this.inventory.forEach(entry => {
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
    }
  },
  mounted() {
    this.fetchSales();
    this.fetchInventory().then(() => {
      this.isMounted = true;
      this.chartInitPromise = this.$nextTick().then(() => {
        if (this.isMounted) {
          try {
            this.initChart();
          } catch (e) {
            this.chartError = "Failed to render chart.";
          }
        }
      });
    });
    this.fetchProducts();
  },
  beforeUnmount() {
    this.isMounted = false;
    this.destroyChart();
  },
  methods: {
    async fetchSales() {
      this.loadingSales = true;
      this.salesError = "";
      try {
        const res = await api.get("/api/sales/");
        this.sales = res.data;
        this.updateProductSalesStats();
      } catch (e) {
        this.sales = [];
        this.topSellingProducts = [];
        this.leastSellingProducts = [];
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
      if (this.chart) {
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
    updateProductSalesStats() {
      const productSalesMap = {};
      this.sales.forEach(sale => {
        if (!productSalesMap[sale.product_id]) {
          productSalesMap[sale.product_id] = {
            name: sale.product_name,
            quantity: 0
          };
        }
        productSalesMap[sale.product_id].quantity += Number(sale.quantity) || 0;
      });

      const productSalesArr = Object.values(productSalesMap);

      this.topSellingProducts = [...productSalesArr].sort((a, b) => b.quantity - a.quantity).slice(0, 3);
      this.leastSellingProducts = [...productSalesArr].sort((a, b) => a.quantity - b.quantity).slice(0, 3);
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
    
    initChart() {
      if (!this.$refs.chartCanvas || this.chart || !this.isMounted) return;
      const ctx = this.$refs.chartCanvas.getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: this.chartDataFromInventory,
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
      if (this.chart) {
        this.chart.data = this.chartDataFromInventory;
        this.chart.update();
      }
    },
    destroyChart() {
      if (this.chart) {
        try {
          this.chart.destroy();
        } catch (error) {
          console.error('Chart destruction error:', error);
        } finally {
          this.chart = null;
        }
      }
      this.chartInitPromise = null;
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
.error-message {
  color: #e53e3e;
  padding: 12px 16px;
  font-size: 15px;
}

@media (max-width: 768px) {
  .performance-section {
    flex-direction: column;
  }
}
</style>