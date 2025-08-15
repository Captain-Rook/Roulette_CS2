<template>
    <div class="btn_list">
            <button class="info_users button_admin" @click="toUsers">users</button>
            <button class="add_skin button_admin" @click="toSkins">skins</button>
            <button class="add_case button_admin" @click="toCases">cases</button>
    </div>
</template>

<script setup>
import UserTable from '@/admin/components/UserTable.vue'
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, watch } from 'vue'

const router = useRouter()
const route = useRoute()
const host = document.documentElement

const setActiveButton = (key) => {
    const colors = {
        users: 'rgb(121, 113, 113)',
        skins: 'rgb(121, 113, 113)',
        cases: 'rgb(121, 113, 113)',
    }

    colors[key] = 'rgb(44, 44, 44)'

    host.style.setProperty('--btn-users', colors.users)
    host.style.setProperty('--btn-skins', colors.skins)
    host.style.setProperty('--btn-cases', colors.cases)
}

const toUsers = () => {
    router.push({name: 'Users'})
    setActiveButton('users')
}

const toSkins = () => {
    router.push({name: 'SkinsIditor'})
    setActiveButton('skins')
}

const toCases = () => {
    router.push({name: 'CasesIditor'})
    setActiveButton('cases')
}

const updateButtonColor = () => {
  if (route.name === 'Users') setActiveButton('users')
  else if (route.name === 'SkinsIditor') setActiveButton('skins')
  else if (route.name === 'CasesIditor') setActiveButton('cases')
}

onMounted(updateButtonColor)
watch(() => route.name, updateButtonColor)    

</script>

<style scoped>

.btn_list {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 5px;
}
.button_admin {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 60px;
    color: rgb(252, 252, 252);
    font-size: 20px;
    transition-duration: 0.2s;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
.info_users {
    background: var(--btn-users);
}
.add_skin {
    background: var(--btn-skins);
}
.add_case {
    background: var(--btn-cases);
}

</style>