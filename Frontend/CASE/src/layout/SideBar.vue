<template>
    <div class="sidebar">
        <div class="sidebar_content">
            <TransitionGroup name="list" tag="div" class="card-list">
                <SkinForLeftBar
                    v-for="item in inventoryStore.latestList"
                    :key="item.id"
                    :skin="item"
                />
            </TransitionGroup>
        </div>
    </div>
</template>

<script setup>
import SkinForLeftBar from '@/components/ui/SkinForLeftBar.vue'
import { useInventoryStore } from '@/stores/InventoryStore.js'
import { onMounted } from 'vue'

const inventoryStore = useInventoryStore()


setInterval(async () => {
  await inventoryStore.getLatestList()
}, 5000)


onMounted(async () => {
    await inventoryStore.getLatestList()
})
</script>

<style scoped>
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
}

.sidebar_content {
    margin-top: 80px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.8s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}
.list-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.list-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.list-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>