<template>
  <BaseModal :isOpen="true" title="Sell Product" @close="$emit('close')">
    <div class="product-form">
      <div class="form-group">
        <label for="sellQuantity">Quantity to Sell:</label>
        <input
          id="sellQuantity"
          type="number"
          v-model.number="quantity"
          :max="maxQuantity"
          min="1"
          class="form-control"
        />
        <small class="form-text">Available: {{ maxQuantity }}</small>
      </div>
      <div class="form-group">
        <label for="sellDate">Sell Date:</label>
        <input
          id="sellDate"
          type="date"
          v-model="sellDate"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="remarks">Remarks (optional):</label>
        <input
          id="remarks"
          type="text"
          v-model="remarks"
          class="form-control"
        />
      </div>
    </div>
    <template v-slot:footer>
      <button class="submit-btn" @click="submitSale" :disabled="!isValid">
        Complete Sale
      </button>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "@/components/BaseModal.vue";
import api from "@/services/api";

export default {
  name: "SalesModal",
  components: { BaseModal },
  props: {
    product: Object,
  },
  data() {
    return {
      quantity: 1,
      sellDate: new Date().toISOString().split("T")[0],
      remarks: "",
      maxQuantity: this.product
        ? this.product.batches.reduce((sum, b) => sum + (b.quantity || 0), 0)
        : 0,
    };
  },
  computed: {
    isValid() {
      return (
        this.quantity > 0 &&
        this.quantity <= this.maxQuantity &&
        !!this.sellDate
      );
    },
  },
  methods: {
    async submitSale() {
      try {
        await api.post(`/api/sales/`, {
            product_id: this.product.id,
            quantity: this.quantity,
            sell_date: this.sellDate,
            remarks: this.remarks,
            });
        this.$emit("close");
      } catch (error) {
        alert("Failed to process sale.");
      }
    },
  },
};
</script>

<style scoped>
.product-form {
  width: 100%;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 6px;
}
.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 14px;
}
.form-text {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #718096;
}
.submit-btn {
  padding: 10px 24px;
  background-color: #0066cc;
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
  background-color: #0052a3;
}
</style>