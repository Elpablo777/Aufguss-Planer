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
    *   Verwende `select_related` und `prefetch_related` in ViewSets, um N+1 Query-Probleme zu vermeiden (bereits für `AufgussViewSet`, `UserViewSet`, `ChatViewSet` umgesetzt).
    *   Typ-Hints sind erwünscht, aber noch nicht durchgängig vorhanden.
    *   **Berechtigungsklassen:** Für Objekt-Level-Berechtigungen wurden `IsOwnerOrAdminOrReadOnly` (für `AufgussViewSet`) und `IsSenderOrAdminOrReadOnly` (für `ChatViewSet`) in `backend/aufguss_backend/aufguss_app/views.py` implementiert. Diese stellen sicher, dass nur Eigentümer oder Admins bestimmte schreibende Operationen durchführen können.
*   **Frontend:**
    *   Vermeide Inline-Styles zugunsten von CSS-Dateien oder CSS-in-JS-Lösungen.
    *   Komponenten sollten möglichst klein und fokussiert sein.
    *   Für das Linting wurde `eslint` mit den Plugins `eslint-plugin-react`, `eslint-plugin-react-hooks`, `@typescript-eslint/eslint-plugin`, `@typescript-eslint/parser`, `eslint-plugin-jest-dom` und `eslint-plugin-testing-library` zu den `devDependencies` in `frontend/package.json` hinzugefügt und eine Basiskonfiguration in `frontend/.eslintrc.js` erstellt.

## 5. Wichtige Hinweise und getroffene Entscheidungen

*   Die `backend/requirements.txt` verwendet nun `psycopg2-binary` statt `psycopg2` für eine einfachere Installation.
*   **Consumer-Tests:** Für `AufgussConsumer` und `ChatConsumer` wurden grundlegende Tests mit `channels.testing.WebsocketCommunicator` in `backend/aufguss_backend/tests.py` hinzugefügt. Diese sind als `@pytest.mark.asyncio` markiert.
*   **Frontend-Komponententests:** Erste Komponententests für `Login.tsx` wurden in `frontend/src/__tests__/Login.test.tsx` erstellt, die `@testing-library/react` verwenden und den `AuthContext` mocken. Für `Calendar.tsx` wurde ein Testgerüst in `frontend/src/__tests__/Calendar.test.tsx` angelegt:
    *   Das Modul `frontend/src/api.ts` wird via `jest.mock('../api')` gemockt.
    *   FullCalendar-Komponenten werden via `jest.config.js` und dem Mock in `frontend/__mocks__/fullcalendar-react.js` gemockt. Der Mock wurde angepasst, um ein identifizierbares Element für Tests zu rendern.
    *   Globale `WebSocket` und `localStorage` werden bei Bedarf in den Testdateien gemockt.

Bitte halte dich an diese Hinweise, um die Konsistenz und Qualität des Projekts zu gewährleisten.
