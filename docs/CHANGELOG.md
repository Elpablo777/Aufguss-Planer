# Changelog & Patchlog

Alle Änderungen am Projekt werden hier dokumentiert. Für Details siehe auch die Pull-Requests und Issues auf GitHub.

## 01.07.2025
- Initiale Projektstruktur angelegt
- .gitignore und README.md erstellt/überarbeitet
- Wiki und ToDo-Liste angelegt
- Backend: Django-Projekt initialisiert, requirements und README angelegt
- Backend: Serializers, Views, Admin und API-Routing für User, Aufguss und Chat erstellt
- Frontend: React/TypeScript-Projekt initialisiert, Kalender-Abhängigkeiten installiert
- Frontend: Grundstruktur (src, public, tsconfig), Kalender-Komponente, Styles und Startskripte angelegt
- Backend: Channels/ASGI, Routing und WebSocket-Consumer für Aufguss- und Chat-Echtzeit-Updates angelegt

## [Unreleased]
### Hinzugefügt
- WebSocket-Authentifizierung für Chat und Aufguss-Live-Updates (Kalender) im Backend (consumers.py)
- Frontend: WebSocket-Verbindung mit JWT-Token für Chat und Kalender
- Live-Updates für Aufguss-Plan (Kalender) bei Änderungen

### Geändert
- Sicherheit und Kollaboration durch Authentifizierung und Live-Updates verbessert
