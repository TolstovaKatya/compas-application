import axios from "axios";
const API_URL = import.meta.env.VITE_API

const createLessonsClient = () => {
    const client = axios.create({
        baseURL: 'http://127.0.0.1:8000/',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    client.interceptors.request.use((config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    });

    return {
        async lessonDetail(lessonId) {
            const response = await client.get(`api/lessons/${lessonId}/`)

            return response.data;
        }, 

        async checkAnswers(lessonId, answers) {
            const response = await client.post(`api/lessons/${lessonId}`, answers)

            return response.data;
        },

        async getAllLessons() {
            const response = await client.get('api/lessons/')

            return response.data
        }
    }
}

export default createLessonsClient;

