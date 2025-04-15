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
              <th>ID</th>
              <th>Order Date</th>
              <th>Description</th>
              <th>Total Cost</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in filteredOrders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.orderDate }}</td>
              <td>{{ order.description }}</td>
              <td>{{ order.totalCost }}</td>
              <td>
                <span 
                  class="status-badge" 
                  :class="{ 
                    'status-delivered': order.status === 'Delivered',
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
    </div>
  </template>
  
  <script>
  export default {
    name: 'PurchaseOrder',
    data() {
      return {
        searchQuery: '',
        orders: [
          {
            id: 1,
            orderDate: '05/3/2024',
            description: 'Canned Foods',
            totalCost: '300.00',
            status: 'Delivered'
          },
          {
            id: 2,
            orderDate: '18/6/2024',
            description: 'Canned Foods',
            totalCost: '220.00',
            status: 'Pending'
          }
        ]
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
                 order.description.toLowerCase().includes(query);
        });
      }
    },
    mounted() {
      // You could add API call to fetch orders here
      // this.fetchOrders();
    },
    methods: {
      // fetchOrders() {
      //   // Example implementation with axios
      //   // axios.get('/api/purchase-orders')
      //   //   .then(response => {
      //   //     this.orders = response.data;
      //   //   })
      //   //   .catch(error => {
      //   //     console.error('Error fetching orders:', error);
      //   //   });
      // }
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
  
  .status-pending {
    background-color: #fff7ed;
    color: #c2410c;
  }
  </style>