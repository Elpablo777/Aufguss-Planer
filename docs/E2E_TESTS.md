# End-to-End-Test mit Playwright

Playwright ist ein modernes Open-Source-Framework für End-to-End-Tests (E2E) von Webanwendungen. Es unterstützt alle modernen Browser und ist ideal für Open-Source-Projekte.

## Setup

1. Playwright installieren:
   ```bash
   npm install --save-dev playwright @playwright/test
   npx playwright install
   ```
2. Testskript anlegen (z. B. `e2e.spec.ts` im Verzeichnis `e2e/`):
   ```typescript
   import { test, expect } from '@playwright/test';

   test('Startseite lädt und zeigt Login', async ({ page }) => {
     await page.goto('http://localhost:8000');
     await expect(page.locator('text=Anmelden')).toBeVisible();
   });
   ```
3. Test ausführen:
   ```bash
   npx playwright test
   ```

## Hinweise
- Die App muss lokal laufen (`npm start` und `python manage.py runserver`).
- Weitere Tests für Auth, Kalender, Chat, Barrierefreiheit etc. können ergänzt werden.
- Siehe [Playwright-Doku](https://playwright.dev/) für Details.
