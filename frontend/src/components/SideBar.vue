<template>
    <div class="sidebar">
      <img src="@/assets/img/ISM_LOGO.png" alt="ISM Logo" class="logo" />
      <nav>
        <ul>
          <li @click="navigate('/manage-account')">
            <img src="@/assets/icons/manage_account.png" alt="Manage Account" />
            <span>Manage Account</span>
          </li>
          <li @click="navigate('/product-catalog')">
            <img src="@/assets/icons/product_catalog.png" alt="Product Catalog" />
            <span>Product Catalog</span>
          </li>
          <li @click="navigate('/purchase-order')">
            <img src="@/assets/icons/purchase_order.png" alt="Purchase Order" />
            <span>Purchase Order</span>
          </li>
          <li v-if="role === 'supplier'" @click="navigate('/extra-page-1')">
            <img src="@/assets/icons/extra1.png" alt="Extra Page 1" />
            <span>Extra Page 1</span>
          </li>
          <li v-if="role === 'supplier'" @click="navigate('/extra-page-2')">
            <img src="@/assets/icons/extra2.png" alt="Extra Page 2" />
            <span>Extra Page 2</span>
          </li>
          <li @click="logout">
            <img src="@/assets/icons/logout.png" alt="Log Out" />
            <span>Log Out</span>
          </li>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      role: {
        type: String,
        required: true,
      },
    },
    methods: {
      navigate(path) {
        this.$router.push(path);
      },
      logout() {
        console.log("Logging out...");
        this.$router.push("/login");
      },
    },
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 250px;
    height: 100vh;
    background: #101540;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1rem;
  }
  
  .logo {
    width: 150px;
    margin-bottom: 1rem;
  }
  
  nav ul {
    list-style: none;
    padding: 0;
    width: 100%;
  }
  
  nav ul li {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  nav ul li:hover {
    background: rgba(255, 255, 255, 0.2);
  }
  
  nav ul li img {
    width: 24px;
    margin-right: 10px;
  }
  </style>
  