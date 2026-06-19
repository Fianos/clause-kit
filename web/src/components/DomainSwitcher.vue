<script setup lang="ts">
import type { DomainId } from '../types'
defineProps<{ modelValue: DomainId }>()
const emit = defineEmits<{ 'update:modelValue': [DomainId] }>()
</script>

<template>
  <div class="domain-switcher">
    <button
      :class="{ active: modelValue === 'eu-ai-act' }"
      @click="emit('update:modelValue', 'eu-ai-act')"
    >EU AI Act</button>
    <button
      :class="{ active: modelValue === 'ndb' }"
      @click="emit('update:modelValue', 'ndb')"
    >NDB (Australia)</button>
  </div>
</template>

<style scoped>
.domain-switcher { display: flex; gap: 4px; }
button {
  padding: 6px 16px; border: 1px solid #ced4da; border-radius: 4px;
  background: #fff; cursor: pointer; font-size: 14px; color: #495057;
}
button.active { background: #1971c2; color: #fff; border-color: #1971c2; }
button:hover:not(.active) { background: #f1f3f5; }
</style>
