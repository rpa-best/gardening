<template>
  <div
    ref="qrCode"
    class="qrcode"
  />
</template>

<script setup lang="ts">
import QRCodeStyling from 'qr-code-styling'
import { ref, watch, onMounted, defineProps } from 'vue'

const props = defineProps({
  data: String
})

const qrCode = ref<HTMLElement | null>(null)

// Default options
const options = {
  width: 300,
  height: 300,
  type: 'svg',
  data: props.data,
  image: '/favicon.ico',
  dotsOptions: {
    color: '#000',
    type: 'rounded'
  },
  backgroundOptions: {
    color: '#fff'
  },
  imageOptions: {
    crossOrigin: 'anonymous',
    margin: 10
  }
}

const qrCodeStyling: QRCodeStyling = new QRCodeStyling(options)

onMounted(() => {
  // Append QR code to DOM element
  qrCodeStyling.append(qrCode.value)
  // Add viewbox to make it resizable
  qrCode.value!.firstChild!.setAttribute('viewBox', '0 0 300 300')
})

watch(() => props.data, (newValue: string) => {
  // Update QR code data when props change
  options.data = newValue
  qrCodeStyling.update(options)
  // Add viewbox to make it resizable
  qrCode.value!.firstChild!.setAttribute('viewBox', '0 0 300 300')
})
</script>

<style scoped>
svg {
  width: 100%;
  height: 100%;
}
</style>

<style>
.qrcode > svg {
  border-radius: 5px;
}
.qrcode {
  display: inline-block;
  width: 300px
}
</style>
