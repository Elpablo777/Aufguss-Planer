# Admin- und Moderationsfunktionen

## Status
- Das Django-Admin-Panel ist für alle Models aktiviert und dokumentiert.
- User-Ban, Rollenverwaltung und Meldefunktion sind als Features geplant (siehe Roadmap).

## Geplante Features
- **User-Ban:** Admins können Nutzer:innen temporär oder dauerhaft sperren.
- **Rollen:** Einführung von Rollen (z. B. Admin, Moderator, Nutzer:in) für differenzierte Rechte.
- **Meldesystem:** Nutzer:innen können Inhalte melden, Admins/Moderatoren bearbeiten diese Meldungen.
- **Moderations-Log:** Alle Moderationsaktionen werden nachvollziehbar protokolliert.

## Open-Source-Workflow
- Entwicklung erfolgt transparent über Issues, Pull Requests und Wiki.
- Feature-Vorschläge und Diskussionen über GitHub Discussions.
- Alle Änderungen werden im [CHANGELOG.md](./CHANGELOG.md) dokumentiert.

## Technische Hinweise
- Django-Admin ist über `/admin/` erreichbar (nur für berechtigte User).
- Erweiterungen erfolgen in `aufguss_app/admin.py` und ggf. eigenen Views/Permissions.

## Weiterführende Doku
- [Django Admin Doku](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/)
- [Mitwirken.md](./Mitwirken.md)
- [Wiki: Admin-Moderation](./WIKI.md)
