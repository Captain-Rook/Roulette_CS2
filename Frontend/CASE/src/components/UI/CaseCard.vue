<template>
    <div class="container_card" @click="$router.push({name: 'OpenCase', params: { id: caseCS.id }})">
        <h2 class="wrap case_name">{{caseCS.name}}</h2>
        <img :src="`http://127.0.0.1:8000${caseCS.image}`" alt="case" class="case_img" />
        <p class="wrap case_price">{{caseCS.price}} руб.</p> 
    </div>
</template>

<script setup>
const props = defineProps({
    caseCS: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});
</script>

<style scoped>
.container_card {
    padding: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    cursor: pointer;
    color:rgb(180, 90, 30);
    transition-duration: 0.5s;
    border-radius: 20px;
    font-weight: 700;
}

.case_name {
    font-size: 18px;
}
.container_card:hover {
    background: rgb(128, 127, 141);
    color:rgb(255, 255, 255);
    transform: scale(1.05);
}

.case_img {
    max-width: 200px;
    max-height: 200px;
    object-fit: contain;
}

@media (max-width: 1025px) {
  .case_img {
    max-width: 120px;
    max-height: 120px;
    object-fit: contain;
    }
    .case_name {
    font-size: 14px;
    }
    .container_card {
    padding: 20px;
    transition-duration: 0.5s;
    border-radius: 20px;
    font-weight: 700;
    }
}
</style>