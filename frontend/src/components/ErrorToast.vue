<template>
  <BaseToast :message="message" type="error" :duration="duration" @close="$emit('close')" />
</template>

<script>
import BaseToast from './BaseToast.vue';
export default {
  name: "ErrorToast",
  components: { BaseToast },
  props: {
    message: { type: String, required: true },
    duration: { type: Number, default: 3000 }
  }
};
</script>