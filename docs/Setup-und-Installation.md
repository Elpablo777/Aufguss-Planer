# Setup und Installation

## Voraussetzungen
- Node.js & npm
- Python 3.10+
- Django, pip, venv

## Backend starten
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Frontend starten
```bash
cd frontend
npm install
npm start
```

## Weitere Hinweise
- Siehe README und Wiki für Details
- Bei Problemen: Discussions oder Issues nutzen
