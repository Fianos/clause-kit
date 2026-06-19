<script setup lang="ts">
import { ref, watch } from 'vue'
import DomainSwitcher from './components/DomainSwitcher.vue'
import ScenarioBar from './components/ScenarioBar.vue'
import SandboxPane from './components/SandboxPane.vue'
import ResultsSummary from './components/ResultsSummary.vue'
import RuleList from './components/RuleList.vue'
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
  await loadDomain(d)
}, { immediate: true })

function onLoadScenario(scenario: Scenario) {
  facts.value = { ...(scenario.facts as EuFacts | NdbFacts) }
  runEvaluate()
}

async function runEvaluate() {
  loading.value = true
  error.value = null
  try {
    results.value = await apiEvaluate(domain.value, facts.value as Record<string, unknown>)
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
      <DomainSwitcher v-model="domain" />
    </header>

    <div v-if="error" class="error-banner">{{ error }}</div>

    <main class="main">
      <aside class="sidebar">
        <ScenarioBar :scenarios="scenarios" @load="onLoadScenario" />
        <SandboxPane
          :domain="domain"
          :facts="facts"
          @update:facts="facts = $event"
          @evaluate="runEvaluate"
        />
      </aside>

      <section class="results">
        <ResultsSummary :results="results" :loading="loading" />
        <RuleList :rules="rules" :results="results" />
      </section>
    </main>
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
</style>
