<script setup lang="ts">
useHead({
  bodyAttrs: {
    class: 'dark:bg-gray-950'
  }
})
</script>

<template>
  <div class="topLayer">
    <div class="left" />
    <div class="right">
      <div class="h-screen flex items-center justify-center overlay">
        <div class="gradient">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gradient {
  width: 100%;
  height: 100%;
  position: relative;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(50% 50% at 50% 50%, rgb(var(--color-primary-500) / 0.25) 0, #FFF 100%);
}

.dark {
  .gradient {
    background: radial-gradient(50% 50% at 50% 50%, rgb(var(--color-primary-400) / 0.1) 0, rgb(var(--color-gray-950)) 100%);
  }
}

.overlay {
  background-size: 100px 100px;
  background-image: linear-gradient(to right, rgb(var(--color-gray-200)) 0.5px, transparent 0.5px),
  linear-gradient(to bottom, rgb(var(--color-gray-200)) 0.5px, transparent 0.5px);
}

.dark {
  .overlay {
    background-image: linear-gradient(to right, rgb(var(--color-gray-900)) 0.5px, transparent 0.5px),
    linear-gradient(to bottom, rgb(var(--color-gray-900)) 0.5px, transparent 0.5px);
  }
}

body {
  height: 100%;
  overflow: hidden;
  width: 100% !important;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

.topLayer {
  width: 100%;
  height: 100%;
  position: relative;
  transition: 0.5s;
  display: flex;
  flex-direction: row;
}

.left {
  width: 50%;
  height: 100vh;
  background: #B5B5B5;
  background-size: cover;
  background-position: 50% 50%;
}

.right {
  width: 50%;
  height: 100%;
  background: var(--surface-0);
}

@media screen and (max-width: 966px) {
  .left {
    display: none;
  }
  .right {
    width: 100%;
  }
}
</style>
