<template>
    <div class="flex justify-content-between" style="flex-direction: column; height: 100%;">
        <div></div>
        <div class="flex flex-column align-items-center justify-content-center">
            <h1 style="font-size: 35px; font-weight: 500; line-height: 42px; color: #222222;" class="text-center">{{ $t('Вход') }}</h1>
            <form @submit.prevent="login" style="width: 400px;" class="mt-5" autocomplete="off">
                <div class="field"> 
                    <label v-if="!username_error" for="username" class="block text-600 text-xl font-medium" style="font-size: 15px;">{{ $t('Почта') }}<span class="ml-1" style="color: var(--primary-color)">*</span></label>
                    <label v-else class="block text-600 text-xl font-medium" style="font-size: 15px; color: var(--error-color);">{{ $t('Почта введен неверно') }}</label>
                    <InputText required :class="{invalid: username_error}" id="username" type="email" :placeholder="$t('Введите почту')" class="w-full" style="width: 100%;" v-model="username" />
                </div>
                <div class="field mt-3">
                    <label v-if="!password_error" for="password1" class="block text-600 font-medium text-xl" style="font-size: 15px;">{{ $t('Пароль') }}<span class="ml-1" style="color: var(--primary-color)">*</span></label>
                    <label v-else class="block text-600 text-xl font-medium" style="font-size: 15px; color: var(--error-color);">{{ $t('Пароль введен неверно') }}</label>
                    <Password required :class="{invalid: password_error}" :feedback="false" id="password" v-model="password" :placeholder="$t('Введите пароль')" 
                    style="width: 100%; background: #F4F6F8; padding: 10px 16px;" :toggleMask="true" class="w-full d-flex justify-content-between align-items-center"></Password>
                </div>
                <div class="field mt-3">
                    <p class="cursor-pointer" @click="forget_password = true" style="color: var(--primary-color);font-size: 14px; font-weight: 600;">{{ $t('Забыли пароль?') }}</p>
                </div>
                <div class="flex justify-content-between mt-4">
                    <div class="flex align-items-center">
                        <Checkbox v-model="save_login" inputId="save_login" :binary="true">
                            <template #icon="{checked}">
                                <i v-if="checked" class="pi pi-check" style="color: #fff; font-size: 10px;"></i>
                            </template>
                        </Checkbox>
                        <label for="save_login" class="ml-2" style="font-weight: 500; font-size: 12px;"> {{ $t('Запомнить меня') }} </label>
                    </div>
                    <Button type="submit" :label="$t('Вход')"></Button>
                </div>
            </form>
        </div>
        <div>
            <p class="text-center mb-4">{{$t('Нет аккаунта?')}}
                <strong @click="signUp" style="color: var(--primary-color); font-weight: bold;" class="ml-1 cursor-pointer">
                    {{ $t('Зарегистрироваться') }}
                </strong>
            </p>
        </div>
    </div>
</template>

<script>
import { useToken } from "~/composables/token"

export default {
    name: "Login",
    data() {
        return {
            username: null,
            password: null,
            password_error: false,
            username_error: false,
            save_login: true,
            loading: false,
            forget_password: false,
        }
    },
    methods: {
        signUp() {
            document.querySelector("#slideBox").classList.remove("marginLeft-50")
            document.querySelector(".topLayer").classList.remove("marginLeft-0")
            document.querySelector("#slideBox").classList.add("marginLeft-0")
            document.querySelector(".topLayer").classList.add("marginLeft-100")
        },
        login() {
            this.loading = true
            navigateTo('/')
            // this.$api.post("/oauth/auth/", { username: this.username, password: this.password }).then((response) => {
            //     if (response.status == 201) {
            //         useToken.value = response.data
            //         navigateTo('/')
            //     } else {
            //         this.error({response})
            //     }
            // }).catch(this.error).finally(() => {
            //     this.loading = false
            // })
        },
        error(e) {
            const detail = e.response.data.detail
            if (detail) {
                this.$toast.add({ severity: 'error', summary: 'Ошибка', detail: detail.join(". "), life: 5000 });
                delete e.response.data.detail
            }
            this.username_error = e.response.data.username ? e.response.data.username.join(". ") : null
            this.password_error = e.response.data.password ? e.response.data.password.join(". ") : null
        }
    }
}
</script>
<style>
.login {
    background-color: var(--surface-ground);
    height: 100vh;
}
</style>