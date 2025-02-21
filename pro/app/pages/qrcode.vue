<template>
  <WithNavbar>
    <div
      v-if="error"
      class="flex flex-col mt-3"
      style="align-items: center"
    >
      <qr
        :data="useRoute().fullPath"
      />
      <p class="mt-3">
        {{ error }}
      </p>
<!--      <u-button label="test" @click="send_qr_data('a7f7ca44-ffa3-446e-8a45-f19e64d71519')" />-->
    </div>

    <div class="flex justify-center mt-3 border-r-4" v-else>
      <qrcode-stream
        :paused="paused"
        class="qrcode-stream"
        @detect="onDetect"
        @error="onError"
      >
        <div
          v-if="validationSuccess"
          class="validation-success"
        >
          <UIcon
            name="i-heroicons-check-circle-16-solid"
            class="w-20 h-20 text-green-500"
          />
        </div>

        <div
          v-else-if="validationFailure"
          class="validation-failure"
        >
          <UIcon
            name="i-heroicons-x-circle-16-solid"
            class="w-20 h-20 text-red-500"
          />
        </div>

        <div
          v-else-if="validationPending"
          class="validation-pending"
        />
        <div
          v-else
          class="screen"
        >
          <div />
        </div>
      </qrcode-stream>
    </div>
    {{ data }}
  </WithNavbar>
</template>

<script lang="ts">
import { QrcodeStream } from 'vue-qrcode-reader'

export default {
  name: 'Qrcode',
  components: { QrcodeStream },
  data() {
    return {
      paused: false,
      error: null,
      data: null,
      isValid: undefined
    }
  },
  computed: {
    validationPending() {
      return this.isValid === undefined && this.paused
    },

    validationSuccess() {
      return this.isValid === true && this.paused
    },

    validationFailure() {
      return this.isValid === false && this.paused
    }
  },
  methods: {
    localPath: useLocalePath(),
    onError(error: any) {
      this.error = error
    },
    timeout(ms: any) {
      return new Promise((resolve) => {
        window.setTimeout(resolve, ms)
      })
    },
    async onDetect([firstDetectedCode]) {
      this.data = firstDetectedCode.rawValue
      this.paused = true
      this.isValid = undefined

      // pretend it's taking really long
      await this.timeout(500)
      this.isValid = this.data.startsWith('https://onson-mail.uz/qrcode/?order_id=')
      const url = new URL(this.data)
      await this.send_qr_data(url.searchParams.get('order_id'))
      // some more delay, so users have time to read the message
      await this.timeout(1000)
      this.paused = false
    },
    async send_qr_data(order_id: any) {
      try {
        await this.$api(`cargo/order/admin/order/${order_id}/change_status/`, { method: 'PATCH', body: { status: 'departure_datetime' } })
        useToast()
      } catch (e: any) {
        console.log(e)
        useToast().add({ title: `${e}`, icon: 'i-heroicons-x-circle-16-solid', color: 'red' })
      }
    }
  }
}
</script>

<style>
.qrcode-stream {
  width: 80%!important;
  aspect-ratio: 1/1;
}

.validation-success,
.validation-failure,
.validation-pending {
  position: absolute;
  width: 100%;
  height: 100%;

  background-color: rgba(255, 255, 255, 0.6);
  filter: blur(0.5);
  padding: 10px;
  text-align: center;
  font-weight: bold;
  font-size: 1.4rem;
  color: black;

  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  align-items: center;
}

.screen {
  position: absolute;
  width: 100%;
  height: 100%;

  background-color: transparent;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  font-size: 1.4rem;
  color: black;

  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  align-items: center;
}

.screen > div {
  width: 60%;
  height: 60%;
  border: 4px solid green;
  border-radius: 5px;
}
</style>
