<template>
    <p class="title">ВВЕДЕНИЕ</p>
    <div class="lessons">
        <div class="lessons-columns">
            <!-- Левая колонка -->
            <div class="lessons-column">
                <div 
                    v-for="lesson in introductionLessonsLeft" 
                    :key="lesson.id"
                    class="lessons-list"
                >
                    <router-link :to="`/lessons/${lesson.id}`" class="lesson-link">
                        <span class="lesson-number">
                            УРОК {{ lesson.task_indexs }}.
                        </span> 
                        <span class="lesson-title">
                            {{ lesson.title }}
                        </span>
                    </router-link>
                </div>
            </div>
            
            <!-- Правая колонка -->
            <div class="lessons-column">
                <div 
                    v-for="lesson in introductionLessonsRight" 
                    :key="lesson.id"
                    class="lessons-list"
                >
                    <router-link :to="`/lessons/${lesson.id}`" class="lesson-link">
                        <span class="lesson-number">
                            УРОК {{ lesson.task_indexs }}.
                        </span> 
                        <span class="lesson-title">
                            {{ lesson.title }}
                        </span>
                    </router-link>
                </div>
            </div>
        </div>
    </div>

    <p class="title">ЧЕРЧЕНИЕ</p>
    <div class="lessons">
        <div class="lessons-columns">
            <!-- Левая колонка -->
            <div class="lessons-column">
                <div 
                    v-for="lesson in drawingLessonsLeft" 
                    :key="lesson.id"
                    class="lessons-list"
                >
                    <router-link :to="`/lessons/${lesson.id}`" class="lesson-link">
                        <span class="lesson-number">
                            УРОК {{ lesson.task_indexs }}.
                        </span> 
                        <span class="lesson-title">
                            {{ lesson.title }}
                        </span>
                    </router-link>
                </div>
            </div>
            
            <!-- Правая колонка -->
            <div class="lessons-column">
                <div 
                    v-for="lesson in drawingLessonsRight" 
                    :key="lesson.id"
                    class="lessons-list"
                >
                    <router-link :to="`/lessons/${lesson.id}`" class="lesson-link">
                        <span class="lesson-number">
                            УРОК {{ lesson.task_indexs }}.
                        </span> 
                        <span class="lesson-title">
                            {{ lesson.title }}
                        </span>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import createLessonsClient from '@/services/api_lessonns';

const lessons = ref([]);
const client = createLessonsClient();

const getLessonsList = async() => {
    const data = await client.getAllLessons();
    lessons.value = data;
};

// Введение: уроки с id < 9
const introductionLessons = computed(() => 
    lessons.value.filter(lesson => lesson.id < 9)
);

// Черчение: уроки с id > 8
const drawingLessons = computed(() => 
    lessons.value.filter(lesson => lesson.id > 8)
);

// Разделяем на левую и правую колонки (первая половина / вторая половина)
const introductionLessonsLeft = computed(() => {
    const mid = Math.ceil(introductionLessons.value.length / 2);
    return introductionLessons.value.slice(0, mid);
});

const introductionLessonsRight = computed(() => {
    const mid = Math.ceil(introductionLessons.value.length / 2);
    return introductionLessons.value.slice(mid);
});

const drawingLessonsLeft = computed(() => {
    const mid = Math.ceil(drawingLessons.value.length / 2);
    return drawingLessons.value.slice(0, mid);
});

const drawingLessonsRight = computed(() => {
    const mid = Math.ceil(drawingLessons.value.length / 2);
    return drawingLessons.value.slice(mid);
});

onMounted(() => {
    getLessonsList();
});
</script>

<style scoped>
.lessons {
    max-width: 80vw;
    margin: 0 auto;
    padding: 10vh;
}

.lessons-columns {
    display: flex;
    gap: 2vw; /* Расстояние между колонками */
}

.lessons-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2vh; /* Расстояние между элементами в колонке */
}

.lessons-list {
    display: flex;
    align-items: center;
    justify-content: flex-start;
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

.title {
    color: #00B1FF;
    text-shadow: 4px 4px 50px rgba(0, 175, 255, 1);
    font-size: 2em;
    font-weight: bolder;
    text-align: center;
    margin-top: 5vh;
}
</style>