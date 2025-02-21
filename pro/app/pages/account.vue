<script lang="ts">
definePageMeta({
    layout: 'auth'
})

useSeoMeta({
    title: 'Sign up'
})


export default {
    name: 'SignUp',
    data() {
        return {
            user: {},
            state: 'phone',
            providers: [],
            phone: null,
            title: 'Подтвердите телефон',
            fields: [{
                name: 'phone',
                type: 'phone',
                label: this.$t('Номер телефона'),
                placeholder: this.$t('Введите номер телефона')
            }]
        }
    },
    methods: {
        validate(state: any) {
            const errors = []

            if (this.state == 'phone') {
                if (!state.phone) errors.push({ path: 'phone', message: this.$t('Телефон – обязательное поле') })
                return errors
            }

            if (!state.first_name) errors.push({ path: 'first_name', message: 'Пожалуйста, введите свое имя.' })
            if (!state.last_name) errors.push({ path: 'last_name', message: 'Пожалуйста, введите свое фамилия.' })
            if (!state.password1) errors.push({ path: 'password1', message: 'Password is required' })
            if (!state.password2) errors.push({ path: 'password2', message: 'Password is required' })
            return errors
        },
        async onSubmit(data: any) {
            if (this.state === 'phone') {
                this.state = 'otp'
                this.phone = data.phone
                await this.$api('oauth/opt/', { method: 'POST', body: data })
                return
            }

            const response = await this.$api('oauth/account/', { method: 'PATCH', body: data })
            this.user = response.data.value
            this.$router.push(useRoute().query.next ?? useLocalePath()('/'))
        },
        async onSubmitOtp(e: any) {
            const opt = e.join('')
            const { data } = await this.$api('oauth/opt-verify/', { method: 'POST', body: { phone: this.phone, opt: opt } })
            token.value.access = data.value.access
            token.value.refresh = data.value.refresh

            this.user = data.value.user
            this.title = 'Заменить пароль'
            if (!data.value.has_usable_password) {
                this, title = 'Регистрация'
                this.fields = [
                    {
                        name: 'first_name',
                        type: 'text',
                        label: this.$t('Имя'),
                    }, {
                        name: 'last_name',
                        type: 'text',
                        label: this.$t('Фамилия'),
                    }
                ]
            } else {
                this.fields = [{
                    name: 'account',
                    label: '',
                    disabled: true,
                    type: 'hidden'
                }]
            }
            this.fields = [
                ...this.fields,
                {
                    name: 'password1',
                    type: 'password',
                    label: this.$t('Password1'),
                }, {
                    name: 'password2',
                    type: 'password',
                    label: this.$t('Password2'),
                }
            ]
            this.state = 'account'
        }

    },
}
</script>

<!-- eslint-disable vue/multiline-html-element-content-newline -->
<!-- eslint-disable vue/singleline-html-element-content-newline -->
<template>
    <UCard class="max-w-sm w-full bg-white/75 dark:bg-white/5 backdrop-blur">
        <Otp v-if="state == 'otp'" @complete="onSubmitOtp" />

        <UAuthForm v-else :fields="fields" :validate="validate" :providers="providers" align="top"
            :title="$t(this.title)" :ui="{ base: 'text-center', footer: 'text-center' }"
            :submit-button="{ label: 'Подтвердить' }" @submit="onSubmit">
            <template v-if="state=='phone'" #description>
                {{ $t('У вас уже есть аккаунт?') }} 
                <NuxtLink
                :to="useLocalePath()('/login')"
                class="text-primary font-medium"
                >{{ $t('Вход') }}</NuxtLink>.
            </template>
            <template #account-description>
                <div class="flex justify-center w-full" style="align-items: center;">
                    <UAvatar :src="user.avatar" size="xs" />
                    <UButton style="font-size: 18px; font-weight: bold;" color="gray" variant="ghost" :label="`${user.first_name} ${user.last_name}`"/>
                </div>
            </template>
        </UAuthForm>
    </UCard>
</template>
