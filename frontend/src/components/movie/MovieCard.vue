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
  position: relative;
  min-width: 220px;
  height: 330px;
  background: #141414;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease, z-index 0.3s ease;
  cursor: pointer;
  display: block;
}

.movie-card:hover {
  transform: scale(1.1);
  z-index: 10;
}

.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 아래는 기존 overlay + 한줄평 스타일 */
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
  font-size: 14px;
  font-weight: 600;
}

.rating {
  font-size: 12px;
  margin-top: 2px;
  opacity: 0.9;
}

.short-review {
  margin-top: 6px;
  font-size: 11px;
  line-height: 1.3;
  color: #ddd;
  max-height: 2.6em;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
