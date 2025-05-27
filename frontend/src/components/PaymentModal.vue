<template>
  <BaseModal :isOpen="true" title="Payment" @close="$emit('close')">
    <div class="payment-modal-content">
      <h3>Supplier Bank Details</h3>
      <div v-if="bankInfo" class="bank-details">
        <div><strong>Bank Name:</strong> {{ bankInfo.bank_name }}</div>
        <div><strong>Account Number:</strong> {{ bankInfo.account_number }}</div>
        <div><strong>Account Holder:</strong> {{ bankInfo.account_holder }}</div>
      </div>
      <div v-else class="bank-details">
        <em>No bank info available for this supplier.</em>
      </div>
      <div class="upload-section">
        <label for="receipt-upload">Upload Payment Receipt (PDF):</label>
        <input id="receipt-upload" type="file" accept="application/pdf" @change="onFileChange" />
        <div v-if="fileName" class="file-name">Selected: {{ fileName }}</div>
      </div>
      <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
    </div>
    <template v-slot:footer>
      <button class="submit-btn" :disabled="!file" @click="submitPayment">
        Submit Payment
      </button>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "@/components/BaseModal.vue";
import api from "@/services/api";

export default {
  name: "PaymentModal",
  components: { BaseModal },
  props: {
    order: Object,
  },
  data() {
    return {
      file: null,
      fileName: "",
      uploadError: "",
      bankInfo: null,
    };
  },
  async mounted() {
    if (this.order && this.order.supplier_id) {
      try {
        const res = await api.get(`/api/supplier-bank-accounts/by-supplier/${this.order.supplier_id}`);
        this.bankInfo = res.data.length > 0 ? res.data[0] : null;
      } catch (e) {
        this.bankInfo = null;
      }
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      if (file && file.type === "application/pdf") {
        this.file = file;
        this.fileName = file.name;
        this.uploadError = "";
      } else {
        this.file = null;
        this.fileName = "";
        this.uploadError = "Please select a PDF file.";
      }
    },
    async submitPayment() {
      if (!this.file) {
        this.uploadError = "Please upload a PDF receipt.";
        return;
      }
      try {
        const formData = new FormData();
        formData.append("file", this.file);
        await api.post(`/api/purchase-orders/${this.order.id}/payment`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.$emit("payment-success");
      } catch (e) {
        this.uploadError = "Failed to upload payment receipt.";
      }
    },
  },
};
</script>

<style scoped>
.payment-modal-content {
  padding: 8px 0;
}
.bank-details {
  margin-bottom: 18px;
  font-size: 15px;
}
.upload-section {
  margin-bottom: 18px;
}
.file-name {
  margin-top: 6px;
  font-size: 13px;
  color: #2563eb;
}
.error-message {
  color: #e53e3e;
  font-size: 14px;
  margin-top: 8px;
}
.submit-btn {
  padding: 10px 24px;
  background-color: #059669;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.submit-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}
.submit-btn:hover:not(:disabled) {
  background-color: #047857;
}
</style>