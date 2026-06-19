import { test, expect } from '@playwright/test'

test.describe('EU AI Act domain', () => {
  test('page loads with ClauseKit heading', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: /ClauseKit/i })).toBeVisible()
  })

  test('DomainSwitcher shows both tabs; EU AI Act is active by default', async ({ page }) => {
    await page.goto('/')
    const euBtn = page.getByRole('button', { name: 'EU AI Act' })
    const ndbBtn = page.getByRole('button', { name: 'NDB (Australia)' })
    await expect(euBtn).toBeVisible()
    await expect(ndbBtn).toBeVisible()
    await expect(euBtn).toHaveClass(/active/)
  })

  test('ScenarioBar shows at least one scenario button', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector('.scenario-bar button')
    const buttons = page.locator('.scenario-bar button')
    expect(await buttons.count()).toBeGreaterThan(0)
  })

  test('facial recognition scenario auto-evaluates and produces matched rows', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector('.scenario-bar button')
    await page.getByRole('button', { name: 'Facial recognition (public space)' }).click()
    await page.waitForSelector('.rule-row.matched')
    await expect(page.locator('.results-summary')).toBeVisible()
    expect(await page.locator('.rule-row.matched').count()).toBeGreaterThan(0)
  })

  test('customer service chatbot scenario produces no matched rows', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector('.scenario-bar button')
    await page.getByRole('button', { name: 'Customer service chatbot' }).click()
    await page.waitForSelector('.results-summary .count')
    expect(await page.locator('.rule-row.matched').count()).toBe(0)
  })

  test('switching to NDB tab updates ScenarioBar to NDB scenarios', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector('.scenario-bar button')
    await page.getByRole('button', { name: 'NDB (Australia)' }).click()
    await page.waitForSelector('.scenario-bar button')
    await expect(
      page.getByRole('button', { name: /Unencrypted health records/i })
    ).toBeVisible()
  })
})
