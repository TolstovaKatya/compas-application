<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <n-card class="lesson-conteiner">
            <div v-if="lesson" class="lesson-card">
                <n-button class="btn">
                    <router-link to="/lessons" class="back-button">
                        Назад к урокам
                    </router-link>
                </n-button>

                <div class="lesson-content">
                    <div class="lesson-id">УРОК {{ lesson.id }}</div>
                    <h1 class="lesson-name">{{ lesson.title }}</h1>
                    
                    <div class="lesson-description" v-if="lesson.description">
                        <p>{{ lesson.description }}</p>
                    </div>
                    
                    <div class="lesson-video">
                        <span class="video-title">ВИДЕОУРОК</span>
                        <iframe
                            :src="lessonVideo"
                            class="video"
                            allow="autoplay;
                            encrypted-media;
                            fullscreen;
                            picture-in-picture;
                            screen-wake-lock;"
                            frameborder="0"
                            allowfullscreen>
                        </iframe>
                    </div>
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

const route = useRoute();
const client = createLessonsClient();

const lesson = ref(null);
const lessonVideo = ref();

const themeOverrides = {
    Button: {
        textColor: '#ffffff',
        colorPrimary: '#00B1FF',
        colorHoverPrimary: '#009ce0',
        colorPressedPrimary: '#0088c4',
    }
};


const getLessonDetail = async () => {
    try {
        const lessonId = route.params.id;
        
        const data = await client.lessonDetail(lessonId);
        lesson.value = data;

        lessonVideo.value = data.video_url
        
        console.log('Данные урока:', data);
    } catch (error) {
        console.error(error);
        lesson.value = null;
    }
};

onMounted(() => {
    getLessonDetail();
});
</script>

<style>
.lesson-conteiner {
    display: flex;
    position: relative;
    margin: 10vh auto;
    min-width: 80vw;
    background-color: black !important;
    border: none !important;
    box-shadow: none !important;
}

.btn {
    background-color: white !important;
}

.back-button {
    text-decoration: none !important;
    color: #00B1FF !important;
    font-weight: bold !important;
}

.lesson-id {
    text-align: center;
    color: #00B1FF;
    text-shadow: 4px 4px 50px rgba(0, 175, 255, 1);
    font-size: 2em;
    text-decoration: none;
    font-weight: bolder;
}

.lesson-name {
    text-align: center;
    color: white;
    font-size: 1.5em;
    font-weight: bold;
}

.lesson-description {
    color: white;
    max-width: 80%;
    font-size: 1.1em;
    margin: 5vh auto;
}

.lesson-video {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.video {
    aspect-ratio: 16 / 9;
    display: block;
    width: 80%;
}

.video-title {
    font-size: 1.3em;
    color: #00B1FF;
    font-weight: bold;
    margin: 2vh auto 3vh auto;
}
</style>