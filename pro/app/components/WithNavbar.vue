<script lang="ts">
export default {
  name: 'WithNavbar',
  props: ['title']
}
</script>

<template>
  <UDashboardPage>
    <UDashboardPanel grow>
      <UDashboardNavbar :title="this.title">
        <template #right>
<!--          <UTooltip-->
<!--            :text="$t('Qrcode Сканер')"-->
<!--            :shortcuts="['Q']"-->
<!--          >-->
<!--            <UButton-->
<!--              color="gray"-->
<!--              variant="ghost"-->
<!--              square-->
<!--              to="/qrcode"-->
<!--            >-->
<!--              <UIcon-->
<!--                name="i-heroicons-qr-code-16-solid"-->
<!--                class="w-5 h-5"-->
<!--              />-->
<!--            </UButton>-->
<!--          </UTooltip>-->
          <ThemeSwitcher color="gray" />
        </template>
      </UDashboardNavbar>
      <slot />
    </UDashboardPanel>
  </UDashboardPage>
</template>
