<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Object as PropType<any | null>,
    default: null
  },
  locations: {
    type: Array as PropType<any[]>,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const locationsRefs = ref<Element[]>([])

const selectedLocation = computed({
  get() {
    return props.modelValue
  },
  set(value: any | null) {
    emit('update:modelValue', value)
  }
})

watch(selectedLocation, () => {
  if (!selectedLocation.value) {
    return
  }

  const ref = locationsRefs.value[selectedLocation.value.number]
  if (ref) {
    ref.scrollIntoView({block: 'nearest'})
  }
})

defineShortcuts({
  arrowdown: () => {
    const index = props.locations.findIndex(location => location.id === selectedLocation.value?.id)

    if (index === -1) {
      selectedLocation.value = props.locations[0]
    } else if (index < props.locations.length - 1) {
      selectedLocation.value = props.locations[index + 1]
    }
  },
  arrowup: () => {
    const index = props.locations.findIndex(location => location.id === selectedLocation.value?.id)

    if (index === -1) {
      selectedLocation.value = props.locations[props.locations.length - 1]
    } else if (index > 0) {
      selectedLocation.value = props.locations[index - 1]
    }
  }
})
</script>

<template>
  <UDashboardPanelContent class="p-0 overflow-y-scroll">
    <div
      v-for="(location, index) in locations"
      :key="index"
      :ref="el => { locationsRefs[location.id] = el as Element }"
    >
      <div
        class="p-4 text-sm cursor-pointer border-l-2"
        :class="[
          'text-gray-600 dark:text-gray-300',
          selectedLocation && selectedLocation.id === location.id ? 'border-primary-500 dark:border-primary-400 bg-primary-100 dark:bg-primary-900/25' : 'border-white dark:border-gray-900 hover:border-primary-500/25 dark:hover:border-primary-400/25 hover:bg-primary-100/50 dark:hover:bg-primary-900/10'
        ]"
        @click="selectedLocation = location"
      >
        <div
          class="flex items-center justify-between"
        >
          <div>{{ location.name }}</div>
          <UBadge
            :color="location.status === 'accepted' ? 'green' : 'orange'"
          >
            {{ location.status === 'accepted' ? $t('Принята') : $t('На проверке') }}
          </UBadge>
        </div>
      </div>
    </div>
  </UDashboardPanelContent>
</template>
