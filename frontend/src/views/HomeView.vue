<template>
  <TheNavbar />
  <div class="home-page">
    <div class="hero" v-if="heroMovie" :style="heroBgStyle">
      <div class="hero-overlay"></div>

      <div class="hero-content">
        <h1 class="hero-title">{{ heroMovie.title }}</h1>

        <button class="detail-btn" @click="goDetail(heroMovie.id)">
          자세히 보기
        </button>
      </div>

      <!-- 좌/우 슬라이드 버튼 -->
      <button class="slide-btn left" @click="prevSlide">‹</button>
      <button class="slide-btn right" @click="nextSlide">›</button>
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
  </div>
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
.home-page {
  padding: 60px;
}
.hero {
  position: relative;
  height: 70vh;
  background-size: contain;   /* 🔥 이미지 전체 보이게 */
  background-repeat: no-repeat;
  background-position: center;
  background-color: #000;     /* 포스터 비율 남는 부분 검정 */
  display: flex;
  align-items: flex-end;
  padding: 40px 60px;
  color: white;
}


.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0));
}

.hero-content {
  position: absolute;
  bottom: 40px;
  left: 60px;
  z-index: 10;
}

.hero-title {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 16px;
}

.detail-btn {
  background: #e50914;
  padding: 12px 22px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 18px;
}

.slide-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 48px;
  color: white;
  background: rgba(0,0,0,0.3);
  border: none;
  cursor: pointer;
  padding: 10px 20px;
  z-index: 20;
  border-radius: 5px;
}

.slide-btn.left { left: 20px; }
.slide-btn.right { right: 20px; }

.slide-btn:hover {
  background: rgba(0,0,0,0.6);
}


</style>
