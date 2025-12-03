<template>
  <TheNavbar />

  <div class="page">
    <h1 class="title">영화 전체 보기</h1>

    <p v-if="loading">영화 불러오는 중...</p>
    <p v-else-if="movies.length === 0">등록된 영화가 없습니다.</p>

    <div v-else class="grid">
      <MovieCard
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TheNavbar from '@/components/layout/TheNavbar.vue'
import MovieCard from '@/components/movie/MovieCard.vue'
import api from '@/api/axios'

const movies = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('movies/')
    const data = res.data
    const list = Array.isArray(data) ? data : data.results ?? []
    movies.value = list
  } catch (error) {
    console.error('영화 목록 불러오기 실패:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page {
  padding: 80px 60px 40px;
  color: white;
}

.title {
  font-size: 28px;
  margin-bottom: 20px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}
</style>
