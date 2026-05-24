<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <n-card class="lesson-conteiner">
            <div v-if="lesson" class="lesson-card">
                
                <div class="content-wrapper">
                    
                    <!-- Кнопка "Назад" -->
                    <n-button class="btn" type="primary">
                        <router-link to="/lessons" class="back-button">
                            Назад к урокам
                        </router-link>
                    </n-button>

                    <div class="lesson-id">УРОК {{ lesson.task_indexs }}</div>
                    <h1 class="lesson-name">{{ lesson.title }}</h1>
                    
                    <!-- Описание урока -->
                    <div class="lesson-description" v-if="lesson.description">
                        <div v-html="lesson.description"></div>
                    </div>
                    
                    <!-- Видео -->
                    <div class="lesson-video" v-if="lessonVideo">
                        <span class="video-title">ВИДЕОУРОК</span>
                        <iframe
                            :src="lessonVideo"
                            class="video"
                            allow="autoplay; encrypted-media; fullscreen; picture-in-picture; screen-wake-lock;"
                            frameborder="0"
                            allowfullscreen>
                        </iframe>
                    </div>

                    <!-- Кнопка "К тесту" -->
                    <n-button class="btn" type="primary">
                        <router-link :to="`/lessons/${lesson.id}/test`" class="back-button">
                            Перейти к тесту
                        </router-link>
                    </n-button>
                </div>
                
            </div>
        </n-card>
    </n-config-provider>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router'; 
import { NCard, NButton, NConfigProvider } from 'naive-ui';
import createLessonsClient from '@/services/api_lessonns';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const route = useRoute();
const client = createLessonsClient();

const lesson = ref(null);
const lessonVideo = ref();

const themeOverrides = {
    Button: {
        textColor: '#ffffff',
        colorPrimary: 'none',
        colorHoverPrimary: 'none',
        borderPrimary: '#00B1FF 1px solid',
        borderHoverPrimary: '#00B1FF 1px solid',
        borderPressedPrimary: '#00B1FF 1px solid',
        borderFocusPrimary: '#00B1FF 1px solid',
        backgroundColorPrimary: 'none'
    }
};

const fixMediaUrls = (html) => {
    if (!html) return html;
    return html.replace(/src="\/media\//g, `src="${API_URL}/media/`);
};

const getLessonDetail = async () => {
    try {
        const lessonId = route.params.id;
        const data = await client.lessonDetail(lessonId);
        
        if (data.description) {
            data.description = fixMediaUrls(data.description);
        }
        if (data.content) {
            data.content = fixMediaUrls(data.content);
        }
        
        lesson.value = data;
        lessonVideo.value = data.video_url;

        console.log(lesson.value)
    } catch (error) {
        console.error('Ошибка загрузки урока:', error);
        lesson.value = null;
    }
};

onMounted(() => {
    getLessonDetail();
});
</script>

<style scoped>
.lesson-conteiner {
    display: flex;
    justify-content: center; 
    margin: 10vh auto;
    width: 100%;
    background-color: black !important;
    border: none !important;
    box-shadow: none !important;
}

.lesson-card {
    display: flex;
    flex-direction: column;
    align-items: center; 
    width: 100%;
}

.content-wrapper {
    display: flex;
    flex-direction: column;
    width: 80%; 
    gap: 3vh;
}

.btn {
    align-self: flex-start; 
    margin: 0;
}

.back-button {
    text-decoration: none !important;
    color: #00B1FF !important;
    font-weight: bold !important;
}

.lesson-id {
    color: #00B1FF;
    text-shadow: 4px 4px 50px rgba(0, 175, 255, 1);
    font-size: 2em;
    font-weight: bolder;
    text-align: center;
}

.lesson-name {
    color: white;
    font-size: 1.5em;
    font-weight: bold;
    margin: 0;
}

.lesson-description {
    color: #fff;
    font-size: 1.1em;
    margin: auto;
}

.lesson-video {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.video {
    aspect-ratio: 16 / 9;
    width: 100%;
    border-radius: 8px;
}

.video-title {
    font-size: 1.3em;
    color: #00B1FF;
    font-weight: bold;
    margin-bottom: 1.5vh;
    text-align: center;
}

/* .lesson-img {
    display: block;
    margin: 0 auto;
} */


</style>