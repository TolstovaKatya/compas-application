import { createRouter, createWebHistory } from "vue-router";
import Main from "@/components/main.vue";
import Login from "@/components/login.vue";
import Profile from "@/components/profile.vue";
import Registration from "@/components/registration.vue";
import Lessonslist from "@/components/lessons_list.vue";
import LessonDetail from "@/components/lesson_detail.vue";
import Test from '@/components/test.vue'

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
        },
        {
            path: '/lessons',
            name: 'Lessonslist',
            component: Lessonslist
        },
        {
            path: '/lessons/:id',
            name: 'LessonDetail',
            component: LessonDetail
        },
        {
            path: '/lessons/:id/test',
            name: 'Test',
            component: Test
        }
    ]
})

export default router; 