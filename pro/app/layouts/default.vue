<script setup lang="ts">
import { useIFetch } from "~/plugins/useIFetch";

const i18n = useI18n()
const checked_links = reactive([])

const links = [{
  id: 'home',
  label: i18n.t('Главная страница'),
  icon: 'i-heroicons-home',
  to: '/',
  tooltip: {
    text: i18n.t('Главная страница'),
    shortcuts: ['G', 'H']
  }
}, {
  id: 'locations',
  label: i18n.t('Локация'),
  icon: 'i-heroicons-map-pin-16-solid',
  to: '/locations',
  // badge: '4',
  tooltip: {
    text: i18n.t('Локация'),
    shortcuts: ['G', 'L']
  }
}, {
  id: 'users',
  label: i18n.t('Участники'),
  icon: 'i-heroicons-user-group-solid',
  to: '/users',
  tooltip: {
    text: i18n.t('Участники'),
    shortcuts: ['G', 'U']
  },
  _check: 'location/user/'
},
{
  id: 'cars',
  label: i18n.t('Автомобили'),
  icon: 'i-heroicons-truck-20-solid',
  to: '/cars',
  tooltip: {
    text: i18n.t('Автомобили'),
    shortcuts: ['G', 'U']
  }
},{
  id: 'delivery',
  label: i18n.t('Доставка'),
  icon: 'i-heroicons-truck-20-solid',
  disabled: true,
  badge: 'Скоро'
}]

const groups = [{
  key: 'links',
  label: 'Go to',
  commands: links.map(link => ({ ...link, shortcuts: link.tooltip?.shortcuts }))
}]

const localPath = useLocalePath()

onMounted(async () => {
  for (const link of links) {
    if (link._check) {
      try {
        await useIFetch(link._check, { method: 'HEAD' })
        checked_links.push(link)
      } catch { /* empty */ }
    } else {
      checked_links.push(link)
    }
  }
})
</script>

<template>
  <UDashboardLayout>
    <UDashboardPanel
      :width="250"
      :resizable="{ min: 200, max: 300 }"
      collapsible
    >
      <UDashboardNavbar
        class="!border-transparent"
        :ui="{ left: 'flex-1' }"
      >
        <template #left>
          <NuxtLink
            :to="localPath('/')"
            class=" flex items-center gap-2"
          >
            <span class="flex">
              <img
                src="/favicon.ico"
                width="45"
                height="45"
                alt="logo"
              >
            </span>
            <span class="text-lg text-gray-700 dark:text-white">
              <p
                class="mb-0 font-bold text-transparent bg-clip-text bg-gradient-to-br from-primary to-[#8cd66a]"
                style="line-height: 16px;"
              >{{ $t('Садоводы') }}</p>
            </span>
          </NuxtLink>
        </template>
      </UDashboardNavbar>

      <UDashboardSidebar>
        <template #header>
          <UDashboardSearchButton :label="$t('Поиск')" />
        </template>
        <UDashboardSidebarLinks :links="checked_links" />

        <UDivider />

        <template #footer>
          <!-- ~/components/UserDropdown.vue -->
          <UserDropdown />
        </template>
      </UDashboardSidebar>
    </UDashboardPanel>
    <slot />

    <!-- ~/components/HelpSlideover.vue -->
    <HelpSlideover />
    <!-- ~/components/NotificationsSlideover.vue -->
    <NotificationsSlideover />

    <ClientOnly>
      <LazyUDashboardSearch :groups="groups" />
    </ClientOnly>
  </UDashboardLayout>
</template>
