<template>
    <div class="inventory-analysis-container">
      <h1>Inventory Analysis</h1>
      
      <!-- Chart Section -->
      <!-- <div class="chart-section">
        <div class="chart-container">
          <canvas id="inventoryChart" ref="chartCanvas"></canvas>
        </div>
      </div> -->
      
      <!-- Product Performance Section -->
      <div class="performance-section">
        <!-- Top Selling Products -->
        <div class="performance-card">
          <h2>Top selling Products</h2>
          <div class="product-table">
            <table>
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Quantity sold</th>
                  <th>Revenue</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(product, index) in topSellingProducts" :key="'top-' + index">
                  <td>{{ product.name }}</td>
                  <td>{{ product.quantity }}</td>
                  <td>{{ product.revenue }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- Least Selling Products -->
        <div class="performance-card">
          <h2>Least selling Products</h2>
          <div class="product-table">
            <table>
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Quantity sold</th>
                  <th>Revenue</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(product, index) in leastSellingProducts" :key="'least-' + index">
                  <td>{{ product.name }}</td>
                  <td>{{ product.quantity }}</td>
                  <td>{{ product.revenue }}</td>
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
                  <th>Alert amt.</th>
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
        topSellingProducts: [
          {
            name: 'product name',
            quantity: 'Quantity',
            revenue: 'revenue'
          },
          {
            name: 'product name',
            quantity: 'Quantity',
            revenue: 'revenue'
          }
        ],
        leastSellingProducts: [
          {
            name: 'product name',
            quantity: 'Quantity',
            revenue: 'revenue'
          },
          {
            name: 'product name',
            quantity: 'Quantity',
            revenue: 'revenue'
          }
        ],
        stockAlerts: [
          {
            productId: 'product ID',
            date: 'Date',
            quantity: 'Quantity',
            alertAmount: 'Alert amt.',
            status: 'Status'
          },
          {
            productId: 'product ID',
            date: 'Date',
            quantity: 'Quantity',
            alertAmount: 'Alert amt.',
            status: 'Status'
          },
          {
            productId: 'product ID',
            date: 'Date',
            quantity: 'Quantity',
            alertAmount: 'Alert amt.',
            status: 'Status'
          },
          {
            productId: 'product ID',
            date: 'Date',
            quantity: 'Quantity',
            alertAmount: 'Alert amt.',
            status: 'Status'
          }
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
    mounted() {
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
              // Disable all animations
              animation: {
                duration: 0 // general animation time
              },
              hover: {
                animationDuration: 0 // duration of animations when hovering an item
              },
              responsiveAnimationDuration: 0, // animation duration after a resize
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: false
                },
                // Disable tooltip animations
                tooltip: {
                  animation: {
                    duration: 0
                  }
                }
              },
              // Disable animations for all elements (bars, lines, etc)
              elements: {
                line: {
                  tension: 0 // disables bezier curves
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  // Disable animations for scales
                  ticks: {
                    animation: {
                      duration: 0
                    }
                  }
                },
                x: {
                  // Disable animations for scales
                  ticks: {
                    animation: {
                      duration: 0
                    }
                  }
                }
              },
              // Additional global animation settings
              transitions: {
                active: {
                  animation: {
                    duration: 0
                  }
                },
                resize: {
                  animation: {
                    duration: 0
                  }
                }
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
        
        // Cancel any pending chart initialization
        this.chartInitPromise = null;
      }
    },
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
  
  .stock-alert-section {
    margin-bottom: 24px;
  }
  
  .stock-alert-card {
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
  
  @media (max-width: 768px) {
    .performance-section {
      flex-direction: column;
    }
  }
  </style>