<template>
  <TheNavbar />

  <div class="page">
    <h1 class="title">마이페이지</h1>

    <p class="desc">
      내가 찜한 영화와 본 영화를 한 눈에 볼 수 있어요.
    </p>

    <div v-if="loading">불러오는 중...</div>

    <template v-else>
      <section class="box">
        <h2>👀 보고싶어요</h2>
        <p v-if="wantList.length === 0">보고싶어요로 표시한 영화가 없습니다.</p>
        <div v-else class="grid">
          <MovieCard
            v-for="item in wantList"
            :key="item.id"
            :movie="item.movie"
          />
        </div>
      </section>

      <section class="box">
        <h2>✅ 봤어요</h2>
        <p v-if="doneList.length === 0">봤어요로 표시한 영화가 없습니다.</p>
        <div v-else class="grid">
          <MovieCard
            v-for="item in doneList"
            :key="item.id"
            :movie="item.movie"
          />
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TheNavbar from '@/components/layout/TheNavbar.vue'
import MovieCard from '@/components/movie/MovieCard.vue'
import api from '@/api/axios'
import { useAuth } from '@/stores/auth'

const loading = ref(true)
const wantList = ref([])
const doneList = ref([])
const auth = useAuth()
const fetchWatchList = async () => {
  loading.value = true

  try {
    const res = await api.get('watchlist/me/')
    const items = res.data

    wantList.value = items.filter((item) => item.status === 'WANT')
    doneList.value = items.filter((item) => item.status === 'DONE')
  } catch (error) {
    console.error('워치리스트 불러오기 실패:', error)
  } finally {
    loading.value = false
  }
}


onMounted(fetchWatchList)
</script>

<style scoped>
.page {
  padding: 80px 60px 40px;
  color: white;
}

.title {
  font-size: 28px;
  margin-bottom: 10px;
}

.desc {
  margin-bottom: 20px;
  opacity: 0.9;
}

.box {
  margin-top: 20px;
  padding: 16px 18px;
  border-radius: 8px;
  background: #181818;
}

.box + .box {
  margin-top: 24px;
}

.grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}
</style>
