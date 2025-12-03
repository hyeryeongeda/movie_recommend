<!-- src/components/review/ReviewItem.vue -->
<template>
  <div class="review-item">
    <div class="header">
      <span class="author">{{ review.user_nickname || '익명' }}</span>
      <span class="date">{{ review.created_at.slice(0, 10) }}</span>
    </div>

    <p class="content">
      {{ review.content }}
    </p>

    <div class="footer">
      <!-- ✅ 좋아요 버튼 -->
      <button
        class="like-btn"
        @click="toggleLike"
      >
        <span v-if="isLiked">❤️</span>
        <span v-else>🤍</span>
        좋아요 {{ likeCount }}개
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import { useAuth } from '@/stores/auth'

const props = defineProps({
  review: {
    type: Object,
    required: true,
  },
})

const auth = useAuth()

// 화면에 보이는 개수 / 상태
const likeCount = ref(props.review.like_count ?? 0)
// 백엔드에서 is_liked 안 주면 일단 false 로 시작
const isLiked = ref(props.review.is_liked ?? false)

const toggleLike = async () => {
  if (!auth.isAuthenticated) {
    alert('좋아요는 로그인 후 이용 가능합니다.')
    return
  }

  try {
    const res = await api.post(`reviews/${props.review.id}/like/`)
    isLiked.value = res.data.liked
    likeCount.value = res.data.like_count
  } catch (error) {
    console.error('리뷰 좋아요 실패', error)
  }
}
</script>
<style scoped>
.review-item {
  padding: 10px 0;
  border-bottom: 1px solid #333;
}
.header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 4px;
  opacity: 0.8;
}

.content {
  margin: 6px 0 10px;
}

.footer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: 1px solid #444;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  color: #fff;
  cursor: pointer;
}
.top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}
.author {
  font-size: 14px;
}
.date {
  font-size: 12px;
  opacity: 0.7;
}
.content {
  font-size: 14px;
  line-height: 1.4;
}
.meta {
  margin-top: 4px;
  font-size: 12px;
  opacity: 0.8;
}
</style>
