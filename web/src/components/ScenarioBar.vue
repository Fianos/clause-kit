<script setup lang="ts">
import type { Scenario } from '../types'
defineProps<{ scenarios: Scenario[] }>()
const emit = defineEmits<{ load: [Scenario] }>()
</script>

<template>
  <div class="scenario-bar">
    <p class="label">Preset scenarios</p>
    <div class="scenario-buttons">
      <button
        v-for="s in scenarios"
        :key="s.id"
        :title="s.description"
        @click="emit('load', s)"
      >{{ s.label }}</button>
    </div>
  </div>
</template>

<style scoped>
.scenario-bar { padding: 10px 12px; background: #fff; border: 1px solid #dee2e6; border-radius: 6px; }
.label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #868e96; margin-bottom: 6px; }
.scenario-buttons { display: flex; flex-wrap: wrap; gap: 6px; }
button {
  padding: 4px 10px; font-size: 12px; border: 1px solid #ced4da;
  border-radius: 4px; background: #f8f9fa; cursor: pointer; color: #212529;
}
button:hover { background: #e9ecef; }
</style>
