<template>
  <div class="registration-page">
    <n-card 
      title="Вход" 
      class="centered-card"
      style="width: 40vw; text-align: center;" 
    >
      <n-form ref="formRef">
        <n-form-item label="Логин">
          <n-input v-model:value="formData.username" class="custom-input" placeholder="Введите логин" style="text-align: start;" color="#00B1FF"/>
        </n-form-item>
        
        <n-form-item label="Пароль">
          <n-input v-model:value="formData.password" class="custom-input" type="password" placeholder="Введите пароль" style="text-align: start;" color="#00B1FF"/>
        </n-form-item>

        <n-button 
          html-type="button" 
          @click="handleSubmit" 
          style="width: 100%;"
          color="#00B1FF"
        >
          Войти
        </n-button>
      </n-form>
    </n-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { NForm, NFormItem, NInput, NButton, NCard } from 'naive-ui';
import createRegistrationClient from '@/services/api_accounts'; 


const authClient = createRegistrationClient(); 

const formData = ref({ username: '', password: '' });
const error = ref(null);

const handleSubmit = async () => {
  error.value = null;

  try {
    const data = await authClient.login(formData.value);
    
    if (data.token) {
      localStorage.setItem('access_token', data.token);
      window.location.href = '/profile'; 
    }
  } catch (error) {
    console.log(error);
  }
} 
</script>

<style scoped>

.registration-page {
  display: flex;
  justify-content: center; 
  align-items: center;   
  min-height: 100vh;       
  width: 100%;
}

.n-input {
  border: 1px solid #00B1FF !important;
}

.n-input:hover {
  border-color: #00B1FF !important;
}
</style>