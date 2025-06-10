<template>
  <BaseToast :message="message" type="success" :duration="duration" @close="$emit('close')" />
</template>

<script>
import BaseToast from './BaseToast.vue';
export default {
  name: "SuccessToast",
  components: { BaseToast },
  props: {
    message: { type: String, required: true },
    duration: { type: Number, default: 3000 }
  }
};
</script>