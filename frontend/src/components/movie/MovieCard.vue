<template>
  <RouterLink :to="`/movies/${movie.id}`" class="movie-card">
    <img :src="posterSrc" alt="포스터" />

    <div class="overlay">
      <h4 class="title">{{ movie.title }}</h4>
      <p class="rating">⭐ {{ movie.avg_score ?? "평점 없음" }}</p>

      <!-- ✅ 한줄평 영역 -->
      <p v-if="movie.short_review" class="short-review">
        “{{ movie.short_review }}”
      </p>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
});

const posterSrc = computed(() => {
  const url = props.movie.poster_url;
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `http://127.0.0.1:8000${url}`;
});
</script>

<style scoped>
.movie-card {
  position: relative;    /* 카드가 flex 안에서 절대 줄어들지 않도록 고정 */
  flex: 0 0 180px;      /* 🔥 카드 고정 폭 */
  height: 270px;     /* 원하는 비율로 높이 */
  width: 220px;
  aspect-ratio: 2 / 3;
  background: #141414;  /* 여백 색 */
  border-radius: 10px;
  overflow: hidden;
}

.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: contain;     /* 잘림 X, 대신 레터박스 */
}


.movie-card:hover {
  transform: scale(1.1);
  z-index: 10;
}

.overlay {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 10px 12px;
  background: linear-gradient(
    transparent,
    rgba(0, 0, 0, 0.8),
    rgba(0, 0, 0, 0.95)
  );
  box-sizing: border-box;
}

.title {
  margin-top: 6px;
  font-size: 14px;
  font-weight: 600;
}

.rating {
  font-size: 12px;
  margin-top: 2px;
  opacity: 0.9;
}

.short-review {
  margin-top: 20px;
  font-size: 11px;
  line-height: 1.3;
  color: #ddd;
  max-height: 2.6em;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
