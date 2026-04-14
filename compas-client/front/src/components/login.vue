<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <div class="registration-page">
      <n-card 
        title="Вход" 
        class="centered-card"
        style="width: 40vw; text-align: center;" 
      >
        <n-form ref="formRef">
          <n-form-item label="Логин">
            <n-input 
              v-model:value="formData.username" 
              class="custom-input" 
              placeholder="Введите логин" 
              style="text-align: start;"
            />
          </n-form-item>
          
          <n-form-item label="Пароль">
            <n-input 
              v-model:value="formData.password" 
              class="custom-input" 
              type="password" 
              show-password-on="mousedown"
              placeholder="Введите пароль" 
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
        <a href="/registration" style="color: #00B1FF;">Нет аккаунта? Зарегестрируйтесь!</a>
        <router-view />
      </n-card>
    </div>
  </n-config-provider>
</template>

<script setup>
import { ref } from 'vue';
import { NForm, NFormItem, NInput, NButton, NCard, NConfigProvider } from 'naive-ui';
import createRegistrationClient from '@/services/api_accounts'; 
import router from '@/router/router';

const authClient = createRegistrationClient(); 
const formData = ref({ username: '', password: '' });
const error = ref(null);

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

const handleSubmit = async () => {
  error.value = null;
  try {
    const data = await authClient.login(formData.value);
    if (data.token) {
      localStorage.setItem('access_token', data.token);
      window.location.href = '/profile'; 
    }
  } catch (err) {
    console.error(err);
    error.value = "Ошибка входа";
  }
} 
</script>

<style>
.registration-page {
  display: flex;
  justify-content: center; 
  align-items: center;   
  min-height: 100vh;       
  width: 100%;
  background-color: #000000; 
}

.centered-card.n-card {
  background-color: #ffffff !important;
  box-shadow: 4px 4px 40px rgba(0, 175, 255, 1); 
}

</style>