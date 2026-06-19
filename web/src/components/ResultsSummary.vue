<script setup lang="ts">
import { computed } from 'vue'
import type { RuleResult } from '../types'

type FilterStatus = 'matched' | 'not-matched' | 'not-evaluable' | null

const props = defineProps<{
  results: RuleResult[]
  loading: boolean
  filter: FilterStatus
}>()

const emit = defineEmits<{ 'update:filter': [FilterStatus] }>()

const matched = computed(() => props.results.filter(r => r.matched === true).length)
const notMatched = computed(() => props.results.filter(r => r.matched === false).length)
const notEvaluable = computed(() => props.results.filter(r => r.matched === null).length)
const hasResults = computed(() => props.results.length > 0)

function toggle(status: FilterStatus) {
  emit('update:filter', props.filter === status ? null : status)
}
</script>

<template>
  <div class="results-summary">
    <span v-if="loading" class="loading">Evaluating…</span>
    <template v-else-if="hasResults">
      <button
        class="count applies"
        :class="{ active: filter === 'matched' }"
        @click="toggle('matched')"
        title="Filter to rules that apply to this scenario"
      >{{ matched }} applies</button>
      <button
        class="count not-triggered"
        :class="{ active: filter === 'not-matched' }"
        @click="toggle('not-matched')"
        title="Filter to rules that do not apply"
      >{{ notMatched }} not triggered</button>
      <button
        class="count not-evaluable"
        :class="{ active: filter === 'not-evaluable' }"
        @click="toggle('not-evaluable')"
        title="Filter to rules requiring expert legal judgement"
      >{{ notEvaluable }} needs review</button>
      <span class="total">of {{ results.length }} rules</span>
      <button v-if="filter" class="clear-filter" @click="toggle(null)">clear filter ×</button>
    </template>
    <span v-else class="prompt">Configure facts and click Evaluate</span>
  </div>
</template>

<style scoped>
.results-summary {
  display: flex; align-items: center; gap: 8px; padding: 8px 12px;
  background: #fff; border: 1px solid #dee2e6; border-radius: 6px;
  font-size: 13px;
}
.count {
  font-weight: 700; padding: 2px 8px; border-radius: 3px;
  border: 2px solid transparent; cursor: pointer; font-size: 13px;
  font-family: inherit; transition: border-color 0.1s;
}
.count:hover { opacity: 0.8; }
.count.applies { background: #e7f5ff; color: #1971c2; }
.count.applies.active { border-color: #1971c2; }
.count.not-triggered { background: #f1f3f5; color: #868e96; }
.count.not-triggered.active { border-color: #868e96; }
.count.not-evaluable { background: #fff9db; color: #e67700; }
.count.not-evaluable.active { border-color: #e67700; }
.total { color: #868e96; margin-left: 4px; }
.clear-filter {
  margin-left: auto; font-size: 12px; color: #1971c2; background: none;
  border: none; cursor: pointer; padding: 2px 6px;
}
.clear-filter:hover { text-decoration: underline; }
.loading { color: #1971c2; font-style: italic; }
.prompt { color: #adb5bd; }
</style>
