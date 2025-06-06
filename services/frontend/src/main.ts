import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { plugin, defaultConfig } from '@formkit/vue'
import { themeChange } from 'theme-change'

import App from './App.vue'
import router from './router'

themeChange(false)

const app = createApp(App)

app.use(plugin, defaultConfig)
app.use(createPinia())
app.use(router)

app.mount('#app')
