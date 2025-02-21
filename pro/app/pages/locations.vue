<script lang="ts">
export default {
  name: 'Locations',
  data() {
    return {
      locations: [],
      selectedLocation: null
    }
  },
  computed: {
    isLocationPanelOpen: {
      get() {
        return !!this.selectedLocation
      },
      set(value: boolean) {
        if (!value) {
          this.selectedLocation = null
        }
      }
    }
  },
  async mounted() {
    await this.fetch_locations()
  },
  methods: {
    async fetch_locations() {
      const { data } = await this.$api('location/location/')
      this.locations = data.value
    }
  }
}
</script>

<template>
  <UDashboardPage>
    <UDashboardPanel
      :width="500"
    >
      <UDashboardNavbar
        :title="$t('Локации')"
        :badge="locations.length"
      />
      <!-- ~/components/inbox/InboxList.vue -->
      <LocationsList
        v-model="selectedLocation"
        :locations="locations"
      />
    </UDashboardPanel>

    <UDashboardPanel
      v-model="isLocationPanelOpen"
      collapsible
      grow
      side="right"
    >
      <template v-if="selectedLocation">
        <LocationsSingle
          :key="selectedLocation.id"
          :location="selectedLocation"
        />
      </template>
      <div
        v-else
        class="flex-1 hidden lg:flex items-center justify-center"
      >
        <UIcon
          name="i-heroicons-map-pin-16-solid"
          class="w-32 h-32 text-gray-400 dark:text-gray-500"
        />
      </div>
    </UDashboardPanel>
  </UDashboardPage>
</template>
