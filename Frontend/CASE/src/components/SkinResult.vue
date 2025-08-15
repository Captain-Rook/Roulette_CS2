<template>
    <div v-if="shouldShowResult" class="container_result_skin">
        <div class="box_result_skin">
            <h3 class="skin_name">{{skinStoreRoulette.resultingSkin?.fullname}}</h3>
            <img :src="`http://127.0.0.1:8000${skinStoreRoulette.resultingSkin?.skin_image}`" alt="skin" class="skin_img" />
            <div class="btn_list">
                <button @click="oneMore" class="btn_result">one more</button>
                <button @click="sellSkin" class="btn_result">Sell for {{skinStoreRoulette.resultingSkin?.price}}</button>
            </div>
        </div>  
    </div>
</template>

<script setup>
import { useSkinStore } from '@/stores/SkinStore'
import { useCaseStore } from '@/stores/CaseStore'
import { useInventoryStore } from '@/stores/InventoryStore'
import { useUserStore } from '@/stores/UserStore'
import { onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const skinStoreRoulette = useSkinStore()
const caseStoreRoulette = useCaseStore()
const inventoryStore = useInventoryStore()
const userStore = useUserStore()

const userID = userStore.user.id

const resetState = () => {
    console.log('Сброс состояния - текущий маршрут:', route.name)
    skinStoreRoulette.isOpen = false
    caseStoreRoulette.translateX = '0px'
    caseStoreRoulette.endAnimation = false
}

const shouldShowResult = computed(() => {
    return skinStoreRoulette.resultingSkin && caseStoreRoulette.rouletteCase
})

const oneMore = async () => {
    if (skinStoreRoulette && caseStoreRoulette) {
        skinStoreRoulette.isOpen = false
        caseStoreRoulette.translateX = '0px'
        caseStoreRoulette.endAnimation = false
    }
}

const sellSkin = async () => {
    inventoryStore.fromInventory = false
    const success = await inventoryStore.sellFirstSkin(userID)
    if (success) {
    skinStoreRoulette.resultingSkin = null
    skinStoreRoulette.isOpen = false
    caseStoreRoulette.translateX = '0px'
    caseStoreRoulette.endAnimation = false
  }
}

</script>

<style scoped>
.container_result_skin {
    position: relative;
    width: 600px;
    height: 600px;
    background: rgba(41, 8, 8, 0.97);
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5%;
    z-index: 100;
}
.box_result_skin {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 10px;
}
.btn_list {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    margin-top: 50%
}
.btn_result {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    width: 120px;
    height: 60px;
    background: rgb(255, 136, 0);
    font-size: 20px;
    border-radius: 10%;
    margin: 20px;
    transition-duration: 0.5s;
}

.skin_img {
    position: absolute;
    width: 300px;
    height: 300px;
}

.skin_name {
    margin-bottom: 50%
}
</style>