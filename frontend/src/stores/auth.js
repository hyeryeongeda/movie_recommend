// src/stores/auth.js
import { reactive, computed } from 'vue'
import api from '@/api/axios'

const state = reactive({
  access: null,
  refresh: null,
  user: null,
  loaded: false,
})

const isAuthenticated = computed(() => !!state.access)

function loadFromStorage() {
  const access = localStorage.getItem('access')
  const refresh = localStorage.getItem('refresh')

  state.access = access || null
  state.refresh = refresh || null
}

async function fetchMe() {
  if (!state.access) {
    state.user = null
    return
  }

  try {
    const res = await api.get('auth/me/')
    state.user = res.data
  } catch (error) {
    console.error('내 정보 가져오기 실패, 토큰 정리:', error)
    // 토큰이 만료/이상하면 정리
    logout()
  }
}

async function initAuth() {
  loadFromStorage()
  if (state.access) {
    await fetchMe()
  }
  state.loaded = true
}

async function login(username, password) {
  const res = await api.post('auth/login/', { username, password })

  state.access = res.data.access
  state.refresh = res.data.refresh

  localStorage.setItem('access', state.access)
  localStorage.setItem('refresh', state.refresh)

  await fetchMe()
}

function logout() {
  state.access = null
  state.refresh = null
  state.user = null
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}

export function useAuth() {
  return {
    state,
    isAuthenticated,
    initAuth,
    login,
    logout,
    fetchMe,
  }
}
