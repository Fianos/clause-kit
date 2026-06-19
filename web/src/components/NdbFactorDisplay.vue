<script setup lang="ts">
import type { NdbDataCategory } from '../types'

const props = defineProps<{ modelValue: NdbDataCategory[] }>()
const emit = defineEmits<{ 'update:modelValue': [NdbDataCategory[]] }>()

const CATEGORIES: NdbDataCategory[] = ['health', 'financial', 'identity', 'biometric', 'sensitive']

function toggle(cat: NdbDataCategory) {
  const current = [...props.modelValue]
  const idx = current.indexOf(cat)
  if (idx === -1) {
    current.push(cat)
  } else {
    current.splice(idx, 1)
  }
  emit('update:modelValue', current)
}
</script>

<template>
  <div class="ndb-factors">
    <label v-for="cat in CATEGORIES" :key="cat" class="factor-check">
      <input
        type="checkbox"
        :checked="modelValue.includes(cat)"
        @change="toggle(cat)"
      />
      {{ cat }}
    </label>
  </div>
</template>

<style scoped>
.ndb-factors { display: flex; flex-wrap: wrap; gap: 6px; }
.factor-check { display: flex; align-items: center; gap: 4px; cursor: pointer; font-size: 13px; }
</style>
