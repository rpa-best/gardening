<script lang="ts" setup>
const { locales, locale, setLocale } = useI18n()

const lang = computed({
  get: () => locale.value,
  set: (value: any) => {
    setLocale(value)
    console.log(value)
  }
})
</script>

<template>
  <USelect
    v-model="lang"
    :options="locales"
    option-attribute="name"
    value-attribute="code"
  />
</template>
