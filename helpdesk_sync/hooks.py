app_name = "helpdesk_sync"
app_title = "Helpdesk Sync"
app_publisher = "David Nienhaus"
app_description = "Sync ERPNext Customer -> Helpdesk HD Customer"
app_email = "info@example.com"
app_license = "mit"

# ---------------------------------------------------------------------------
# Document Events
# ---------------------------------------------------------------------------
# 1. Customer (ERPNext) -> HD Customer (Helpdesk) Spiegel anlegen/aktualisieren
# 2. HD Customer absichern: kein manuelles Anlegen, das nicht aus einem
#    bestehenden ERPNext-Customer stammt.
# ---------------------------------------------------------------------------

doc_events = {
    "Customer": {
        "after_insert": "helpdesk_sync.sync.upsert_hd_customer",
        "on_update": "helpdesk_sync.sync.upsert_hd_customer",
        "on_trash": "helpdesk_sync.sync.on_customer_trash",
    },
    "HD Customer": {
        "before_insert": "helpdesk_sync.sync.guard_hd_customer_insert",
        "before_rename": "helpdesk_sync.sync.guard_hd_customer_rename",
    },
    "HD Ticket": {
        "after_insert": "helpdesk_sync.sync.create_project_from_ticket",
        "on_update": "helpdesk_sync.sync.on_ticket_update",
    },
    "Project": {
        "on_update": "helpdesk_sync.sync.on_project_update",
    },
}
