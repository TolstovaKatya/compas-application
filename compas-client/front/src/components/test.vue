<template>
    <div v-if="loading" class="loading-wrapper">
        Загрузка теста...
    </div>

    <n-config-provider :theme-overrides="themeOverrides" v-else>
        <h1>{{ titleTest }}</h1>
        
        <div v-if="testComplited">
            <n-card class="test-card">
                <p class="test-title">Тест пройден! Поздравляем!</p>
                <div class="test-card-res">
                    <span class="res">Ваши результаты:</span>
                    <n-progress 
                        type="circle" 
                        :percentage="resultValue" 
                        :offset-degree="100" 
                        class="result"
                    />
                </div>

                <n-button class="btn" type="primary">
                    <router-link :to="`/lessons/${lessonId}`" class="back-button">
                        Назад к уроку
                    </router-link>
                </n-button>
            </n-card>
        </div>

        <div v-else>
            <div v-if="questions && questions.length > 0">
                <n-card class="test-card">
                    <div v-for="question in questions" :key="question.id">
                        <div v-show="question.id === questionId" class="question">
                            {{ question.question_text }}
                        </div>

                        <div>
                            <n-card
                                v-for="answer in currentAnswers"
                                v-show="question.id === questionId"
                                @click="checkAnswer(answer.id)"
                                class="mini-card"
                            >
                                {{ answer.answer_text }}
                            </n-card>
                        </div>  
                    </div>

                    <n-alert 
                        v-show="sucsess" 
                        title="Отличный результат!" 
                        type="success" 
                        closable 
                        class="mistake"
                    >
                        Молодец! Переходим к следующему вопросу!
                    </n-alert>
                    
                    <n-alert 
                        v-show="ifMistake" 
                        title="Ошибка" 
                        type="error" 
                        closable 
                        class="mistake"
                    >
                        Давай подумаем еще :)
                    </n-alert>
                </n-card>
            </div>

            <div v-else-if="questions !== undefined">
                <n-card class="test-card">
                    <p class="test-title">К этому уроку нет теста :)</p>
                    <br><br>
                    <n-button class="btn" type="primary">
                        <router-link :to="`/lessons/${lessonId}`" class="back-button">
                            Назад к уроку
                        </router-link>
                    </n-button>
                </n-card>
            </div>
            
            <div v-else>
                <n-card class="test-card">Загрузка...</n-card>
            </div>
        </div>
    </n-config-provider>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { NCard, NAlert, NConfigProvider, NProgress, NButton } from 'naive-ui';
import createLessonsClient from '@/services/api_lessonns';

const client = createLessonsClient();
const route = useRoute();

const loading = ref(true)

