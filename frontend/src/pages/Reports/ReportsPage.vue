<template>
    <div class="reports-container">
      <h1>Reports</h1>
      
      <div class="reports-actions">
        <div class="search-bar">
          <i class="search-icon"></i>
          <input 
            type="text" 
            placeholder="Search report ID" 
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
      
      <!-- Inventory Reports Section -->
      <div class="report-section">
        <h2>Inventory Report</h2>
        
        <div class="report-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Generated Date</th>
                <th>Report Name</th>
                <th class="action-cell">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in filteredInventoryReports" :key="report.id">
                <td>{{ report.id }}</td>
                <td>{{ report.generatedDate }}</td>
                <td>{{ report.name }}</td>
                <td class="action-cell">
                  <button 
                    class="download-btn" 
                    @click="downloadReport(report.id, 'inventory')"
                    title="Download report"
                  >
                    <i class="download-icon"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Sales Reports Section -->
      <div class="report-section">
        <h2>Sales Report</h2>
        
        <div class="report-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Date Generated</th>
                <th>Report Content</th>
                <th class="action-cell">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in filteredSalesReports" :key="report.id">
                <td>{{ report.id }}</td>
                <td>{{ report.generatedDate }}</td>
                <td>{{ report.content }}</td>
                <td class="action-cell">
                  <button 
                    class="download-btn" 
                    @click="downloadReport(report.id, 'sales')"
                    title="Download report"
                  >
                    <i class="download-icon"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <button class="generate-report-btn" @click="generateReport">
        <i class="plus-icon"></i>
        Generate Report
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ReportsPage',
    data() {
      return {
        searchQuery: '',
        inventoryReports: [
          {
            id: 1,
            generatedDate: '01/5/2024',
            name: 'Inventory Report April 2024'
          },
          {
            id: 2,
            generatedDate: '15/5/2024',
            name: 'Inventory Report March 2024'
          }
        ],
        salesReports: [
          {
            id: 1,
            generatedDate: '06/5/2024',
            content: 'Sales Report April 2024'
          },
          {
            id: 2,
            generatedDate: '15/6/2024',
            content: 'Sales Report March 2024'
          }
        ]
      };
    },
    computed: {
      filteredInventoryReports() {
        if (!this.searchQuery) {
          return this.inventoryReports;
        }
        
        const query = this.searchQuery.toLowerCase();
        return this.inventoryReports.filter(report => {
          return report.id.toString().includes(query) ||
                 report.name.toLowerCase().includes(query) ||
                 report.generatedDate.includes(query);
        });
      },
      filteredSalesReports() {
        if (!this.searchQuery) {
          return this.salesReports;
        }
        
        const query = this.searchQuery.toLowerCase();
        return this.salesReports.filter(report => {
          return report.id.toString().includes(query) ||
                 report.content.toLowerCase().includes(query) ||
                 report.generatedDate.includes(query);
        });
      }
    },
    methods: {
      generateReport() {
        console.log('Generate report clicked');
        // Implement your generate report logic here
        // This could open a modal or navigate to a report generation form
      },
      downloadReport(id, type) {
        console.log(`Download ${type} report with ID ${id} clicked`);
        // Implement your download report logic here
        // This would typically trigger a file download
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
  
  .action-cell {
    width: 60px;
    text-align: center;
  }
  
  .download-btn {
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
  
  .download-btn:hover {
    background-color: #edf2f7;
  }
  
  .download-icon {
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4' /%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
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
    margin-left: auto;
    transition: background-color 0.2s;
  }
  
  .generate-report-btn:hover {
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