# Helpdesk Sync

---

## Deutsch

Frappe-App: Hält den Helpdesk-`HD Customer` automatisch als Read-only-Spiegel
des ERPNext-`Customer` synchron und blockiert manuelles Anlegen/Umbenennen
von HD-Kunden im Helpdesk.

### Funktion

- **Single Source of Truth:** Kunden werden ausschließlich in ERPNext als
  `Customer` gepflegt.
- **Automatischer Spiegel:** Bei Anlegen/Ändern eines Customers wird ein
  gleichnamiger `HD Customer` erzeugt/aktualisiert (Namensgleichheit
  garantiert: `HD Customer.name == Customer.name`).
- **Schutz:** Manuelles Anlegen eines HD Customers im Helpdesk wird
  blockiert, sofern kein gleichnamiger ERPNext-Customer existiert.
  Umbenennen des Spiegels wird ebenfalls blockiert.
- **Optional Domain-Mapping:** Es wird versucht, die E-Mail-Domain des
  Kunden zu ermitteln und am HD Customer zu hinterlegen (für automatische
  Ticketzuordnung über die Absender-Domain).

### Installation

```bash
# Im bench-Verzeichnis
bench get-app helpdesk_sync /pfad/zur/app
# oder von Git:
# bench get-app https://.../helpdesk_sync.git

bench --site <deine-site> install-app helpdesk_sync
bench --site <deine-site> migrate
bench restart
```

### Initialabgleich (Bestandskunden)

```bash
bench --site <deine-site> execute helpdesk_sync.sync.backfill_all
```

### Deinstallation

```bash
bench --site <deine-site> uninstall-app helpdesk_sync
```

---

## English

Frappe app: Automatically keeps the Helpdesk `HD Customer` as a read-only
mirror of the ERPNext `Customer` and blocks manual creation/renaming of
HD customers in the Helpdesk.

### Features

- **Single Source of Truth:** Customers are managed exclusively in ERPNext
  as `Customer` records.
- **Automatic Mirror:** When a Customer is created or updated, a matching
  `HD Customer` is created/updated accordingly (name parity guaranteed:
  `HD Customer.name == Customer.name`).
- **Protection:** Manually creating an HD Customer in the Helpdesk is
  blocked if no matching ERPNext Customer exists. Renaming the mirror is
  also blocked.
- **Optional Domain Mapping:** The app attempts to determine the customer's
  e-mail domain and store it on the HD Customer (for automatic ticket
  assignment based on sender domain).

### Installation

```bash
# Inside the bench directory
bench get-app helpdesk_sync /path/to/app
# or from Git:
# bench get-app https://.../helpdesk_sync.git

bench --site <your-site> install-app helpdesk_sync
bench --site <your-site> migrate
bench restart
```

### Initial Sync (Existing Customers)

```bash
bench --site <your-site> execute helpdesk_sync.sync.backfill_all
```

### Uninstallation

```bash
bench --site <your-site> uninstall-app helpdesk_sync
```
