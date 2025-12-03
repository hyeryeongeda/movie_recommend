// src/api/axios.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
})

// 🔑 모든 요청에 access 토큰을 자동으로 실어주기
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      // DJango SimpleJWT 기본 포맷: "Bearer <token>"
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

export default api
