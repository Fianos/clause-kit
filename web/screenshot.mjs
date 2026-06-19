import { chromium } from '@playwright/test';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setViewportSize({ width: 1280, height: 900 });

await page.goto('http://localhost:5173/');
await page.waitForLoadState('networkidle');
await page.click('button:has-text("Facial recognition")');
await page.waitForTimeout(1500);
await page.screenshot({ path: '/tmp/ck-sorted.png', fullPage: false });
console.log('done');

await browser.close();
