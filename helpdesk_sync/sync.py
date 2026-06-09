"""
Sync ERPNext `Customer` -> Helpdesk `HD Customer`.

Designprinzipien
----------------
* `Customer` (ERPNext) ist die einzige Pflegequelle (Single Source of Truth).
* `HD Customer` ist ein reiner Read-only-Spiegel.
* Namensgleichheit ist garantiert: HD Customer.name == Customer.name.
* Manuelles Anlegen eines HD Customer im Helpdesk wird blockiert, es sei
  denn, es existiert bereits ein gleichnamiger ERPNext-Customer (dann ist es
  ein legitimer Spiegel, der z. B. durch diesen Sync ausgelöst wurde).

Hinweis zur Namensgebung
------------------------
Wir verwenden bewusst `Customer.name` (die ID des Customers) als Schlüssel,
nicht `customer_name` (das Anzeigefeld). In ERPNext kann die Customer-ID je
nach Naming-Series vom Anzeigenamen abweichen; die ID ist der stabile,
eindeutige Schlüssel. So bleibt die 1:1-Zuordnung auch dann sauber, wenn zwei
Kunden denselben Anzeigenamen tragen.
"""

import frappe
from frappe import _

# Flag, mit dem der Sync sich selbst als "autorisierte Quelle" markiert.
# Der Insert-Guard erlaubt nur Inserts, die dieses Flag tragen ODER für die
# bereits ein passender ERPNext-Customer existiert.
_SYNC_FLAG = "_nienhaus_sync_from_customer"


def upsert_hd_customer(doc, method=None):
    """Legt den HD-Customer-Spiegel an oder aktualisiert ihn.

    Wird an Customer.after_insert und Customer.on_update gehängt.
    """
    if not _helpdesk_installed():
        return

    # Disabled Customers nicht spiegeln (optional - hier: überspringen).
    customer_id = doc.name

    if frappe.db.exists("HD Customer", customer_id):
        hd = frappe.get_doc("HD Customer", customer_id)
        _apply_fields(hd, doc)
        # Flag setzen, damit ein evtl. greifender Guard den Save durchlässt.
        hd.flags[_SYNC_FLAG] = True
        hd.save(ignore_permissions=True)
    else:
        hd = frappe.new_doc("HD Customer")
        # Namensgleichheit erzwingen.
        hd.name = customer_id
        _apply_fields(hd, doc)
        hd.flags[_SYNC_FLAG] = True
        # autoname umgehen: wir setzen den Namen explizit.
        hd.insert(ignore_permissions=True, set_name=customer_id)


def _apply_fields(hd, customer):
    """Mappt Felder vom Customer auf den HD Customer.

    Das HD-Customer-DocType hat in der Standardinstallation v. a.:
      - customer_name (Pflicht-/Anzeigefeld)
      - domain (für E-Mail-Domain-basierte Ticketzuordnung)
    Weitere Felder können hier ergänzt werden.
    """
    hd.customer_name = (
        f"{customer.customer_name} {customer.name}"
        if customer.customer_name
        else customer.name
    )

    # E-Mail-Domain für automatische Ticketzuordnung ableiten, falls vorhanden.
    domain = _derive_domain(customer)
    if domain and hd.meta.has_field("domain"):
        hd.domain = domain


def _derive_domain(customer):
    """Versucht, eine E-Mail-Domain für den Kunden zu ermitteln.

    Reihenfolge: primärer Kontakt -> erste Kontakt-E-Mail des Customers.
    Liefert z. B. 'kunde.de' aus 'ansprechpartner@kunde.de'.
    """
    email = None

    # Primärer Kontakt am Customer (falls gesetzt).
    primary_contact = customer.get("customer_primary_contact")
    if primary_contact:
        email = frappe.db.get_value("Contact", primary_contact, "email_id")

    if not email:
        # Fallback: irgendeine verknüpfte Kontakt-E-Mail über Dynamic Link.
        rows = frappe.get_all(
            "Dynamic Link",
            filters={
                "link_doctype": "Customer",
                "link_name": customer.name,
                "parenttype": "Contact",
            },
            fields=["parent"],
            limit=1,
        )
        if rows:
            email = frappe.db.get_value("Contact", rows[0].parent, "email_id")

    if email and "@" in email:
        return email.split("@", 1)[1].strip().lower()
    return None


def on_customer_trash(doc, method=None):
    """Wenn ein ERPNext-Customer gelöscht wird, den Spiegel ebenfalls entfernen.

    Vorsicht: Schlägt fehl, wenn am HD Customer noch Tickets hängen. In dem
    Fall wird der Spiegel bewusst NICHT gelöscht (Datenintegrität vor
    Aufräumen). Wir fangen den Fehler ab und loggen ihn nur.
    """
    if not _helpdesk_installed():
        return

    if frappe.db.exists("HD Customer", doc.name):
        try:
            frappe.delete_doc(
                "HD Customer", doc.name, ignore_permissions=True, force=False
            )
        except frappe.LinkExistsError:
            frappe.log_error(
                title="HD Customer nicht gelöscht (verknüpfte Tickets)",
                message=f"HD Customer {doc.name} hat noch verknüpfte Belege.",
            )


# ---------------------------------------------------------------------------
# Guards: manuelles Anlegen / Umbenennen im Helpdesk verhindern
# ---------------------------------------------------------------------------

