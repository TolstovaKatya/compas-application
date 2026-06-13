<template>
    <div v-if="loading" class="loading-wrapper">
        Загрузка уроков...
    </div>

    <div v-else>
        <p class="title">ВВЕДЕНИЕ</p>
        <div class="lessons">
            <div class="lessons-columns">
                <!-- левая колонка -->
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
                
                <!-- правая колонка -->
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
                <!-- левая колонка -->
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
                
                <!-- правая колонка -->
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
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import createLessonsClient from '@/services/api_lessonns';

const lessons = ref([]);
const client = createLessonsClient();

const loading = ref(true)

const getLessonsList = async() => {
    loading.value = true;
    try {
        const data = await client.getAllLessons();
        lessons.value = data;
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false;
    }
};

// введение: уроки с id < 9
const introductionLessons = computed(() => 
    lessons.value.filter(lesson => lesson.id < 9)
);

// черчение: уроки с id > 8
const drawingLessons = computed(() => 
    lessons.value.filter(lesson => lesson.id > 8)
);

// разделяем на левую и правую колонки 
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 4vh 5vw;
}

.lessons-columns {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

.lessons-column {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.lessons-list {
  display: flex;
  align-items: center;
  padding: 0.8rem 1rem;
  border-radius: var(--radius);
  transition: background 0.25s, transform 0.25s;
  cursor: pointer;
}

.lessons-list:hover {
  background: var(--bg-surface);
  transform: translateX(6px);
}

.lesson-link {
  text-decoration: none;
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  width: 100%;
  flex-wrap: nowrap; 
}

.lesson-number {
  color: var(--accent);
  font-weight: 700;
  font-size: var(--body);
  text-decoration: underline;
  text-underline-offset: 4px;
  white-space: nowrap;
  flex-shrink: 0;
  transition: text-shadow 0.3s ease, color 0.3s ease;
}

.lesson-title {
  color: var(--text-main);
  font-size: var(--body);
  font-weight: 500;
  line-height: 1.4;
  transition: text-shadow 0.3s ease;
}

.lessons-list:hover .lesson-number {
  text-shadow: 
    0 0 8px rgba(0, 177, 255, 0.9),
    0 0 18px rgba(0, 177, 255, 0.7),
    0 0 28px rgba(0, 177, 255, 0.5);
  color: #00c8ff; 
}

.lessons-list:hover .lesson-title {
  text-shadow: 0 0 12px rgba(0, 177, 255, 0.4);
}

.lesson-link {
  text-decoration: none;
}

.title {
  color: var(--accent);
  text-shadow: 
    0 0 12px rgba(0, 177, 255, 0.7),
    0 0 24px rgba(0, 177, 255, 0.5);
  font-size: var(--h2);
  font-weight: 700;
  text-align: center;
  margin: 6vh 0 3vh;
}

.loading-wrapper {
  text-align: center;
  font-size: var(--h2);
  color: var(--accent);
  text-shadow: 
    0 0 12px rgba(0, 177, 255, 0.7),
    0 0 24px rgba(0, 177, 255, 0.5);
  font-weight: 700;
}

/* адаптив */
@media (max-width: 768px) {
  .lessons-columns {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .title {
    font-size: 1.75rem;
    margin: 4vh 0 2vh;
  }
}
</style>