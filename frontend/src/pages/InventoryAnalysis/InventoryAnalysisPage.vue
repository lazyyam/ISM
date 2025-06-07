<template>
  <div class="inventory-analysis-container">
    <h1>Inventory Analysis</h1>

    <!-- Notifications -->
    <div class="notification-section" v-if="notifications.length">
      <div v-for="(note, idx) in notifications" :key="'note-' + idx" class="notification">
        {{ note }}
      </div>
    </div>

    <!-- Summary Section -->
    <div class="summary-section">
      <div class="summary-card">
        <div class="summary-title">Total Sales</div>
        <div class="summary-value">
          {{ totalSalesQuantity }} (Qty) / {{ formatCurrency(totalSalesValue) }}
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-title">Total Restocked/Adjusted</div>
        <div class="summary-value">{{ totalRestockedQuantity }}</div>
      </div>
      <div class="summary-card">
        <div class="summary-title">Transactions</div>
        <div class="summary-value">{{ totalTransactions }}</div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-section">
      <div class="chart-container">
        <canvas id="inventoryChart" ref="chartCanvas"></canvas>
      </div>
    </div>

    <!-- Product Performance Section -->
    <div class="performance-section">
      <!-- Top Selling Products -->
      <div class="performance-card">
        <h2>Top Selling Products</h2>
        <div class="product-table">
          <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Quantity Sold</th>
                <th>Revenue</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in topSellingProducts" :key="'top-' + index">
                <td>{{ product.name }}</td>
                <td>{{ product.quantity }}</td>
                <td>{{ formatCurrency(product.revenue) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- Least Selling Products -->
      <div class="performance-card">
        <h2>Least Selling Products</h2>
        <div class="product-table">
          <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Quantity Sold</th>
                <th>Revenue</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in leastSellingProducts" :key="'least-' + index">
                <td>{{ product.name }}</td>
                <td>{{ product.quantity }}</td>
                <td>{{ formatCurrency(product.revenue) }}</td>
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
        <div class="alert-table">
          <table>
            <thead>
              <tr>
                <th>Product ID</th>
                <th>Date</th>
                <th>Quantity</th>
                <th>Alert Amt.</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(alert, index) in stockAlerts" :key="'alert-' + index">
                <td>{{ alert.productId }}</td>
                <td>{{ alert.date }}</td>
                <td>{{ alert.quantity }}</td>
                <td>{{ alert.alertAmount }}</td>
                <td>{{ alert.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Expiry Alert Section -->
    <div class="expiry-alert-card">
      <h2>Expiry Date Alerts</h2>
      <div class="expiry-table">
        <table>
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Batch</th>
              <th>Expiry Date</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in expiryAlerts" :key="'expiry-' + idx">
              <td>{{ item.productName }}</td>
              <td>{{ item.batchId }}</td>
              <td>{{ item.expiryDate }}</td>
              <td>{{ item.quantity }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'InventoryAnalysisPage',
  data() {
    return {
      chart: null,
      isMounted: false,
      chartInitPromise: null,
      notifications: [],
      topSellingProducts: [
        // Replace with real data from backend
        { name: 'Product A', quantity: 120, revenue: 2400 },
        { name: 'Product B', quantity: 90, revenue: 1800 }
      ],
      leastSellingProducts: [
        { name: 'Product X', quantity: 5, revenue: 100 },
        { name: 'Product Y', quantity: 8, revenue: 160 }
      ],
      stockAlerts: [
        { productId: 'A123', date: '2025-06-04', quantity: 3, alertAmount: 5, status: 'Low' },
        { productId: 'B456', date: '2025-06-04', quantity: 2, alertAmount: 5, status: 'Critical' }
      ],
      expiryAlerts: [
        { productName: 'Product A', batchId: 'BATCH001', expiryDate: '2025-06-10', quantity: 10 },
        { productName: 'Product B', batchId: 'BATCH002', expiryDate: '2025-06-12', quantity: 5 }
      ],
      chartData: {
        labels: ['January', 'February', 'March', 'April'],
        datasets: [
          {
            label: 'Incoming Stock',
            data: [65, 70, 62, 67],
            backgroundColor: '#ffda77',
            borderColor: '#ffda77',
            borderWidth: 1
          },
          {
            label: 'Outgoing Stock',
            data: [70, 75, 69, 72],
            backgroundColor: '#5b6ff9',
            borderColor: '#5b6ff9',
            borderWidth: 1
          }
        ]
      }
    };
  },
  computed: {
    totalSalesQuantity() {
      return this.topSellingProducts.reduce((sum, p) => sum + Number(p.quantity || 0), 0);
    },
    totalSalesValue() {
      return this.topSellingProducts.reduce((sum, p) => sum + Number(p.revenue || 0), 0);
    },
    totalRestockedQuantity() {
      // Replace with your real restock data
      return 123; // Example
    },
    totalTransactions() {
      // Replace with your real transaction data
      return this.topSellingProducts.length + this.leastSellingProducts.length;
    }
  },
  mounted() {
    this.fetchNotifications();
    this.isMounted = true;
    this.chartInitPromise = this.$nextTick().then(() => {
      if (this.isMounted) {
        this.initChart();
      }
    });
  },
  beforeUnmount() {
    this.isMounted = false;
    this.destroyChart();
  },
  methods: {
    fetchNotifications() {
      // Fetch from backend or websocket
      // Example:
      this.notifications = [
        "Supplier ABC accepted your order.",
        "Supplier XYZ declined your order."
      ];
    },
    formatCurrency(val) {
      return "RM " + Number(val).toLocaleString();
    },
    initChart() {
      if (!this.$refs.chartCanvas || this.chart || !this.isMounted) return;

      try {
        const ctx = this.$refs.chartCanvas.getContext('2d');
        this.chart = new Chart(ctx, {
          type: 'bar',
          data: this.chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 0 },
            hover: { animationDuration: 0 },
            responsiveAnimationDuration: 0,
            plugins: {
              legend: { position: 'top' },
              title: { display: false },
              tooltip: { animation: { duration: 0 } }
            },
            elements: { line: { tension: 0 } },
            scales: {
              y: {
                beginAtZero: true,
                ticks: { animation: { duration: 0 } }
              },
              x: { ticks: { animation: { duration: 0 } } }
            },
            transitions: {
              active: { animation: { duration: 0 } },
              resize: { animation: { duration: 0 } }
            }
          }
        });
      } catch (error) {
        if (this.isMounted) {
          console.error('Chart initialization error:', error);
        }
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

.chart-section {
  margin-bottom: 24px;
}
.chart-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  padding: 20px;
  height: 300px;
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
.notification-section {
  margin-bottom: 16px;
}
.notification {
  background: #fffbe6;
  color: #b7791f;
  padding: 10px 16px;
  border-radius: 4px;
  margin-bottom: 6px;
  border: 1px solid #f6e05e;
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

@media (max-width: 768px) {
  .performance-section {
    flex-direction: column;
  }
}
</style>