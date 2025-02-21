<template>
  <UDashboardNavbar
    :title="location.name"
  >
    <template #right>
      <UButton
        v-if="location.role === 'admin'"
        :label="$t('Приглашение')"
        @click="qrcode_open"
      />

      <UDashboardModal
        v-model="modal.open"
        :title="$t('Автаризуйте в системе и сканируйте')"
        :close="{
          color: 'primary',
          variant: 'outline',
          class: 'rounded-full'
        }"
        :ui="{ width: 'sm:max-w-l' }"
      >
        <div class="flex flex-col justify-center items-center">
          <qr
            :data="modal.url"
          />
          <UButton
            label="Скопировать приглашение"
            class="mt-3"
            @click="copy_invite"
          />
        </div>
      </UDashboardModal>
    </template>
    <template #toggle>
      <UDashboardNavbarToggle icon="i-heroicons-x-mark" />
    </template>
  </UDashboardNavbar>
  <UTabs
    v-model="selectedCamera"
    class="sticky top-0"
    label-attribute="name"
    :items="location.cameras"
    :ui="{ wrapper: '', list: { height: 'h-9', tab: { height: 'h-7', size: 'text-[13px]' } } }"
  >
    <template #default="{ item }">
      {{ item.name }}
    </template>
  </UTabs>
  <div
    class="w-full flex justify-center items-center mx-auto"
    style="aspect-ratio: 4/3; background-color: #B5B5B5; max-width: 1000px"
  >
    <UIcon
      name="i-heroicons-video-camera-slash-20-solid"
      class="w-32 h-32 text-gray-200 dark:text-gray-500"
    />
  </div>
  <LocationsHistory
    v-if="location.role === 'admin'"
    :key="location.cameras[selectedCamera].id"
    :cil_id="location.cameras[selectedCamera].id"
  />
</template>

<script>
export default {
  name: 'Single',
  // eslint-disable-next-line vue/require-prop-types
  props: ['location'],
  data() {
    return {
      selectedCamera: 0, modal: {}
    }
  },
  methods: {
    async qrcode_open() {
      const { data } = await this.$api(`location/location/${this.location.id}/create_invite/`)
      this.modal.url = `${location.origin}/invite?id=${data.value.uuid}`
      this.modal.open = true
    },
    async copy_invite() {
      await navigator.clipboard.writeText(this.modal.url)
      useToast().add({
        title: `Операция выполнена успешно`,
        icon: 'i-heroicons-x-circle-16-solid',
        color: 'green'
      })
    }
  }

}
</script>
