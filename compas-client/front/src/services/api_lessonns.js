import axios from "axios";
const API_URL = import.meta.env.VITE_API

const createClient = () => {
    const client = axios.create({
        baseURL: API_URL,
        'Content-Type': 'application/json'
    });
    return {
        async lessonDetail(lessonId) {
            const response = await client.get(`api/lessons/${lessonId}`)

            return response.data;
        }, 

        async checkAnswers(lessonId, answers) {
            const response = await client.post(`api/lessons/${lessonId}`, answers)

            return response.data;
        },

        async getAllLessons() {
            const response = await client.get('lessons/')

            return response.data
        }
    }
}

export default createClient();

