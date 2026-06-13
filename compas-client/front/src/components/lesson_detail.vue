<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <n-card class="lesson-conteiner">

            <div v-if="loading" class="loading-wrapper">
              Загрузка урока...
            </div>

            <div v-else-if="lesson" class="lesson-card">
                
                <div class="content-wrapper">
                    
                    <!-- кнопка назад -->
                    <n-button class="btn" type="primary">
                        <router-link to="/lessons" class="back-button">
                            Назад к урокам
                        </router-link>
                    </n-button>

                    <div class="lesson-id">УРОК {{ lesson.task_indexs }}</div>
                    <h1 class="lesson-name">{{ lesson.title }}</h1>
                    
                    <!-- оеписане урока -->
                    <div class="lesson-description" v-if="lesson.description">
                        <div v-html="lesson.description"></div>
                    </div>
                    
                    <!-- видео -->
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

                    <!-- кнопка к тесту -->
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

const API_URL = import.meta.env.VITE_API;

const route = useRoute();
const client = createLessonsClient();

const lesson = ref(null);
const lessonVideo = ref();

const loading = ref(true)

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
    loading.value = true; 

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
    } finally {
        loading.value = false;
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
  background: var(--bg-primary) !important;
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
  margin: 0 auto;
  gap: 3vh;
}

.btn {
  align-self: flex-start; 
  background: transparent !important;
  border: 1px solid var(--accent) !important;
  color: var(--accent) !important;
  font-weight: 600;
  font-size: var(--body) !important; 
  padding: 1rem 2.5rem !important; 
  border-radius: var(--radius) !important;
  transition: all 0.25s ease;
  cursor: pointer;
}

.btn:hover {
  box-shadow: 
    0 0 12px rgba(0, 177, 255, 0.5),
    0 0 24px rgba(0, 177, 255, 0.3);
  transform: scale(2px);
}

.back-button {
  text-decoration: none !important;
  color: inherit !important;
  font-weight: 600 !important;
  font-size: var(--body);
  display: block;
  width: 100%;
  text-align: center;
  line-height: 1.2;
}

.lesson-id {
  color: var(--accent);
  text-shadow: 
    0 0 12px rgba(0, 177, 255, 0.7),
    0 0 24px rgba(0, 177, 255, 0.5);
  font-size: var(--h2);
  font-weight: 700;
  text-align: center;
}

.lesson-name {
  color: var(--text-main);
  font-size: var(--h2);
  text-shadow: 
    0 0 12px rgba(0, 177, 255, 0.7),
    0 0 24px rgba(0, 177, 255, 0.5);
  font-weight: 600;
  margin: 0;
  text-align: center;
}

.lesson-description {
  color: var(--text-main);
  font-size: var(--body);
  line-height: 1.6;
}

.lesson-video {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1.5vh;
}

.video {
  aspect-ratio: 16 / 9;
  width: 100%;
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.video-title {
  font-size: var(--h2);
  color: var(--accent);
  font-weight: 600;
  text-align: center;
  text-shadow: 
    0 0 12px rgba(0, 177, 255, 0.7),
    0 0 24px rgba(0, 177, 255, 0.5);
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
  .content-wrapper { 
    width: 90%; 
    gap: 2vh; 
  }
  .btn {
    padding: 0.85rem 2rem !important; 
    font-size: 1rem !important;
  }
}
</style>