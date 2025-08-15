import { defineStore } from "pinia";
import api from '@/services/api';

export const useUserStore = defineStore("userStore", {
  state: () => ({
    isAdmin: true,
    isAuth: localStorage.getItem('isAuth') === 'true',
    user: null,
    balance: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),
  actions: {
    setTokens(access, refresh) {
      console.log('Setting tokens:', { access: access?.slice(0, 10) + '...', refresh: refresh?.slice(0, 10) + '...' });
      this.accessToken = access;
      this.refreshToken = refresh;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      if (access) {
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      }
    },
    setAuth(status) {
      console.log('Setting auth status:', status);
      this.isAuth = status;
      localStorage.setItem('isAuth', status);
    },
    async setBalance() {
      try {
        if(!this.isAuth) return
          const response = await api.get('/auth/user/');
          this.balance = response.data.balance
      } catch(error) {
        this.error = error
      }
    },
    logout() {
      console.log('Logging out user');
      this.isAuth = false;
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('isAuth');
      delete api.defaults.headers.common['Authorization'];
    },
    async setUser() {
      try {
        if (!this.accessToken) {
          console.log('No access token available');
          this.logout();
          return null;
        }

        console.log('Fetching user data...');
        console.log('Current access token:', this.accessToken?.slice(0, 10) + '...');
        
        const response = await api.get('/auth/user/');
        console.log('User data received:', response.data);
        
        this.user = response.data;
        this.balance = response.data.balance;
        this.isAuth = true;
        localStorage.setItem('isAuth', 'true');
        return response.data;
      } catch (error) {
        console.error('Error fetching user data:', error);
        if (error.response) {
          console.error('Error response:', {
            status: error.response.status,
            data: error.response.data
          });
        }
        if (error.response?.status === 401) {
          this.logout();
        }
        throw error;
      }
    }
  }
})