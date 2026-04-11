<template>
    <div class="registration-form">
        <n-card title="Регистрация">
            <n-form>
                <n-form-item label="Логин">
                    <n-input 
                        placeholder="Логин"
                        v-model:value="formData.username"
                    />
                </n-form-item>

                <n-form-item label="E-mail">
                    <n-input 
                        placeholder="E-mail"
                        v-model:value="formData.email"
                    />
                </n-form-item>

                <n-form-item label="Фамилия">
                    <n-input 
                        placeholder="Фамилия"
                        v-model:value="formData.lastname"
                    />
                </n-form-item>

                <n-form-item label="Имя">
                    <n-input 
                        placeholder="Имя"
                        v-model:value="formData.name"
                    />
                </n-form-item>

                <n-form-item label="Пароль">
                    <n-input 
                        type="password"
                        show-password-on="mousedown"
                        placeholder="Пароль"
                        v-model:value="formData.password"
                    />
                </n-form-item>

                <n-form-item label="Повторите пароль">
                    <n-input 
                        type="password"
                        show-password-on="mousedown"
                        placeholder="Повторите пароль"
                        v-model:value="formData.password2"
                    />
                </n-form-item>
            </n-form>
        </n-card>
    </div>
</template>

<script setup>
import {
    NCard,
    NForm,
    NFormItem,
    NInput
} from 'naive-ui'

</script>

<style>

</style>