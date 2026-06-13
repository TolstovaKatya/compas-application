<template>
    <div v-if="loading" class="loading-wrapper">
        Загрузка данных профиля...
    </div>

    <n-config-provider :theme-overrides="themeOverrides" v-else-if="user" class="content">
        <div class="user">
            <n-card class="custom-card">
                <template #header>
                    <div class="card-title">
                        Здравствуйте, {{ user.first_name }} {{ user.last_name }}! <br>
                        Готовы приступить к обучению?
                    </div>
                </template>

                <div class="buttons">
                    <n-button class="btn" type="primary">
                        <router-link to="/lessons" class="back-button">
                            Вперед к урокам
                        </router-link>
                    </n-button>
                    <n-button class="btn" @click="logout" type="primary">
                            Выйти
                    </n-button>
                </div>
            </n-card>

            <n-card class="custom-card">
                <br>
                <template #header>
                    <div class="card-title">Ваши результаты по прохождению уроков:</div>
                    <n-progress
                      type="line"
                      :percentage="60"
                      :height="30"
                      indicator-placement="inside"
                      class="lesson-progress"
                    />
                </template>
            </n-card>
        </div>

        <div class="progress">
            <n-card class="custom-card-test">
            
            <template #header>
                <div class="card-title">Ваши результаты по прохождению тестов:</div>
            </template>

                <n-select 
                class="custom-select"
                v-model:value="selectedLessonId" 
                :options="lessonOptions" 
                placeholder="Выберите урок"
                style="width: 100%; max-width: 400px; margin-bottom: 20px;"
                :theme-overrides="{
                    common: {
                    primaryColor: '#00B1FF',
                    primaryColorHover: '#009ce0',
                    primaryColorPressed: '#0088c4',
                    },
                    peers: {
                    InternalSelection: {
                        color: '#ffffff',
                        textColor: '#000000',
                        placeholderColor: '#888888',
                        borderHover: '#00B1FF 1px solid',
                        borderActive: '#00B1FF 1px solid',
                        borderFocus: '#00B1FF 1px solid',
                        arrowColor: '#00B1FF',
                        boxShadowFocus: '0 0 0 2px rgba(0, 177, 255, 0.2)',
                        boxShadowActive: '0 0 0 2px rgba(0, 177, 255, 0.2)',
                        boxShadowHover: 'none',
                        caretColor: '#00B1FF',
                    },
                    InternalSelectMenu: {
                        color: '#ffffff',
                        textColor: '#000000',
                        optionColorHover: '#e6f7ff',
                        optionColorActive: '#e6f7ff',
                        optionTextColorActive: '#00B1FF',
                        optionTextColorHover: '#00B1FF',
                        optionTextColor: '#000000',
                        optionCheckColor: '#00B1FF',
                    }
                    }
                }"
                />

                <div 
                    v-for="res in filteredAttempts"
                    :key="res.attempt_id"  
                    class="result"
                >

                    <div class="attemt-text">
                        <div class="attent-text-blue">
                            <span class="attemt-text-blue-number">Попытка №{{ res.attempt_number }}</span><br>
                            <span class="attemt-text-blue">{{ res.completed_at }}</span>
                        </div>  
                        <span class="attemt-text-black">УРОК №{{ res.lesson_id }} </span>
                    </div>
                    
                    
                    <n-progress
                        type="line"
                        :percentage="Math.round(Number(res.score) || 0)"
                        :indicator-placement="'inside'"
                        :height="20"
                        :border-radius="4"
                        :stroke-width="20"
                        processing
                    />
                    
                </div>
            </n-card>
        </div>
    </n-config-provider>
</template>

<script setup>
import createRegistrationClient from '@/services/api_accounts'
import { ref, onMounted, computed } from 'vue';
import { NCard, NButton, NConfigProvider, NProgress, NSelect } from 'naive-ui';

const results = ref([])
const selectedLessonId = ref(null)
const loading= ref(true)

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

const user = ref()

const profileClient = createRegistrationClient();

const profile = async() => {
    loading.value = true;

    try {
        const profile = await profileClient.profile();
        
        user.value = profile.user; 
        console.log(user)

        if (profile.token) {
            localStorage.setItem('access_token', profile.token);
        }
    }
    catch(error) {
        console.log(error)
    } finally {
        loading.value = false;
    }
}

const logout = async() => {
    const logout = await profileClient.logout();
    localStorage.removeItem('access_token', profile.token)
    localStorage.removeItem('user_name')
    location.href = '/';
}

const getAttempts = async() => {
    const data = await profileClient.getQuizAttemts()
    console.log(data)
    results.value = data.attempts
}

