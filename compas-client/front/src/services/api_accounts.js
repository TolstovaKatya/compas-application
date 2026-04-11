import axios from "axios";

const API_URL = import.meta.env.VITE_API

const createRegistrationClient = () => {
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
        async registration(userData) {
            const response = await client.post('/api/accounts/registration', userData);
            return response.data;
        },

        async login(userData) {
            const response = await client.post('/api/accounts/login', userData);
            return response.data;
        },

        async logout() {
            const response = await client.post('/api/accounts/logout');
            return response.data;           
        },

        async profile() {
            const response = await client.get('/api/accounts/profile');
            return response.data; 
        }
    }
}

export default createRegistrationClient;