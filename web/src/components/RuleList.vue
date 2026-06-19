<script setup lang="ts">
import { ref } from 'vue'
import type { Rule, RuleResult } from '../types'

const props = defineProps<{
  rules: Rule[]
  results: RuleResult[]
}>()

const expanded = ref<Set<string>>(new Set())

function toggle(ruleId: string) {
  if (expanded.value.has(ruleId)) {
    expanded.value.delete(ruleId)
  } else {
    expanded.value.add(ruleId)
  }
}

function resultFor(ruleId: string): RuleResult | undefined {
  return props.results.find(r => r.rule_id === ruleId)
}

function statusClass(result: RuleResult | undefined): string {
  if (!result) return ''
  if (result.matched === true) return 'matched'
  if (result.matched === false) return 'not-matched'
  return 'not-evaluable'
}

function statusLabel(result: RuleResult | undefined): string {
  if (!result) return '—'
  if (result.matched === true) return 'MATCHED'
  if (result.matched === false) return 'NO MATCH'
  return 'NOT EVALUABLE'
}
</script>

<template>
  <div class="rule-list">
    <div
      v-for="rule in rules"
      :key="rule.rule_id"
      class="rule-row"
      :class="statusClass(resultFor(rule.rule_id))"
      @click="toggle(rule.rule_id)"
    >
      <div class="rule-row-header">
        <span class="status-chip">{{ statusLabel(resultFor(rule.rule_id)) }}</span>
        <span class="rule-label">{{ rule.label }}</span>
        <span class="codif-badge" :class="rule.codifiability">{{ rule.codifiability }}</span>
        <span class="expand-icon">{{ expanded.has(rule.rule_id) ? '▲' : '▼' }}</span>
      </div>
      <div v-if="expanded.has(rule.rule_id)" class="rule-inspector">
        <!-- TODO: Inspector -->
        <p><strong>Rule ID:</strong> {{ rule.rule_id }}</p>
        <p><strong>Scope:</strong> {{ rule.scope }}</p>
        <p><strong>Obligation:</strong> {{ rule.obligation }}</p>
        <p v-if="rule.exceptions.length"><strong>Exceptions:</strong></p>
        <ul v-if="rule.exceptions.length">
          <li v-for="ex in rule.exceptions" :key="ex">{{ ex }}</li>
        </ul>
        <div v-if="rule.condition">
          <strong>Condition (JSON Logic):</strong>
          <pre>{{ JSON.stringify(rule.condition, null, 2) }}</pre>
        </div>
        <div v-else class="condition-null">Not codifiable</div>
        <p>
          <strong>Source:</strong>
          {{ rule.docref.article }} {{ rule.docref.section }} —
          <a :href="rule.docref.url" target="_blank" rel="noopener">{{ rule.docref.source_doc }}</a>
        </p>
        <p v-if="rule.docref.provision_uri">
          <strong>Provision URI:</strong>
          <code>{{ rule.docref.provision_uri }}</code>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rule-list { display: flex; flex-direction: column; gap: 4px; }

.rule-row {
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  background: #fff;
  transition: background 0.1s;
}
.rule-row:hover { background: #f1f3f5; }
.rule-row.matched { border-left: 4px solid #2f9e44; }
.rule-row.not-matched { border-left: 4px solid #e03131; }
.rule-row.not-evaluable { border-left: 4px solid #868e96; }

.rule-row-header { display: flex; align-items: center; gap: 8px; }

.status-chip {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 3px;
  min-width: 100px;
  text-align: center;
  background: #e9ecef;
  color: #495057;
}
.matched .status-chip { background: #ebfbee; color: #2f9e44; }
.not-matched .status-chip { background: #fff5f5; color: #e03131; }
.not-evaluable .status-chip { background: #f1f3f5; color: #868e96; }

.rule-label { flex: 1; font-size: 13px; }

.codif-badge {
  font-size: 10px;
  padding: 2px 5px;
  border-radius: 2px;
  text-transform: uppercase;
  font-weight: 600;
}
.codif-badge.high { background: #fff9db; color: #e67700; }
.codif-badge.medium { background: #e7f5ff; color: #1971c2; }
.codif-badge.low { background: #f1f3f5; color: #868e96; }

.expand-icon { color: #adb5bd; font-size: 10px; }

.rule-inspector {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e9ecef;
  font-size: 13px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.rule-inspector pre {
  background: #f1f3f5;
  padding: 8px;
  border-radius: 3px;
  font-size: 11px;
  overflow-x: auto;
  white-space: pre-wrap;
}

.condition-null {
  color: #6c757d;
  font-style: italic;
}
</style>
