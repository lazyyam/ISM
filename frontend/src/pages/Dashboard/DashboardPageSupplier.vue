<template>
    <div class="dashboard-container">
      <h1>Supplier Dashboard</h1>
      
      <div class="dashboard-stats">
        <div class="stat-card">
          <div class="stat-icon pending-icon"></div>
          <div class="stat-content">
            <h3>{{ pendingOrders.length }}</h3>
            <p>Pending Orders</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon shipment-icon"></div>
          <div class="stat-content">
            <h3>{{ activeShipments.length }}</h3>
            <p>Active Shipments</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon inventory-icon"></div>
          <div class="stat-content">
            <h3>{{ lowStockItems.length }}</h3>
            <p>Low Stock Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon bestseller-icon"></div>
          <div class="stat-content">
            <h3>{{ revenueThisMonth }}</h3>
            <p>Monthly Revenue</p>
          </div>
        </div>
      </div>
      
      <!-- Pending Orders Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>📦 Pending Orders</h2>
          <button class="view-all-btn">View All</button>
        </div>
        
        <div class="order-list">
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Date</th>
                  <th>Customer</th>
                  <th>Items</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in pendingOrders.slice(0, 5)" :key="order.id">
                  <td>#{{ order.id }}</td>
                  <td>{{ order.date }}</td>
                  <td>{{ order.customer }}</td>
                  <td>{{ order.items }}</td>
                  <td>${{ order.total }}</td>
                  <td>
                    <span class="status-badge" :class="`status-${order.status.toLowerCase()}`">
                      {{ order.status }}
                    </span>
                  </td>
                  <td>
                    <button class="action-btn process-btn" @click="processOrder(order.id)">
                      Process
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <!-- Shipment Tracking Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>🚚 Shipment Tracking</h2>
          <button class="view-all-btn">View All</button>
        </div>
        
        <div class="shipment-cards">
          <div class="shipment-card" v-for="shipment in activeShipments.slice(0, 3)" :key="shipment.id">
            <div class="shipment-header">
              <span class="shipment-id">Order #{{ shipment.orderId }}</span>
              <span class="shipment-date">{{ shipment.shippedDate }}</span>
            </div>
            <div class="shipment-details">
              <p><strong>Customer:</strong> {{ shipment.customer }}</p>
              <p><strong>Location:</strong> {{ shipment.currentLocation }}</p>
              <p><strong>Expected Delivery:</strong> {{ shipment.expectedDelivery }}</p>
            </div>
            <div class="shipment-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="`width: ${shipment.progressPercentage}%`"></div>
              </div>
              <div class="progress-labels">
                <span>Shipped</span>
                <span>In Transit</span>
                <span>Delivered</span>
              </div>
            </div>
            <button class="track-btn">View Details</button>
          </div>
        </div>
      </div>
      
      <!-- Inventory Updates Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>🔄 Inventory Updates</h2>
          <button class="view-all-btn">View All</button>
        </div>
        
        <div class="inventory-container">
          <div class="inventory-column">
            <h3>Low Stock Items</h3>
            <div class="inventory-list">
              <div class="inventory-item" v-for="item in lowStockItems.slice(0, 5)" :key="item.id">
                <div class="item-info">
                  <h4>{{ item.name }}</h4>
                  <p>{{ item.category }}</p>
                </div>
                <div class="item-stock">
                  <span class="stock-level critical">{{ item.currentStock }}</span>
                  <span class="stock-threshold">of {{ item.threshold }}</span>
                </div>
                <button class="restock-btn" @click="restockItem(item.id)">Restock</button>
              </div>
            </div>
          </div>
          
          <div class="inventory-column">
            <h3>Recent Stock Changes</h3>
            <div class="inventory-activity">
              <div class="activity-item" v-for="(activity, index) in recentStockChanges" :key="index">
                <div class="activity-icon" :class="activity.type"></div>
                <div class="activity-details">
                  <p class="activity-name">{{ activity.productName }}</p>
                  <p class="activity-description">{{ activity.description }}</p>
                </div>
                <span class="activity-time">{{ activity.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Best-Selling Products Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>🏆 Best-Selling Products</h2>
          <div class="period-selector">
            <button class="period-btn active">Week</button>
            <button class="period-btn">Month</button>
            <button class="period-btn">Year</button>
          </div>
        </div>
        
        <div class="bestsellers-container">
          <div class="bestseller-chart">
            <!-- Simple bar chart representation -->
            <div class="chart-container">
              <div class="chart-bars">
                <div v-for="product in bestSellingProducts" :key="product.id" class="chart-bar-container">
                  <div class="chart-label">{{ product.name }}</div>
                  <div class="chart-bar" :style="`height: ${(product.salesPercentage)}%`">
                    <div class="chart-value">{{ product.unitsSold }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bestseller-list">
            <div class="bestseller-item" v-for="(product, index) in bestSellingProducts" :key="product.id">
              <div class="bestseller-rank">{{ index + 1 }}</div>
              <div class="bestseller-info">
                <h4>{{ product.name }}</h4>
                <p>{{ product.category }}</p>
              </div>
              <div class="bestseller-stats">
                <div class="stats-item">
                  <span class="stats-label">Units</span>
                  <span class="stats-value">{{ product.unitsSold }}</span>
                </div>
                <div class="stats-item">
                  <span class="stats-label">Revenue</span>
                  <span class="stats-value">${{ product.revenue }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SupplierDashboard',
    data() {
      return {
        pendingOrders: [
          { id: 12345, date: '15/4/2025', customer: 'AC Mart', items: 5, total: 650.00, status: 'Pending' },
          { id: 12346, date: '15/4/2025', customer: 'SuperStore', items: 8, total: 1200.00, status: 'Processing' },
          { id: 12347, date: '14/4/2025', customer: 'GreenGrocer', items: 3, total: 480.00, status: 'Pending' },
          { id: 12348, date: '14/4/2025', customer: 'Quick Shop', items: 2, total: 320.00, status: 'Pending' },
          { id: 12349, date: '13/4/2025', customer: 'Family Mart', items: 7, total: 950.00, status: 'Processing' }
        ],
        activeShipments: [
          { 
            id: 'SH-1001', 
            orderId: 12340, 
            customer: 'AC Mart', 
            shippedDate: '12/4/2025', 
            currentLocation: 'Distribution Center', 
            expectedDelivery: '17/4/2025',
            progressPercentage: 30
          },
          { 
            id: 'SH-1002', 
            orderId: 12335, 
            customer: 'SuperStore', 
            shippedDate: '11/4/2025', 
            currentLocation: 'In Transit', 
            expectedDelivery: '16/4/2025',
            progressPercentage: 65
          },
          { 
            id: 'SH-1003', 
            orderId: 12328, 
            customer: 'Quick Shop', 
            shippedDate: '10/4/2025', 
            currentLocation: 'Local Warehouse', 
            expectedDelivery: '15/4/2025',
            progressPercentage: 85
          }
        ],
        lowStockItems: [
          { id: 101, name: 'Red Beans Original', category: 'Canned Food', currentStock: 25, threshold: 100 },
          { id: 102, name: 'Canned Curry Ayam', category: 'Canned Food', currentStock: 15, threshold: 50 },
          { id: 103, name: 'White Bun', category: 'Bread', currentStock: 8, threshold: 30 },
          { id: 104, name: 'Brown Rice', category: 'Grains', currentStock: 12, threshold: 40 },
          { id: 105, name: 'Sweetened Milk', category: 'Dairy', currentStock: 18, threshold: 45 }
        ],
        recentStockChanges: [
          { type: 'decrease', productName: 'Red Beans Original', description: 'Order #12345 - 50 units', time: '2 hours ago' },
          { type: 'increase', productName: 'Brown Rice', description: 'Stock replenished - 100 units', time: '5 hours ago' },
          { type: 'update', productName: 'Canned Curry Ayam', description: 'Inventory adjusted - +5 units', time: '8 hours ago' },
          { type: 'decrease', productName: 'White Bun', description: 'Order #12342 - 22 units', time: '1 day ago' },
          { type: 'increase', productName: 'Sweetened Milk', description: 'Stock replenished - 50 units', time: '1 day ago' }
        ],
        bestSellingProducts: [
          { id: 101, name: 'Red Beans Original', category: 'Canned Food', unitsSold: 450, revenue: '2,250.00', salesPercentage: 90 },
          { id: 103, name: 'White Bun', category: 'Bread', unitsSold: 380, revenue: '1,140.00', salesPercentage: 76 },
          { id: 102, name: 'Canned Curry Ayam', category: 'Canned Food', unitsSold: 310, revenue: '3,720.00', salesPercentage: 62 },
          { id: 105, name: 'Sweetened Milk', category: 'Dairy', unitsSold: 290, revenue: '1,450.00', salesPercentage: 58 },
          { id: 104, name: 'Brown Rice', category: 'Grains', unitsSold: 210, revenue: '1,890.00', salesPercentage: 42 }
        ],
        revenueThisMonth: '$9,450'
      };
    },
    methods: {
      processOrder(orderId) {
        console.log(`Processing order ${orderId}`);
        // Implement order processing logic
      },
      restockItem(itemId) {
        console.log(`Restocking item ${itemId}`);
        // Implement restock logic
      }
    }
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  h1 {
    color: #4a5568;
    margin-bottom: 24px;
    font-weight: 500;
    font-size: 24px;
  }
  
  h2 {
    color: #4a5568;
    font-size: 18px;
    font-weight: 500;
    margin: 0;
  }
  
  h3 {
    color: #4a5568;
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 16px 0;
  }
  
  /* Dashboard Stats Cards */
  .dashboard-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .stat-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    align-items: center;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    background-size: 30px;
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 8px;
    margin-right: 16px;
  }
  
  .pending-icon {
    background-color: #ebf8ff;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%230066cc'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4' /%3E%3C/svg%3E");
  }
  
  .shipment-icon {
    background-color: #fefcbf;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23d69e2e'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4' /%3E%3C/svg%3E");
  }
  
  .inventory-icon {
    background-color: #e6fffa;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2338b2ac'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' /%3E%3C/svg%3E");
  }
  
  .bestseller-icon {
    background-color: #fed7d7;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23e53e3e'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' /%3E%3C/svg%3E");
  }
  
  .stat-content h3 {
    font-size: 20px;
    font-weight: 600;
    margin: 0;
    color: #2d3748;
  }
  
  .stat-content p {
    margin: 4px 0 0 0;
    color: #718096;
    font-size: 14px;
  }
  
  /* Dashboard Sections */
  .dashboard-section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
    padding: 20px;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .view-all-btn {
    padding: 6px 12px;
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    color: #4a5568;
    font-size: 14px;
    cursor: pointer;
  }
  
  .view-all-btn:hover {
    background-color: #edf2f7;
  }
  
  /* Order Table Styles */
  .table-container {
    overflow-x: auto;
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
    color: #718096;
    font-weight: 500;
    font-size: 14px;
  }
  
  td {
    color: #2d3748;
    font-size: 14px;
  }
  
  .status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
  }
  
  .status-pending {
    background-color: #fef6e0;
    color: #d69e2e;
  }
  
  .status-processing {
    background-color: #e6f6ff;
    color: #3182ce;
  }
  
  .status-shipped {
    background-color: #e6fffa;
    color: #38b2ac;
  }
  
  .action-btn {
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
  }
  
  .process-btn {
    background-color: #0066cc;
    color: white;
    border: none;
  }
  
  .process-btn:hover {
    background-color: #0052a3;
  }
  
  /* Shipment Cards */
  .shipment-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  
  .shipment-card {
    border: 1px solid #edf2f7;
    border-radius: 8px;
    padding: 16px;
  }
  
  .shipment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
  }
  
  .shipment-id {
    font-weight: 600;
    color: #2d3748;
  }
  
  .shipment-date {
    color: #718096;
    font-size: 14px;
  }
  
  .shipment-details p {
    margin: 8px 0;
    font-size: 14px;
    color: #4a5568;
  }
  
  .shipment-progress {
    margin: 20px 0;
  }
  
  .progress-bar {
    height: 6px;
    background-color: #edf2f7;
    border-radius: 3px;
    margin-bottom: 8px;
  }
  
  .progress-fill {
    height: 100%;
    background-color: #0066cc;
    border-radius: 3px;
  }
  
  .progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #718096;
  }
  
  .track-btn {
    display: block;
    width: 100%;
    padding: 8px;
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    color: #4a5568;
    font-size: 14px;
    text-align: center;
    margin-top: 16px;
    cursor: pointer;
  }
  
  .track-btn:hover {
    background-color: #edf2f7;
  }
  
  /* Inventory Styles */
  .inventory-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  
  .inventory-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .inventory-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border: 1px solid #edf2f7;
    border-radius: 6px;
  }
  
  .item-info {
    flex: 1;
  }
  
  .item-info h4 {
    margin: 0;
    font-size: 15px;
    color: #2d3748;
  }
  
  .item-info p {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: #718096;
  }
  
  .item-stock {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-right: 16px;
  }
  
  .stock-level {
    font-size: 16px;
    font-weight: 600;
  }
  
  .stock-level.critical {
    color: #e53e3e;
  }
  
  .stock-threshold {
    font-size: 12px;
    color: #718096;
  }
  
  .restock-btn {
    padding: 6px 12px;
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 13px;
    cursor: pointer;
  }
  
  .restock-btn:hover {
    background-color: #0052a3;
  }
  
  /* Activity Feed */
  .inventory-activity {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .activity-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border: 1px solid #edf2f7;
    border-radius: 6px;
  }
  
  .activity-icon {
    width: 30px;
    height: 30px;
    border-radius: 15px;
    margin-right: 12px;
    background-size: 18px;
    background-position: center;
    background-repeat: no-repeat;
  }
  
  .increase {
    background-color: #e6fffa;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2338b2ac'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 10l7-7m0 0l7 7m-7-7v18' /%3E%3C/svg%3E");
  }
  
  .decrease {
    background-color: #fed7d7;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23e53e3e'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 14l-7 7m0 0l-7-7m7 7V3' /%3E%3C/svg%3E");
  }
  
  .update {
    background-color: #ebf8ff;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%233182ce'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' /%3E%3C/svg%3E");
  }
  
  .activity-details {
    flex: 1;
  }
  
  .activity-name {
    margin: 0;
    font-size: 15px;
    color: #2d3748;
    font-weight: 500;
  }
  
  .activity-description {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: #718096;
  }
  
  .activity-time {
    font-size: 12px;
    color: #a0aec0;
  }
  
  /* Best Sellers Section */
  .period-selector {
    display: flex;
  }
  
  .period-btn {
    padding: 6px 12px;
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    color: #4a5568;
    font-size: 14px;
    cursor: pointer;
  }
  
  .period-btn:first-child {
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }
  
  .period-btn:last-child {
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
  }
  
  .period-btn.active {
    background-color: #0066cc;
    color: white;
    border-color: #0066cc;
  }
  
  .bestsellers-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  
  /* Simple Chart */
  .chart-container {
    height: 250px;
    display: flex;
    align-items: flex-end;
    position: relative;
    padding-bottom: 30px;
  }
  
  .chart-bars {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    width: 100%;
    height: 100%;
  }
  
  .chart-bar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 18%;
  }
  
  .chart-bar {
    width: 40px;
    background-color: #0066cc;
    border-radius: 4px 4px 0 0;
    position: relative;
    display: flex;
    justify-content: center;
  }
  
  .chart-value {
    position: absolute;
    top: -25px;
    color: #4a5568;
    font-weight: 500;
    font-size: 13px;
  }
  
  .chart-label {
    margin-top: 8px;
    text-align: center;
    font-size: 13px;
    color: #718096;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }
  
  /* Bestseller List */
  .bestseller-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .bestseller-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border: 1px solid #edf2f7;
    border-radius: 6px;
  }
  
  .bestseller-rank {
    width: 30px;
    height: 30px;
    background-color: #f7fafc;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: #4a5568;
    margin-right: 12px;
  }
  
  .bestseller-info {
    flex: 1;
  }
  
  .bestseller-info h4 {
    margin: 0;
    font-size: 15px;
    color: #2d3748;
  }
  
  .bestseller-info p {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: #718096;
  }
  
  .bestseller-stats {
    display: flex;
    gap: 16px;
  }
  
  .stats-item {
    display: flex;
  }
</style>