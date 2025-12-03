<template>
  <TheNavbar />

  <!-- 1) 로딩 중 -->
  <div v-if="loading" class="detail-page">
    로딩중...
  </div>

  <!-- 2) 영화 데이터가 있을 때 -->
  <div v-else-if="movie" class="detail-page">
    <!-- ✅ 1. 상세 영역 -->
    <div class="detail-hero">
      <div class="poster">
        <img :src="posterSrc" />
      </div>

      <div class="info">
        <h1>{{ movie.title }}</h1>
        <p class="meta">{{ movie.release_year }} · {{ movie.country }}</p>

        <!-- ✅ 장르 태그 -->
        <div class="genre-chips" v-if="movie.genres?.length">
          <span
            v-for="genre in movie.genres"
            :key="genre.id"
            class="chip"
          >
            {{ genre.name }}
          </span>
        </div>

        <!-- ✅ 감독/배우 정보 -->
        <div class="people" v-if="directors.length || actors.length">
          <p v-if="directors.length">
            <strong>감독</strong>
            <span
              v-for="d in directors"
              :key="d.id"
              class="person-name"
            >
              {{ d.person.name }}
            </span>
          </p>

          <p v-if="actors.length">
            <strong>출연</strong>
            <span
              v-for="a in actors"
              :key="a.id"
              class="person-name"
            >
              {{ a.person.name }}
              <span v-if="a.character_name"> ({{ a.character_name }})</span>
            </span>
          </p>
        </div>

        <!-- 별점 컴포넌트 -->
        <RatingStar v-model="myRating" />

        <WatchButtons :movie-id="movie.id" />

        <p class="overview">{{ movie.overview }}</p>

        <!-- ✅ 리뷰 작성 + 목록 -->
        <ReviewForm
          :movie-id="movie.id"
          @created="onReviewCreated"
        />

        <ReviewList
          :movie-id="movie.id"
          :reload-key="reviewsReloadKey"
        />

      </div>
  
    </div>

    <!-- ✅ 2. 아래에 비슷한 영화 -->
    <section class="similar-section" v-if="similarMovies.length > 0">
      <MovieRow
        title="비슷한 영화 추천"
        :movies="similarMovies"
      />
    </section>
  </div>

  <!-- 3) 영화 못 불러왔을 때 -->
  <div v-else class="detail-page">
    영화를 불러오지 못했습니다.
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/stores/auth'
import MovieRow from '@/components/movie/MovieRow.vue'
import TheNavbar from '@/components/layout/TheNavbar.vue'
import RatingStar from '@/components/movie/RatingStar.vue'
import WatchButtons from '@/components/movie/WatchButtons.vue'
import ReviewForm from '@/components/review/ReviewForm.vue'
import ReviewList from '@/components/review/ReviewList.vue'
import api from '@/api/axios'
const reviewsReloadKey = ref(0)

const onReviewCreated = () => {
  // 리뷰가 새로 작성될 때마다 key를 바꿔서 ReviewList를 다시 불러오게 함
  reviewsReloadKey.value++
}
const auth = useAuth()


const route = useRoute()

const movie = ref(null)
const similarMovies = ref([])
const loading = ref(true)
const myRating = ref(0)

const directors = ref([])
const actors = ref([])

// 포스터 URL 계산
const posterSrc = computed(() => {
  if (!movie.value?.poster_url) return ''
  const url = movie.value.poster_url
  return url.startsWith('http')
    ? url
    : `http://127.0.0.1:8000${url}`
})

// ✅ 영화 불러올 때 내 점수 세팅
const fetchMovie = async (id) => {
  console.log("📌 Fetch Movie:", id)
  loading.value = true

  try {
    const res = await api.get(`movies/${id}/`)
    console.log("📌 API Response movie:", res.data)

    movie.value = res.data

    // 여기서 user_score 를 myRating 에 반영
    myRating.value = movie.value.user_score ?? 0

    // ...비슷한 영화 부분은 그대로
  } catch (err) {
    console.error("❌ fetchMovie ERROR:", err)
  } finally {
    loading.value = false
  }
}
// ✅ 별점 변경 시 서버에 저장 + 다시 불러오기
const onChangeRating = async (score) => {
  if (!auth.isAuthenticated) {
    alert('평점은 로그인 후 남길 수 있습니다.')
    // 로그인 안 되어 있으면 별 다시 0으로 돌려도 됨
    myRating.value = movie.value?.user_score ?? 0
    return
  }
  if (!movie.value) return

  try {
    console.log('⭐ 평점 저장 요청:', movie.value.id, score)

    await api.post(`movies/${movie.value.id}/ratings/`, {
      score,
    })

    // 평균 점수 / 내 점수 최신값으로 다시 가져오기
    await fetchMovie(movie.value.id)
  } catch (error) {
    console.error('평점 저장 실패:', error)
  }
}


onMounted(() => {
  fetchMovie(route.params.id)
})

watch(() => route.params.id, (newId, oldId) => {
  console.log("📌 route changed:", oldId, "→", newId)
  if (newId) fetchMovie(newId)
})
// myRating 값이 바뀔 때마다 서버에 저장
watch(myRating, (newScore, oldScore) => {
  // 0 → 0 같은 초기 세팅은 무시
  if (!movie.value) return
  if (newScore === oldScore) return
  if (!newScore) return

  onChangeRating(newScore)
})

</script>

<style scoped>
.detail-page {
  padding: 40px 60px;
  color: white;
}

.detail-hero {
  display: flex;
  align-items: center;
  gap: 60px;
  padding: 40px 20px;
}

.poster img {
  width: 260px;
  border-radius: 8px;
  object-fit: cover;
}

.info {
  max-width: 600px;
}

.meta {
  margin-top: 10px;
  opacity: 0.8;
}

.overview {
  margin-top: 20px;
  line-height: 1.6;
}

.similar-section {
  padding: 40px 0;
}
.genre-chips {
  margin-top: 8px;
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chip {
  padding: 4px 8px;
  border-radius: 999px;
  background: #262626;
  font-size: 12px;
}

.people {
  margin-top: 8px;
  margin-bottom: 12px;
  font-size: 13px;
}

.people p {
  margin: 2px 0;
}

.person-name + .person-name::before {
  content: ' · ';
}

</style>
