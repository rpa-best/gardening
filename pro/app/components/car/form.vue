<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '#ui/types'
import { useIFetch } from "~/plugins/useIFetch";

const emit = defineEmits(['close'])
// eslint-disable-next-line vue/require-prop-types
const props = defineProps(['initial'])
const state = reactive(props.initial)
const locations = ref([])
// https://ui.nuxt.com/components/form
const validate = (state: any): FormError[] => {
  const errors = []
  if (!state.model) errors.push({ path: 'model', message: 'Марка – обязательное поле' })
  if (!state.number) errors.push({ path: 'number', message: 'Номер – обязательное поле' })
  return errors
}

onMounted(async () => {
  const { data } = await useIFetch('location/location/')
  locations.value = data.value
})

async function onSubmit(event: FormSubmitEvent<any>) {
  // Do something with data
  console.log(event.data)
  if (event.data.id) {
    await useIFetch(`car/car/${event.data.id}/`, { method: 'PATCH', body: event.data })
  } else {
    await useIFetch(`car/car/`, { method: 'POST', body: event.data })
  }
  emit('close')
}
</script>

<template>
  <UForm :validate="validate" :validate-on="['submit']" :state="state" class="space-y-4" @submit="onSubmit">
    <UFormGroup label="Марка" name="model">
      <UInput v-model="state.model" autofocus />
    </UFormGroup>

    <UFormGroup label="Номер" name="number">
      <UInput v-model="state.number" />
    </UFormGroup>
    <UFormGroup label="Лакации" name="locations">
      <USelectMenu v-model="state.locations" option-attribute="name" :options="locations" value-attribute="id" multiple>
        <template #label="{selected}">
          <span v-if="selected.length" class="truncate">{{ selected.reduce((a, v) => [...a, v.name], []).join(', ') }}</span>
          <span v-else>Выбрать локация</span>
        </template>
      </USelectMenu>
    </UFormGroup>

    <div class="flex justify-end gap-3">
      <UButton label="Назад" color="gray" variant="ghost" @click="emit('close')" />
      <UButton type="submit" label="Сохранить" color="black" />
    </div>
  </UForm>
</template>
