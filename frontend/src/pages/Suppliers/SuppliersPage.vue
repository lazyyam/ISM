<template>
    <div class="suppliers-container">
      <h1>Suppliers</h1>
      
      <div class="suppliers-actions">
        <div class="search-bar">
          <i class="search-icon"></i>
          <input 
            type="text" 
            placeholder="Search Supplier by name, company, or phone number" 
            v-model="searchQuery"
          />
        </div>
      </div>

      <div v-if="loading" class="loading-message">Loading suppliers...</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <div class="suppliers-table">
        <table>
          <thead>
            <tr>
              <th>No. </th>
              <th>Name</th>
              <th>Company</th>
              <th>Address</th>
              <th>Phone no.</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(supplier, index) in paginatedSuppliers" :key="supplier.id">
              <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
              <td>{{ supplier.full_name }}</td>
              <td>{{ supplier.company_name }}</td>
              <td>{{ supplier.company_address }}</td>
              <td>
                <div class="whatsapp-container">
                  <a 
                    :href="`https://wa.me/${supplier.phone_number.replace(/\D/g, '')}`" 
                    target="_blank" 
                    class="whatsapp-link"
                  >
                    <img 
                      :src="require(`@/assets/icons/whatsapp_icon.svg`)" 
                      alt="WhatsApp" 
                      class="whatsapp-icon"
                    />
                  </a>
                  <span class="phone-text">{{ supplier.phone_number }}</span>
                </div>
              </td>
              <td>{{ supplier.email }}</td>
            </tr>
          </tbody>
          <tr v-if="filteredSuppliers.length === 0">
            <td colspan="7" style="text-align: center;">No suppliers found.</td>
          </tr>
        </table>
        <div class="pagination">
          <button @click="currentPage--" :disabled="currentPage === 1" title="Previous">
            &lt;
          </button>
          <span>
            Page
            <input
              type="number"
              v-model.number="pageInput"
              @change="goToPage"
              :min="1"
              :max="totalPages"
              style="width: 40px; text-align: center;"
            />
            of {{ totalPages }}
          </span>
          <button @click="currentPage++" :disabled="currentPage === totalPages" title="Next">
            &gt;
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from "@/services/api";

  export default {
    name: 'SuppliersPage',
    data() {
      return {
        currentPage: 1,
        pageSize: 5,
        pageInput: 1,
        searchQuery: '',
        suppliers: [],
        loading: false,
        errorMessage: "",
      };
    },
    mounted() {
        this.fetchSuppliers();
    },
    watch: {
      currentPage(val) {
        this.pageInput = val;
      },
      searchQuery() {
        this.currentPage = 1;
      }
    },
    computed: {
      paginatedSuppliers() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.filteredSuppliers.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.filteredSuppliers.length / this.pageSize) || 1;
      },
      filteredSuppliers() {
        if (!this.searchQuery) {
          return this.suppliers;
        }
        
        const query = this.searchQuery.toLowerCase();
        return this.suppliers.filter(supplier => {
          return supplier.full_name.toLowerCase().includes(query) ||
                 supplier.company_name.toLowerCase().includes(query) ||
                 supplier.phone_number.includes(query);
        });
      }
    },
    methods: {
      goToPage() {
        if (this.pageInput < 1) this.pageInput = 1;
        if (this.pageInput > this.totalPages) this.pageInput = this.totalPages;
        this.currentPage = this.pageInput;
      },
      async fetchSuppliers() {
        this.loading = true;
        this.errorMessage = "";
        try {
          const response = await api.get('/api/suppliers');
          this.suppliers = response.data;
        } catch (error) {
          this.suppliers = [];
          this.errorMessage = "Failed to fetch suppliers. Please try again.";
        } finally {
          this.loading = false;
        }
      },
    }
  };
  </script>
  
  <style scoped>
  .suppliers-container {
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
  
  .suppliers-actions {
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
  
  .chevron-down {
    width: 16px;
    height: 16px;
    margin-left: 8px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23718096'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7' /%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
  }
  
  .suppliers-table {
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
  
  .add-supplier-btn {
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
  
  .add-supplier-btn:hover {
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

  .whatsapp-container {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .whatsapp-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    transition: background-color 0.3s ease;
  }

  .whatsapp-link:hover {
    background-color: #25d36633;
    transform: scale(1.1);
  }

  .whatsapp-icon {
    width: 18px;
    height: 18px;
  }

  .phone-text {
    color: #2d3748;
    font-size: 14px;
  }

  .loading-message {
    color: #2d3748;
    font-size: 15px;
    padding: 12px 16px;
  }
  .error-message {
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

  /* Hide number on mobile */
  @media (max-width: 640px) { 
    .phone-text {
      display: none;
    }
  }
  </style>