<template>
  <div class="reports-container">
    <h1>Reports</h1>

    <div class="reports-actions">
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
      <div class="button-group">
        <button class="generate-report-btn" @click="downloadSalesPDF">
          <span class="download-icon"></span>
          Download Sales PDF
        </button>
        <button class="generate-report-btn" @click="downloadInventoryPDF">
          <span class="download-icon"></span>
          Download Restock/Adjustment PDF
        </button>
      </div>
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
              <td>{{ entry.created_at ? entry.created_at.split('T')[0] : '-' }}</td>
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
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default {
  name: 'ReportsPage',
  data() {
    const savedViewMode = localStorage.getItem('reportsViewMode') || "daily";
    const today = new Date().toLocaleDateString('en-CA');
    const thisMonth = today.slice(0, 7);
    const thisYear = today.slice(0, 4);
    return {
      viewMode: savedViewMode,
      selectedDate: today,
      selectedMonth: thisMonth,
      selectedYear: thisYear,
      sales: [],
      inventory: [],
    };
  },
  watch: {
    viewMode(newVal) {
      localStorage.setItem('reportsViewMode', newVal);
    }
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
        return this.inventory.filter(e => e.created_at && e.created_at.split('T')[0] === this.selectedDate);
      }
      if (this.viewMode === "monthly") {
        return this.inventory.filter(e => e.created_at && e.created_at.startsWith(this.selectedMonth));
      }
      if (this.viewMode === "yearly") {
        return this.inventory.filter(e => e.created_at && e.created_at.startsWith(this.selectedYear));
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
        this.sales = res.data;
      } catch (e) {
        this.sales = [];
      }
    },
    async fetchInventory() {
      try {
        const res = await api.get("/api/inventory/");
        this.inventory = res.data;
      } catch (e) {
        this.inventory = [];
      }
    },
    downloadSalesPDF() {
      const doc = new jsPDF();
      doc.setFontSize(18);
      doc.text("Sales Report", 14, 18);
      doc.setFontSize(12);
      doc.text(`Period: ${this.getReportPeriod()}`, 14, 28);

      autoTable(doc, {
        startY: 34,
        head: [["Date", "Product", "Quantity", "Remarks"]],
        body: this.filteredSales.map(sale => [
          sale.sell_date,
          sale.product_name,
          sale.quantity,
          sale.remarks || "-"
        ]),
        theme: 'grid',
        headStyles: { fillColor: [0, 102, 204] },
        styles: { fontSize: 11 }
      });

      doc.save(`sales_report_${this.viewMode}_${this.getReportPeriod()}.pdf`);
    },
    downloadInventoryPDF() {
      const doc = new jsPDF();
      doc.setFontSize(18);
      doc.text("Restock & Adjustment Report", 14, 18);
      doc.setFontSize(12);
      doc.text(`Period: ${this.getReportPeriod()}`, 14, 28);

      autoTable(doc, {
        startY: 34,
        head: [["Date", "Product", "Type", "Quantity", "Batch"]],
        body: this.filteredInventory.map(entry => [
          entry.created_at ? entry.created_at.split('T')[0] : '-',
          entry.product_name,
          entry.transaction_type,
          entry.change_amount,
          entry.batch_id || '-'
        ]),
        theme: 'grid',
        headStyles: { fillColor: [0, 102, 204] },
        styles: { fontSize: 11 }
      });

      doc.save(`restock_report_${this.viewMode}_${this.getReportPeriod()}.pdf`);
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

.button-group {
  display: flex;
  gap: 12px;
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
  transition: background-color 0.2s;
  white-space: nowrap;
}

.generate-report-btn:hover {
  background-color: #0052a3;
}

.download-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23ffffff'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4' /%3E%3C/svg%3E");
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
</style>