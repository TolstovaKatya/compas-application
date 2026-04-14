import { createRouter, createWebHistory } from "vue-router";
import Main from "@/components/main.vue";
import Login from "@/components/login.vue";
import Profile from "@/components/profile.vue";
import registration from "@/components/registration.vue";
import Registration from "@/components/registration.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.VITE_API),
    routes: [
        {
            path: '/',
            name: 'Main',
            component: Main
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/profile',
            name: 'Profile',
            component: Profile
        },
        {
            path: '/registration',
            name: 'Registration',
            component: Registration
        }
    ]
})

export default router; 