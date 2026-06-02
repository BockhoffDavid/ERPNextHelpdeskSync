# Helpdesk Sync

Frappe-App: Hält den Helpdesk-`HD Customer` automatisch als Read-only-Spiegel
des ERPNext-`Customer` synchron und blockiert manuelles Anlegen/Umbenennen
von HD-Kunden im Helpdesk.

## Funktion

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

## Installation

```bash
# Im bench-Verzeichnis
bench get-app helpdesk_sync /pfad/zur/app
# oder von Git:
# bench get-app https://.../helpdesk_sync.git

bench --site <deine-site> install-app helpdesk_sync
bench --site <deine-site> migrate
bench restart
```

## Initialabgleich (Bestandskunden)

```bash
bench --site <deine-site> execute helpdesk_sync.sync.backfill_all
```

## Deinstallation

```bash
bench --site <deine-site> uninstall-app helpdesk_sync
```
