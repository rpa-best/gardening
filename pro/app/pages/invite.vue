<template>
  <div>
    <UMain>
      <UContainer>
        <UPage>
          <UPageError :error="{ name: $t('Садоводы'), statusCode: 200, message: $t('Приглашение на локацию') }" />
        </UPage>
      </UContainer>
    </UMain>

    <UNotifications />
  </div>
</template>

<script>
definePageMeta({
  layout: 'empty'
})

export default {
  name: 'Invite',
  async mounted() {
    const invite_id = useRoute().query.id
    await this.$api(`location/accept-invite/${invite_id}/`)
    await useRouter().push(useLocalePath()('/locations'))
  }
}
</script>
