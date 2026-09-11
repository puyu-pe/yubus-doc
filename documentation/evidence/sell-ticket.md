# Sell Ticket Evidence

## Scope

Pilot evidence for `docs/tickets/sell_ticket.md`. The source checkout was read
only; no transaction or browser action was performed.

## Trace

| Layer | Evidence |
| --- | --- |
| UI | `resources/views/trip/list.blade.php` includes `ticket.partial.modal_register` in the trip list. |
| JavaScript | `public/develop/ticket/index_jquery.js` assigns the create form action to `sales/insertTicket`; `public/develop/ticket/index_jscript.js` contains the ticket-sale confirmation flow. |
| Route | `routes/web.php`: `POST sales/insertTicket` uses `SaleController::insertTicket` and `permission:ticket.create`. |
| Controller | `app/Http/Controllers/SaleController.php::insertTicket` requires AJAX, validates `Sale::TICKET_VALIDATION`, checks the seat, and wraps persistence in a database transaction. |
| Services/models | `TicketService::checkSeatNumber`, `TicketService::getOrUpdateTicket`, `SaleService::findOrUpdateTicketSale`, and `Sale::TICKET_VALIDATION` participate in the flow. |
| Tests | `tests/Feature/Regression/SaleControllerTicketEndpointsTest.php` covers tenant, login, permission, and controller-boundary behavior. `tests/Unit/Services/Regression/TicketSaleRegressionTest.php` covers ticket-sale service regression behavior. |

## Claim Classification

- Proven: the request uses the `ticket.create` permission, validates submitted data, checks a seat number, and returns either a registered or reserved message after a successful transaction.
- Conditional: whether a sale is registered or reserved depends on ticket status; document/series and CPE behavior depend on request and configured services.
- Operational advice: verify the selected seat and data before confirming.
- Uncertainty: current screenshots were not validated against a live application in this change; field-level mandatory status beyond the validation constant was not asserted in the user guide.
