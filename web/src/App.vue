<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import DomainSwitcher from './components/DomainSwitcher.vue'
import ScenarioBar from './components/ScenarioBar.vue'
import SandboxPane from './components/SandboxPane.vue'
import ResultsSummary from './components/ResultsSummary.vue'
import RuleList from './components/RuleList.vue'
import ComparePane from './components/ComparePane.vue'
import { fetchDomain, fetchScenarios, evaluate as apiEvaluate } from './api'
import type { DomainId, EuFacts, NdbFacts, Rule, RuleResult, Scenario } from './types'
import { DEFAULT_EU_FACTS, DEFAULT_NDB_FACTS } from './types'

const domain = ref<DomainId>('eu-ai-act')
const facts = ref<EuFacts | NdbFacts>({ ...DEFAULT_EU_FACTS })
const rules = ref<Rule[]>([])
const scenarios = ref<Scenario[]>([])
const results = ref<RuleResult[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const evaluatedFacts = ref<EuFacts | NdbFacts | null>(null)
const activeScenarioLabel = ref<string | null>(null)
const activeScenarioDescription = ref<string | null>(null)
const filterStatus = ref<'matched' | 'not-matched' | 'not-evaluable' | null>(null)
const mode = ref<'evaluate' | 'compare'>('evaluate')

const isStale = computed(() =>
  results.value.length > 0 &&
  JSON.stringify(facts.value) !== JSON.stringify(evaluatedFacts.value)
)

async function loadDomain(d: DomainId) {
  error.value = null
  results.value = []
  loading.value = true
  try {
    const [df, sc] = await Promise.all([fetchDomain(d), fetchScenarios(d)])
    rules.value = df.rules
    scenarios.value = sc
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}

watch(domain, async (d) => {
  facts.value = d === 'eu-ai-act' ? { ...DEFAULT_EU_FACTS } : { ...DEFAULT_NDB_FACTS }
  activeScenarioLabel.value = null
  activeScenarioDescription.value = null
  filterStatus.value = null
  await loadDomain(d)
}, { immediate: true })

function onLoadScenario(scenario: Scenario) {
  facts.value = { ...(scenario.facts as EuFacts | NdbFacts) }
  activeScenarioLabel.value = scenario.label
  activeScenarioDescription.value = scenario.description
  filterStatus.value = null
  runEvaluate()
}

async function runEvaluate() {
  loading.value = true
  error.value = null
  try {
    results.value = await apiEvaluate(domain.value, facts.value as Record<string, unknown>)
    evaluatedFacts.value = JSON.parse(JSON.stringify(facts.value))
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="app">
    <header class="header">
      <h1 class="title">ClauseKit</h1>
      <DomainSwitcher v-if="mode === 'evaluate'" v-model="domain" />
      <nav class="mode-nav">
        <button :class="['mode-btn', { active: mode === 'evaluate' }]" @click="mode = 'evaluate'">Evaluate</button>
        <button :class="['mode-btn', { active: mode === 'compare' }]" @click="mode = 'compare'">Compare</button>
      </nav>
    </header>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <main class="main" v-if="mode === 'evaluate'">
      <aside class="sidebar">
        <ScenarioBar :scenarios="scenarios" @load="onLoadScenario" />
        <div v-if="domain === 'ndb'" class="domain-notice">
          All NDB provisions require expert legal judgement — no rules are machine-evaluable under the current fact schema. Results show the contrast with the EU AI Act domain.
        </div>
        <SandboxPane
          :domain="domain"
          :facts="facts"
          @update:facts="facts = $event"
          @evaluate="runEvaluate"
        />
      </aside>

      <section class="results">
        <div v-if="activeScenarioLabel" class="scenario-context">
          <strong>{{ activeScenarioLabel }}</strong>
          <span v-if="activeScenarioDescription"> — {{ activeScenarioDescription }}</span>
        </div>
        <ResultsSummary :results="results" :loading="loading" :filter="filterStatus" @update:filter="filterStatus = $event" />
        <div v-if="isStale" class="stale-banner">Facts changed — click Evaluate to update results.</div>
        <div v-if="results.length === 0 && !loading && rules.length > 0" class="rules-empty">
          Select a scenario preset or configure facts and click Evaluate to see which rules apply.
        </div>
        <RuleList v-else :rules="rules" :results="results" :filter="filterStatus" />
      </section>
    </main>
    <ComparePane v-else />
  </div>
</template>

<style>
.app { min-height: 100vh; display: flex; flex-direction: column; }
.header {
  display: flex; align-items: center; gap: 20px; padding: 12px 20px;
  background: #fff; border-bottom: 1px solid #dee2e6; position: sticky; top: 0; z-index: 10;
}
.title { font-size: 18px; font-weight: 700; color: #212529; }
.error-banner { background: #fff5f5; color: #e03131; padding: 8px 20px; font-size: 13px; }
.main { display: flex; gap: 16px; padding: 16px 20px; flex: 1; align-items: flex-start; }
.sidebar { width: 280px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px; position: sticky; top: 60px; }
.results { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.domain-notice { background: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 8px 12px; font-size: 13px; color: #664d03; }
.stale-banner { background: #e7f5ff; border: 1px solid #74c0fc; border-radius: 4px; padding: 6px 12px; font-size: 13px; color: #1864ab; margin-bottom: 8px; }
.scenario-context { font-size: 13px; color: #495057; margin-bottom: 8px; padding: 8px; background: #f8f9fa; border-radius: 4px; border-left: 3px solid #1971c2; }
.rules-empty { text-align: center; color: #868e96; font-size: 14px; padding: 40px 20px; }
.mode-nav { display: flex; gap: 4px; margin-left: auto; }
.mode-btn { padding: 5px 14px; border: 1px solid #dee2e6; border-radius: 4px; background: #fff; font-size: 13px; cursor: pointer; color: #495057; }
.mode-btn.active { background: #1971c2; color: #fff; border-color: #1971c2; }
.mode-btn:not(.active):hover { background: #f8f9fa; }
</style>
