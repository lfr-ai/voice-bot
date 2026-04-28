import { test, expect } from '@playwright/test'

test('placeholder works', async ({ page }) => {
  await page.goto('http://localhost:5173')
  expect(page).toBeTruthy()
})
