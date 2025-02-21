import { defu } from 'defu'
import type { UseFetchOptions } from '#app'
import token from '~/composables/token'
import { get_api } from '~/utils'

export default defineNuxtPlugin(() => {
  return {
    provide: {
      api: useIFetch
    }
  }
})

const baseURL = get_api

export async function useIFetch<T>(
  url: string,
  options: UseFetchOptions<T> = {}
) {
  const defaults: UseFetchOptions<T> = {
    method: 'GET',
    baseURL,
    key: url,
    headers: token.value.access
      ? { Authorization: `Bearer ${token.value.access}` }
      : {}
  }

  const params = defu(options, defaults)

  const response = await useFetch(url, params)
  if (response.status.value === 'error') {
    if (response.error.value.statusCode === 401) {
      if (token.value.refresh) {
        const newToken = await refreshToken()
        token.value.access = newToken

        params.headers = { Authorization: `Bearer ${newToken}` }
        return await useFetch(url, params as UseFetchOptions<T>)
      }
      await useRouter().push(useLocalePath()(`/login?next=${useRoute().fullPath}`))
    }
    const message = Object.values(response.error.value.data).map(v => {
      if (typeof v === 'string') {
        return v
      } else if (typeof v === 'object') {
        return v.message
      } else {
        return v.join('. ')
      }
    }).join('. ')
    if (response.error.value.statusCode !== 403) {
      useToast().add({ title: message, icon: 'i-heroicons-x-circle-16-solid', color: 'red' })
    }
    throw Error(message)
  } else if (!['GET', 'HEAD'].includes(params.method)) {
    console.log(response)
    useToast().add({
      title: `Операция выполнена успешно`,
      icon: 'i-heroicons-x-circle-16-solid',
      color: 'green'
    })
  }
  return response
}

async function refreshToken() {
  const refreshToken = useCookie('refreshToken')

  const { data, status } = await useFetch<{ access: string }>(
    `${baseURL}oauth/refresh-token/`,
    {
      method: 'POST',
      body: { refresh: refreshToken.value }
    }
  )

  if (status.value === 'success') {
    return data.value?.access
  } else {
    await useRouter().push(useLocalePath()(`/login?next=${useRoute().path}`))
    throw new Error('Token refresh failed')
  }
}
