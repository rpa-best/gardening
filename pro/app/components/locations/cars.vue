<template>
  <UDashboardNavbar
    v-if="table.length"
    :title="$t('Машини в лакации')"
    :badge="table.length"
  />
  <UTable
    v-if="table.length"
    :rows="table"
    :columns="columns"
    class="w-full"
    :ui="{ divide: 'divide-gray-200 dark:divide-gray-800' }"
  >
    <template #blocked-data="{ row }">
      <UBadge
        :color="!row.blocked ? 'green' : 'red'"
      >
        {{ row.blocked ? $t('Блок') : $t('Не блок') }}
      </UBadge>
    </template>
    <template #action-data="{ row }">
      <UIcon
        v-if="row.blocked"
        name="i-heroicons-check-circle-20-solid"
        class="w-8 h-8 text-green-400 cursor-pointer"
        @click="usePopup(row, true)"
      />
      <UIcon
        v-else
        name="i-heroicons-x-circle-20-solid"
        class="w-8 h-8 text-red-400 cursor-pointer"
        @click="usePopup(row, false)"
      />
    </template>
  </UTable>
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
  name: 'Cars',
  data() {
    return {
      table: [],
      columns: [
        {
          key: 'car.model',
          label: 'Марка'
        },
        {
          key: 'car.number',
          label: 'Номер'
        },
        {
          key: 'car.user.name',
          label: 'Участник'
        },
        {
          key: 'car.user.phone',
          label: 'Номер телефона'
        },
        {
          key: 'blocked',
          label: 'Блокирован'
        },
        {
          key: 'action',
          label: ''
        }
      ],
      modal: {}
    }
  },
  async mounted() {
    await this.fetch_car_in_location()
  },
  methods: {
    async fetch_car_in_location() {
      const { data } = await this.$api('location/car/')
      this.table = data.value
    },
    usePopup(row, accept) {
      this.modal = {
        open: true,
        title: accept ? `Вы уверены, что хотите блокировать "${row.car.number}"?` : `Вы уверены, что хотите заблокировать "${row.car.number}"?`,
        accept, row
      }
    },
    async onSuccess() {
      if (this.modal.accept) {
        await this.$api(`location/car/${this.modal.row.id}/`, {
          method: 'PATCH'
        })
      } else {
        await this.$api(`location/car/${this.modal.row.id}/`, {
          method: 'DELETE'
        })
      }
      this.modal.open = false
      await this.fetch_car_in_location()
    }
  }
}
</script>
