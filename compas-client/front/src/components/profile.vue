<template>
    <n-config-provider :theme-overrides="themeOverrides" class="content">
        <div v-if="user" class="user">
            <n-card class="custom-card">
                <template #header>
                    <div class="card-title">Здравствуйте, {{ user.first_name }} {{ user.last_name }}!</div>
                </template>
                Готовы приступить к обучению?<br>

                <div class="buttons">
                    <n-button class="btn" type="primary">
                        <router-link to="/lessons" class="back-button">
                            Вперед к урокам
                        </router-link>
                    </n-button>
                    <n-button class="back-button" @click="logout" type="primary">
                            Выйти
                    </n-button>
                </div>
            </n-card>

            <n-card class="custom-card">
                <br>
                <template #header>
                    <div class="card-title">Ваши результаты по прохождению уроков:</div>
                </template>

                <!-- <n-button class="btn" style="margin-top: 2vh;">
                    <router-link to="/lessons" class="back-button">
                        Вперед к урокам
                    </router-link>
                </n-button>
                <n-button class="back-button" @click="logout">
                        Выйти
                </n-button> -->
            </n-card>
        </div>

        <div class="progress">
            <n-card class="custom-card-test">
            
            <template #header>
                <div class="card-title">Ваши результаты по прохождению тестов:</div>
            </template>

                <div 
                    v-for="res in results"
                    :key="res.attempt_id"  
                    class="result"
                >

                    <div class="attemt-text">
                        <div class="attent-text-blue">
                            <span class="attemt-text-blue">Попытка №{{ res.attempt_number }}</span><br>
                            <span class="attemt-text-blue">{{ res.completed_at }}</span>
                        </div>  
                        <span class="attemt-text-black">УРОК №{{ res.lesson_id }} </span>
                    </div>
                    
                    
                    <n-progress
                        type="line"
                        :percentage="Math.round(Number(res.score) || 0)"
                        :indicator-placement="'inside'"
                        :height="20"
                        :border-radius="4"
                        :stroke-width="20"
                        processing
                    />
                    
                </div>
            </n-card>
        </div>
    </n-config-provider>
</template>

<script setup>
import createRegistrationClient from '@/services/api_accounts'
import { ref, onMounted, computed } from 'vue';
import { NCard, NButton, NConfigProvider, NProgress } from 'naive-ui';
import router from '@/router/router';

//export const isAutentificated = computed(() => !!localStorage.getItem('access_token'))

const results = ref([])

const themeOverrides = {
    Button: {
        textColor: '#ffffff',
        colorPrimary: 'none',
        colorHoverPrimary: 'none',
        borderPrimary: '#00B1FF 1px solid',
        borderHoverPrimary: '#00B1FF 1px solid',
        borderPressedPrimary: '#00B1FF 1px solid',
        borderFocusPrimary: '#00B1FF 1px solid',
        backgroundColorPrimary: 'none'
    }
};


const options = [
  {
    label: "User Profile",
    key: "profile"
  },
  {
    label: "Edit Profile",
    key: "editProfile"
  },
  {
    label: "Logout",
    key: "logout"
  }
]

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

const logout = async() => {
    const logout = await profileClient.logout();
    localStorage.removeItem('access_token', profile.token)
    localStorage.removeItem('user_name')
    location.href = '/';
}

const getAttempts = async() => {
    const data = await profileClient.getQuizAttemts()
    console.log(data)
    results.value = data.attempts
}

onMounted(() => {
  profile(),
  getAttempts()
})

</script>

<style scoped>
.content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 5vh;
}

.user {
  display: flex;
  gap: 2vw;
  justify-content: center;
  margin: auto;
  height: 20vh;
  width: 40vw;       
  width: 100%;
}

.n-card, .custom-card {
  width: 39vw;
  background-color: #fff !important;
  color: black !important;
  border: 1px solid #00B1FF !important;

  --n-header-text-color: white !important; 
  
}

.card-title {
    font-weight: bold;
}


.custom-card-test {
  width: 80vw;
  margin: 2vh auto;
  background-color: white !important;
  color: black !important;
  border: 1px solid #00B1FF !important;

  --n-header-text-color: white !important; 
  
}

.n-card.n-card--bordered {
    border-color: #00B1FF !important;
}

n-button:hover {
    border-color: #00B1FF !important;
}

.buttons {
    margin-top: 2vh;
    display: flex;
    gap: 3px;
    align-items: center;
}

.back-button {
    text-decoration: none !important;
    color: #00B1FF !important;
    font-weight: bold !important;
}

.attemt-text {
    display: inline-flex;
    justify-content: space-between;
    width: 100%;
}

.attemt-text-blue {
    color:#00B1FF;
    font-weight: 600;
}

.attemt-text-black {
    font-weight: 600;
}
</style>