<script setup lang="ts">
import { computed } from 'vue'
import type { RuleResult } from '../types'

const props = defineProps<{
  results: RuleResult[]
  loading: boolean
}>()

const matched = computed(() => props.results.filter(r => r.matched === true).length)
const notMatched = computed(() => props.results.filter(r => r.matched === false).length)
const notEvaluable = computed(() => props.results.filter(r => r.matched === null).length)
const hasResults = computed(() => props.results.length > 0)
</script>

<template>
  <div class="results-summary">
    <span v-if="loading" class="loading">Evaluating…</span>
    <template v-else-if="hasResults">
      <span class="count matched">{{ matched }} matched</span>
      <span class="count not-matched">{{ notMatched }} no match</span>
      <span class="count not-evaluable">{{ notEvaluable }} Needs expert judgement</span>
      <span class="total">of {{ results.length }} rules</span>
    </template>
    <span v-else class="prompt">Configure facts and click Evaluate</span>
  </div>
</template>

<style scoped>
.results-summary {
  display: flex; align-items: center; gap: 12px; padding: 8px 12px;
  background: #fff; border: 1px solid #dee2e6; border-radius: 6px;
  font-size: 13px;
}
.count { font-weight: 700; padding: 2px 8px; border-radius: 3px; }
.count.matched { background: #ebfbee; color: #2f9e44; }
.count.not-matched { background: #fff5f5; color: #e03131; }
.count.not-evaluable { background: #f1f3f5; color: #868e96; }
.total { color: #868e96; }
.loading { color: #1971c2; font-style: italic; }
.prompt { color: #adb5bd; }
</style>
