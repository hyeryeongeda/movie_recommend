import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import { useAuth } from '@/stores/auth'

const app = createApp(App)
app.use(router)

const auth = useAuth()
auth.initAuth()

app.mount('#app')
