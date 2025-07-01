# Hinweise für KI-Assistenten (AGENTS.md)

Dieses Dokument enthält wichtige Hinweise und Konventionen für die Arbeit mit dem Projekt "Sauna-Aufguss-Koordinations-App".

## 1. Umgebungsvariablen (Backend)

Das Backend (`backend/aufguss_backend/aufguss_backend/settings.py`) wurde so konfiguriert, dass kritische Einstellungen aus Umgebungsvariablen geladen werden. Für die lokale Entwicklung können die Fallback-Werte verwendet werden, aber für die Produktion **müssen** folgende Umgebungsvariablen gesetzt werden:

*   `DJANGO_SECRET_KEY`: Ein starker, einzigartiger Secret Key.
*   `DJANGO_DEBUG`: Auf `False` setzen für Produktion, `True` für Entwicklung.
*   `DJANGO_ALLOWED_HOSTS`: Eine Leerzeichen-separierte Liste der erlaubten Hostnamen (z.B. `"meine-domain.de www.meine-domain.de"`).
*   `DB_ENGINE`: (Optional) Standard: `django.db.backends.postgresql`. Für andere Datenbanken anpassen.
*   `DB_NAME`: Name der Datenbank. Standard: `aufguss_db`.
*   `DB_USER`: Benutzername für die Datenbank. Standard: `postgres`.
*   `DB_PASSWORD`: Passwort für den Datenbankbenutzer. Standard: `postgres`.
*   `DB_HOST`: Host der Datenbank. Standard: `localhost`.
*   `DB_PORT`: Port der Datenbank. Standard: `5432`.

Für Tests wird automatisch SQLite verwendet, wenn `PYTEST_CURRENT_TEST` (von pytest gesetzt) oder `USE_SQLITE_FOR_TESTS=1` (in CI gesetzt) vorhanden sind.

## 2. CI/CD Pipeline (`.github/workflows/ci.yml`)

*   Die Pipeline ist so konfiguriert, dass sie bei Linting-Fehlern, Testfehlern oder Problemen bei der Abhängigkeitsinstallation fehlschlägt (kein `|| true` mehr).
*   Python-Abhängigkeiten werden aus `backend/requirements.txt` installiert.
*   Node-Abhängigkeiten werden mit `npm ci` installiert.
*   Caching für `pip` und `npm` ist aktiviert.
*   Frontend-Skripte für die CI:
    *   `npm run lint`: Führt ESLint aus. Stelle sicher, dass ESLint korrekt konfiguriert ist (`frontend/.eslintrc.js` oder ähnlich).
    *   `npm run typecheck`: Führt `tsc --noEmit` aus.
*   Backend-Tests werden mit `python manage.py test` und der Umgebungsvariable `USE_SQLITE_FOR_TESTS=1` ausgeführt.

## 3. Testing

*   **Backend:** Tests befinden sich in `backend/aufguss_backend/tests.py` und verwenden `pytest`. Die Konfiguration ist in `backend/pytest.ini`.
*   **Frontend:** Tests befinden sich in `frontend/src/__tests__/` und verwenden Jest. Die Konfiguration ist in `frontend/jest.config.js`. Das Skript `npm test` enthält nicht mehr `--passWithNoTests`.

## 4. Code-Stil und Konventionen

*   **Backend:**
    *   Verwende `select_related` und `prefetch_related` in ViewSets, um N+1 Query-Probleme zu vermeiden.
    *   Typ-Hints sind erwünscht, aber noch nicht durchgängig vorhanden.
*   **Frontend:**
    *   Vermeide Inline-Styles zugunsten von CSS-Dateien oder CSS-in-JS-Lösungen.
    *   Komponenten sollten möglichst klein und fokussiert sein.

## 5. Wichtige Annahmen bei letzten Änderungen

*   Für das Frontend-Linting in der CI wird angenommen, dass ESLint korrekt im `frontend`-Verzeichnis konfiguriert ist und über `npm run lint` ausgeführt werden kann.
*   Die `backend/requirements.txt` sollte `psycopg2-binary` (statt `psycopg2`) enthalten, wenn keine Build-Tools für `psycopg2` in der CI-Umgebung vorhanden sind, um die Installation zu vereinfachen. Dies wurde noch nicht explizit geprüft.

Bitte halte dich an diese Hinweise, um die Konsistenz und Qualität des Projekts zu gewährleisten.
