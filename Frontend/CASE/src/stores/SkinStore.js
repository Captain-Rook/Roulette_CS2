import { defineStore } from "pinia";
import api from '@/services/api';

export const useSkinStore = defineStore("skinStore", {
  state: () => ({
    skins: [],
    loading: false,
    error: null,
    skinsRoulette: [],
    resultingSkin: [],
    isOpen: false
  }),

  actions: {
    async fetchSkins(caseID) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await api.get(`/cases/${caseID}/`);
        this.skins = response.data.skins;
      } catch (error) {
        this.error = error.message;
        console.error('Ошибка при загрузке скинов:', error);
      } finally {
        this.loading = false;
      }
    },

    async shuffleSkinsToRoulette(caseID) {
      let shuffledSkins = [];
      const response = await api.get(`/cases/${caseID}/open_case/`)
      
      this.resultingSkin = response.data
      console.log('Полученный скин: ' + JSON.stringify(this.resultingSkin))
      
      while (shuffledSkins.length < 65) {
        shuffledSkins = [...shuffledSkins, ...this.skins];
      }
     
      shuffledSkins = shuffledSkins.slice(0, 60);
      
      for (let i = shuffledSkins.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledSkins[i], shuffledSkins[j]] = [shuffledSkins[j], shuffledSkins[i]];
      }
      this.skinsRoulette = shuffledSkins;
      this.skinsRoulette[56] = this.resultingSkin;
    }
  },
});