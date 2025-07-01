# Security-Checks (Backend)

Wir nutzen [Bandit](https://bandit.readthedocs.io/) für automatisierte Security-Checks im Python/Django-Backend.

## Ausführen:

```bash
source ../.venv/bin/activate  # falls nicht aktiv
bandit -r aufguss_backend/
```

## Typische Warnungen (Open-Source-Kontext)
- **Hardcoded SECRET_KEY**: In `settings.py` ist ein Standard-SECRET_KEY für Entwicklung/Test hinterlegt. Für Produktion muss dieser durch eine sichere Umgebungsvariable ersetzt werden.
- **Hardcoded Testpasswörter**: In den Tests werden feste Passwörter verwendet (z. B. `testpass`). Das ist für Testumgebungen akzeptabel, sollte aber nicht in Produktionscode verwendet werden.
- **assert in Tests**: Bandit warnt vor der Nutzung von `assert` in Python, da diese im optimierten Bytecode entfernt werden. Für pytest-Tests ist das akzeptabel, sollte aber dokumentiert werden.

## Integration in CI
- Bandit kann im CI-Workflow als zusätzlicher Security-Check ausgeführt werden.
- Bei kritischen Findings schlägt der Build fehl.

## Weitere Hinweise
- Für produktive Deployments: SECRET_KEY und Passwörter immer über sichere Umgebungsvariablen setzen.
- Siehe [Bandit-Doku](https://bandit.readthedocs.io/) für weitere Regeln und Anpassungen.
