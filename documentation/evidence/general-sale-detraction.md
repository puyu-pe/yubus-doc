# General Sale and Detraction Evidence

## Scope

Evidence for `docs/operations/general_sales.md`. The source checkout was read
only at commit `7870ebd9245846ae873c3b20ae3802b35c390815` (version `2.15.2`).
No browser interaction, transaction, or test runtime execution was performed.

## Similarity Decision

`docs/reports/operation.md` contains a short report-oriented reference to
`Ingreso con Facturación`, but it does not document the general-sale form or
the optional detraction workflow. This is a distinct end-user flow, so a new
guide is appropriate.

## Trace

| Layer | Evidence |
| --- | --- |
| Entry UI | `resources/views/operation/index.blade.php` labels the page `OPERACIONES DE INGRESOS Y EGRESOS`, exposes the `Ingresos` tab, and labels the general-sale entry button `Ingreso con Facturación`. |
| Sale form UI | `resources/views/operation/partial/modal_sale_register.blade.php` provides the general-sale fields, the `REALIZAR VENTA` action, and conditional `Aplicar detracción` controls with type, payment-method, percentage, detraction, and net-collection summary. |
| JavaScript | `public/develop/operation/index_jquery.js` opens and resets the sale form, toggles detraction controls, and blocks submission when the bank-account notice is present. `public/develop/operation/index_jscript.js` validates the form, calculates quantity times unit price, requests confirmation, and submits the sale. `public/develop/operation/detraction.js` calculates gross, detraction, and net in cents. |
| Route and controller | `routes/web.php` maps `POST operations/sale/insertSale` to `OperationController::insertSale` with `permission:operation.create`. The controller validates the sale, verifies the submitted total against quantity times unit price, resolves optional detraction, records the sale and operation, and sends the general-sale CPE. |
| Detraction service and models | `app/Services/SaleDetractionService.php` exposes only active, available, effective catalog entries; accepts electronic tax document codes `01` and `03`; requires the system-level configuration when detraction is applied; and calculates the amount in cents using the local HALF_UP policy. `SaleDetraction` persists the selected type, bank-account, payment-method, percentage, and amount snapshot. |
| Tests inspected | `tests/Feature/Regression/GeneralSaleDetractionUiTest.php` covers UI availability, safe projection, and catalog selectors. `tests/Unit/Services/SaleDetractionServiceTest.php` covers configuration, documents, catalog state, and monetary rounding. `tests/Feature/Regression/GeneralSaleTransactionTest.php` covers gross fiscal values, net collection, receipt support, and a credit-payment scenario. |

## Claim Classification

- Proven: the general-sale entry is `Operaciones de ingresos y egresos` > `Ingresos` > `Ingreso con Facturación`.
- Proven: optional detraction is supported only for electronic tax document codes `01` and `03`; the guide limits the flow to Factura and Boleta, not ticket or package flows.
- Proven: the gross total is quantity times unit price. When detraction is selected, the interface previews the percentage, detraction amount, and net collection; the service rounds the detraction amount to cents with its local HALF_UP policy.
- Proven: no automatic minimum-threshold rule is implemented in the inspected detraction resolution flow.
- Conditional: the detraction controls depend on system configuration, a configured bank account, and active, available, effective catalog entries. A missing or invalid configuration can make the option unavailable or prevent submission.
- Operational advice: verify the total, collection amount, selected type, payment method, and due date before confirming. Contact an administrator for unavailable or misconfigured detraction; do not alter system parameters from this workflow.
- Uncertainty: no live browser action, sale transaction, or test runtime was executed for this documentation change. The guide provides no tax advice and does not establish whether detracción applies to a particular sale.
