<template>
  <div class="stars">
    <span
      v-for="star in 5"
      :key="star"
      class="star"
      :class="{ active: star <= current }"
      @click="setRating(star)"
    >
      ★
    </span>
    <span class="score" v-if="current > 0">({{ current }}점)</span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['update:modelValue'])

const current = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  current.value = newVal
})

const setRating = (value) => {
  current.value = value
  emit('update:modelValue', value)
}
</script>

<style scoped>
.stars {
  font-size: 28px;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 4px;
}

.star {
  color: #555;
  transition: 0.2s;
}

.star.active {
  color: #e50914;
}

.star:hover {
  transform: scale(1.2);
}

.score {
  margin-left: 10px;
  font-size: 14px;
  opacity: 0.8;
}
</style>
