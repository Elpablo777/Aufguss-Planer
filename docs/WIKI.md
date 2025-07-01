# Projekt-Wiki: Sauna-Aufguss-Koordinations-App

Dieses Wiki dokumentiert alle wichtigen Aspekte des Projekts, von Architektur und ToDos bis zu Lizenzen, Datenschutz und Open-Source-Management.

## Übersicht
- [Projektidee & Ziel](#projektidee--ziel)
- [Architektur & Aufbau](#architektur--aufbau)
- [ToDo-Liste](#todo-liste)
- [Changelog & Patchlog](#changelog--patchlog)
- [Abhängigkeiten](#abhängigkeiten)
- [Lizenz & Copyright](#lizenz--copyright)
- [Datenschutz](#datenschutz)
- [Mitwirkende & Beiträge](#mitwirkende--beiträge)
- [GitHub-Management](#github-management)

---

## Projektidee & Ziel
Die App dient der transparenten, effizienten und sicheren Koordination von Sauna-Aufgüssen. Ziel ist eine offene, nachvollziehbare Entwicklung mit Community-Beteiligung.

## Architektur & Aufbau
- **Backend:** Python/Django, REST, Channels
- **Frontend:** React, TypeScript
- **DB:** PostgreSQL
- **Deployment:** PythonAnywhere, Heroku, Render
- **Struktur:**
  - `/backend` (Django-Projekt)
  - `/frontend` (React-App)
  - `/docs` (Dokumentation, Datenschutz, Lizenz)
  - `.github` (GitHub-Workflows, Templates)

## ToDo-Liste
- [ ] Projektstruktur anlegen
- [ ] Grundlegende Dokumentation (Wiki, README, Lizenz, Datenschutz)
- [ ] Backend-Setup (Django, User-Modell, API)
- [ ] Frontend-Setup (React, Kalender, Auth)
- [ ] GitHub-Workflows & Templates
- [ ] Lizenz & Datenschutz

## Changelog & Patchlog
Alle Änderungen werden hier und in GitHub-Issues/PRs dokumentiert.

### 01.07.2025
- Projektstruktur, Wiki, .gitignore, README angelegt
- ToDo-Liste und Plan erstellt

## Abhängigkeiten
- Python 3.11+, Django, djangorestframework, channels, psycopg2
- Node.js, React, TypeScript, FullCalendar

## Lizenz & Copyright
- MIT-Lizenz (siehe LICENSE)
- Hinweise zu genutzten Open-Source-Komponenten im Abschnitt "Abhängigkeiten"

## Datenschutz
- DSGVO-Konformität wird angestrebt
- Datenschutzdokument folgt in `/docs/DATENSCHUTZ.md`

## Mitwirkende & Beiträge
- Beiträge via Pull-Request, alle Änderungen werden dokumentiert
- Code-Kommentare und Dokumentation auf Deutsch

## GitHub-Management
- Branch-Protection, Issue-Templates, PR-Templates, Actions, Wiki, Discussions werden genutzt
- Jede Änderung erfolgt transparent über Issues/PRs
