import { useToken } from "~/composables/token"
import { publicApi } from '~/plugins/api'

const isAuthenticated = () => {  
  if (!useToken.value.access) {
    return false
  }
  const payload = JSON.parse(atob(useToken.value.access?.split(".")[1]))
  const test = payload.exp > Date.now() / 1000
  if (!test) {
    publicApi.post('/oauth/refresh-token/', {refresh: useToken.value.refresh}).then((r) => {
      useToken.value.access = r.data.access
    })
    return true
  }
  return test
}

export default defineNuxtRouteMiddleware(() => {
    // isAuthenticated() is an example method verifying if a user is authenticated
    
    if (false) {
      return navigateTo('/login')
    }
})