const lessonOptions = computed(() => {
    const uniqueLessons = new Map();
    
    results.value.forEach(attempt => {
        const lid = attempt.lesson_id || attempt.id_lesson; 
        const title = attempt.lesson_title || `Урок #${lid}`;

        if (lid && !uniqueLessons.has(lid)) {
            uniqueLessons.set(lid, { label: title, value: lid });
        }
    });

    return [
        { label: 'Все уроки', value: null },
        ...Array.from(uniqueLessons.values())
    ];
});


const filteredAttempts = computed(() => {
    if (!selectedLessonId.value) {
        return results.value;
    }
    return results.value.filter(attempt => {
        const lid = attempt.lesson_id || attempt.id_lesson;
        return lid === selectedLessonId.value;
    });
});


onMounted(() => {
  profile(),
  getAttempts()
})

</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 5vh;
  background: var(--bg-primary);
  min-height: 100vh;
  padding: 2vh 5vw;
}

.user {
  display: flex;
  gap: 2rem;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  flex-wrap: wrap;
}

.custom-card, .custom-card-test {
  background: #f8fafc !important;
  color: #111827 !important;
  border: 1px solid rgba(0, 177, 255, 0.5) !important;
  border-radius: 12px !important;
  
  box-shadow: 
    0 0 20px rgba(0, 177, 255, 0.7),
    0 0 40px rgba(0, 177, 255, 0.4),
    0 0 60px rgba(0, 177, 255, 0.2) !important;
    
  transition: box-shadow 0.3s ease;
}

.custom-card { 
  width: 100%;
  max-width: 480px;
}

.progress {
  width: 100%;
  display: flex;
  justify-content: center;
}

.custom-card-test { 
  width: 100%;
  max-width: 990px; 
  margin: 2vh auto auto auto;
}

.custom-card :deep(.n-card-header),
.custom-card-test :deep(.n-card-header) {
  color: #00B1FF !important;
  font-size: var(--h3) !important;
  font-weight: 700 !important;
}

.card-title { 
  font-weight: 600;
}

.lesson-progress {
  height: 20px;
  margin-top: 3vh;
}

.buttons {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  background: #00B1FF !important;
  color: #ffffff !important;
  font-weight: 600;
  font-size: var(--body) !important; 
  border-radius: 8px !important;
  height: 42px !important; 
  border: none !important;
  padding: 0 1.25rem !important; 
  transition: all 0.2s ease;
  white-space: nowrap;
}
.btn:hover { 
  background: #009ce0 !important;
  box-shadow: 0 0 15px rgba(0, 177, 255, 0.5) !important;
}

.back-button {
  text-decoration: none !important;
  color: inherit !important;
  font-weight: inherit !important;
  font-size: var(--body) !important;
  padding: 0 !important;
  display: block;
  width: 100%;
  text-align: center;
  line-height: 42px;
}

.custom-select {
  width: 100%;
  max-width: 350px;
  margin-bottom: 1.5rem;
}

.custom-select :deep(.n-base-selection) {
  background: #ffffff !important;
  border-color: #d1d5db !important;
  color: #111827 !important;
}

.custom-select :deep(.n-base-selection:hover),
.custom-select :deep(.n-base-selection--active) {
  border-color: #00B1FF !important;
  box-shadow: 0 0 0 2px rgba(0, 177, 255, 0.2) !important;
}

.custom-select :deep(.n-base-option:hover),
.custom-select :deep(.n-base-option.n-base-option--pending),
.custom-select :deep(.n-base-option.n-base-option--selected),
.custom-select :deep(.n-base-option:focus) {
  color: #00B1FF !important;
  outline: none !important;
}

.custom-select :deep(.n-base-selection:focus-within),
.custom-select :deep(.n-base-selection--focus) {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(0, 177, 255, 0.2) !important;
}

.attemt-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 0.8rem;
  font-size: var(--body);
}

.attemt-text-blue { 
  color: #111827; 
  font-weight: 600; 
}
.attemt-text-black { 
  color: #374151; 
  font-weight: 500; 
}

.attemt-text-blue-number{
  color:#111827;
  font-weight: bold;
}

.result { 
  margin-bottom: 1.5rem; 
}

:deep(.n-progress__line-rail) {
  background-color: #e5e7eb !important;
}
:deep(.n-progress__line-fill) {
  background: linear-gradient(90deg, #00B1FF, #009ce0) !important;
}
:deep(.n-progress__line-indicator) {
  color: #ffffff !important;
  font-weight: 600;
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
  .user { 
    flex-direction: column; 
    gap: 1.5rem; 
    align-items: center;
  }
  .custom-card, 
  .custom-card-test { 
    max-width: 100% !important;
    width: 100%;
  }
  .buttons { 
    justify-content: center; 
    width: 100%;
  }
  .btn { 
    width: auto;
    min-width: 140px;
  }
}

</style>