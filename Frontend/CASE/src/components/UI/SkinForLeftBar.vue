<template>
    <div @mouseenter="isHovered = true" @mouseleave="isHovered = false" 
        class="skin_box" 
        :style="{ background: `linear-gradient(160deg, ${getRarityColor},rgb(3, 3, 3))` }"
        >
        <transition name="slide-down">
            <img v-if="!isHovered" :src="`http://127.0.0.1:8000${skin.skin.skin_image}`" alt="skin" class="skin_img" />
            <img v-else :src="`http://127.0.0.1:8000${caseStore.caseCS.find(c => c.id === skin.details.from_case)?.image}`" @click="$router.push({name: 'OpenCase', params: { id: skin.details.from_case }})" alt="skin" class="case_img" />
        </transition>
        <h3 v-if="!isHovered" class="skin_name">{{skin.skin.fullname}}</h3>
        <h3 v-else class="skin_name">{{caseStore.caseCS.find(c => c.id === skin.details.from_case)?.name}}</h3>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useCaseStore } from '@/stores/CaseStore'

const caseStore = useCaseStore()
const isHovered = ref(false)

const props = defineProps({
    skin: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});

const getRarityColor = computed(() => {
    const rarity = props.skin.skin.rare?.toLowerCase();
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
    position: relative;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    font-weight: bold;
    cursor: pointer;
    color: rgb(167, 158, 158);
    width: 180px;
    height: 120px;
    overflow: hidden;
}

.skin_img {
    position: absolute;
    width: 125px;
    height: 125px;
    object-fit: contain;
    transition-duration: 0.5s;
}
.case_img {
    position: absolute;
    width: 110px;
    height: 110px;
    object-fit: contain;
    margin-bottom: 20px;
}
.skin_name {
    font-size: 14px;
    z-index: 100;
    padding-bottom: 10px;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.4s ease, opacity 0.4s ease;
}
.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}
.slide-down-enter-to {
  transform: translateY(0);
  opacity: 1;
}
.slide-down-leave-from {
  transform: translateY(0);
  opacity: 1;
}
.slide-down-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>