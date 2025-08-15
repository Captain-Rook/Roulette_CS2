<template>
<div class="admin_container">
    <Buttons />
    <section class='router_section'>
        <RouterView />
    </section>
</div>
</template>

<script setup>
import UserTable from '@/admin/components/UserTable.vue'
import Buttons from '@/admin/components/ui/Buttons.vue'
</script>

<style scoped>

.admin_container {
    width: 1400px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    flex-direction: column;
}
.btn_list {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 5px;
}
.button_admin {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 60px;
    color: rgb(252, 252, 252);
    font-size: 20px;
    transition-duration: 0.5s;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
.info_users {
    background: var(--btn-users);
}
.add_skin {
    background: var(--btn-skins);
}
.add_case {
    background: var(--btn-ceses);
}
.router_section {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    width: 100%;
    background: rgb(44, 44, 44);
    padding: 24px;
}
.dx-datagrid {
  max-width: 100%;
}
</style>