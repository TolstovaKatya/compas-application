<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <div class="registration-page">
            <n-card title="Регистрация" class="centered-card">
                <n-form ref="formRef">
                    <n-form-item label="Логин">
                        <n-input placeholder="Логин" v-model:value="formData.username" class="custom-input"
                            style="text-align: start;" />
                    </n-form-item>

                    <n-form-item label="E-mail">
                        <n-input placeholder="E-mail" v-model:value="formData.email" class="custom-input"
                            style="text-align: start;" />
                    </n-form-item>

                    <n-form-item label="Фамилия">
                        <n-input placeholder="Введите фамилию" v-model:value="formData.last_name" class="custom-input"
                            style="text-align: start;" />
                    </n-form-item>

                    <n-form-item label="Имя">
                        <n-input placeholder="Введите имя" v-model:value="formData.first_name" class="custom-input"
                            style="text-align: start;" />
                    </n-form-item>

                    <n-form-item label="Пароль">
                        <n-input type="password" show-password-on="mousedown" placeholder="Пароль"
                            v-model:value="formData.password" class="custom-input" style="text-align: start;" />
                    </n-form-item>

                    <n-form-item label="Повторите пароль">
                        <n-input type="password" show-password-on="mousedown" placeholder="Повторите пароль"
                            v-model:value="formData.password2" class="custom-input" style="text-align: start;" />
                    </n-form-item>

                    <n-button html-type="button" @click="handleSubmit"
                        style="width: 100%; margin-top: 10px; margin-bottom: 10px;" class="custom-btn" type="primary">
                        Зарегистрироваться
                    </n-button>
                </n-form>
                <a href="/login" style="color: #00B1FF;">Уже есть аккаунт? Войдите!</a>
                <router-view />
            </n-card>
        </div>
    </n-config-provider>
</template>

<script setup>
import createRegistrationClient from '@/services/api_accounts';
import {
    NCard,
    NForm,
    NFormItem,
    NInput,
    NButton,
    NConfigProvider
} from 'naive-ui'
import { ref } from 'vue';

const themeOverrides = {
    common: {
        primaryColor: '#00B1FF',
        primaryColorHover: '#009ce0',
        primaryColorPressed: '#0088c4',
    },
    Input: {
        color: '#ffffff',
        textColor: '#000000',
        placeholderColor: '#999999',
        border: '1px solid #D3D3D3',
        borderColorHover: '#00B1FF',
        borderColorFocus: '#00B1FF',
        boxShadowHover: '0 0 0 2px rgba(0, 177, 255, 0.15)',
        boxShadowFocus: '0 0 0 2px rgba(0, 177, 255, 0.3)',
        colorHover: '#ffffff',
        colorFocus: '#ffffff',
    },
    Button: {
        textColor: '#ffffff',
        colorPrimary: '#00B1FF',
        colorHoverPrimary: '#009ce0',
        colorPressedPrimary: '#0088c4',
    }
};

const formData = ref({
    username: '',
    email: '',
    last_name: '',
    first_name: '',
    password: '',
    password2: ''
});

const registrationClient = createRegistrationClient();

const handleSubmit = async () => {
    try {
        const response = await registrationClient.registration(formData.value);
        if (response.token) {
            localStorage.setItem('access_token', response.token);
            window.location.href = '/profile';
        } else {
            alert("Ошибка регистрации");
        }
    } catch (error) {
        console.log(error);
    }
};
</script>

<style scoped>
.registration-page {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    background: black;
    padding-top: 10vh;
    padding-left: 1rem;
    padding-right: 1rem;
}

.centered-card {
    background: #f8fafc !important;
    color: #111827 !important;
    border: 1px solid rgba(0, 177, 255, 0.5) !important;
    border-radius: 12px !important;
    width: 100% !important;
    max-width: 480px !important;
    box-shadow:
        0 0 20px rgba(0, 177, 255, 0.7),
        0 0 40px rgba(0, 177, 255, 0.4),
        0 0 60px rgba(0, 177, 255, 0.2) !important;
    transition: box-shadow 0.3s ease;
}

.centered-card:hover {
    box-shadow:
        0 0 20px rgba(0, 177, 255, 0.7),
        0 0 40px rgba(0, 177, 255, 0.4),
        0 0 60px rgba(0, 177, 255, 0.2) !important;
}

.centered-card :deep(.n-card-header__title) {
    color: #00B1FF !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(0, 177, 255, 0.4);
}

.centered-card :deep(.n-form-item-label) {
    color: #374151 !important;
    font-weight: 500;
}

.centered-card :deep(.n-input) {
    background: #ffffff !important;
    border-color: #d1d5db !important;
    color: #111827 !important;
}

.centered-card :deep(.n-input:hover),
.centered-card :deep(.n-input:focus) {
    border-color: #00B1FF !important;
    box-shadow: 0 0 0 2px rgba(0, 177, 255, 0.2) !important;
}

.centered-card :deep(.n-input__placeholder) {
    color: #9ca3af !important;
}

.custom-btn {
    background: #00B1FF !important;
    color: #ffffff !important;
    font-weight: 600;
    border-radius: 8px !important;
    height: 48px !important;
    border: none !important;
    transition: all 0.2s ease;
}

.custom-btn:hover {
    background: #009ce0 !important;
    box-shadow: 0 0 15px rgba(0, 177, 255, 0.5) !important;
}

a {
    color: #00B1FF;
    text-decoration: none;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}

a:hover {
    opacity: 0.8;
    text-decoration: underline;
}

@media (max-width: 480px) {
    .registration-page {
        padding-top: 6vh;
    }

    .centered-card {
        max-width: 100% !important;
    }
}

.centered-card :deep(.n-card-header__main) {
    text-align: center !important;
    width: 100%;
}

.centered-card :deep(.n-card-content) {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.centered-card :deep(.n-form) {
    width: 100%;
}

.centered-card a {
    display: inline-block;
    margin-top: 12px;
    text-align: center;
}
</style>