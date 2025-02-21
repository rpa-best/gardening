<script lang="ts">
import type { FormError, FormSubmitEvent } from '#ui/types'

export default {
  name: 'Settings',
  data() {
    return {
      state: JSON.parse(JSON.stringify(user.value)),
      ava: null
    }
  },
  methods: {
    async onSubmit(event: FormSubmitEvent<any>) {
      // Do something with data
      const form = new FormData()
      for (const key in event.data) {
        form.set(key, event.data[key])
      }
      if (this.ava) {
        form.set('avatar', this.ava)
      } else {
        form.delete('avatar')
      }
      const { data } = await this.$api('oauth/account/', { method: 'PATCH', body: form })
      user.value = data.value
    },
    onFileClick() {
      this.$refs.fileRef?.click()
    },
    onFileChange(e: Event) {
      const input = e.target as HTMLInputElement

      if (!input.files?.length) {
        return
      }

      this.state.avatar = URL.createObjectURL(input.files[0])
      this.ava = input.files[0]
    },
    validate(state: any): FormError[] {
      const errors = []
      if (!state.first_name) errors.push({ path: 'first_name', message: 'Пожалуйста, введите свое имя.' })
      if (!state.last_name) errors.push({ path: 'last_name', message: 'Пожалуйста, введите свое фамилия.' })
      // if ((state.password1 && !state.password2) || (!state.password1 && state.password2)) errors.push({
      //   path: 'password',
      //   message: 'Please enter a valid password.'
      // })
      return errors
    }
  }
}
</script>

<template>
  <UDashboardPanelContent class="pb-24">
    <UDashboardSection
      :title="$t('Тема')"
      :description="$t('Настройте внешний вид панели управления.')"
    >
      <template #links>
        <ThemeSwitcher color="gray" />
      </template>
    </UDashboardSection>

    <UDivider class="mb-4" />

    <UForm
      :state="state"
      :validate="validate"
      :validate-on="['submit']"
      @submit="onSubmit"
    >
      <UDashboardSection
        :title="$t('Профиль')"
        :description="$t('Эта информация будет отображаться публично, поэтому будьте осторожны с тем, чем делитесь.')"
      >
        <template #links>
          <UButton
            type="submit"
            :label="$t('Сохранить изменения')"
            color="black"
          />
        </template>

        <UFormGroup
          name="first_name"
          :label="$t('Имя')"
          required
          class="grid grid-cols-2 gap-2 items-center"
          :ui="{ container: '' }"
        >
          <UInput
            v-model="state.first_name"
            autocomplete="off"
            icon="i-heroicons-user"
            size="md"
          />
        </UFormGroup>

        <UFormGroup
          name="last_name"
          :label="$t('Фамилия')"
          required
          class="grid grid-cols-2 gap-2"
          :ui="{ container: '' }"
        >
          <UInput
            v-model="state.last_name"
            autocomplete="off"
            icon="i-heroicons-envelope"
            size="md"
          />
        </UFormGroup>

        <UFormGroup
          name="avatar"
          :label="$t('Фото')"
          class="grid grid-cols-2 gap-2"
          help="JPG, GIF or PNG. 1MB Max."
          :ui="{ container: 'flex flex-wrap items-center gap-3', help: 'mt-0' }"
        >
          <UAvatar
            :src="state.avatar"
            :alt="state.first_name"
            size="lg"
          />

          <UButton
            label="Choose"
            color="white"
            size="md"
            @click="onFileClick"
          />

          <input
            ref="fileRef"
            type="file"
            class="hidden"
            accept=".jpg, .jpeg, .png, .gif"
            @change="onFileChange"
          >
        </UFormGroup>
      </UDashboardSection>
    </UForm>
  </UDashboardPanelContent>
</template>
