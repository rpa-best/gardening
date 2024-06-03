<template>
  <div v-if="loading" class="row justify-content-center" style="width: 100%; height: 100vh">
        <div class="col">
            <ProgressSpinner style="top:40%; left:47%" />
        </div>
    </div>
  <div v-else>
    <Toast />
    <NuxtPage />
  </div>
</template>

<script>

export default {
  name: "App",
  data() {
    return {
      loading: true
    }
  },
  mounted() {
    this.loading = false
  }
}
</script>
<style>
@import url("~/assets/style.css");
</style>