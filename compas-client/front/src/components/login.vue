<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <div class="registration-page">
      <n-card title="Вход" class="centered-card" style="width: 40vw; text-align: center;">
        <n-form ref="formRef">
          <n-form-item label="Логин">
            <n-input v-model:value="formData.username" class="custom-input" placeholder="Введите логин"
              style="text-align: start;" />
          </n-form-item>

          <n-form-item label="Пароль">
            <n-input v-model:value="formData.password" class="custom-input" type="password" show-password-on="mousedown"
              placeholder="Введите пароль" style="text-align: start;" />
          </n-form-item>

          <n-button html-type="button" @click="handleSubmit"
            style="width: 100%; margin-top: 10px;  margin-bottom: 10px;" class="custom-btn" type="primary">
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
    console.log(data.user)
    if (data.token) {
      localStorage.setItem('access_token', data.token);
      localStorage.setItem('username', data.user.username)
      window.location.href = '/profile';
    }
  } catch (err) {
    console.error(err);
    error.value = "Ошибка входа";
  }
} 
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
</style>