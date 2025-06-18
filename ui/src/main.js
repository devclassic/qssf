import { createPinia } from 'pinia'
import { createApp } from 'vue'
import BaiduMap from 'vue-baidu-map-3x'
import router from './router'
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(BaiduMap, { ak: 'qQYN9vAgKhRohxyeoDODMCRlAG3jPB9p' })
app.mount('#app')
