# Accessibility-Tests mit jest-axe

Wir nutzen [jest-axe](https://github.com/nickcolley/jest-axe) und [@axe-core/react](https://github.com/dequelabs/axe-core-npm) für automatisierte Barrierefreiheits-Checks in React-Komponenten.

## Beispiel-Test (src/__tests__/accessibility.test.tsx):

```tsx
import React from 'react';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import App from '../App';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('App ist barrierefrei (axe)', async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Ausführen:

```bash
npm test -- src/__tests__/accessibility.test.tsx
```

## Integration in CI
- Accessibility-Tests werden im CI-Workflow automatisch ausgeführt.
- Bei Fehlern schlägt der Build fehl.

## Troubleshooting (Jest/Babel/TSX)
- Bei Problemen mit JSX/TSX-Transformation: Alle Babel- und Jest-Abhängigkeiten aktuell halten (`npm install --save-dev babel-jest @babel/core @babel/preset-env @babel/preset-react @babel/preset-typescript`).
- In `jest.config.js` nur `babel-jest` als Transformer nutzen, kein `ts-jest`.
- Falls weiterhin Fehler: `.babelrc` im Frontend-Root anlegen (siehe Projekt).
- Siehe [Jest-Doku](https://jestjs.io/docs/getting-started#using-typescript) und [Babel-Jest](https://github.com/babel/jest) für Details.

## Weitere Hinweise
- Für alle UI-Komponenten sollten Accessibility-Tests ergänzt werden.
- Siehe [axe-core Doku](https://github.com/dequelabs/axe-core-npm) für weitere Regeln und Anpassungen.

## Admin- und Moderationsfunktionen (Ausblick)
- Das Admin-Panel im Backend ist bereits vorhanden (Django Admin).
- Geplant: Erweiterung um Community-Moderation (z. B. User-Ban, Rollen, Meldefunktion für Inhalte).
- Für Open-Source-Kollaboration: Admin- und Moderations-Features werden transparent im Wiki und in Issues/PRs dokumentiert und entwickelt.

## Community-Workflows
- Alle Mitwirkenden finden im [Mitwirken.md](./docs/Mitwirken.md) und im GitHub-Wiki die wichtigsten Community-Regeln und Workflows.
- Diskussionen, Feature-Wünsche und Moderationsanfragen laufen über GitHub Discussions und Issues.

## Testabdeckung & E2E
- Die Testabdeckung wird kontinuierlich erhöht (Unit, Integration, E2E).
- Playwright ist für E2E-Tests eingerichtet (siehe [E2E_TESTS.md](./docs/E2E_TESTS.md)).
- Accessibility- und Security-Checks sind Teil der CI/CD.

## Features & Usability (Roadmap)
- Mobile-Optimierung, Mehrsprachigkeit (i18n), Kalender- und Chat-Features werden iterativ ausgebaut.
- Alle Änderungen werden im [CHANGELOG.md](./docs/CHANGELOG.md) und in Issues/PRs dokumentiert.
