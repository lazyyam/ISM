<template>
  <BaseModal
    :isOpen="isOpen"
    title="Confirm Delete"
    @close="$emit('close')"
  >
    <div>
      <p>{{ message || "Are you sure you want to delete this order?" }}</p>
    </div>
    <template v-slot:footer>
      <button class="close-btn" @click="$emit('close')">Cancel</button>
      <button class="modal-delete-btn" @click="$emit('confirm')">Delete</button>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "@/components/BaseModal.vue";
export default {
  name: "DeleteModal",
  components: { BaseModal },
  props: {
    isOpen: { type: Boolean, default: false },
    message: { type: String, default: "" }
  }
};
</script>

<style scoped>
.close-btn, .modal-delete-btn {
  min-width: 110px;
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 14px;
  border: none;
  cursor: pointer;
  margin-left: 8px;
  transition: background-color 0.2s;
  box-sizing: border-box;
}
.close-btn {
  background-color: #e2e8f0;
  color: #4a5568;
}
.close-btn:hover {
  background-color: #cbd5e0;
}
.modal-delete-btn {
  background-color: #e53e3e;
  color: white;
}
.modal-delete-btn:hover {
  background-color: #b91c1c;
}
</style>