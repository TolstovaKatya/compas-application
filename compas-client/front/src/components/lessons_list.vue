<template>
    <div class="lessons">
        <div 
            v-for="(lesson, index) in lessons" 
            :key="lesson.id"
            class="lessons-list"
        >
            <router-link :to="`/lessons/${lesson.id}`" class="lesson-link">
                <span class="lesson-number">
                    УРОК {{ lesson.id }}.
                </span> 
                <span class="lesson-title">
                    {{ lesson.title }}
                </span>
            </router-link>
        </div>
    </div>
</template>


<script setup>
import router from '@/router/router';
import createLessonsClient from '@/services/api_lessonns'
import { onMounted, ref } from 'vue';

const lessons = ref([])
const client = createLessonsClient();

const getLessonsList = async() => {
    const data = await client.getAllLessons();

    console.log(data[0])
    lessons.value = data
}

onMounted(() => {
    getLessonsList()
})

</script>


<style>
.lessons {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10vw; 
    max-width: 80vw;
    margin: 0 auto;
    padding: 10vh;
}

.lessons-list {
    display: flex;
    align-items: center;
    justify-content: center;

    transition: transform 0.3s, text-shadow 0.3s;
}

.lesson-number {
    text-decoration: underline;
    color: #00B1FF;
    margin-right: 0.5vw;
    font-size: 1.1em !important;
}

.lesson-title {
    text-decoration: none !important;
    color: #ffffff;
    font-size: 1.1em !important;
}

.lesson-number:hover, .lesson-title:hover {
    text-shadow: 10px 0px 10px rgba(0, 175, 255, 1);
}

.lesson-link {
    text-decoration: none !important;
}
</style>