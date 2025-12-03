<template>
  <div class="watch-buttons">
    <button
      :class="['btn', currentStatus === 'WANT' ? 'active' : '']"
      @click="setStatus('WANT')"
    >
      👀 보고싶어요
    </button>

    <button
      :class="['btn', currentStatus === 'DONE' ? 'active' : '']"
      @click="setStatus('DONE')"
    >
      ✅ 봤어요
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  movieId: {
    type: Number,
    required: true,
  },
  initialStatus: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['updated'])

const currentStatus = ref(props.initialStatus)
const loading = ref(false)

watch(
  () => props.initialStatus,
  (val) => {
    currentStatus.value = val
  }
)

const setStatus = async (status) => {
  console.log('버튼 클릭, status = ', status)  // ✅ 이 줄 추가

  if (loading.value) return
  loading.value = true

  try {
    const res = await api.post(`movies/${props.movieId}/watchlist-toggle/`, {
      status,
    })
    console.log('워치리스트 응답:', res.data)  // ✅ 응답도 확인

    currentStatus.value = res.data.status
    emit('updated', currentStatus.value)
  } catch (error) {
    console.error('워치리스트 변경 실패:', error)
    alert('상태 변경에 실패했습니다.')
  } finally {
    loading.value = false
  }
}

</script>


<style scoped>
.watch-buttons {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.btn {
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid #555;
  background: transparent;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
}

.btn.active {
  background: #e50914;
  border-color: #e50914;
}
</style>
