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

## Hinweise
- Alle Änderungen werden im Changelog und in den Commits dokumentiert.
- Siehe `/docs/WIKI.md` und `/docs/TODO.md` für Aufgaben und Architektur.
