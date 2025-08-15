<template>
<div class="container">
    <section class="section_add_skin">
            <DxForm
        :form-data="formData"
        :col-count="2"
        :items="formItems"
        @submit="submitSkin"
        >
        <template #imageUploader>
            <DxFileUploader
                :select-button-text="'Select image'"
                accept="image/*"
                :upload-mode="'useForm'"
                @value-changed="onImageChange"
            />
        </template>
        </DxForm>
        <button class="add" @click="submitSkin">Add skin</button>
    </section>
    <section class="section_del_skin">
        <DelSkin />
    </section>
    
</div>
</template>

<script setup>
import DelSkin from './ui/DelSkin.vue'
import { DxForm } from 'devextreme-vue/form'
import { DxFileUploader } from 'devextreme-vue/file-uploader'
import { reactive } from 'vue'
import api from '@/services/api'

const formData = reactive({
  weapon: '',
  price: 0,
  fullname: '',
  rare: '',
  skin_image: null,
})

const onImageChange = (e) => {
  const file = e.value?.[0]
  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {
    formData.skin_image = reader.result
  }
  reader.readAsDataURL(file)
}

const formItems = [
    { 
        dataField: 'weapon', 
        label: { text: 'Weapon name' }, 
        editorType: 'dxTextBox' 
    },
    { 
        dataField: 'price', 
        label: { text: 'Price' }, 
        editorType: 'dxNumberBox' 
    },
    { 
        dataField: 'fullname', 
        label: { text: 'Skin Name' }, 
        editorType: 'dxTextBox' },
    {  
        dataField: 'rarity', label: { text: 'Rarity' }, editorType: 'dxSelectBox', editorOptions: {
        items: [
            'covert',
            'classified', 
            'restricted', 
            'mil-spec grade', 
            'industrial grade', 
            'consumer grade', 
            'rare'
            ],
        },
    },
  {
    name: 'imageUpload',
    label: { text: 'Skin Image' },
    template: 'imageUploader',
  },
]

const submitSkin = async () => {
    try{
        await api.post('/skins/', {
            weapon: formData.weapon,
            price: formData.price,
            fullname: formData.fullname,
            rare: formData.rarity,
            skin_image: formData.skin_image,
        })
    }catch(err) {
        console.error('Ошибка при обработке:', err)
    }
}
</script>

<style scoped>
.container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column
}
.section_add_skin {
    position: relative;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    width: 100%;
}
.section_del_skin {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
}
.add {
    position: absolute;
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
.add:hover {
    color: rgb(176, 2, 250);
    border: 1px solid rgb(176, 2, 250);
}
</style>