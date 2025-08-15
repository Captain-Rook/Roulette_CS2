<template>
    <div class="skin_box" :style="{ background: `linear-gradient(60deg, ${getRarityColor},rgb(3, 3, 3))` }"> 
        <img :src="`http://127.0.0.1:8000${skinsRoulette.skin_image}`" alt="skin" class="skin_img" />
        <h3 class="skin_name">{{skinsRoulette.fullname}}</h3>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    skinsRoulette: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});

const getRarityColor = computed(() => {
    const rarity = props.skinsRoulette.rare?.toLowerCase();
    switch(rarity) {
        case 'covert':
            return "#a11b1b";
        case 'classified':
            return "#f013c0";
        case 'restricted':
            return "#62078c";
        case 'mil-spec grade':
            return "#301eeb";
        case 'industrial grade':
            return "#474aa1";
        case 'consumer grade':
            return "#898fad";
        case 'rare':
            return "#FFD700";
        case 'secret':
            return "#a11b1b";
        default:
            return "#1ae317";
    }  
});
</script>

<style scoped>
.skin_box {
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    cursor: pointer;
    color: rgb(12, 8, 24);
    border-radius: 20px;
    width: 200px;
    height: 300px;
}

.skin_img {
    position: absolute;
    width: 180px;
    height: 180px;
    object-fit: contain;
}

.skin_name {
    margin-top: 80%;
    font-size: 14px;
    z-index: 100;
}

</style>