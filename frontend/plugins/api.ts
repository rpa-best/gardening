import { defineNuxtPlugin } from "#app";
import { useToken } from "~/composables/token";
import axios from "axios"

const domain = 'https://ichd.tashkent.uz/api/'
const token: string | null = useToken.value.access

export const publicApi = axios.create({
  baseURL: domain,
  headers: {
    common: {
      Authorization: `Bearer ${token}`
    }
  },
  validateStatus(status: number): boolean {
    if (status == 401) {
      navigateTo("/login")
      return false
    }
    return true
  }
})

publicApi.interceptors.request.use((config) => {  
  config.headers.Authorization = `Bearer ${useToken.value.access}`
  return config
});

export default defineNuxtPlugin(nuxtApp => {
    return {
      provide: {
        api: publicApi
      }
    }
  })