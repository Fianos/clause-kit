export type DomainId = 'eu-ai-act' | 'ndb'

export interface Docref {
  source_doc: string
  article: string
  section: string
  url: string
  provision_uri: string | null
}

export interface Rule {
  rule_id: string
  label: string
  condition: object | null
  obligation: string
  scope: string
  exceptions: string[]
  codifiability: 'high' | 'medium' | 'low'
  docref: Docref
}

export interface Scenario {
  id: string
  label: string
  description: string
  facts: Record<string, unknown>
}

export interface DomainFile {
  domain: string
  version: string
  extracted_at: string
  source_url: string
  model_version: string | null
  rules: Rule[]
  scenarios: Scenario[]
}

export interface RuleResult {
  rule_id: string
  matched: boolean | null
  codifiability: 'high' | 'medium' | 'low'
  label: string
  obligation: string
  docref: Docref
  matched_facts: Record<string, unknown> | null
}

// EU AI Act fact schema
export type EuSector =
  | 'employment' | 'education' | 'credit' | 'law_enforcement'
  | 'border' | 'critical_infra' | 'biometric_id' | 'general'

export interface EuFacts {
  system_name: string
  deployment_sector: EuSector
  publicly_accessible_spaces: boolean
  involves_safety_component: boolean
  is_gpai_model: boolean
  real_time_biometric: boolean
  post_hoc_biometric: boolean
  art6_3_exception_narrow_procedure: boolean
  art6_3_exception_human_override: boolean
  art6_3_exception_preparatory_task: boolean
  art6_3_exception_contravention_check: boolean
}

// NDB fact schema
export type NdbIncidentType = 'unauthorised_access' | 'loss' | 'unauthorised_disclosure'
export type NdbDataCategory = 'health' | 'financial' | 'identity' | 'biometric' | 'sensitive'
export type NdbEncryption = 'encrypted' | 'partial' | 'unencrypted'
export type NdbAffected = '1-10' | '10-100' | '100-1000' | '1000+'
export type NdbRecipient = 'unknown' | 'specific_individual' | 'criminal' | 'broad_public'
export type NdbVulnerability = 'general' | 'elderly' | 'children' | 'health_patients'

export interface NdbFacts {
  incident_type: NdbIncidentType
  data_categories: NdbDataCategory[]
  encryption_status: NdbEncryption
  individuals_affected: NdbAffected
  likely_recipient: NdbRecipient
  individual_vulnerability: NdbVulnerability
}

export const DEFAULT_EU_FACTS: EuFacts = {
  system_name: '',
  deployment_sector: 'general',
  publicly_accessible_spaces: false,
  involves_safety_component: false,
  is_gpai_model: false,
  real_time_biometric: false,
  post_hoc_biometric: false,
  art6_3_exception_narrow_procedure: false,
  art6_3_exception_human_override: false,
  art6_3_exception_preparatory_task: false,
  art6_3_exception_contravention_check: false,
}

export const DEFAULT_NDB_FACTS: NdbFacts = {
  incident_type: 'unauthorised_access',
  data_categories: [],
  encryption_status: 'encrypted',
  individuals_affected: '1-10',
  likely_recipient: 'unknown',
  individual_vulnerability: 'general',
}

export interface ComparisonResult {
  domain: string
  section_id: string
  plain_rules: Rule[]
  akn_rules: Rule[]
}
