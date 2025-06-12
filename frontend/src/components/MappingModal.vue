<template>
  <BaseModal :isOpen="isOpen" title="Product Mapping" @close="$emit('close')">
    <p v-if="fetchError" class="error-message">{{ fetchError }}</p>
    <p v-if="saveError" class="error-message">{{ saveError }}</p>
    <div class="mapping-modal-content">
      <div class="form-group">
        <label for="supplier-select">Select Supplier</label>
        <select
          id="supplier-select"
          v-model="selectedSupplierId"
          class="form-control"
          @change="onSupplierChange"
        >
          <option value="">-- Select Supplier --</option>
          <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
            {{ supplier.full_name }} ({{ supplier.company_name }})
          </option>
        </select>
      </div>
      <div v-if="!selectedSupplierId" class="empty-state">
        <p>Please select a supplier to view and map their products.</p>
      </div>
      <div v-else-if="loading" class="empty-state">
        <p>Loading products...</p>
      </div>
      <div v-else-if="supplierProducts.length === 0" class="empty-state">
        <p>No supplier products found for this supplier.</p>
      </div>
      <div v-else>
        <table class="mapping-table">
          <thead>
            <tr>
              <th>Supplier Product</th>
              <th>Mapped Product</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sp in supplierProducts" :key="sp.id">
              <td>{{ sp.name }}</td>
              <td>
                <select v-model="mappings[sp.id]" class="form-control">
                  <option value="">-- Not Mapped --</option>
                  <option
                    v-for="p in products"
                    :key="p.id"
                    :value="p.id"
                    :disabled="isProductMapped(p.id, sp.id)"
                  >
                    {{ p.name }}
                  </option>
                </select>
              </td>
              <td>
                <button class="save-btn" @click="saveMapping(sp.id)">Save</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <template v-slot:footer>
      <button class="close-btn" @click="$emit('close')">Close</button>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "@/components/BaseModal.vue";
import api from "@/services/api";

export default {
  name: "MappingModal",
  components: { BaseModal },
  props: {
    isOpen: Boolean,
  },
  data() {
    return {
      suppliers: [],
      selectedSupplierId: "",
      supplierProducts: [],
      products: [],
      mappings: {}, 
      loading: false,
      fetchError: "",
      saveError: "",
    };
  },
  watch: {
    isOpen(val) {
      if (val) this.initModal();
    }
  },
  methods: {
    async initModal() {
      this.selectedSupplierId = "";
      this.supplierProducts = [];
      this.products = [];
      this.mappings = {};
      this.loading = false;
      await this.fetchSuppliers();
    },
    async fetchSuppliers() {
      try {
        const res = await api.get("/api/suppliers");
        this.suppliers = res.data;
        this.fetchError = "";
      } catch (e) {
        this.suppliers = [];
        this.fetchError = "Failed to fetch suppliers.";
      }
    },
    async onSupplierChange() {
      if (!this.selectedSupplierId) {
        this.supplierProducts = [];
        this.products = [];
        this.mappings = {};
        return;
      }
      this.loading = true;
      await Promise.all([this.fetchSupplierProducts(), this.fetchProducts(), this.fetchMappings()]);
      this.loading = false;
    },
    async fetchSupplierProducts() {
      try {
        const res = await api.get(`/api/supplier-products/by-supplier/${this.selectedSupplierId}`);
        this.supplierProducts = res.data;
        this.fetchError = "";
      } catch (e) {
        this.supplierProducts = [];
        this.fetchError = "Failed to fetch supplier products.";
      }
    },
    async fetchProducts() {
      try {
        const res = await api.get("/api/products");
        this.products = res.data;
        this.fetchError = "";
      } catch (e) {
        this.products = [];
        this.fetchError = "Failed to fetch products.";
      }
    },
    async fetchMappings() {
      try {
        const res = await api.get("/api/product-mappings");
        this.mappings = {};
        res.data.forEach(m => {
          if (m.supplier_id == this.selectedSupplierId) {
            this.mappings[m.supplier_product_id] = m.product_id;
          }
        });
        this.fetchError = "";
      } catch (e) {
        this.mappings = {};
        this.fetchError = "Failed to fetch product mappings.";
      }
    },
    isProductMapped(productId, currentSupplierProductId) {
      return Object.entries(this.mappings).some(
        ([supplierProductId, mappedProductId]) =>
          Number(supplierProductId) !== Number(currentSupplierProductId) &&
          Number(mappedProductId) === Number(productId)
      );
    },
    async saveMapping(supplierProductId) {
      this.saveError = "";
      const productId = this.mappings[supplierProductId];
      try {
        if (!productId) {
          const res = await api.get("/api/product-mappings");
          const mapping = res.data.find(
            m => m.supplier_id == this.selectedSupplierId && m.supplier_product_id == supplierProductId
          );
          if (mapping) {
            await api.delete(`/api/product-mappings/${mapping.id}`);
            this.$emit("mapping-success");
            await this.fetchMappings();
          }
          return;
        }
        await api.post("/api/product-mappings", {
          supplier_id: this.selectedSupplierId,
          supplier_product_id: supplierProductId,
          product_id: productId,
        });
        this.$emit("mapping-success");
        await this.fetchMappings();
      } catch (e) {
        this.saveError = "Failed to save mapping.";
      }
    },
  },
};
</script>

<style scoped>
.mapping-modal-content {
  padding: 8px 0;
}
.form-group {
  margin-bottom: 18px;
}
.form-group label {
  font-size: 14px;
  color: #4a5568;
  font-weight: 500;
  margin-bottom: 6px;
  display: block;
}
.mapping-table {
  width: 100%;
  border-collapse: collapse;
}
.mapping-table th, .mapping-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 14px;
}
.save-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 14px;
  cursor: pointer;
  font-size: 13px;
}
.save-btn:hover {
  background: #1d4ed8;
}
.close-btn {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  padding: 10px 24px;
  transition: background-color 0.2s;
}
.close-btn:hover {
  background-color: #cbd5e0;
}
.form-control {
  width: 100%;
  padding: 7px 8px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 13px;
}
.empty-state {
  text-align: center;
  color: #64748b;
  padding: 24px 0;
}
.error-message {
  color: #e53e3e;
  font-size: 14px;
  margin-bottom: 10px;
  text-align: center;
}
</style>