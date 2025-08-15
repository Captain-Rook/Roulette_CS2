<template>
    <div class="skin_box" :style="{ '--glow-color': getRarityColor, background: `linear-gradient(240deg, ${getRarityColor},rgb(3, 3, 3))` }"> 
        <div class="box_price">
            <p class="skin_price">{{skinData.price}}₽</p>
            <div v-if="forInventory" class="forInventory_box">
                <font-awesome-icon v-if="skinAction === 'saled'" :icon="['fas', 'hand-holding-dollar']" size="lg" style="color: #0ea809;" />
                <div v-else class="to_sell" @click="toSell">sell</div>
            </div>
        </div>
        <h3 class="skin_name">{{skinData.fullname}}</h3>
        <img :src="`http://127.0.0.1:8000${skinData.skin_image}`" alt="skin" class="skin_img" />
    </div>  
</template>

<script setup>
import { computed } from 'vue';
import { useInventoryStore } from '@/stores/InventoryStore.js'
import { useUserStore } from '@/stores/UserStore.js'


const inventoryStore = useInventoryStore()
const userStore = useUserStore()

const props = defineProps({
    skin: {
        type: Object,
        required: true,
        default: () => ({}),
    },
    forInventory: {
        type: Boolean,
        default: false,
    },
});

const toSell = async () => {
    if (skinAction.value === 'saled') {
        console.warn('Скин уже продан');
        return;
    }

    inventoryStore.fromInventory = true
    const skinForSaleId = props.skin.id
    const userID = userStore.user.id
    await inventoryStore.sellFirstSkin(userID, skinForSaleId)
}
const skinData = computed(() => {
  return props.skin?.skin ? props.skin.skin : props.skin
})

const skinAction = computed(() => {
  return props.skin?.action ?? null
})

const getRarityColor = computed(() => {
    const rarity = skinData.value.rare?.toLowerCase();
    switch(rarity) {
        case 'covert':
            return "#8d0707";
        case 'classified':
            return "#8d0770";
        case 'restricted':
            return "#57078d";
        case 'mil-spec grade':
            return "#07348d";
        case 'industrial grade':
            return "#474aa1";
        case 'consumer grade':
            return "#898fad";
        case 'rare':
            return "#8d7b07";
        case 'secret':
            return "#8d0707";
        default:
            return "#1ae317";
    }  
});
</script>

<style scoped>
.skin_box {
    position: relative;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: space-between;
    cursor: pointer;
    transition-duration: 0.5s;
    border-radius: 5%;
    width: 200px;
    height: 160px;
    color: rgb(255, 255, 255);
}

.box_price {
    width: 100%;
    z-index: 90;
    display: flex;
    justify-content: space-between;
    padding: 5px;
    font-weight: 700;
}

.skin_price {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: rgb(14, 168, 9);
    background: rgba(0, 0, 0, 0.57);
    padding: 3px 5px 3px 5px;
    border-radius: 8px;
    z-index: 10;
}

.to_sell { 
    z-index: 90;
}

.forInventory_box {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
}

.not_sold:hover {
    color:rgb(84, 25, 194);
    transform: scale(1.02);
}

.skin_name {
    margin: 0px 5px 5px 5px;
    font-size: 14px;
}

.skin_img {
    position: absolute;
    width: 180px;
    height: 180px;
    object-fit: contain;
}

@media (max-width: 1025px) {
    .skin_box {
        width: 160px;
        height: 120px;
    }
    .skin_img {
        width: 140px;
        height: 140px;
    }

}
</style>