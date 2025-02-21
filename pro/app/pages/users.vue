<template>
  <UDashboardPage>
    <UDashboardPanel grow>
      <div
        class="m-5"
        style="border-radius: 5px; border: 1px solid rgb(var(--color-gray-200))"
      >
        <UDashboardNavbar
          :title="$t('Заявки')"
          :badge="invites.length"
        />
        <UTable
          :rows="invites"
          :columns="columns"
          class="w-full"
          :ui="{ divide: 'divide-gray-200 dark:divide-gray-800' }"
        >
          <template #avatar-data="{ row }">
            <UAvatar
              :src="row.user.avatar"
              size="lg"
              class="mx-auto"
            />
          </template>
          <template #action-data="{ row }">
            <UIcon
              name="i-heroicons-check-circle-20-solid"
              class="w-8 h-8 text-green-400 cursor-pointer"
              @click="usePopup(row, true, 'invite')"
            />
            <UIcon
              name="i-heroicons-x-circle-20-solid"
              class="w-8 h-8 ml-3 text-red-400 cursor-pointer"
              @click="usePopup(row, false, 'invite')"
            />
          </template>
        </UTable>
      </div>
      <UDashboardNavbar
        :title="$t('Учасники')"
        :badge="users.length"
      />
      <UTable
        :rows="users"
        :columns="columns"
        class="w-full"
        :ui="{ divide: 'divide-gray-200 dark:divide-gray-800' }"
      >
        <template #avatar-data="{ row }">
          <UAvatar
            :src="row.user.avatar"
            size="lg"
            class="mx-auto"
          />
        </template>
        <template #action-data="{ row }">
          <UIcon
            name="i-heroicons-pencil-square-16-solid"
            class="w-6 h-6 ml-3 text-blue-400 cursor-pointer"
            @click="usePopup(row, true, 'user')"
          />
          <UIcon
            name="i-heroicons-trash-20-solid"
            class="w-6 h-6 ml-3 text-red-400 cursor-pointer"
            @click="usePopup(row, false, 'user')"
          />
        </template>
      </UTable>
    </UDashboardPanel>
  </UDashboardPage>

  <UDashboardModal
    v-model="modal.open"
    :title="modal.title"
    :close="{
      color: 'primary',
      variant: 'outline',
      class: 'rounded-full'
    }"
    :ui="{ width: 'sm:max-w-l' }"
  >
    <UFormGroup
      v-if="modal.accept"
      :label="$t('Макс. кол-во машин')"
      name="max_count_cars"
    >
      <UInput
        v-model="modal.row.max_count_cars"
        type="number"
        placeholder="0"
      />
    </UFormGroup>
    <template #footer>
      <div class="flex gap-2">
        <UButton
          color="red"
          label="Отмена"
          @click="modal.open = false"
        />
        <UButton
          label="Да"
          @click="onSuccess"
        />
      </div>
    </template>
  </UDashboardModal>
</template>

<script lang="ts">
export default {
  name: 'Users',
  data() {
    return {
      modal: {},
      invites: [],
      users: [],
      columns: [
        {
          key: 'avatar',
          label: this.$t('Фото')
        },
        {
          key: 'user.name',
          label: this.$t('ФИО')
        },
        {
          key: 'user.phone',
          label: this.$t('Телефон')
        },
        {
          key: 'location.name',
          label: this.$t('Локация')
        },
        {
          key: 'action',
          label: ''
        }
      ],
      users: [],
      users_columns: [
        {
          key: 'avatar',
          label: this.$t('Фото')
        },
        {
          key: 'user.name',
          label: this.$t('ФИО')
        },
        {
          key: 'user.phone',
          label: this.$t('Телефон')
        },
        {
          key: 'location.name',
          label: this.$t('Локация')
        },
        {
          key: 'action',
          label: ''
        }
      ]
    }
  },
  async mounted() {
    await this.fetch_data()
  },
  methods: {
    async fetch_data() {
      const { data } = await this.$api('location/invite/')
      this.invites = data
      const response = await this.$api('location/user/')
      this.users = response.data
    },
    usePopup(row, accept, url) {
      if (url == 'invite') {
        this.modal = {
          open: true,
          title: accept ? `Вы уверены, что хотите принимать заявку "${row.user.name}"?` : `Вы уверены, что хотите откланить заявку "${row.user.name}"?`,
          accept, url, row
        }
      } else {
        this.modal = {
          open: true,
          title: accept ? `Вы уверены, что хотите изменить учасника "${row.user.name}"?` : `Вы уверены, что хотите удалить учасника "${row.user.name}"?`,
          accept, url, row
        }
      }
    },
    async onSuccess() {
      if (this.modal.accept) {
        await this.$api(`location/${this.modal.url}/${this.modal.row.id}/`, {
          method: 'PATCH',
          body: { max_count_cars: this.modal.row.max_count_cars }
        })
      } else {
        await this.$api(`location/${this.modal.url}/${this.modal.row.id}/`, {
          method: 'DELETE'
        })
      }
      this.modal.open = false
      await this.fetch_data()
    }
  }
}
</script>
