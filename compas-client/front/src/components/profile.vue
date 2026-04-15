<template>
    <div v-if="user" class="user">
        <n-card class="custom-card" :title="'Здравствуйте, ' + user.first_name + ' ' + user.last_name + '!'">
            Готовы приступить к обучению?
        </n-card>
    </div>
</template>

<script setup>
import createRegistrationClient from '@/services/api_accounts'
import { ref, onMounted } from 'vue';
import { NCard } from 'naive-ui';

const user = ref()

const profileClient = createRegistrationClient();

const profile = async() => {
    try {
        const profile = await profileClient.profile();
        
        user.value = profile.user; 
        console.log(user)

        if (profile.token) {
            localStorage.setItem('access_token', profile.token);
        }
    }
    catch(error) {
        console.log(error)
    }
}

onMounted(() => {
  profile()
})

</script>

<style>
.user {
  display: flex;
  justify-content: center; 
  align-items: center;   
  min-height: 100vh;       
  width: 100%;
}

.n-card, .custom-card {
  width: 70vw;
  background-color: black !important;
  color: black !important;
  border: 1px solid #00B1FF !important;

  --n-header-text-color: white !important; 
  
}

.n-card.n-card--bordered {
    border-color: #00B1FF !important;
}

</style>