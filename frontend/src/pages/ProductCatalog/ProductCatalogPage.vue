<template>
    <div class="catalog-container">
      <h1>Product Catalog</h1>
      
      <div class="catalog-actions">
        <div class="search-bar">
          <i class="search-icon"></i>
          <input 
            type="text" 
            placeholder="Search product ID" 
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
      
      <div class="product-table">
        <table>
          <thead>
            <tr>
              <th class="action-cell">Action</th>
              <th>ID</th>
              <th>Name</th>
              <th>Category</th>
              <th>Code</th>
              <th>Cost</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in filteredProducts" :key="product.id">
              <td class="action-cell">
                <button 
                  class="edit-btn" 
                  @click="editProduct(product.id)"
                  title="Edit product"
                >
                  <i class="edit-icon"></i>
                </button>
              </td>
              <td>{{ product.id }}</td>
              <td>{{ product.name }}</td>
              <td>{{ product.category }}</td>
              <td>{{ product.code }}</td>
              <td>{{ product.cost }}</td>
              <td>{{ product.quantity }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <button class="add-product-btn" @click="addProduct">
        <i class="plus-icon"></i>
        Add Product
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProductCatalog',
    data() {
      return {
        searchQuery: '',
        products: [
          {
            id: 1,
            name: 'Red Beans Original',
            category: 'Canned Food',
            code: '123456',
            cost: '5.00',
            quantity: 300
          },
          {
            id: 2,
            name: 'Canned Curry Ayam',
            category: 'Canned Food',
            code: '123456',
            cost: '12.00',
            quantity: 300
          },
          {
            id: 3,
            name: 'White Bun',
            category: 'Bread',
            code: '123456',
            cost: '3.00',
            quantity: 200
          }
        ]
      };
    },
    computed: {
      filteredProducts() {
        if (!this.searchQuery) {
          return this.products;
        }
        
        const query = this.searchQuery.toLowerCase();
        return this.products.filter(product => {
          return product.id.toString().includes(query) ||
                 product.name.toLowerCase().includes(query) ||
                 product.category.toLowerCase().includes(query) ||
                 product.code.includes(query);
        });
      }
    },
    methods: {
      addProduct() {
        console.log('Add product clicked');
        // Implement your add product logic here
        // This could open a modal or navigate to a product form
      },
      editProduct(id) {
        console.log(`Edit product with ID ${id} clicked`);
        // Implement your edit product logic here
        // This could open a modal with the product details or navigate to an edit form
      }
    }
  };
  </script>
  
  <style scoped>
  .catalog-container {
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
  
  .catalog-actions {
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
  
  .product-table {
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
  
  .action-cell {
    width: 60px;
    text-align: center;
  }
  
  .edit-btn {
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
  
  .edit-btn:hover {
    background-color: #edf2f7;
  }
  
  .edit-icon {
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z' /%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
  }
  
  .add-product-btn {
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
    transition: background-color 0.2s;
  }
  
  .add-product-btn:hover {
    background-color: #0052a3;
  }
  
  .plus-icon {
    width: 16px;
    height: 16px;
    margin-right: 8px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 6v6m0 0v6m0-6h6m-6 0H6' /%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
  }
  </style>