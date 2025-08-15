import { createRouter, createWebHistory } from 'vue-router'



const routes = [
    {   
        name: 'Main',
        path: '/', 
        component: () => import('@/pages/Main.vue')
    },
    {   
        name: 'OpenCase',
        path: '/case/:id', 
        component: () => import('@/pages/OpenCase.vue'),
        props: true
    },    
    {   
        name: 'Inventory',
        path: '/Inventory/:id', 
        component: () => import('@/pages/Inventory.vue'),
        props: true
    },
    {
        name: 'SteamCallback',
        path: '/steam-callback',
        component: () => import('@/pages/SteamCallback.vue')
    },
    {   
        name: 'Admin',
        path: '/admin', 
        component: () => import('@/admin/Admin.vue'),
        props: true,
        children: [
            {
                name: 'Users',
                path: 'users',
                component: () => import('@/admin/components/UserTable.vue'),
            },
            {
                name: 'SkinsIditor',
                path: 'skins',
                component: () => import('@/admin/components/EditorSkins.vue'),
            },
            {
                name: 'CasesIditor',
                path: 'cases',
                component: () => import('@/admin/components/EditorCases.vue'),
            },
        ]
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router