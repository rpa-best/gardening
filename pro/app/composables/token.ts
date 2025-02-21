import { useStorage } from '@vueuse/core'

export default useStorage('token', { access: null, refresh: null })
