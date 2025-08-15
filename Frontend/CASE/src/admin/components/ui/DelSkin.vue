<template>
<div class="remove_container">'
    <DxForm :form-data="skin">
        <DxSimpleItem 
        @submit="submitSkin"
        data-field="id_skin" 
        :label="{ text: 'id скина который нужно удалить' }" 
        :validation-rules="[
            { type: 'required', message: 'введи значение' },
            { type: 'numeric', message: 'Введите число' },
        ]"/>
    </DxForm>
    <button class="rem_skin" @click="removeSkin">remove skin</button>
</div>

</template>

<script setup>
import { DxForm, DxSimpleItem } from 'devextreme-vue/form'
import { ref } from 'vue'
import api from '@/services/api.js'

const skin = ref({id_skin: null})

const removeSkin = async () => {
    try {
        await api.delete(`/skins/${skin.value.id_skin}`)
    } catch(e) {
        console.log(e)
    }
}

</script>

<style scoped>
.remove_container {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    flex-direction: column;
}
.rem_skin {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 60px;
    color: rgb(107, 12, 145);
    font-size: 20px;
    transition-duration: 0.2s;
    border: 1px solid rgb(107, 12, 145);
    border-radius: 10%
}
.rem_skin:hover {
    color: rgb(176, 2, 250);
    border: 1px solid rgb(176, 2, 250);
}
</style>