const themeOverrides = {
    common: {
        primaryColor: '#00B1FF',
    },
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

const questionId = ref(null);
const questions = ref(null);
const selectedAnswerId = ref(null);
const tryCount = ref(0);
const lessonId = route.params.id;

const ifMistake = ref(false);
const sucsess = ref(false);
const testComplited = ref(false);
const titleTest = ref('');

const correctCount = ref(0);
const wrongAttempts = ref(0);

const resultValue = computed(() => {
    if (!questions.value || questions.value.length === 0) return 0;
    const res = correctCount.value - wrongAttempts.value * 0.1;
    const percent = (res / questions.value.length) * 100;
    return Math.max(0, Math.round(percent * 10) / 10);
});

const currentAnswers = computed(() => {
    if (!questions.value || !questionId.value) return [];
    const currentQuestion = questions.value.find(item => item.id === questionId.value);
    if (currentQuestion?.answers) {
        return currentQuestion.answers.map(ans => ({
            answer_text: ans.answer_text,
            id: ans.id
        }));
    }
    return [];
});

const getQuestions = async() => {
    loading.value = true;

    try {
        const response = await client.getTest(lessonId);

        if (!response || !response.questions) {
            questions.value = [];
            return;
        }

        titleTest.value = response.title || 'Тест';
        questions.value = response.questions;

        if (questions.value.length > 0) {
            questionId.value = questions.value[0].id;
        }
    } catch (error) {
        console.error('Ошибка загрузки теста:', error);
        questions.value = [];
    } finally {
        loading.value = false;
    }
};

const goToNextQuestion = () => {
    if (!questions.value) return;
    
    const currentIndex = questions.value.findIndex(q => q.id === questionId.value);

    if (currentIndex >= questions.value.length - 1) {
        testComplited.value = true;
    } else {
        questionId.value = questions.value[currentIndex + 1].id;
        tryCount.value = 0;
    }
};

const checkAnswer = async(id) => {
    if (!questions.value) return;

    selectedAnswerId.value = id;
    const answerss = [{ "question_id": questionId.value, "answer_id": id }];

    const currentIndex = questions.value.findIndex(q => q.id === questionId.value);
    const isLastQuestion = currentIndex === questions.value.length - 1;

    try {
        const response = await client.checkAnswer(
            lessonId,
            answerss,
            isLastQuestion,
            correctCount.value,
            wrongAttempts.value
        );

        const questionKey = String(questionId.value);
        const questionResult = response[questionKey] || response[questionId.value];
        
        const isCorrect = questionResult?.is_correct || response.is_correct || false;

        if (!isCorrect) {
            ifMistake.value = true;
            wrongAttempts.value += 1;
            tryCount.value += 1;

            setTimeout(() => { ifMistake.value = false }, 2000);

            if (tryCount.value >= 3) {
                alert("К сожалению, попытки закончились :(");
                goToNextQuestion();
            }
        } else {
            sucsess.value = true;
            correctCount.value += 1;

            setTimeout(() => {
                sucsess.value = false;
                goToNextQuestion();
            }, 2000);
        }
    } catch (error) {
        console.error('Ошибка проверки ответа:', error);
        alert('Произошла ошибка при проверке ответа');
    }
};

onMounted(() => {
    getQuestions();
});
</script>

<style scoped>
.test-card {
    margin: 8vh auto;
    background: var(--bg-surface) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    width: 80%;
    max-width: 900px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.mini-card {
    width: 80%;
    min-height: 50px;
    margin: 1vh auto;
    background: var(--bg-surface) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: none !important;
    cursor: pointer;
    transition: all 0.25s ease;
    user-select: none; 
}

.mini-card:hover {
    background: var(--bg-primary) !important;
    border-color: var(--accent) !important;
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(0, 177, 255, 0.3);
}

.mini-card:active {
    transform: scale(1.0);
    transition: transform 0.1s ease; 
}

.question {
    margin-left: 10%;
    margin-bottom: 2vh;
    font-weight: 600;
    font-size: var(--body);
    color: var(--text-main);
}

.mistake {
    width: 80%;
    margin: 2vh auto;
}

h1 {
    color: var(--accent);
    text-shadow: 
        0 0 12px rgba(0, 177, 255, 0.7),
        0 0 24px rgba(0, 177, 255, 0.5);
    text-align: center;
    margin: 2vh 0 1vh;
    font-size: var(--h2);
    font-weight: 700;
}

.test-card-res {
    display: flex !important;
    flex-direction: column !important;    
    width: 80%;
    margin: 8vh auto;
    background: var(--bg-primary) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    text-align: center;
    padding: 2vh;
}

.res {
    font-size: var(--body);
}

.result {
    margin: 5vh auto;
}

.result :deep(.n-progress-text) {
    fill: #00B1FF !important;
    color: #00B1FF !important;
    font-weight: bold;
    font-size: 1.5rem;
}

.btn {
    width: 80% !important;
    margin: 3vh auto 0 auto !important;
    display: block !important;
    background: transparent !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-weight: 600;
    border-radius: var(--radius) !important;
    transition: all 0.25s ease;
}

.btn:hover {
    background: var(--accent) !important;
    color: #fff !important;
    box-shadow: 0 0 15px rgba(0, 177, 255, 0.5);
}

.back-button {
    text-decoration: none !important;
    color: inherit !important;
    font-weight: 600 !important;
    display: block;
    width: 100%;
    text-align: center;
    padding: 8px 0;
}

.test-title {
    text-align: center;
    margin: auto;
    font-size: var(--h2);
    font-weight: 700;
    color: var(--accent);
    text-shadow: 
        0 0 12px rgba(0, 177, 255, 0.7),
        0 0 24px rgba(0, 177, 255, 0.5);
}

@media (max-width: 768px) {
    .test-card {
        width: 90%;
        margin: 4vh auto;
    }
    .mini-card {
        width: 90%;
    }
    h1, .test-title {
        font-size: 1.75rem;
    }
}
</style>