<template>
    <div class="open-case-container">
        <Roulette />
        <div class="box-skins">
            <div v-if="skinStore.loading">Загрузка...</div>
            <div v-else-if="skinStore.error">{{ skinStore.error }}</div>
            <Skin 
                v-else
                v-for="skin in skinStore.skins"
                :key="skin.id"
                :skin="skin"
            />
        </div>
    </div>
</template>

<script setup>
import Skin from '@/components/ui/Skin.vue'
import Roulette from '@/components/Roulette.vue'
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSkinStore } from '@/stores/SkinStore.js'

const route = useRoute()
const skinStore = useSkinStore()

const loadSkins = async (id) => {
  await skinStore.fetchSkins(Number(id))
  console.log('Загруженные скины:', skinStore.skins)
}

onMounted(() => {
  loadSkins(route.params.id)
})

watch(
  () => route.params.id,
  async (newId, oldId) => {
    if (newId !== oldId) {
      await loadSkins(newId)
    }
  }
)
</script>

<style scoped>

.open-case-container {
    margin: 0 auto;
    max-width: 1700px;
    width: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    flex-direction: column;
}

.box-skins {
    max-width: 1600px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    justify-content: flex-start;
    padding: 20px;
}
    
</style>