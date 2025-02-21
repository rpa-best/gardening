<script lang="ts">
definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Вход'
})

export default {
  name: 'Login',
  data() {
    return {
      loading: false,
      fields: [{
        name: 'phone',
        type: 'phone',
        label: this.$t('Номер телефона'),
        placeholder: this.$t('Введите номер телефона')
      }, {
        name: 'password',
        label: this.$t('Пароль'),
        type: 'password',
        placeholder: this.$t('Введите номер пароль')
      }],
      providers: []
    }
  },
  methods: {
    validate(state: any) {
      const errors = []
      if (!state.phone) errors.push({path: 'phone', message: i18n.t('Телефон – обязательное поле')})
      if (!state.password) errors.push({path: 'password', message: i18n.t('Пароль – обязательное поле')})
      return errors
    },
    async onSubmit(data: any) {
      this.loading = true
      try {
        const response = await this.$api('oauth/', {method: 'POST', body: data})
        token.value.access = response.data.value.access
        token.value.refresh = response.data.value.refresh
        await useRouter().push(useRoute().query.next ?? useLocalePath()('/'))
        this.loading = false
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<!-- eslint-disable vue/multiline-html-element-content-newline -->
<!-- eslint-disable vue/singleline-html-element-content-newline -->
<template>
  <UCard class="max-w-sm w-full bg-white/75 dark:bg-white/5 backdrop-blur">
    <UAuthForm
      :fields="fields"
      :validate="validate"
      :providers="providers"
      title="Садоводы"
      align="top"
      :loading="loading"
      icon="i-heroicons-lock-closed"
      :ui="{ base: 'text-center', footer: 'text-center' }"
      :submit-button="{ trailingIcon: 'i-heroicons-arrow-right-20-solid', label: $t('Вход') }"
      @submit="onSubmit"
    >
      <template #description>
        {{ $t('У вас нет учетной записи?') }}
        <NuxtLink
          :to="useLocalePath()(`/account?next=${useRoute().query.next}`)"
          class="text-primary font-medium"
        >{{ $t('Зарегистрироваться') }}
        </NuxtLink>
        .
      </template>

      <template #password-hint>
        <NuxtLink
          :to="useLocalePath()('/account')"
          class="text-primary font-medium"
        >{{ $t('Забыли пароль?') }}
        </NuxtLink>
      </template>
    </UAuthForm>
  </UCard>
</template>
