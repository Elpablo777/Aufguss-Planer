# Sauna-Aufguss-Koordinations-App

Dieses Repository enthält die offene Entwicklung einer cloudbasierten Web-App zur Koordination von Sauna-Aufgüssen. Alle Änderungen werden transparent über GitHub-Issues und Pull-Requests dokumentiert und bearbeitet.

## Projektziele
- **Interaktiver Kalender** (Tages-, Wochen-, Monatsansicht)
- **Farbcodierte Nutzer** mit automatischen Avataren
- **Admin-Panel** mit unveränderlichen Rootrechten (E-Mail: Hannover84@msn.com)
- **Whitelist-System** für autorisierten Zugang
- **Responsive Design** für alle Geräte
- **Echtzeit-Synchronisation** (WebSockets)
- **Chat-Funktion** und **Benachrichtigungen**
- **Statistikmodul** für Aufguss-Auswertungen

## Technischer Stack
- **Backend:** Python/Django, Django REST Framework, Channels
- **Frontend:** React, TypeScript, FullCalendar
- **Datenbank:** PostgreSQL
- **Deployment:** PythonAnywhere, Heroku oder Render (kostenlos)

## Entwicklung & Transparenz
- **Alle Änderungen** erfolgen über GitHub-Issues und Pull-Requests
- **Projektleitung & Review**: KI-gestützt, alle Entscheidungen und Umsetzungen werden dokumentiert
- **Einstellungen & CI/CD** werden im Repo gepflegt und regelmäßig geprüft

## Erste Schritte
1. Forke das Repo oder erstelle einen neuen Branch
2. Richte die Entwicklungsumgebung ein (siehe `docs/SETUP.md`)
3. Folge dem [Implementierungsplan](#implementierungsplan)

## Implementierungsplan
1. **Grundgerüst:** Backend-Modelle, Auth, API, Whitelist
2. **Frontend:** Kalender, Benutzeroberfläche, Farbcodierung
3. **Erweiterungen:** Chat, Avatare, Admin-Panel, Benachrichtigungen
4. **Tests & Deployment:** Funktionstests, Hosting, Dokumentation

## Projektbeschreibung

**Aufguss-Planer** ist eine offene, kollaborative Web-App zur Koordination von Sauna-Aufgüssen und Teams. Ziel ist es, die Planung, Kommunikation und Organisation von Aufguss-Sessions für Saunabetriebe, Vereine und Aufgussmeister*innen zu vereinfachen – transparent, sicher und gemeinschaftlich.

**Features:**
- Benutzerverwaltung & Rechte
- Kalender mit Aufgussplanung (CRUD)
- Live-Chat & Team-Kommunikation
- Admin-Panel & Rollen
- Barrierefreiheit & Datenschutz
- Moderne UI (React, TypeScript, Django)
- Offene API, Dokumentation, Community-Features

**Mitmachen:**
Jede*r ist eingeladen, sich zu beteiligen! Siehe [CONTRIBUTING](.github/CONTRIBUTING.md), [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md), [Wiki](https://github.com/Elpablo777/Aufguss-Planer/wiki) und [Discussions](https://github.com/Elpablo777/Aufguss-Planer/discussions).

## Community-Workflows

- [Projects-Workflow](docs/Projects-Workflow.md): Aufgabenverwaltung, Kanban, Automatisierung
- [Discussions-Moderation](docs/Discussions-Moderation.md): Austausch, Moderation, Community-Regeln
- [Admin- und Moderationsfunktionen](./docs/Admin-Moderation.md)
- [Community-Workflows](./docs/Community-Workflows.md)

## Verhaltenskodex

Dieses Projekt und alle Mitwirkenden verpflichten sich zu einem respektvollen, offenen und inklusiven Umgang. Siehe [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) für Details.

## Lizenz
Dieses Projekt ist Open Source und steht unter der MIT-Lizenz.

## Dokumentationen

Für eine transparente Open-Source-Entwicklung sind hier die aktuellen Dokumentationen zu finden:
- [Accessibility-Tests](./docs/ACCESSIBILITY_TESTS.md)
- [Security-Checks](./docs/SECURITY_CHECKS.md)
- [Testabdeckung & E2E](./docs/Testabdeckung-E2E.md)
- [Features & Usability (Roadmap)](./docs/Features-Roadmap.md)
- [Benutzerfreundlichkeit & Verständlichkeit](./docs/GITHUB_BENUTZERFREUNDLICH.md)