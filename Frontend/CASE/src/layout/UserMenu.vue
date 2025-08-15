<template>
    <button v-if="!userStore.isAuth" class="login" @click="handleLogin">Login</button>
    <div v-else-if="userStore.user" class="user_box">
        <img 
            :src="userStore.user.avatar"
            alt="profile" 
            class="icon"
            @error="handleImageError" 
            @click="$router.push({name: 'Inventory', params: { id: userStore.user.id }})"
        />
        <div class="inf_txt">
            <p class="user_name">{{userStore.user.username}}</p>
            <p class="balance">{{userStore.balance}}</p>
        </div>
            <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']" size="2xs" style="color: #0c186e;" @click="handleLogout"/>
    </div>
</template>

<script setup>
import prof_test from '@/assets/prof_test.jpg'
import { useUserStore } from '@/stores/UserStore.js'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

async function handleLogout() {
    try {
    userStore.logout()
        router.push('/')
    } catch(e) {
        console.error('не получается выйти', e)
    }
}

const handleLogin = () => {
    window.location.href = 'http://127.0.0.1:8000/api/v1/auth/steam/'
}

const handleImageError = (e) => {
    e.target.src = prof_test
}
</script>

<style scoped>
.login {
    font-size: 16px;
    color: rgb(253, 206, 66);
    width: 100px;
    height: 50px;
    border: 1px solid rgb(253, 206, 66);
    border-radius: 10px;
    transition: 0.3s ease;
}
.login:hover {
    border-color: #ccc;
    transform: scale(1.05);
}
.login:active {
    border-color: rgb(39, 197, 150);
}
.user_box {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 10px;
    gap: 15px;
    cursor: pointer;
}

.icon {
    height: 55px;
    width: 55px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #666;
    transition: 0.3s ease;
}

.icon:hover {
    border-color: #ccc;
}

.inf_txt {
    display: flex;
    flex-direction: column;
    font-size: 1rem;
    gap: 5px;
}

.user_name {
    font-weight: bold;
    color: #333;
    transition: all 0.3s ease;
}
.user_name:hover {
    color: #ccc;
}
.balance {
    color: #666;
    transition: all 0.3s ease;
}
.balance:hover {
    color: #ccc;
}

@media (max-width: 1025px) {
    .login {
        font-size: 14px;
        width: 60px;
        height: 30px;
    }
    .icon {
        height: 25px;
        width: 25px;
        margin-left: 30px;
    }
    .inf_txt {
        font-size: 0.4rem;
        gap: 2px;
    }

    .user_name {
        font-size: 0.4rem;
    }
}
</style>