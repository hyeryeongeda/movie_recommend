<template>
  <TheNavbar />

  <!-- 히어로 영역 -->
  <div class="hero" v-if="heroMovie" :style="heroBgStyle">
    <!-- 좌측 버튼 -->
    <button class="hero-btn left" @click="prevSlide">❮</button>

    <div class="hero-content">
      <h1>{{ heroMovie.title }}</h1>
      <p>{{ heroMovie.overview }}</p>
      <button class="detail-btn" @click="goDetail(heroMovie.id)">
        자세히 보기
      </button>
    </div>

    <!-- 우측 버튼 -->
    <button class="hero-btn right" @click="nextSlide">❯</button>
  </div>

  <div v-else class="hero hero-empty">
    <div class="hero-content">
      <h1>영화가 아직 없습니다</h1>
      <p>Django admin에서 Movie를 추가해보세요.</p>
    </div>
  </div>

  <!-- 영화 Row 섹션 -->
  <MovieRow
    v-if="popularMovies.length > 0"
    title="지금 인기 영화"
    :movies="popularMovies"
  />

  <MovieRow
    v-if="recommendMovies.length > 0"
    title="내 취향 추천"
    :movies="recommendMovies"
  />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter } from "vue-router";
import TheNavbar from "@/components/layout/TheNavbar.vue";
import MovieRow from "@/components/movie/MovieRow.vue";
import api from "@/api/axios";

const router = useRouter();

const movies = ref([]);
const popularMovies = ref([]);
const recommendMovies = ref([]);

const currentHeroIndex = ref(0);
let heroTimer = null;

// 현재 히어로 영화
const heroMovie = computed(() => {
  if (!popularMovies.value.length) return null;
  return popularMovies.value[currentHeroIndex.value];
});

// 배경 이미지 스타일
const heroBgStyle = computed(() => {
  if (!heroMovie.value) return {};
  const url = heroMovie.value.poster_url;
  const finalUrl = url.startsWith("http") ? url : `http://127.0.0.1:8000${url}`;
  return {
    backgroundImage: `url(${finalUrl})`,
  };
});

// 이전 슬라이드
function prevSlide() {
  currentHeroIndex.value =
    (currentHeroIndex.value - 1 + popularMovies.value.length) %
    popularMovies.value.length;
}

// 다음 슬라이드
function nextSlide() {
  currentHeroIndex.value =
    (currentHeroIndex.value + 1) % popularMovies.value.length;
}

const goDetail = (id) => {
  router.push(`/movies/${id}`);
};

// 자동 슬라이드
function startAutoSlide() {
  heroTimer = setInterval(() => {
    nextSlide();
  }, 5000);
}

onMounted(async () => {
  try {
    const res = await api.get("movies/");
    const data = res.data;
    const list = Array.isArray(data) ? data : data.results ?? [];

    movies.value = list;
    popularMovies.value = list.slice(0, 10);

    // 추천도 10개 랜덤
    recommendMovies.value = [...list]
      .sort(() => 0.5 - Math.random())
      .slice(0, 10);

    startAutoSlide();
  } catch (error) {
    console.error("영화 불러오기 실패:", error);
  }
});

onBeforeUnmount(() => {
  if (heroTimer) clearInterval(heroTimer);
});
</script>

<style scoped>
.hero {
  position: relative;
  height: 70vh;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
}

.hero-content {
  margin-left: 60px;
  max-width: 500px;
  z-index: 2;
}

.hero-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  border: none;
  color: white;
  font-size: 40px;
  padding: 10px 18px;
  cursor: pointer;
  border-radius: 6px;
  z-index: 3;
}

.hero-btn.left {
  left: 20px;
}

.hero-btn.right {
  right: 20px;
}

.hero-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

.detail-btn {
  background: #e50914;
  padding: 12px 20px;
  font-size: 16px;
  border-radius: 5px;
}
</style>
