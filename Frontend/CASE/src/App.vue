<template>
  <Header />
  <SideBar class="side_bar" />
  <main class="main-content">
    <RouterView />
  </main>
</template>

<script setup>
import Header from '@/layout/Header.vue'
import SideBar from '@/layout/SideBar.vue'
import { useUserStore } from '@/stores/UserStore.js'
import { useCaseStore } from '@/stores/CaseStore.js'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

const caseStore = useCaseStore()
const userStore = useUserStore()
const route = useRoute()

onMounted(async () => {
  await caseStore.fetchCases()
  const accessT = localStorage.getItem('access_token')
  console.log(accessT)
  try {
    const access = route.query.access || localStorage.getItem('access_token')
    const refresh = route.query.refresh || localStorage.getItem('refresh_token')

    if (route.query.access && route.query.refresh) {
      localStorage.setItem('access_token', route.query.access)
      localStorage.setItem('refresh_token', route.query.refresh)
    }

    if (access && refresh) {
      userStore.setTokens(access, refresh)
      userStore.setAuth(true)
      await userStore.setUser()
    }
  } catch (error) {
    console.error('Ошибка при восстановлении состояния авторизации:', error)
  }
})
</script>

<style>
.main-content {
  margin-left: 220px;
  padding: 20px;
  box-sizing: border-box;
}

@media (max-width: 1025px) {
  .side_bar {
    display: none;
  }
  .main-content {
    margin-left: 0px;
  }
}
</style>