<template>
  <DxDataGrid :data-source="usersStore.users" :show-borders="true" :column-auto-width="true">
    <DxColumn data-field="id" caption="ID" />
    <DxColumn data-field="steam_id" caption="steam_id" />
    <DxColumn data-field="username" caption="Имя" />
    <DxColumn data-field="balance" caption="Баланс" />
    <DxColumn data-field="steam_profile_url" caption="steam_profile" />
    <DxPaging :default-page-size="5"/>
  </DxDataGrid>
</template>

<script setup>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid'
import { onMounted } from 'vue'
import { useUsersStore } from '@/stores/UsersStore'

const usersStore = useUsersStore()

onMounted(() => {
  usersStore.fetchUsers()
  console.log(usersStore.users.map(u => u.avatar))
})
</script>