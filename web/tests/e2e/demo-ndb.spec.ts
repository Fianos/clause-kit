import { test, expect } from '@playwright/test'

test.describe('NDB domain', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector('.scenario-bar button')
    await page.getByRole('button', { name: 'NDB (Australia)' }).click()
    await page.waitForSelector('.scenario-bar button')
  })

  test('4 NDB scenario buttons are visible', async ({ page }) => {
    const buttons = page.locator('.scenario-bar button')
    await expect(buttons).toHaveCount(4)
  })

  test('clicking NDB scenario auto-evaluates and shows ResultsSummary', async ({ page }) => {
    await page.getByRole('button', { name: /Unencrypted health records/i }).click()
    await page.waitForSelector('.results-summary .count')
    await expect(page.locator('.results-summary')).toBeVisible()
  })

  test('all rule rows are not-evaluable after NDB scenario evaluation', async ({ page }) => {
    await page.getByRole('button', { name: /Unencrypted health records/i }).click()
    await page.waitForSelector('.rule-row.not-evaluable')
    expect(await page.locator('.rule-row.matched').count()).toBe(0)
    expect(await page.locator('.rule-row.not-matched').count()).toBe(0)
    expect(await page.locator('.rule-row.not-evaluable').count()).toBeGreaterThan(0)
  })

  test('clicking a rule row expands inspector showing obligation text', async ({ page }) => {
    const firstRow = page.locator('.rule-row').first()
    await firstRow.click()
    await expect(firstRow.locator('.rule-inspector')).toBeVisible()
    await expect(firstRow.locator('.rule-inspector')).toContainText('Obligation')
  })
})
