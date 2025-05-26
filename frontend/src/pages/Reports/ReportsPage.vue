<template>
  <div class="reports-container">
    <h1>Reports</h1>

    <div class="reports-actions">
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
        />
        <input
          v-if="viewMode === 'monthly'"
          type="month"
          v-model="selectedMonth"
        />
        <input
          v-if="viewMode === 'yearly'"
          type="number"
          min="2000"
          max="2100"
          v-model="selectedYear"
          style="width: 90px"
        />
      </div>
      <button class="generate-report-btn" @click="downloadPDF">
        <span class="download-icon"></span>
        Download PDF
      </button>
    </div>

    <!-- Sales History Section -->
    <div class="report-section" ref="salesSection">
      <h2>Sales History</h2>
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
            <tr v-for="sale in filteredSales" :key="sale.id">
              <td>{{ sale.sell_date }}</td>
              <td>{{ sale.product_name }}</td>
              <td>{{ sale.quantity }}</td>
              <td>{{ sale.remarks || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Restock/Adjustment History Section -->
    <div class="report-section" ref="restockSection">
      <h2>Restock & Adjustment History</h2>
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
            <tr v-for="entry in filteredInventory" :key="entry.id">
              <td>{{ entry.date }}</td>
              <td>{{ entry.product_name }}</td>
              <td>{{ entry.transaction_type }}</td>
              <td>{{ entry.change_amount }}</td>
              <td>{{ entry.batch_id || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import html2pdf from "html2pdf.js";

export default {
  name: 'ReportsPage',
  data() {
    const today = new Date().toISOString().split("T")[0];
    const thisMonth = today.slice(0, 7);
    const thisYear = today.slice(0, 4);
    return {
      viewMode: "daily",
      selectedDate: today,
      selectedMonth: thisMonth,
      selectedYear: thisYear,
      sales: [],
      inventory: [],
    };
  },
  computed: {
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
        return this.inventory.filter(e => e.date === this.selectedDate);
      }
      if (this.viewMode === "monthly") {
        return this.inventory.filter(e => e.date && e.date.startsWith(this.selectedMonth));
      }
      if (this.viewMode === "yearly") {
        return this.inventory.filter(e => e.date && e.date.startsWith(this.selectedYear));
      }
      return this.inventory;
    }
  },
  mounted() {
    this.fetchSales();
    this.fetchInventory();
  },
  methods: {
    async fetchSales() {
      try {
        const res = await api.get("/api/sales/");
        this.sales = res.data.map(sale => ({
          ...sale,
          product_name: sale.product?.name || sale.product_name || 'Unknown'
        }));
      } catch (e) {
        this.sales = [];
      }
    },
    async fetchInventory() {
      try {
        const res = await api.get("/api/inventory/");
        this.inventory = res.data.map(entry => ({
          ...entry,
          product_name: entry.product?.name || entry.product_name || 'Unknown',
          date: entry.timestamp ? entry.timestamp.split('T')[0] : entry.date
        }));
      } catch (e) {
        this.inventory = [];
      }
    },
    downloadPDF() {
      // Combine both sections for PDF
      const element = document.createElement("div");
      element.innerHTML =
        `<h2>Sales History</h2>` +
        this.$refs.salesSection.innerHTML +
        `<h2>Restock & Adjustment History</h2>` +
        this.$refs.restockSection.innerHTML;
      html2pdf().from(element).set({
        margin: 0.5,
        filename: `report_${this.viewMode}_${this.getReportPeriod()}.pdf`,
        html2canvas: { scale: 1 },
        jsPDF: { unit: "in", format: "a4", orientation: "portrait" }
      }).save();
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

.view-mode {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-right: 20px;
}
.date-picker {
  margin-right: 20px;
}
.download-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23ffffff'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4' /%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}
</style>