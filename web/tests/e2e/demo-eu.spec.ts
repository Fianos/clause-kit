import { test, expect } from '@playwright/test'

test.describe('EU AI Act domain', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.getByRole('button', { name: 'EU AI Act' }).click()
    await page.getByRole('button', { name: 'HR screening tool' }).click()
    await page.waitForSelector('.rule-row')
  })

  test('loads 32 rules', async ({ page }) => {
    const rows = page.locator('.rule-row')
    await expect(rows).toHaveCount(32)
  })

  test('facial recognition scenario triggers matches', async ({ page }) => {
    await page.getByRole('button', { name: 'Facial recognition (public space)' }).click()
    await page.waitForSelector('.rule-row.applies')
    const matched = page.locator('.rule-row.applies')
    expect(await matched.count()).toBeGreaterThan(0)
  })

  test('customer service chatbot has no matches', async ({ page }) => {
    await page.getByRole('button', { name: 'Customer service chatbot' }).click()
    await page.waitForSelector('.rule-row.not-triggered')
    const matched = page.locator('.rule-row.applies')
    expect(await matched.count()).toBe(0)
    const notMatched = page.locator('.rule-row.not-triggered')
    expect(await notMatched.count()).toBeGreaterThan(0)
  })

  test('HR screening scenario has matches', async ({ page }) => {
    await page.getByRole('button', { name: 'HR screening tool' }).click()
    await page.waitForSelector('.rule-row.applies')
    expect(await page.locator('.rule-row.applies').count()).toBeGreaterThan(0)
  })

  test('clicking a rule expands the inspector', async ({ page }) => {
    const firstRow = page.locator('.rule-row').first()
    await firstRow.click()
    await expect(firstRow.locator('.rule-inspector')).toBeVisible()
    await expect(firstRow.locator('a')).toBeVisible()
  })

  test('manual evaluate button triggers results', async ({ page }) => {
    await page.getByRole('button', { name: 'Evaluate' }).click()
    await page.waitForSelector('.count')
    await expect(page.locator('.results-summary')).toBeVisible()
  })
})
