<template>
  <span class='cs cs-css'> <span>борис лох</span></span>
    <div class="inventory_container">
        <Skin
          forInventory
          v-for="item in inventoryStore.inventory"
          :key="item.id"
          :skin="item"
        />
        <div class="arrow_box">
          <font-awesome-icon icon="fa-solid fa-arrow-left" size="lg" class="arrow" @click="inventoryStore.loadPage(inventoryStore.previousPageUrl)"/>
          <font-awesome-icon icon="fa-solid fa-arrow-right" size="lg" class="arrow" @click="inventoryStore.loadPage(inventoryStore.nextPageUrl)"/>        
        </div>
    </div>
    
</template>

<script setup>
import { onMounted } from 'vue'
import { useInventoryStore } from '@/stores/InventoryStore.js'
import { useRoute } from 'vue-router'
import Skin from '@/components/ui/Skin.vue'

const inventoryStore = useInventoryStore()


const route = useRoute()
const userID = Number(route.params.id)

onMounted(async () => {
    inventoryStore.getInventory(userID)
    console.log(inventoryStore.inventory)
})
</script>

<style scoped>
.inventory_container {
  margin: 0 auto;
  max-width: 1500px;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  justify-content: flex-start;
  padding: 20px;
}
.arrow_box {
  margin: 0 auto;
  max-width: 1500px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 5px;
  cursor: pointer;
  overflow: hidden;
  margin-bottom: 20px;
  user-select: none;
}

.arrow {
  color:rgb(35, 124, 184);
  font-size: 20px;
  display: inline-block;
  transition: transform 0.3s, color 0.3s;
}

.arrow:hover {
  color:rgb(80, 54, 228);
  transform: scale(1.05);
}

</style>