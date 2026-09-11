# Cargo and Zero Seats Evidence

## Scope

Evidence for the LOT1 updates to the bus, trip scheduling, package registration,
and package assignment guides. The source checkout was read only at commit
`7870ebd9245846ae873c3b20ae3802b35c390815` (version `2.15.2`); no transaction
or browser action was performed.

## Trace

| Layer | Evidence |
| --- | --- |
| Bus UI | `resources/views/bus/partial/modal_register.blade.php` renders `Modo Servicio` from `Bus::SERVICE_MODE` and gives `Asientos`, `Asientos seg.`, and `Adicional` a minimum of `0`. |
| Bus model and controller | `app/Models/Bus.php` defines `Mixto`, `Pasajero`, and `Carga` as values `1`, `2`, and `3`; it validates the three capacity fields as numeric and validates the mode independently. `app/Http/Controllers/BusController.php::insert` and `::update` use that validation. |
| Trip UI and JavaScript | `app/Http/Controllers/TripController.php::index` supplies active buses to the trip view. `public/develop/trip/index_jscript.js::loadSeatDetail` labels the preview unavailable for cargo, then parses the stored distribution. |
| Trip controller and route | `TripController::insert` requires an existing bus identifier; `::getAvailableSeats` creates the available-seat list from `seats_first_class`. `routes/web.php` exposes `POST trips/insert` with `permission:trip.create`. |
| Package registration UI and JavaScript | `resources/views/commend/partial/modal_register.blade.php` groups scheduled trips by each bus service mode. `public/develop/commend/receipt_jscript.js::filterTrips` limits displayed trips to the selected line and retains the unassigned option. |
| Package assignment UI, controller, and route | `public/develop/trip/index_jquery.js` loads pending and assigned packages and invokes assignment endpoints. `TripController::getCommendAvailable` filters active, unassigned packages by line and departure station; `::setCommendAssigned` stores the selected trip. `routes/web.php` protects assignment mutations with `permission:trip.update`. |
| Tests | `tests/Feature/Regression/TripMutationAuthorizationMariaDbTest.php` covers authorization boundaries for package assignment mutations. No focused test for cargo mode, zero seats, or ticket-sale blocking was found. |

## Claim Classification

- Proven: `Carga` is a supported bus service mode; it is independent of the three numeric capacity fields; each capacity input permits zero.
- Proven: scheduled trips are grouped by bus service mode during package registration, and a package can remain unassigned for later assignment to a trip.
- Proven: a cargo trip shows an unavailable seat-preview label while still parsing its stored layout; guides must not recommend an empty layout.
- Proven: a zero value for first-class seats produces an empty available-seat list.
- Operational advice: use a cargo-mode trip with zero passenger seats to manage packages, and verify the selected cargo trip before assigning packages.
- Uncertainty: no hard backend prohibition on ticket sales for a zero-seat cargo trip was demonstrated. The public guides therefore do not promise such a prohibition.
