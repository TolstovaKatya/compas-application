<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <h1>{{ titleTest }}</h1>

        <div v-if="testComplited">
            <n-card class="test-card">
                <p class="test-title">Тест пройден! Поздравляем!</p>
                <div class="test-card-res">
                    <span>Ваши результаты:</span>
                    <n-progress type="circle" :percentage="resultValue" :offset-degree="100" class="result"/>
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
                    <div 
                        v-for="question in questions"
                        :key="question.id"
                    >
                        <div
                            v-show="question.id === questionId"
                            class="question"
                        >
                            {{ question.question_text }}
                        </div>

                        <!--ответы--->
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

                    <n-alert v-show="sucsess" title="Отличный результат!" type="success" closable class="mistake">
                        Молодец! Переходим к следующему вопросу!
                    </n-alert>
                    
                    <n-alert v-show="ifMistake" title="Ошибка" type="error" closable class="mistake">
                        Давай подумаем еще :)
                    </n-alert>
                </n-card>
            </div>

            <div v-else-if="questions !== undefined">
                <n-card class="test-card">
                    <p class="test-title">К этому уроку нет теста :)</p> <br><br>
                    <n-button class="btn" type="primary">
                        <router-link :to="`/lessons/${lessonId}`" class="back-button">
                            Назад к уроку
                        </router-link>
                    </n-button>
                </n-card>
            </div>
            
            <div v-else>
                <!-- Загрузка -->
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
}

const questionId = ref(null)
const questions = ref(null)
const selectedAnswerId = ref(null)
const tryCount = ref(0)
const lessonId = route.params.id

const ifMistake = ref(false)
const sucsess = ref(false)
const testComplited = ref(false)
const titleTest = ref('')

const correctCount = ref(0)
const wrongAttempts = ref(0)

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
    }
}

const goToNextQuestion = () => {
    if (!questions.value) return;
    
    const currentIndex = questions.value.findIndex(q => q.id === questionId.value);

    if (currentIndex >= questions.value.length - 1) {
        testComplited.value = true;
    } else {
        questionId.value = questions.value[currentIndex + 1].id;
        tryCount.value = 0; // сброс попыток для нового вопроса
    }
}

const checkAnswer = async(id) => {
    if (!questions.value) return;

    selectedAnswerId.value = id;
    const answerss = [{ "question_id": questionId.value, "answer_id": id }];

    // определяем, последний ли это вопрос
    const currentIndex = questions.value.findIndex(q => q.id === questionId.value);
    const isLastQuestion = currentIndex === questions.value.length - 1;

    try {
        // отправляем текущие счетчики ДО их обновления в этом запросе
        const response = await client.checkAnswer(
            lessonId,
            answerss,
            isLastQuestion,
            correctCount.value,
            wrongAttempts.value
        );

        // парсим ответ сервера. Ключ может быть строкой или числом
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
}

onMounted(() => {
    getQuestions();
})
</script>

<style scoped>
.test-card {
    margin: auto;
    margin-top: 8vh;
    background-color: black !important;
    color: white !important;
    width: 80%;
}

.mini-card {
    width: 80%;
    min-height: 50px;
    margin: auto;
    margin-top: 1vh;
    background-color: black !important;
    color: white !important;
    box-shadow: none !important;
    cursor: pointer;
    transition: 0.3s;
}

.mini-card:hover {
    background-color: #1a1a1a !important;
}

.question {
    margin-left: 10%;
    margin-bottom: 2vh;
    font-weight: bold;
}

.mistake {
    width: 80%;
    margin: auto;
    margin-top: 2vh;
}

h1 {
    color: #00B1FF;
    text-shadow: 4px 4px 40px rgba(0, 175, 255, 1);
    text-align: center;
    margin-top: 2vh;
    margin-bottom: 1vh;
}

.test-card-res  {
    display: flex !important;
    flex-direction: column !important;    
    width: 80%;
    margin: auto;
    margin-top: 8vh;
    background-color: black !important;
    color: white !important;
    border: #00B1FF 1px solid;
    text-align: center;
    padding: 2vw 2vh;
}

.result {
    margin: auto;
    margin-top: 5vh;
}

.btn {
    width: 80% !important;
    margin: 3vh auto 0 auto !important; 
    display: block !important;
}

.back-button {
    text-decoration: none !important;
    color: #00B1FF !important;
    font-weight: bold !important;
    display: block;
    width: 100%;
    text-align: center;
    padding: 8px 0;
}

.test-title {
    text-align: center;
    margin: auto;
    font-size: 2em;
}
</style>