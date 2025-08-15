<template>
<div class="container">
    <section class="section_add_cases">
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
        <button class="add" @click="submitSkin">Add case</button>
    </section>
    <section class="section_del_case">
        <DelCase />
    </section>
</div>
  
</template>

<script setup>
import DelCase from './ui/DelCase.vue'
import { DxForm } from 'devextreme-vue/form'
import { DxFileUploader } from 'devextreme-vue/file-uploader'
import { reactive } from 'vue'
import api from '@/services/api'

const formData = reactive({
  name: '',
  price: 0,
  skins: '',
  image: '',
})

const onImageChange = (e) => {
  const file = e.value?.[0]
  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {
    formData.image = reader.result
  }
  reader.readAsDataURL(file)
}

const formItems = [
   { 
      dataField: 'name', 
      label: { text: 'Case name' }, 
      editorType: 'dxTextBox' 
   },
   { 
      dataField: 'price', 
      label: { text: 'Price' }, 
      editorType: 'dxNumberBox' 
   },
   { 
      dataField: 'skins', 
      label: { text: 'Skin Name (id скина через запятую)' }, 
      editorType: 'dxTextBox' 
   },
   {    
    name: 'image',
    label: { text: 'Skin Image' },
    template: 'imageUploader',
  },
]

const submitSkin = async () => {
    if (!formData.name.trim()) {
       alert('Поле "Case name" не может быть пустым')
       return
   }
   if (!formData.price || formData.price <= 0) {
       alert('Введите корректную цену')
       return
   }
   if (!formData.skins.trim()) {
       alert('Введите хотя бы один скин (ID через запятую)')
       return
   }
   try{
      const skinsArray = formData.skins
      .split(',')
      .map(s => s.trim())
      .filter(s => s !== '')
      .map(Number)
      .filter(n => !isNaN(n))

      await api.post('/cases/', {
          name: formData.name,
          price: formData.price,
          skins: skinsArray,
          image: formData.image,
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
.section_add_case {
    position: relative;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    width: 100%;
}
.section_del_case {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    margin-top: 80px;
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