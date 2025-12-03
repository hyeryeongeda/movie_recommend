<template>
  <div class="row" v-if="movies && movies.length > 0">
    <h2 class="row-title">{{ title }}</h2>

    <button
      class="arrow left"
      @click="scrollLeft"
    >
      ◀
    </button>

    <button
      class="arrow right"
      @click="scrollRight"
    >
      ▶
    </button>

    <div class="movies" ref="movieContainer">
      <MovieCard
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieCard from './MovieCard.vue'

defineProps({
  title: String,
  movies: {
    type: Array,
    default: () => [],
  },
})

const movieContainer = ref(null)

const scrollLeft = () => {
  movieContainer.value?.scrollBy({
    left: -400,
    behavior: 'smooth',
  })
}

const scrollRight = () => {
  movieContainer.value?.scrollBy({
    left: 400,
    behavior: 'smooth',
  })
}
</script>

<style scoped>
.row {
  position: relative;
  margin: 40px 0;
  padding: 0 60px;
}

.row-title {
  color: white;
  font-size: 22px;
  margin-bottom: 10px;
}

.movies {
  display: flex;
  gap: 20px;
  overflow-x: hidden;
  padding: 10px 0;
  min-height: 260px;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: #141414;
  border: none;
  color: white;
  font-size: 22px;
  padding: 12px;
  cursor: pointer;
  z-index: 10;
}

.arrow.left {
  left: 20px;
}

.arrow.right {
  right: 20px;
}
</style>
