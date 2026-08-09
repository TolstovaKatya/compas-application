import axios from "axios";
const API_URL = import.meta.env.VITE_API || 'http://localhost:8000'

const createLessonsClient = () => {
    const client = axios.create({
        baseURL: '/', 
        headers: {
            'Content-Type': 'application/json'
        }
    });

    client.interceptors.request.use((config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        if (!config.url.startsWith('/api/') && !config.url.startsWith('http')) {
            config.url = '/api/' + config.url;
        }
        return config;
    });

    return {
        async lessonDetail(lessonId) {
            const response = await client.get(`api/lessons/${lessonId}/`)

            return response.data;
        }, 

        async getTest(lessonId) {
            const response = await client.get(`api/lessons/${lessonId}/test/single`)

            return response.data
        },

        async checkAnswer(lessonId, answers, isLastQuestion = false, correctCount = 0, wrongCount = 0) {
            const response = await client.post(`api/lessons/${lessonId}/test/single`, {
                answers: answers,
                is_last: isLastQuestion,
                correct_count: correctCount,
                wrong_count: wrongCount
            })

            return response.data
        },

        async getAllLessons() {
            const response = await client.get('api/lessons/')

            return response.data
        }
    }
}

export default createLessonsClient;

