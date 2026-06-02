# Helpdesk Sync

---

## Deutsch

Frappe-App für Frappe v16: Synchronisiert ERPNext und Frappe Helpdesk automatisch.
Kunden werden aus ERPNext in den Helpdesk gespiegelt, und für jedes neue Ticket
wird automatisch ein ERPNext-Projekt angelegt.

### Funktionen

- **Single Source of Truth:** Kunden werden ausschließlich in ERPNext als
  `Customer` gepflegt.
- **Automatischer Kundenspiegel:** Bei Anlegen/Ändern eines Customers wird ein
  gleichnamiger `HD Customer` erzeugt/aktualisiert (Namensgleichheit
  garantiert: `HD Customer.name == Customer.name`).
- **Schutz:** Manuelles Anlegen oder Umbenennen eines HD Customers im Helpdesk
  wird blockiert, sofern kein gleichnamiger ERPNext-Customer existiert.
- **Optional Domain-Mapping:** Die E-Mail-Domain des Kunden wird am HD Customer
  hinterlegt (für automatische Ticketzuordnung über die Absender-Domain).
- **Automatische Projekterstellung:** Für jedes neue Helpdesk-Ticket wird
  automatisch ein ERPNext-Projekt angelegt (`Ticket-ID - Betreff`), inklusive
  Kunde, Priorität und Beschreibung.
- **Bidirektionale Kundensync:** Wird der Kunde am Ticket oder am Projekt
  geändert, wird die Änderung automatisch auf das jeweils andere Dokument
  übertragen.

### Voraussetzungen

- Frappe `>=16.0.0,<17.0.0`
- ERPNext
- Frappe Helpdesk

### Installation

```bash
# Im bench-Verzeichnis
bench get-app helpdesk_sync https://.../helpdesk_sync.git

bench --site <deine-site> install-app helpdesk_sync
bench --site <deine-site> migrate
bench restart
```

### Initialabgleich (Bestandskunden)

Legt für alle bestehenden ERPNext-Kunden einen HD-Customer-Spiegel an:

```bash
bench --site <deine-site> execute helpdesk_sync.sync.backfill_all
```

### Deinstallation

```bash
bench --site <deine-site> uninstall-app helpdesk_sync
```

---

## English

Frappe app for Frappe v16: Automatically synchronizes ERPNext and Frappe Helpdesk.
Customers are mirrored from ERPNext into the Helpdesk, and a new ERPNext Project
is created for every incoming ticket.

### Features

- **Single Source of Truth:** Customers are managed exclusively in ERPNext
  as `Customer` records.
- **Automatic Customer Mirror:** When a Customer is created or updated, a matching
  `HD Customer` is created/updated accordingly (name parity guaranteed:
  `HD Customer.name == Customer.name`).
- **Protection:** Manually creating or renaming an HD Customer in the Helpdesk is
  blocked if no matching ERPNext Customer exists.
- **Optional Domain Mapping:** The customer's e-mail domain is stored on the
  HD Customer for automatic ticket assignment based on sender domain.
- **Automatic Project Creation:** For every new Helpdesk ticket an ERPNext Project
  is created automatically (`Ticket-ID - Subject`), including customer, priority,
  and description.
- **Bidirectional Customer Sync:** Changing the customer on either the ticket or
  the project automatically updates the other document.

### Requirements

- Frappe `>=16.0.0,<17.0.0`
- ERPNext
- Frappe Helpdesk

### Installation

```bash
# Inside the bench directory
bench get-app helpdesk_sync https://.../helpdesk_sync.git

bench --site <your-site> install-app helpdesk_sync
bench --site <your-site> migrate
bench restart
```

### Initial Sync (Existing Customers)

Creates an HD Customer mirror for all existing ERPNext customers:

```bash
bench --site <your-site> execute helpdesk_sync.sync.backfill_all
```

### Uninstallation

```bash
bench --site <your-site> uninstall-app helpdesk_sync
```
