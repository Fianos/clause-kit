<script setup lang="ts">
import { computed } from 'vue'
import NdbFactorDisplay from './NdbFactorDisplay.vue'
import type {
  DomainId, EuFacts, NdbFacts, EuSector,
  NdbIncidentType, NdbEncryption, NdbAffected, NdbRecipient, NdbVulnerability,
} from '../types'

const props = defineProps<{
  domain: DomainId
  facts: EuFacts | NdbFacts
}>()
const emit = defineEmits<{
  'update:facts': [EuFacts | NdbFacts]
  evaluate: []
}>()

const euFacts = computed(() => props.facts as EuFacts)
const ndbFacts = computed(() => props.facts as NdbFacts)

function updateEu(field: keyof EuFacts, value: unknown) {
  emit('update:facts', { ...euFacts.value, [field]: value })
}

function updateNdb(field: keyof NdbFacts, value: unknown) {
  emit('update:facts', { ...ndbFacts.value, [field]: value })
}

const EU_SECTORS: EuSector[] = [
  'general', 'employment', 'education', 'credit',
  'law_enforcement', 'border', 'critical_infra', 'biometric_id',
]
const EU_BOOL_FIELDS: { key: keyof EuFacts; label: string }[] = [
  { key: 'publicly_accessible_spaces', label: 'Publicly accessible spaces' },
  { key: 'involves_safety_component', label: 'Safety component' },
  { key: 'is_gpai_model', label: 'GPAI model' },
  { key: 'real_time_biometric', label: 'Real-time biometric ID' },
  { key: 'post_hoc_biometric', label: 'Post-hoc biometric ID' },
  { key: 'art6_3_exception_narrow_procedure', label: 'Art 6(3) exception: narrow procedure' },
  { key: 'art6_3_exception_human_override', label: 'Art 6(3) exception: human override' },
  { key: 'art6_3_exception_preparatory_task', label: 'Art 6(3) exception: preparatory task' },
  { key: 'art6_3_exception_contravention_check', label: 'Art 6(3) exception: contravention check' },
]

const EU_BOOL_TOOLTIPS: Partial<Record<keyof EuFacts, string>> = {
  publicly_accessible_spaces: 'System operates in spaces the general public can access (streets, shopping centres, airports)',
  involves_safety_component: 'System is a safety component of a product covered by EU harmonisation legislation',
  is_gpai_model: 'System is a General Purpose AI model (e.g. a foundation model or large language model)',
  real_time_biometric: 'System identifies people in real-time using biometric data (face, gait, fingerprint) in public spaces',
  post_hoc_biometric: 'System identifies people after the fact from recorded footage or data',
  art6_3_exception_narrow_procedure: 'System only assists a human decision-maker via a preparatory assessment; it does not make or influence the final decision',
  art6_3_exception_human_override: 'Every output is reviewed and can be overridden by a human before it takes effect',
  art6_3_exception_preparatory_task: 'System performs only a preparatory task that is not directly decisive for any individual outcome',
  art6_3_exception_contravention_check: 'System only detects possible contraventions of EU law; it does not assess people',
}
</script>

<template>
  <div class="sandbox-pane">
    <!-- EU AI Act form -->
    <template v-if="domain === 'eu-ai-act'">
      <div class="field">
        <label>System name</label>
        <input
          type="text"
          :value="euFacts.system_name"
          @input="updateEu('system_name', ($event.target as HTMLInputElement).value)"
          placeholder="e.g. HR Screener v2"
        />
      </div>
      <div class="field">
        <label>Deployment sector</label>
        <select
          :value="euFacts.deployment_sector"
          @change="updateEu('deployment_sector', ($event.target as HTMLSelectElement).value as EuSector)"
        >
          <option v-for="s in EU_SECTORS" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div class="bool-fields">
        <label v-for="f in EU_BOOL_FIELDS" :key="f.key" class="bool-field" :title="EU_BOOL_TOOLTIPS[f.key]">
          <input
            type="checkbox"
            :checked="(euFacts[f.key] as boolean)"
            @change="updateEu(f.key, ($event.target as HTMLInputElement).checked)"
          />
          {{ f.label }}
        </label>
      </div>
    </template>

    <!-- NDB form -->
    <template v-else>
      <div class="field">
        <label>Incident type</label>
        <select
          :value="ndbFacts.incident_type"
          @change="updateNdb('incident_type', ($event.target as HTMLSelectElement).value as NdbIncidentType)"
        >
          <option value="unauthorised_access">Unauthorised access</option>
          <option value="loss">Loss</option>
          <option value="unauthorised_disclosure">Unauthorised disclosure</option>
        </select>
      </div>
      <div class="field">
        <label>Data categories</label>
        <NdbFactorDisplay
          :model-value="ndbFacts.data_categories"
          @update:model-value="updateNdb('data_categories', $event)"
        />
      </div>
      <div class="field">
        <label>Encryption status</label>
        <select
          :value="ndbFacts.encryption_status"
          @change="updateNdb('encryption_status', ($event.target as HTMLSelectElement).value as NdbEncryption)"
        >
          <option value="encrypted">Encrypted</option>
          <option value="partial">Partial</option>
          <option value="unencrypted">Unencrypted</option>
        </select>
      </div>
      <div class="field">
        <label>Individuals affected</label>
        <select
          :value="ndbFacts.individuals_affected"
          @change="updateNdb('individuals_affected', ($event.target as HTMLSelectElement).value as NdbAffected)"
        >
          <option value="1-10">1–10</option>
          <option value="10-100">10–100</option>
          <option value="100-1000">100–1,000</option>
          <option value="1000+">1,000+</option>
        </select>
      </div>
      <div class="field">
        <label>Likely recipient</label>
        <select
          :value="ndbFacts.likely_recipient"
          @change="updateNdb('likely_recipient', ($event.target as HTMLSelectElement).value as NdbRecipient)"
        >
          <option value="unknown">Unknown</option>
          <option value="specific_individual">Specific individual</option>
          <option value="criminal">Criminal</option>
          <option value="broad_public">Broad public</option>
        </select>
      </div>
      <div class="field">
        <label>Individual vulnerability</label>
        <select
          :value="ndbFacts.individual_vulnerability"
          @change="updateNdb('individual_vulnerability', ($event.target as HTMLSelectElement).value as NdbVulnerability)"
        >
          <option value="general">General</option>
          <option value="elderly">Elderly</option>
          <option value="children">Children</option>
          <option value="health_patients">Health patients</option>
        </select>
      </div>
    </template>

    <button class="evaluate-btn" @click="emit('evaluate')">Evaluate</button>
  </div>
</template>

<style scoped>
.sandbox-pane { display: flex; flex-direction: column; gap: 10px; padding: 12px; background: #fff; border: 1px solid #dee2e6; border-radius: 6px; }
.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 12px; font-weight: 600; color: #495057; }
.field input[type="text"], .field select {
  padding: 6px 8px; border: 1px solid #ced4da; border-radius: 4px; font-size: 13px;
}
.bool-fields { display: flex; flex-direction: column; gap: 6px; }
.bool-field { display: flex; align-items: center; gap: 6px; font-size: 13px; cursor: pointer; }
.evaluate-btn {
  margin-top: 4px; padding: 8px 16px; background: #1971c2; color: #fff;
  border: none; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer;
}
.evaluate-btn:hover { background: #1864ab; }
</style>
