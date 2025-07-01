# Backend (Django)

Dieses Verzeichnis enthält das Backend der Sauna-Aufguss-Koordinations-App.

## Stack & Abhängigkeiten
- Python 3.11+
- Django
- Django REST Framework
- Django Channels (WebSockets)
- psycopg2 (PostgreSQL)

## Setup
1. Virtuelle Umgebung aktivieren:
   ```bash
   source venv/bin/activate
   ```
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. Django-Projekt starten:
   ```bash
   cd aufguss_backend
   python manage.py migrate
   python manage.py runserver
   ```

## Backend: Setup & Test-Umgebung

**Empfohlener Workflow für alle Entwickler:**

1. Virtuelle Umgebung anlegen (falls nicht vorhanden):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-django
   ```
3. Migrationen ausführen:
   ```bash
   python manage.py migrate
   ```
4. Superuser anlegen (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Tests ausführen:
   ```bash
   pytest aufguss_backend/tests.py
   ```
6. Backend starten:
   ```bash
   python manage.py runserver
   ```

**Hinweis:**
- Immer nur eine virtuelle Umgebung verwenden (z. B. nur `venv` oder `.venv`).
- Bei Problemen: Umgebung löschen und neu anlegen.
- Siehe auch Wiki für weitere Hinweise.

## Hinweise
- Alle Änderungen werden im Changelog und in den Commits dokumentiert.
- Siehe `/docs/WIKI.md` und `/docs/TODO.md` für Aufgaben und Architektur.
