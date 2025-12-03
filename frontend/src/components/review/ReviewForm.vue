<template>
  <form class="review-form" @submit.prevent="submitReview">
    <div class="row">
      <input
        v-model="author"
        type="text"
        placeholder="닉네임 (선택)"
      />
    </div>
    <div class="row">
      <textarea
        v-model="content"
        placeholder="이 영화에 대한 한 줄 리뷰를 남겨보세요."
        rows="3"
      ></textarea>
    </div>
    <button type="submit" :disabled="!content.trim()">
      리뷰 남기기
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  movieId: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['created'])

const author = ref('')
const content = ref('')

const submitReview = async () => {
  if (!content.value.trim()) return

  try {
    await api.post(`movies/${props.movieId}/reviews/`, {
      author: author.value,
      content: content.value,
    })

    author.value = ''
    content.value = ''
    emit('created')   // 부모에게 "새 리뷰 만들어짐" 알림
  } catch (error) {
    console.error('리뷰 작성 실패:', error)
    alert('리뷰 작성에 실패했습니다.')
  }
}
</script>

<style scoped>
.review-form {
  margin-top: 30px;
  margin-bottom: 20px;
}
.row {
  margin-bottom: 8px;
}
input,
textarea {
  width: 100%;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid #444;
  background: #111;
  color: white;
}
button {
  margin-top: 6px;
  padding: 8px 14px;
  border-radius: 4px;
  border: none;
  background: #e50914;
  color: white;
  cursor: pointer;
  font-size: 14px;
}
button:disabled {
  background: #555;
  cursor: not-allowed;
}
</style>
