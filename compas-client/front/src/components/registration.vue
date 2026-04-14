<template>
    <n-config-provider :theme-overrides="themeOverrides">
        <div class="registration-form">
            <n-card 
                title="Регистрация"
                style="width: 40vw; text-align: center;" 
                >
                <n-form>
                    <n-form-item label="Логин">
                        <n-input 
                            placeholder="Логин"
                            v-model:value="formData.username"
                            style="text-align: start;"
                        />
                    </n-form-item>

                    <n-form-item label="E-mail">
                        <n-input 
                            placeholder="E-mail"
                            v-model:value="formData.email"
                            style="text-align: start;"
                        />
                    </n-form-item>

                    <n-form-item label="Фамилия">
                        <n-input 
                            placeholder="Введите фамилию"
                            v-model:value="formData.last_name"
                            style="text-align: start;"
                        />
                    </n-form-item>

                    <n-form-item label="Имя">
                        <n-input 
                            placeholder="Введите имя"
                            v-model:value="formData.first_name"
                            style="text-align: start;"
                        />
                    </n-form-item>

                    <n-form-item label="Пароль">
                        <n-input 
                            type="password"
                            show-password-on="mousedown"
                            placeholder="Пароль"
                            v-model:value="formData.password"
                            style="text-align: start;"
                        />
                    </n-form-item>

                    <n-form-item label="Повторите пароль">
                        <n-input 
                            type="password"
                            show-password-on="mousedown"
                            placeholder="Повторите пароль"
                            v-model:value="formData.password2"
                            style="text-align: start;"
                        />
                    </n-form-item>

                    <n-button 
                        html-type="button" 
                        @click="handleSubmit" 
                        style="width: 100%; margin-top: 10px;  margin-bottom: 10px;"
                        class="custom-btn"
                        type="primary" 
                    >
                        Войти
                    </n-button>
                </n-form>
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
})

console.log(formData)

const registrationClient = createRegistrationClient();

const handleSubmit = async() => {
    try {
        const response = await registrationClient.registration(formData.value)
        if (response.token) {
            localStorage.setItem('access_token', response.token);
            
            window.location.href = '/profile'; 
        }
        else{
            alert("я долбьоеб")
        }
    }
    catch(error){
        console.log(error)
    }
}

</script>

<style>

.registration-form {
  display: flex;
  justify-content: center; 
  align-items: center;   
  min-height: 100vh;       
  width: 100%;
  background-color: #000000; 
}

.n-card {
  background-color: #ffffff !important; 
  box-shadow: 4px 4px 40px rgba(0, 175, 255, 1);
}

</style>