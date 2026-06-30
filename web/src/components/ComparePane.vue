<script setup lang="ts">
import { ref } from 'vue'
import { compare as apiCompare } from '../api'
import type { ComparisonResult } from '../types'

const SECTIONS = [
  { id: '26wa', label: '26WA — Eligible data breach' },
]

const selectedSection = ref('26wa')
const result = ref<ComparisonResult | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function runComparison() {
  loading.value = true
  error.value = null
  result.value = null
  try {
    result.value = await apiCompare('ndb', selectedSection.value)
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="compare-pane">
    <div class="compare-intro">
      <p>Runs the same NDB section through two extraction paths: plain text (XML tags stripped) vs AKN-structured XML. Same model, same prompt — only the input format differs.</p>
    </div>

    <div class="compare-controls">
      <div class="field">
        <label>Section</label>
        <select v-model="selectedSection">
          <option v-for="s in SECTIONS" :key="s.id" :value="s.id">{{ s.label }}</option>
        </select>
      </div>
      <button class="run-btn" :disabled="loading" @click="runComparison">
        {{ loading ? 'Running...' : 'Run comparison' }}
      </button>
      <span v-if="loading" class="loading-note">Making 2 Claude API calls — may take 20–30s</span>
    </div>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <div v-if="result" class="compare-grid">
      <div class="col">
        <h3 class="col-label">Plain text <span class="rule-count">{{ result.plain_rules.length }} rules</span></h3>
        <div v-if="result.plain_rules.length === 0" class="empty">No rules extracted.</div>
        <div v-for="r in result.plain_rules" :key="r.rule_id" class="rule-card">
          <div class="rule-label">{{ r.label }}</div>
          <div class="rule-meta">
            <span :class="['codif', r.codifiability]">{{ r.codifiability }}</span>
            <span class="section-ref">{{ r.docref.section }}</span>
          </div>
          <pre v-if="r.condition" class="rule-condition">{{ JSON.stringify(r.condition, null, 2) }}</pre>
          <div v-else class="rule-null">condition: null</div>
        </div>
      </div>

      <div class="col">
        <h3 class="col-label">AKN structured <span class="rule-count">{{ result.akn_rules.length }} rules</span></h3>
        <div v-if="result.akn_rules.length === 0" class="empty">No rules extracted.</div>
        <div v-for="r in result.akn_rules" :key="r.rule_id" class="rule-card">
          <div class="rule-label">{{ r.label }}</div>
          <div class="rule-meta">
            <span :class="['codif', r.codifiability]">{{ r.codifiability }}</span>
            <span class="section-ref">{{ r.docref.section }}</span>
            <span v-if="r.docref.provision_uri" class="provision-uri">{{ r.docref.provision_uri }}</span>
          </div>
          <pre v-if="r.condition" class="rule-condition">{{ JSON.stringify(r.condition, null, 2) }}</pre>
          <div v-else class="rule-null">condition: null</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.compare-pane { padding: 16px 20px; display: flex; flex-direction: column; gap: 16px; }
.compare-intro { background: #f8f9fa; border-left: 3px solid #1971c2; padding: 10px 14px; font-size: 13px; color: #495057; border-radius: 0 4px 4px 0; }
.compare-controls { display: flex; align-items: flex-end; gap: 12px; flex-wrap: wrap; }
.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 12px; font-weight: 600; color: #495057; }
.field select { padding: 6px 8px; border: 1px solid #ced4da; border-radius: 4px; font-size: 13px; }
.run-btn { padding: 8px 18px; background: #1971c2; color: #fff; border: none; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer; }
.run-btn:disabled { background: #adb5bd; cursor: not-allowed; }
.run-btn:not(:disabled):hover { background: #1864ab; }
.loading-note { font-size: 12px; color: #868e96; align-self: center; }
.error-banner { background: #fff5f5; color: #e03131; padding: 8px 14px; border-radius: 4px; font-size: 13px; }
.compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.col { display: flex; flex-direction: column; gap: 8px; }
.col-label { font-size: 14px; font-weight: 700; color: #212529; display: flex; align-items: center; gap: 8px; margin: 0; }
.rule-count { font-size: 12px; font-weight: 400; color: #868e96; }
.rule-card { background: #fff; border: 1px solid #dee2e6; border-radius: 6px; padding: 10px 12px; display: flex; flex-direction: column; gap: 4px; }
.rule-label { font-size: 13px; font-weight: 600; color: #212529; }
.rule-meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.codif { font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 3px; text-transform: uppercase; }
.codif.high { background: #d3f9d8; color: #2b8a3e; }
.codif.medium { background: #fff3bf; color: #875a00; }
.codif.low { background: #f1f3f5; color: #868e96; }
.section-ref { font-size: 12px; color: #495057; }
.provision-uri { font-size: 11px; color: #1971c2; font-family: monospace; }
.rule-condition { font-size: 11px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 6px 8px; margin: 0; white-space: pre-wrap; overflow-x: auto; }
.rule-null { font-size: 12px; color: #adb5bd; font-style: italic; }
.empty { font-size: 13px; color: #868e96; text-align: center; padding: 20px; }
</style>
