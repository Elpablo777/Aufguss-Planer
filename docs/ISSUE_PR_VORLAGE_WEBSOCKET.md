## WebSocket-Authentifizierung & Live-Updates für Kalender und Chat

### Zusammenfassung
- WebSocket-Authentifizierung mit JWT-Token für Chat und Aufguss-Live-Updates (Kalender) implementiert
- Frontend: Token wird als Query-Parameter beim Verbindungsaufbau übergeben
- Backend: Verbindungen ohne gültigen Token werden abgelehnt
- Kalender und Chat erhalten jetzt Echtzeit-Updates, sobald Änderungen auftreten
- Sicherheit und Kollaboration deutlich verbessert

### Betroffene Dateien
- `backend/aufguss_backend/aufguss_app/consumers.py`
- `frontend/src/components/Chat.tsx`
- `frontend/src/components/Calendar.tsx`

### Hinweise
- Test mit mehreren Nutzern empfohlen
- Fehlerbehandlung und Security geprüft
- Siehe Changelog und Wiki für Details

Closes #<ISSUE_NR> (bitte Issue-Nummer ergänzen)
