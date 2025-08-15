<template>
    <header class="main_header">
        <h3 class="logo" @click="$router.push({name: 'Main'})">DAGGA CS2</h3>
        <div class="box_hed">
            <button v-if="userStore.isAuth" @click="$router.push({name: 'Users'})" class="admin_btn">Admin</button>
            <UserMenu />
        </div>
    </header>
</template>
  
<script setup>
import UserMenu from './UserMenu.vue'
import { useUserStore } from '@/stores/UserStore'

const userStore = useUserStore()
</script>

<style scoped>
.main_header {
    position: sticky;
    top: 0;
    background: rgba(12, 12, 12, 0.9);
    padding: 20px;
    text-align: center;
    font-size: 2.2rem;
    letter-spacing: 2px;
    height: 80px;
    display: flex;
    align-items: center; 
    justify-content: space-between;
    z-index: 100;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.logo {
    font-weight: bold;
    background: #2A7B9B;
    background: linear-gradient(90deg, rgba(42, 123, 155, 1) 0%, rgba(31, 120, 255, 1) 35%, rgba(177, 232, 39, 1) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    width: 350px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    cursor: pointer;
    transition-duration: 0.5s;
}
.logo:hover {
    transform: scale(1.05);
}

.box_hed {
    display: flex;
    align-items: center;
    justify-content: center
}

.admin_btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 60px;
    background: rgb(255, 136, 0);
    font-size: 20px;
    border-radius: 10%;
    transition-duration: 0.5s;
}
.admin_btn:hover {
    transform: scale(1.05);
}
@media (max-width: 1025px) {
    .admin_btn {
        width: 60px;
        height: 30px;
        font-size: 16px;
    }
    .logo {
        font-size: 24px;
    }
    .main_header {
        padding: 10px;
        font-size: 1rem;
        height: 80px;
    }
    .main_header {
        height: 50px;
        justify-content: center;
    }
    .box_hed {
        justify-content: space-between
    }
}
</style>