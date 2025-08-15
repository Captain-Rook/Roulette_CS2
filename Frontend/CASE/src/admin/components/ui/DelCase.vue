<template>
<div class="remove_container">'
    <DxForm :form-data="case_cs">
        <DxSimpleItem 
        @submit="submitSkin"
        data-field="id_case" 
        :label="{ text: 'id кейса который нужно удалить' }" 
        :validation-rules="[
            { type: 'required', message: 'введи значение' },
            { type: 'numeric', message: 'Введите число' },
        ]"/>
    </DxForm>
    <button class="rem_case" @click="removeCase">remove skin</button>
</div>

</template>

<script setup>
import { DxForm, DxSimpleItem } from 'devextreme-vue/form'
import { ref } from 'vue'
import api from '@/services/api.js'

const case_cs = ref({id_case: null})

const removeCase = async () => {
    try {
        await api.delete(`/cases/${case_cs.value.id_case}`)
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
.rem_case {
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
.rem_case:hover {
    color: rgb(176, 2, 250);
    border: 1px solid rgb(176, 2, 250);
}
</style>