import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUsersStore = defineStore('usersStore', {
  state: () => ({
    users: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchUsers() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/users/')
        this.users = response.data
      } catch (err) {
        this.error = err
        console.error('Ошибка загрузки пользователей:', err)
      } finally {
        this.loading = false
      }
    }
  }
})