<template>
    <div class="flex justify-content-between" style="flex-direction: column; height: 100%;">
        <div></div>
        <div class="flex flex-column align-items-center justify-content-center">
            <Stepper orientation="vertical" linear>
                <StepperPanel :header="$t('Регистрация')">
                    <template #content="{ nextCallback }">
                        <form @submit.prevent="sign_up(nextCallback)" style="max-width: 400px;" class="mt-5"
                            autocomplete="off">
                            <div class="field">
                                <label v-if="!error.email" for="email" class="block text-600 text-xl font-medium"
                                    style="font-size: 15px;">{{ $t('Почта') }}<span class="ml-1"
                                        style="color: var(--primary-color)">*</span></label>
                                <label v-else class="block text-600 text-xl font-medium"
                                    style="font-size: 15px; color: var(--error-color);">{{ $t('Почта введен неверно')
                                    }}</label>
                                <InputText required :class="{ invalid: error.username }" id="email" type="email"
                                    :placeholder="$t('Введите почту')" class="w-full" style="width: 100%;"
                                    v-model="data.email" />
                            </div>
                            <div class="field">
                                <label for="surname" class="block text-600 text-xl font-medium" style="font-size: 15px;">{{
                                    $t('Фамилия') }}<span class="ml-1" style="color: var(--primary-color)">*</span></label>
                                <InputText required id="surname" type="text" :placeholder="$t('Введите фамилию')"
                                    class="w-full" style="width: 100%; " v-model="data.surname" />
                            </div>
                            <div class="field">
                                <label for="first_name" class="block text-600 text-xl font-medium"
                                    style="font-size: 15px;">{{ $t('Имя') }}<span class="ml-1"
                                        style="color: var(--primary-color)">*</span></label>
                                <InputText required id="first_name" type="text" :placeholder="$t('Введите имя')"
                                    class="w-full" style="width: 100%; " v-model="data.first_name" />
                            </div>
                            <div class="field">
                                <label for="last_name" class="block text-600 text-xl font-medium"
                                    style="font-size: 15px;">{{ $t('Отчество') }}</label>
                                <InputText id="last_name" type="text" :placeholder="$t('Введите отчество')" class="w-full"
                                    style="width: 100%; " v-model="data.last_name" />
                            </div>
                            <div class="field mt-3">
                                <label v-if="!password_error" for="password1" class="block text-600 font-medium text-xl"
                                    style="font-size: 15px;">{{ $t('Пароль') }}<span class="ml-1"
                                        style="color: var(--primary-color)">*</span></label>
                                <label v-else class="block text-600 text-xl font-medium"
                                    style="font-size: 15px; color: var(--error-color);">{{ $t('Пароль введен неверно')
                                    }}</label>
                                <Password :class="{ invalid: password_error }" :feedback="false" id="password"
                                    v-model="password" :placeholder="$t('Введите пароль')" style="width: 100%; "
                                    :toggleMask="true" class="w-full d-flex justify-content-between align-items-center">
                                </Password>
                            </div>
                            <div class="flex justify-content-between mt-4">
                                <div class="flex align-items-center">
                                    <Checkbox v-model="accept" inputId="accept" :binary="true">
                                        <template #icon="{ checked }">
                                            <i v-if="checked" class="pi pi-check" style="color: #fff; font-size: 10px;"></i>
                                        </template>
                                    </Checkbox>
                                    <label for="accept" class="ml-2 pr-2 flex" style="font-weight: 500; font-size: 12px;"> {{
                                        $t('Я принимаю') }}
                                        <NuxtLink to="#"><strong style="color: var(--primary-color); font-weight: 400;"
                                                class="ml-1">
                                                {{ $t('Условия и политику') }}
                                            </strong>
                                        </NuxtLink>
                                    </label>
                                </div>
                                <Button type="submit" :label="$t('Далее')"></Button>
                            </div>
                        </form>
                    </template>
                </StepperPanel>
                <StepperPanel :header="$t('Подтверждение входа')">
                    <template #content="{ prevCallback }">

                        <form @submit.prevent="send_otp" style="width: 400px;" class="mt-5" autocomplete="off">
                            <div class="field flex align-items-center flex-column">
                                <p style="font-size: 12px;text-wrap: nowrap;">Введите код, который мы отправили на номер
                                    <span style="color: var(--primary-color);" class="ml-1">
                                        {{ data.email }}
                                    </span>
                                </p>
                                <div>
                                    <label for="pvc" class="block text-600 text-xl font-medium" style="font-size: 15px;">
                                        {{ $t('Код') }}
                                    </label>
                                    <InputOtp @change="try_send_otp" id="pvc" required v-model="data.pvc" mask integer-only />
                                </div>
                            </div>
                            <div class="flex justify-content-between mt-3">
                                <p class="cursor-pointer" style="padding: 16px 32px; margin: 0;" @click="prevCallback">{{ $t('Назад') }}</p>
                                <Button class="send-otp" type="submit" :label="$t('Отправить')" style="background-color: var(--surface-100)"></Button>
                            </div>
                        </form>
                    </template>
                </StepperPanel>
            </Stepper>
        </div>
        <div>
            <p class="text-center mb-4">{{ $t('Есть аккаунт?') }}
                <strong @click="login" style="color: var(--primary-color); font-weight: bold;" class="ml-1 cursor-pointer">
                    {{ $t('Войти') }}
                </strong>
            </p>
        </div>
    </div>
</template>

<script>
import { useToken } from "~/composables/token"
import Stepper from "primevue/stepper/Stepper.vue"

export default {
    name: "SighUp",
    data() {
        return {
            data: {},
            error: {},
            accept: false,
            loading: false
        }
    },
    components: { Stepper },
    methods: {
        login() {
            document.querySelector("#slideBox").classList.add("marginLeft-50")
            document.querySelector(".topLayer").classList.add("marginLeft-0")
            document.querySelector("#slideBox").classList.remove("marginLeft-0")
            document.querySelector(".topLayer").classList.remove("marginLeft-100")
        },
        sign_up(callback) {
            if (!this.accept) {
                return this.$toast.add({ severity: 'error', summary: this.$t('Ошибка'), detail: this.$t("Принимайте \"Условия и политику\""), life: 3000 })
            }
            callback()
        },
        _error(e) {
            const detail = e.response.data.detail
            if (detail) {
                this.$toast.add({ severity: 'error', summary: this.$t('Ошибка'), detail: detail.join(". "), life: 5000 });
                delete e.response.data.detail
            }
            this.username_error = e.response.data.username ? e.response.data.username.join(". ") : null
            this.password_error = e.response.data.password ? e.response.data.password.join(". ") : null
        },
        try_send_otp() {
            if (this.data.pvc && `${this.data.pvc}`.length == 4) {
                this.send_otp()
            }
        },
        send_otp() {
            if (!this.data.pvc || `${this.data.pvc}`.length < 4) {
                this.$toast.add({ severity: 'error', summary: this.$t('Ошибка'), detail: this.$t("Не верный код"), life: 3000 })
                return
            }
            this.$toast.add({ severity: 'success', summary: this.$t('Подтверждено'), life: 1000 })
            setTimeout(() => {
                this.$router.push({name: "index"})
            }, 1000);
        }
    }
}
</script>
<style>
.login {
    background-color: var(--surface-ground);
    height: 100vh;
}

.send-otp > .p-button-label {
    color: var(--surface-800)
}
@media screen and (max-width: 966px) {
    .login-image {
        display: none;
    }
}
</style>