app_name = "helpdesk_erp_sync"
app_title = "Helpdesk ERP Sync"
app_publisher = "David Nienhaus"
app_description = "Synchronisiert Helpdesk Tickets automatisch zu ERPNext Sales Orders"
app_email = "info@example.com"
app_license = "MIT"
app_version = "0.0.1"

doc_events = {
    "HD Ticket": {
        "after_insert": "helpdesk_erp_sync.sync.create_sales_order_for_ticket"
    }
}
