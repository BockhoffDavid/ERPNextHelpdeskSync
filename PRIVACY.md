# Privacy Policy / Datenschutzerklärung

---

## Deutsch

### Verantwortlicher

Michael Bockhoff GmbH
Weitere Kontaktdaten entnehmen Sie bitte dem Impressum Ihrer Frappe-Instanz.

### Welche Daten werden verarbeitet?

Diese App verarbeitet ausschließlich Daten, die bereits innerhalb Ihrer eigenen
Frappe-Instanz gespeichert sind. Es werden keine Daten an externe Dienste
übertragen. Konkret werden folgende Daten zwischen den installierten Apps
(ERPNext und Frappe Helpdesk) synchronisiert:

| Datenfeld | Quelle | Ziel | Zweck |
|-----------|--------|------|-------|
| Kundenname | ERPNext `Customer` | Helpdesk `HD Customer` | Kundenspiegel |
| E-Mail-Domain | ERPNext Kontakt | Helpdesk `HD Customer` | Automatische Ticketzuordnung |
| Ticketbetreff | Helpdesk `HD Ticket` | ERPNext `Project` | Projekterstellung |
| Ticketbeschreibung | Helpdesk `HD Ticket` | ERPNext `Project` | Projekterstellung |
| Priorität | Helpdesk `HD Ticket` | ERPNext `Project` | Projekterstellung |
| Kunde (Zuordnung) | Helpdesk `HD Ticket` | ERPNext `Project` | Bidirektionale Sync |

### Wo werden die Daten gespeichert?

Alle Daten verbleiben ausschließlich in der Datenbank Ihrer eigenen
Frappe-/ERPNext-Instanz. Die App überträgt keine Daten an Dritte oder
externe Server.

### Wie lange werden die Daten gespeichert?

Die synchronisierten Datensätze (`HD Customer`, `Project`) bleiben so lange
gespeichert, wie sie in der jeweiligen App vorhanden sind. Die App löscht
einen `HD Customer`-Spiegel automatisch, wenn der zugrundeliegende
ERPNext-`Customer` gelöscht wird – sofern keine verknüpften Tickets mehr
vorhanden sind.

### Rechte der betroffenen Personen

Da diese App ausschließlich innerhalb Ihrer eigenen Infrastruktur operiert,
obliegt die Wahrnehmung der Betroffenenrechte (Auskunft, Berichtigung,
Löschung) dem Betreiber der Frappe-Instanz.

### Änderungen dieser Erklärung

Diese Datenschutzerklärung kann bei Erweiterungen des Funktionsumfangs der
App aktualisiert werden.

---

## English

### Controller

Michael Bockhoff GmbH
For contact details please refer to the legal notice of your Frappe instance.

### What data is processed?

This app processes only data that is already stored within your own Frappe
instance. No data is transmitted to external services. The following data is
synchronized between the installed apps (ERPNext and Frappe Helpdesk):

| Field | Source | Destination | Purpose |
|-------|--------|-------------|---------|
| Customer name | ERPNext `Customer` | Helpdesk `HD Customer` | Customer mirror |
| E-mail domain | ERPNext Contact | Helpdesk `HD Customer` | Automatic ticket assignment |
| Ticket subject | Helpdesk `HD Ticket` | ERPNext `Project` | Project creation |
| Ticket description | Helpdesk `HD Ticket` | ERPNext `Project` | Project creation |
| Priority | Helpdesk `HD Ticket` | ERPNext `Project` | Project creation |
| Customer (assignment) | Helpdesk `HD Ticket` | ERPNext `Project` | Bidirectional sync |

### Where is the data stored?

All data remains exclusively in the database of your own Frappe/ERPNext
instance. The app does not transfer any data to third parties or external
servers.

### How long is the data retained?

Synchronized records (`HD Customer`, `Project`) are retained as long as they
exist in the respective app. The app automatically deletes an `HD Customer`
mirror when the underlying ERPNext `Customer` is deleted — provided no linked
tickets remain.

### Rights of data subjects

Since this app operates exclusively within your own infrastructure, the
exercise of data subject rights (access, rectification, erasure) is the
responsibility of the operator of the Frappe instance.

### Changes to this policy

This privacy policy may be updated when the functionality of the app is
extended.
