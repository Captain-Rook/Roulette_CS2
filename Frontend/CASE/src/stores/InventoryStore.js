import { defineStore } from "pinia";
import api from '@/services/api';
import { useUserStore } from './UserStore'

export const useInventoryStore = defineStore('inventoryStore', {
    state: () => ({
        inventory: [],
        nextPageUrl: 2,
        previousPageUrl: null,
        skinForSale: null,
        fromInventory: false,
        latestList: []
    }),
    actions: {
       async getInventory(userID) {
        try {
            const response = await api.get(`/users/${userID}/inventory/?page=1`)
            this.inventory = response.data.results
            this.nextPageUrl = response.data.next
            this.previousPageUrl = response.data.previous
        } catch(error) {
            this.error = error
        }
            
        },
        async loadPage(url) {
            if (!url) return;
            const cleanUrl = url.replace('http://127.0.0.1:8000/api/v1', '');
            const response = await api.get(cleanUrl);
            this.inventory = response.data.results;
            this.nextPageUrl = response.data.next;
            this.previousPageUrl = response.data.previous;
        },
        async executeTransaction(transaction) {
            try {
              if (!transaction) {
                console.error("skinId is undefined");
                return;
            }
            await api.put(`/transactions/${transaction}/sell_item/`, {});  
            } catch (err) {
                console.error("Ошибка при продаже скина:", err?.response?.data || err.message);
            }
        },
        async sellFirstSkin(userID, skinForSaleId) {
            this.skinForSale = null
            if(!this.fromInventory) {
                await this.getInventory(userID)
                this.skinForSale = this.inventory[0].id
            } else{
                this.skinForSale = skinForSaleId
            }
            const transaction = this.inventory.find(item => item.id === this.skinForSale)
            transaction.action = 'saled';
            if (!transaction) {
              console.error("Нет id у resultingSkin")
              return false
            }
            await this.executeTransaction(transaction.id)
            const userStore = useUserStore()
            await userStore.setBalance()
            return true
          },
          async getLatestList() {
            const response = await api.get('/transactions/latest/')
            this.latestList = response.data
          }

    },

})