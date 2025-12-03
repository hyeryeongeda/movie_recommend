<template>
  <nav class="nav">
    <div class="logo" @click="goHome">MYFLIX</div>

    <ul class="menu">
      <li><RouterLink to="/">홈</RouterLink></li>
      <li><RouterLink to="/movies">영화</RouterLink></li>
      <li><RouterLink to="/mypage">마이페이지</RouterLink></li>
    </ul>

    <div class="right">
      <span class="icon">🔍</span>

      <!-- 로그인 안 된 상태: access 토큰이 없을 때 -->
      <RouterLink
        v-if="!auth.state.access"
        to="/login"
        class="login-link"
      >
        로그인
      </RouterLink>

      <!-- 로그인 된 상태: access 토큰이 있을 때 -->
      <div v-else class="user-area">
        <span class="username">{{ auth.state.user?.username || '유저' }}</span>
        <button @click="onLogout">로그아웃</button>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'

const router = useRouter()
const auth = useAuth()

// ⭐⭐ 가장 중요한 부분 — state.user 초기화 ⭐⭐
onMounted(() => {
  auth.initAuth()
})

const goHome = () => {
  router.push('/')
}

const onLogout = () => {
  auth.logout()
  router.push('/')
}
</script>



<style scoped>
.nav {
  height: 60px;
  background: #000;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
}

.logo {
  font-weight: bold;
  cursor: pointer;
}

.menu {
  display: flex;
  gap: 20px;
  list-style: none;
}

.menu a {
  color: white;
  text-decoration: none;
}

.menu a.router-link-active {
  font-weight: bold;
}

.right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-area button {
  background: transparent;
  border: 1px solid #555;
  color: white;
  border-radius: 16px;
  padding: 4px 10px;
  cursor: pointer;
  font-size: 12px;
}

.login-link {
  color: white;
  text-decoration: none;
  font-size: 14px;
}

.icon {
  font-size: 16px;
}
</style>
