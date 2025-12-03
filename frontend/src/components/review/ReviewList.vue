<template>
  <div class="review-list">
    <h3>리뷰</h3>

    <p v-if="loading">리뷰 불러오는 중...</p>
    <p v-else-if="reviews.length === 0">아직 작성된 리뷰가 없습니다.</p>

    <ReviewItem
      v-for="review in reviews"
      :key="review.id"
      :review="review"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import ReviewItem from './ReviewItem.vue'
import api from '@/api/axios'

const props = defineProps({
  movieId: {
    type: Number,
    required: true,
  },
  reloadKey: {
    type: Number,
    default: 0,
  },
})

const reviews = ref([])
const loading = ref(false)

const fetchReviews = async () => {
  if (!props.movieId) return
  loading.value = true
  try {
    const res = await api.get(`movies/${props.movieId}/reviews/`)
    reviews.value = res.data
  } catch (error) {
    console.error('리뷰 목록 불러오기 실패:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchReviews)
watch(() => props.reloadKey, fetchReviews)
</script>

<style scoped>
.review-list {
  margin-top: 10px;
  color: white;
}
.review-list h3 {
  margin-bottom: 10px;
}
</style>
