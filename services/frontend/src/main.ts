import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import { themeChange } from 'theme-change'

import App from './App.vue'
import router from './router'

themeChange(false)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
