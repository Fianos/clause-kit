import { test, expect } from '@playwright/test'

test.describe('NDB domain', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.getByRole('button', { name: 'NDB (Australia)' }).click()
    await page.waitForSelector('.rule-row')
  })

  test('loads 54 rules', async ({ page }) => {
    const rows = page.locator('.rule-row')
    await expect(rows).toHaveCount(54)
  })

  test('unencrypted health scenario evaluates with all not-evaluable', async ({ page }) => {
    await page.getByRole('button', { name: 'Unencrypted health records' }).click()
    await page.waitForSelector('.rule-row.not-evaluable')
    const notEval = page.locator('.rule-row.not-evaluable')
    expect(await notEval.count()).toBeGreaterThan(0)
    const matched = page.locator('.rule-row.matched')
    expect(await matched.count()).toBe(0)
  })

  test('results summary shows not-evaluable count', async ({ page }) => {
    await page.getByRole('button', { name: 'Evaluate' }).click()
    await page.waitForSelector('.count.not-evaluable')
    const notEvalChip = page.locator('.count.not-evaluable')
    await expect(notEvalChip).toBeVisible()
    const text = await notEvalChip.textContent()
    expect(parseInt(text ?? '0')).toBeGreaterThan(0)
  })

  test('data categories checkboxes are visible', async ({ page }) => {
    const checkboxes = page.locator('.ndb-factors input[type="checkbox"]')
    await expect(checkboxes).toHaveCount(5)
  })
})
