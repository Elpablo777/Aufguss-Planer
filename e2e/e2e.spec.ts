import { test, expect } from '@playwright/test';

test('Startseite lädt und zeigt Login', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('text=Anmelden')).toBeVisible();
});
