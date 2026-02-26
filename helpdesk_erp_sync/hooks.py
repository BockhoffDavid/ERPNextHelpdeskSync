
doc_events = {
    "HD Ticket": {
        "after_insert": "helpdesk_erp_sync.sync.create_sales_order_for_ticket"
    }
}
