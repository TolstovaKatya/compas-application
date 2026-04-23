<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <h1>{{ titleTest }}</h1>

        <div v-if="testComplited">
            <n-card class="test-card">
                Тест пройден! Поздравляем!
                <div class="test-card-res">
                    <span>Ваши результаты:</span>
                    <n-progress type="circle" :percentage="resultValue" :offset-degree="120" class="result"/>
                </div>

                <n-button class="btn">
                    <router-link :to="`/lessons/${lessonId}`" class="back-button">
                        Назад к уроку
                    </router-link>
                </n-button>
            </n-card>
        </div>

        <div v-else>
            <n-card
                class="test-card"
            >
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
                    <n-card
                        v-for="answer in currentAnswers"
                        v-show="question.id === questionId"
                        @click="checkAnswer(answer.id)"
                        class="mini-card"
                    >
                        {{ answer.answer_text }}
                    </n-card>
                </div>
                <n-alert v-show="ifMistake" title="Ошибка" type="error" closable class="mistake">
                    Давай подумаем еще :)
                </n-alert>
            </n-card>
        </div>
    </n-config-provider>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { NCard, NAlert, NConfigProvider, NProgress } from 'naive-ui';
import createLessonsClient from '@/services/api_lessonns';

const client = createLessonsClient();
const route = useRoute();

const questionId = ref()
const question_text = ref('')
const question = ref()

const questions = ref()
const answers = ref({})
const answers1 = ref({})

const selectedAnswerId = ref()

const tryCount = ref(0)

const lessonId = route.params.id;

const ifMistake = ref(false)
const testComplited = ref(false)
const titleTest = ref()

const correctCount = ref(0)
const wrongAttempts = ref(0)

const resultValue = computed(() => {
    const res = correctCount.value - wrongAttempts.value * 0.1
    const percent = (res / questions.value.length) * 100

    return Math.round(percent * 10) / 10;
});


const currentAnswers = computed(() => {
    const currentQuestion = questions.value.find(item => item.id === questionId.value);
    if (currentQuestion.answers) {
        return currentQuestion.answers.map(ans => ({
            answer_text: ans.answer_text,
            id: ans.id
        }));
    }
});

const getQuestions = async() => {
    const response = await client.getTest(lessonId);

    titleTest.value = response.title

    //id вопроса
    questionId.value = response.questions[0].id
    console.log(0, questionId.value)

    //массив вопросов
    questions.value = response.questions
    console.log(1, response.questions);
    console.log(2, response.questions[questionId.value])

    // конкретный вопрос (для отладки)
    question.value = response.questions.find(item => item.id = questionId.value);

    // текст конкретного вопроса (для отладки)
    question_text.value = question.value.question_text
    console.log(3, question_text.value)

    //ответы на вопрос 
    answers.value = response.questions.find(item => item.id === questionId.value).answers
    console.log(answers.value)

    answers1.value = answers.value.map(ans => ({
        answer_text: ans.answer_text,
        id: ans.id
    }))
    console.log(answers1.value)
}


const checkAnswer = async(id) => {
    selectedAnswerId.value = id

    const answerss = [
        {
            "question_id": questionId.value,
            "answer_id": id
        }
    ]

    const response = await client.checkAnswer(lessonId, answerss)
    console.log(response[questionId.value].is_correct)

    const goToNextQuestion = () => {
        if (questionId.value >= questions.value.length) {
            testComplited.value = true
        }
        else {
            questionId.value ++
        }
    }

    if (!response[questionId.value].is_correct) {

        ifMistake.value = true

        setTimeout(() => {
            ifMistake.value = false
        }, 2000)

        wrongAttempts.value += 1
        tryCount.value += 1
        console.log(tryCount.value)

        if (tryCount.value === 3){
            alert("К сожалению попытки закончились :(")
            //questionId.value += 1;
            goToNextQuestion()
            ifMistake.value = false
        }
    }
    else {
        alert("Молодец! Переходим к следующему вопросу!")
        // questionId.value ++
        goToNextQuestion()
        tryCount.value = 0
        correctCount.value += 1
    }
}



onMounted(() => {
    getQuestions();
})

</script>

<style>
.test-card {
    margin: auto;
    margin-top: 8vh;
    background-color: black !important;
    color: white !important;
}

.mini-card {
    width: 80%;
    height: 20%;
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

</style>