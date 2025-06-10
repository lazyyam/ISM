<template>
  <transition name="toast-fade">
    <div v-if="visible" :class="['base-toast', type]" @mouseenter="pause" @mouseleave="resume">
      <slot>
        {{ message }}
      </slot>
      <button class="close-btn" @click="close">&times;</button>
    </div>
  </transition>
</template>

<script>
export default {
  name: "BaseToast",
  props: {
    message: { type: String, default: "" },
    type: { type: String, default: "info" }, 
    duration: { type: Number, default: 3000 }
  },
  data() {
    return {
      visible: true,
      timer: null,
      remaining: this.duration,
      start: null
    };
  },
  mounted() {
    this.startTimer();
  },
  methods: {
    close() {
      this.visible = false;
      this.$emit("close");
    },
    startTimer() {
      this.start = Date.now();
      this.timer = setTimeout(this.close, this.remaining);
    },
    pause() {
      clearTimeout(this.timer);
      this.remaining -= Date.now() - this.start;
    },
    resume() {
      this.startTimer();
    }
  }
};
</script>

<style scoped>
.base-toast {
  min-width: 220px;
  max-width: 350px;
  padding: 14px 24px 14px 18px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  color: #2d3748;
  background: #f8fafc;
  position: fixed;
  top: 32px;
  right: 32px;
  z-index: 2000;
  display: flex;
  align-items: center;
  font-size: 15px;
  animation: slide-in 0.3s;
}
.base-toast.success {
  background: #e6fffa;
  color: #2c7a7b;
  border-left: 5px solid #38b2ac;
}
.base-toast.error {
  background: #fff5f5;
  color: #c53030;
  border-left: 5px solid #e53e3e;
}
.base-toast.info {
  background: #ebf8ff;
  color: #3182ce;
  border-left: 5px solid #4299e1;
}
.close-btn {
  background: none;
  border: none;
  color: #a0aec0;
  font-size: 20px;
  margin-left: 16px;
  cursor: pointer;
}
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.3s;
}
.toast-fade-enter, .toast-fade-leave-to {
  opacity: 0;
}
@keyframes slide-in {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>