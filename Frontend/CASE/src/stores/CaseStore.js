import { defineStore } from "pinia";
import api from '@/services/api';

export const useCaseStore = defineStore("caseStore", {
  state: () => ({
    caseCS: [],
    loading: false,
    error: null,
    rouletteCase: [],
    translateX: '0px',
    endAnimation: false
  }),
  

  actions: {
    async fetchCases() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await api.get('/cases/');
        this.caseCS = response.data;
      } catch (error) {
        this.error = error.message;
        console.error('Ошибка при загрузке кейсов:', error);
      } finally {
        this.loading = false;
      }
    },
    async getRouletteCase(caseID) {
        const response = await api.get(`/cases/${caseID}/`);
        this.rouletteCase = response.data;
    }
  }
});
