<template>
  <TheNavbar />

  <div class="auth-page">
    <div class="auth-card">
      <h1>회원가입</h1>
      <p class="subtitle">MYFLIX 계정을 만들어주세요</p>

      <form @submit.prevent="onSubmit">
        <label>
          아이디
          <input
            v-model="username"
            type="text"
            placeholder="아이디를 입력하세요"
            required
          />
        </label>

        <label>
          비밀번호
          <input
            v-model="password1"
            type="password"
            placeholder="비밀번호 (6자 이상)"
            required
          />
        </label>

        <label>
          비밀번호 확인
          <input
            v-model="password2"
            type="password"
            placeholder="비밀번호를 한 번 더 입력"
            required
          />
        </label>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button
          class="submit-btn"
          type="submit"
          :disabled="loading"
        >
          {{ loading ? '가입 중...' : '회원가입' }}
        </button>
      </form>

      <p class="bottom-text">
        이미 계정이 있나요?
        <RouterLink to="/login">로그인하러 가기</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TheNavbar from '@/components/layout/TheNavbar.vue'
import api from '@/api/axios'
import { useAuth } from '@/stores/auth'

const router = useRouter()
const auth = useAuth()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const error = ref('')
const loading = ref(false)

const onSubmit = async () => {
  error.value = ''

  if (password1.value !== password2.value) {
    error.value = '비밀번호가 서로 일치하지 않습니다.'
    return
  }

  if (password1.value.length < 6) {
    error.value = '비밀번호는 최소 6자 이상이어야 합니다.'
    return
  }

  try {
    loading.value = true

    // 1) 회원가입 요청
    await api.post('auth/register/', {
      username: username.value,
      password: password1.value,
    })

    // 2) 바로 로그인까지 시켜주기 (편의성 UP)
    await auth.login(username.value, password1.value)

    alert('회원가입 및 로그인 완료!')
    router.push('/')
  } catch (err) {
    console.error('회원가입 실패:', err)
    if (err.response?.data?.username) {
      // 예: {"username": ["이미 존재하는 아이디입니다."]}
      error.value = err.response.data.username[0]
    } else {
      error.value = '회원가입에 실패했습니다. (아이디 중복 여부를 확인해 주세요)'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 80px; /* 네비바 높이 보정 */
}

.auth-card {
  width: 360px;
  padding: 32px 28px;
  background: #141414;
  color: #fff;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
}

.auth-card h1 {
  font-size: 24px;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #bbbbbb;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

label {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  gap: 4px;
}

input {
  height: 38px;
  border-radius: 6px;
  border: 1px solid #333;
  background: #000;
  color: #fff;
  padding: 0 10px;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #e50914;
}

.error-msg {
  color: #ff7070;
  font-size: 13px;
}

.submit-btn {
  margin-top: 4px;
  height: 40px;
  border-radius: 6px;
  border: none;
  background: #e50914;
  color: #fff;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: default;
}

.bottom-text {
  margin-top: 16px;
  font-size: 13px;
  color: #cccccc;
}

.bottom-text a {
  color: #fff;
  text-decoration: underline;
}
</style>
