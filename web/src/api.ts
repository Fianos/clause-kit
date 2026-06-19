import type { DomainFile, DomainId, RuleResult, Scenario } from './types'

export async function fetchDomain(domain: DomainId): Promise<DomainFile> {
  const res = await fetch(`/domains/${domain}/rules`)
  if (!res.ok) throw new Error(`Failed to load domain: ${domain}`)
  return res.json()
}

export async function fetchScenarios(domain: DomainId): Promise<Scenario[]> {
  const res = await fetch(`/domains/${domain}/scenarios`)
  if (!res.ok) throw new Error(`Failed to load scenarios: ${domain}`)
  return res.json()
}

export async function evaluate(
  domain: DomainId,
  facts: Record<string, unknown>,
): Promise<RuleResult[]> {
  const res = await fetch(`/domains/${domain}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(facts),
  })
  if (!res.ok) throw new Error(`Evaluation failed`)
  return res.json()
}
