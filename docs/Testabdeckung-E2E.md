# Testabdeckung & E2E-Tests

## Status
- Unit- und Integrationstests sind für Backend (pytest, pytest-django) und Frontend (Jest, Testing Library) eingerichtet.
- Playwright ist für E2E-Tests im Projekt-Root konfiguriert (siehe [E2E_TESTS.md](./E2E_TESTS.md)).
- Coverage-Reports können für Backend und Frontend erzeugt werden.

## Coverage-Report Backend
```bash
cd backend
pytest --cov=aufguss_backend --cov-report=term-missing
```

## Coverage-Report Frontend
```bash
cd frontend
npm run test -- --coverage
```

## E2E-Tests ausführen
```bash
npx playwright test
```

## Integration in CI
- Coverage- und E2E-Tests sind im CI-Workflow integriert.
- Ziel: Testabdeckung kontinuierlich erhöhen, alle Kernfunktionen abdecken.

## Weiterführende Links
- [E2E_TESTS.md](./E2E_TESTS.md)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Jest Coverage](https://jestjs.io/docs/configuration#collectcoverage-boolean)
- [Playwright](https://playwright.dev/)
