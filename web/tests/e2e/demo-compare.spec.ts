import { test, expect } from '@playwright/test'
import type { ComparisonResult } from '../../src/types'

const MOCK_RESULT: ComparisonResult = {
  domain: 'ndb',
  section_id: '26wa',
  plain_rules: [
    {
      rule_id: 'ndb-26wa-001-plain',
      label: 'Eligible data breach (plain)',
      condition: null,
      obligation: 'Notify the Commissioner and affected individuals.',
      scope: 'APP entities',
      exceptions: [],
      codifiability: 'low',
      docref: {
        source_doc: 'Privacy Act 1988 (Cth)',
        article: 'Section 26WA',
        section: '26WA(1)',
        url: 'https://www.legislation.gov.au/Details/C2024C00091',
        provision_uri: null,
      },
    },
  ],
  akn_rules: [
    {
      rule_id: 'ndb-26wa-001-akn',
      label: 'Eligible data breach (AKN)',
      condition: null,
      obligation: 'Notify the Commissioner and affected individuals within 30 days.',
      scope: 'APP entities',
      exceptions: [],
      codifiability: 'low',
      docref: {
        source_doc: 'Privacy Act 1988 (Cth)',
        article: 'Section 26WA',
        section: '26WA(1)',
        url: 'https://www.legislation.gov.au/Details/C2024C00091',
        provision_uri: '/akn/au/act/1988/119/section/26WA',
      },
    },
  ],
}

test.describe('Compare mode', () => {
  test.beforeEach(async ({ page }) => {
    await page.route('**/compare', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_RESULT),
      })
    )
    await page.goto('/')
    await page.getByRole('button', { name: 'Compare' }).click()
  })

  test('compare tab renders section picker and run button', async ({ page }) => {
    await expect(page.locator('.compare-pane')).toBeVisible()
    await expect(page.locator('select')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Run comparison' })).toBeVisible()
  })

  test('run comparison shows two columns', async ({ page }) => {
    await page.getByRole('button', { name: 'Run comparison' }).click()
    await page.waitForSelector('.compare-grid')
    const cols = page.locator('.col')
    await expect(cols).toHaveCount(2)
  })

  test('plain text column shows rule count', async ({ page }) => {
    await page.getByRole('button', { name: 'Run comparison' }).click()
    await page.waitForSelector('.compare-grid')
    await expect(page.locator('.col-label').filter({ hasText: 'Plain text' }).first()).toBeVisible()
    await expect(page.getByText('1 rules')).toHaveCount(2)
  })

  test('AKN column shows provision_uri', async ({ page }) => {
    await page.getByRole('button', { name: 'Run comparison' }).click()
    await page.waitForSelector('.compare-grid')
    await expect(page.locator('.provision-uri')).toBeVisible()
    await expect(page.locator('.provision-uri')).toHaveText('/akn/au/act/1988/119/section/26WA')
  })

  test('switching back to Evaluate restores main view', async ({ page }) => {
    await page.getByRole('button', { name: 'Rules' }).click()
    await expect(page.locator('.sidebar')).toBeVisible()
    await expect(page.locator('.compare-pane')).not.toBeVisible()
  })
})
