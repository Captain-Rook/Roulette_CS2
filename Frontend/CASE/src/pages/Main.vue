<template>
    <div class="container">
        <div v-if="caseStore.loading" class="loading">
            Загрузка кейсов...
        </div>
        <div v-else-if="caseStore.error" class="error">
            {{ caseStore.error }}
        </div>
        <div v-else class="cases-grid">
            <CaseCard 
                v-for="caseCS of caseStore.caseCS" 
                :key="caseCS.id" 
                :caseCS="caseCS"
            />
        </div>
    </div>
</template>
  
<script setup>
import CaseCard from '@/components/ui/CaseCard.vue'
import { useCaseStore } from '@/stores/CaseStore.js'
import { onMounted } from 'vue'

const caseStore = useCaseStore();


onMounted(async () => {
    await caseStore.fetchCases()
})
</script>
  
<style scoped>
.container {
    margin: 0 auto;
    max-width: 1400px;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.cases-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    width: 100%;
}

.loading, .error {
    width: 100%;
    text-align: center;
    padding: 20px;
    font-size: 18px;
}

.error {
    color: red;
}


</style>
  