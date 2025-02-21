<template>
  <UTable
    :rows="table"
    :columns="columns"
    class="w-full"
    :ui="{ divide: 'divide-gray-200 dark:divide-gray-800' }"
  >
    <template #mode-data="{ row }">
      <UBadge
        class="mr-3"
        :color="row.mode === 'in' ? 'green' : 'red'"
      >
        {{ row.mode === 'in' ? 'Вход' : 'Выход' }}
      </UBadge>
    </template>
  </UTable>
</template>

<script>
import { get_ws_api } from '~/utils.js'

export default {
  name: 'History',
  props: ['cil_id'],
  data() {
    return {
      columns: [{
        key: 'car_number',
        label: '#'
      }, {
        key: 'car_user.name',
        label: 'Участник'
      }, {
        key: 'date',
        label: 'Дата'
      }, {
        key: 'mode',
        label: 'Тип собития'
      }],
      table: []
    }
  },
  async mounted() {
    const { data } = await this.$api(`location/location/${this.cil_id}/history/`)
    this.table = data.value
    const ws = new WebSocket(`${get_ws_api}cil/${this.cil_id}/?token=${token.value.access}`)
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.table = [data, ...this.table]
    }
  }
}
</script>
