<template>
    <transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container" :style="{ width: width }">
          <div class="modal-header">
            <h2>{{ title }}</h2>
            <button class="close-btn" @click="closeModal">
              <span>&times;</span>
            </button>
          </div>
          
          <div class="modal-content">
            <slot></slot>
          </div>
          
          <div class="modal-footer" v-if="$slots.footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </transition>
  </template>
  
  <script>
  export default {
    name: 'BaseModal',
    props: {
      isOpen: {
        type: Boolean,
        default: false
      },
      title: {
        type: String,
        required: true
      },
      width: {
        type: String,
        default: '500px'
      }
    },
    methods: {
      closeModal() {
        this.$emit('close');
      }
    },
    mounted() {
      if (this.isOpen) {
        document.body.style.overflow = 'hidden';
      }
    },
    beforeUnmount() {
      document.body.style.overflow = 'auto';
    },
    watch: {
      isOpen(newVal) {
        if (newVal) {
          document.body.style.overflow = 'hidden';
        } else {
          document.body.style.overflow = 'auto';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    max-width: 95%;
    max-height: 95vh;
    display: flex;
    flex-direction: column;
  }
  
  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .modal-header h2 {
    margin: 0;
    font-size: 18px;
    color: #4a5568;
    font-weight: 500;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #718096;
  }
  
  .modal-content {
    padding: 24px;
    overflow-y: auto;
    max-height: calc(95vh - 130px);
  }
  
  .modal-footer {
    padding: 16px 24px;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: flex-end;
  }
  
  .modal-fade-enter-active, .modal-fade-leave-active {
    transition: opacity 0.3s;
  }
  
  .modal-fade-enter, .modal-fade-leave-to {
    opacity: 0;
  }
  
  .modal-fade-enter .modal-container,
  .modal-fade-leave-to .modal-container {
    transform: translateY(-20px);
    transition: transform 0.3s;
  }
  </style>