def guard_hd_customer_insert(doc, method=None):
    """Blockt das Anlegen eines HD Customer, der nicht aus einem ERPNext-
    Customer stammt.

    Erlaubt ist ein Insert nur, wenn:
      (a) der Sync ihn ausgelöst hat (Flag gesetzt), ODER
      (b) ein gleichnamiger ERPNext-Customer bereits existiert.
    """
    if doc.flags.get(_SYNC_FLAG):
        return

    # Während der App-/Site-Installation und bei Migrationen keine Blockade,
    # sonst können Fixtures/Defaults nicht angelegt werden.
    if getattr(frappe.flags, "in_install", False) or getattr(
        frappe.flags, "in_migrate", False
    ):
        return

    candidate = doc.name or doc.customer_name
    if candidate and frappe.db.exists("Customer", candidate):
        # Legitimer Spiegel eines existierenden Customers -> erlauben,
        # aber Namensgleichheit erzwingen.
        doc.name = candidate
        return

    frappe.throw(
        _(
            "HD-Kunden dürfen nicht direkt im Helpdesk angelegt werden. "
            "Bitte zuerst den Kunden in ERPNext (Customer) anlegen – der "
            "Helpdesk-Kunde wird daraus automatisch erzeugt."
        ),
        title=_("Anlegen blockiert"),
    )


def guard_hd_customer_rename(doc, method=None, old=None, new=None, merge=False):
    """Verhindert das Umbenennen des Spiegels von Hand.

    Umbenennungen sollen ausschließlich über den ERPNext-Customer laufen,
    damit die Namensgleichheit erhalten bleibt.
    """
    if getattr(frappe.flags, "in_migrate", False):
        return
    frappe.throw(
        _(
            "HD-Kunden dürfen nicht direkt umbenannt werden. Bitte den Namen "
            "über den ERPNext-Customer pflegen."
        ),
        title=_("Umbenennen blockiert"),
    )


# ---------------------------------------------------------------------------
# HD Ticket <-> ERPNext Project  (bidirektionale Kundensync)
# ---------------------------------------------------------------------------

# Verhindert Sync-Schleifen: gesetzt bevor ein Gegenstück gespeichert wird.
_TICKET_SYNC_FLAG = "_sync_from_ticket_project"


def create_project_from_ticket(doc, method=None):
    """Legt für jedes neue HD Ticket ein ERPNext-Projekt an."""
    project = frappe.new_doc("Project")
    project.project_name = f"{doc.name} - {doc.subject}"

    if doc.get("customer"):
        project.customer = doc.customer

    priority = doc.get("priority")
    if priority:
        project.priority = priority

    description = doc.get("description")
    if description:
        project.description = description

    project.insert(ignore_permissions=True)


def on_ticket_update(doc, method=None):
    """Überträgt Kundenänderung vom HD Ticket auf das verknüpfte Projekt."""
    if doc.flags.get(_TICKET_SYNC_FLAG):
        return
    project = _find_project_for_ticket(doc.name)
    if not project:
        return
    if (project.customer or "") == (doc.get("customer") or ""):
        return
    project.flags[_TICKET_SYNC_FLAG] = True
    project.customer = doc.get("customer") or ""
    project.save(ignore_permissions=True)


def on_project_update(doc, method=None):
    """Überträgt Kundenänderung vom Projekt auf das verknüpfte HD Ticket."""
    if doc.flags.get(_TICKET_SYNC_FLAG):
        return
    ticket_name = _extract_ticket_name(doc.project_name)
    if not ticket_name or not frappe.db.exists("HD Ticket", ticket_name):
        return
    ticket = frappe.get_doc("HD Ticket", ticket_name)
    if (ticket.get("customer") or "") == (doc.customer or ""):
        return
    ticket.flags[_TICKET_SYNC_FLAG] = True
    ticket.customer = doc.customer or ""
    ticket.save(ignore_permissions=True)


def _find_project_for_ticket(ticket_name):
    """Gibt das zum Ticket gehörende Projekt-Dokument zurück oder None."""
    results = frappe.get_all(
        "Project",
        filters={"project_name": ["like", f"{ticket_name} - %"]},
        fields=["name"],
        limit=1,
    )
    if not results:
        return None
    return frappe.get_doc("Project", results[0].name)


def _extract_ticket_name(project_name):
    """Extrahiert die Ticket-ID aus dem Projektnamen (Format: 'ID - Betreff')."""
    if " - " in (project_name or ""):
        return project_name.split(" - ", 1)[0]
    return None


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _helpdesk_installed():
    """True, wenn die Helpdesk-App auf dieser Site installiert ist."""
    return "helpdesk" in frappe.get_installed_apps()


# ---------------------------------------------------------------------------
# Einmaliger Initialabgleich (manuell per bench console aufrufbar)
# ---------------------------------------------------------------------------

def backfill_all():
    """Legt für alle bestehenden Customer einen HD-Customer-Spiegel an.

    Aufruf:
        bench --site <site> execute \
            helpdesk_sync.sync.backfill_all
    """
    if not _helpdesk_installed():
        frappe.throw(_("Helpdesk ist auf dieser Site nicht installiert."))

    created = 0
    for row in frappe.get_all("Customer", fields=["name"]):
        if not frappe.db.exists("HD Customer", row.name):
            customer = frappe.get_doc("Customer", row.name)
            upsert_hd_customer(customer)
            created += 1
    frappe.db.commit()
    print(f"Backfill abgeschlossen. Neu angelegte HD Customer: {created}")
    return created
