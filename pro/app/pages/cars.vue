<template>
  <UDashboardPage>
    <UDashboardPanel grow>
      <div
        class="m-5"
        style="border-radius: 5px; border: 1px solid rgb(var(--color-gray-200)); border-width: 0"
      >
        <UDashboardNavbar
          :title="$t('Мои машины')"
          :badge="cars.length"
        >
          <template #right>
            <UButton
              :label="$t('Добавить')"
              @click="isModalOpen=true; selected = {}"
            />
          </template>
        </UDashboardNavbar>
        <UTable
          :rows="cars"
          :columns="columns"
          class="w-full"
          :ui="{ divide: 'divide-gray-200 dark:divide-gray-800' }"
        >
        <template #location_names-data="{ row }">
            <div v-if="row.location_names && row.location_names.length">{{ row.location_names.join(', ') }}</div>
            <div v-else>-</div>
          </template>
          <template #action-data="{ row }">
            <UIcon
              name="i-heroicons-pencil-square-16-solid"
              class="w-6 h-6 ml-3 text-blue-400 cursor-pointer"
              @click="isModalOpen=true; selected=row"
            />
          </template>
        </UTable>
      </div>
      <UDashboardModal
        v-model="isModalOpen"
        :ui="{ width: 'sm:max-w-l' }"
      >
        <template #title>
          {{ $t('Изменить машину') }}:
          <UBadge color="black">
            {{ selected.number }}
          </UBadge>
        </template>
        <!-- ~/components/users/UsersForm.vue -->
        <CarForm
          :initial="selected"
          @close="isModalOpen = false; fetch_data(); key += 1"
        />
      </UDashboardModal>
      <LocationsCars
        :key="key"
        class="mt-3"
      />
    </UDashboardPanel>
  </UDashboardPage>
</template>

<script lang="ts">
export default {
  name: 'Cars',
  data() {
    return {
      key: 0,
      cars: [],
      selected: {},
      isModalOpen: false,
      columns: [
        {
          key: 'model',
          label: 'Марка'
        },
        {
          key: 'number',
          label: 'Номер'
        },
        {
          key: 'location_names',
          label: 'Локация'
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
      const { data } = await this.$api('car/car/')
      this.cars = data.value
    }
  }
}
</script>
