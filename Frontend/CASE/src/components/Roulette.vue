<template>
    <div class="container_roulette">
        <div class="box_roulette">
            <div v-if="!skinStore.isOpen" class="case_in_roulette">
                <p class="case_name">{{caseStore.rouletteCase.name}}</p>
                <img
                    v-if="caseStore.rouletteCase.image"
                    :src="`http://127.0.0.1:8000${caseStore.rouletteCase.image}`" 
                    alt="case" 
                    class="img_skin_roulette"
                />
            </div>
            <div v-else class="box_roulette_skins">
            <div class="line"></div>
                <div class="list_skins" :style="{ transform: `translateX(${caseStore.translateX})` }">
                    <SkinRoulette 
                        v-for="skin in skinStore.skinsRoulette" 
                        :key="skin.id" 
                        :skinsRoulette="skin"
                    />
                </div>
            </div>
            <h2 v-if="!userStore.isAuth">Необходимо авторизоваться чтобы открыть кейс</h2>
            <div v-else>
                <button v-if="!skinStore.isOpen" :disabled="!hasBalance"  @click="openCase" class="open_case">Open case {{caseStore.rouletteCase.price}}</button>
                <div v-if="!skinStore.isOpen && !hasBalance" class="no_money">
                    <p class="text_no_money">Не хватает денег</p>
                    <p class="up_balance">пополнить</p>
                </div>
            </div>
            <SkinResult v-if="showSkinResult" />
        </div>
    </div>
</template>


<script setup>
import { computed, onBeforeUnmount, watch, ref } from 'vue'

import SkinRoulette from "./ui/SkinRoulette.vue"
import SkinResult from "./SkinResult.vue"

import { useSkinStore } from '@/stores/SkinStore'
import { useCaseStore } from '@/stores/CaseStore'
import { useUserStore } from '@/stores/UserStore'
import { useInventoryStore } from '@/stores/InventoryStore'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { nextTick } from 'vue'

let timeoutId = null
const route = useRoute()
const caseID = Number(route.params.id)

const skinStore = useSkinStore()
const caseStore = useCaseStore()
const userStore = useUserStore()
const inventoryStore = useInventoryStore()


const hasBalance = computed(() => {
  return userStore.user.balance >= caseStore.rouletteCase.price
})

const showSkinResult = computed(() => {
  return caseStore.endAnimation && skinStore.isOpen;
});

const openCase = async () => {
    await skinStore.fetchSkins(caseID)
    await skinStore.shuffleSkinsToRoulette(caseID)
    await userStore.setBalance()

    skinStore.isOpen = true
    await nextTick()

    caseStore.translateX = '0px'
    await nextTick()

    const startNum = -11400
    const random = Math.floor(Math.random() * 50)
    const result = startNum + random
    caseStore.translateX = `${result}px`

    timeoutId = setTimeout(() => {
        caseStore.endAnimation = true
    }, 15000)
}

const loadCase = async (id) => {
  await caseStore.getRouletteCase(Number(id))

  skinStore.isOpen = false
  caseStore.endAnimation = false
  caseStore.translateX = '0px'
  await nextTick()

  const element = document.querySelector('.list_skins')
  if (element) {
    element.style.transition = 'none'
    element.style.transform = 'translateX(0px)'
    void element.offsetHeight
    element.style.transition = 'transform 15s ease-out'
  }
}

onMounted(() => {
  loadCase(route.params.id)
})

onBeforeUnmount(() => {
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
  skinStore.isOpen = false
  caseStore.endAnimation = false
  caseStore.translateX = '0px'
})

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId !== oldId) {
      loadCase(newId)
    }
  }
)
</script>

<style scoped>

.container_roulette {
    padding: 20px;
    width: 100%;
    max-width: 1700px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    font-weight: 700;
}

.box_roulette {
    max-width: calc(1700px - 180px);
    width: 100%;
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgb(31, 35, 36);
    flex-direction: column;
    border-radius: 20px;
}

.case_in_roulette {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column
}

.case_name {
    font-size: 30px;
    color: rgb(7, 98, 104);
}

.box_roulette_skins {
    border: 2px solid rgb(255, 255, 255);
    width: 750px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    background: #141416;
    overflow: hidden;
    position: relative;
}
.line {
    width: 50%;
    height: 310px;
    position: absolute;
    border-right: 3px solid rgb(0, 0, 0);
    z-index: 50;
}
.list_skins {
    transform: translateZ(0);
    will-change: transform;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 8px;
    transition: transform 15s cubic-bezier(0.4, 1, 0.8, 1);
}  

.open_case {
    width: 120px;
    height: 60px;
    background: rgb(255, 136, 0);
    font-size: 18px;
    border-radius: 10%;
    margin: 20px;
    transition-duration: 0.5s;
}

.no_money {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 5px;
}

.text_no_money {
    font-size: 20px;
    color: rgb(104, 7, 7);
}

.up_balance {
    font-size: 14px;
    color: rgb(26, 93, 155);
    cursor: pointer;
}
.up_balance:hover {
    color: rgb(35, 182, 226);
}

@media (max-width: 1025px) {
    .login {
        font-size: 14px;
        width: 60px;
        height: 30px;
    }
    .icon {
        height: 25px;
        width: 25px;
        margin-left: 30px;
    }
    .inf_txt {
        font-size: 0.4rem;
        gap: 2px;
    }

    .user_name {
        font-size: 0.4rem;
    }
}
</style>