# Salida y entrega de encomiendas

## Salida de encomiendas

Cuando se [registra la salida de un bus (inicia un viaje)](../trips/register_departure.md),
automaticamente las encomiendas asignadas a ese viaje tambien registran su salida. Por ende no es un proceso
que se realice manualmente.

## Entrega de encomiendas

Cuando se [registra la llegada de un bus (finaliza un viaje)](../trips/register_arrival.md)
automaticamente las encomiendas asignadas a ese viaje pasan del estado "vigente" a **"en destino"**.

Toda encomienda que este marcado con el estado **"en destino"** es valido para ser entregado.

Pasos:

1. [Ir a entrega encomiendas](#ir-a-entrega-encomiendas)
2. [Buscar encomienda](#buscar-encomienda)
3. [Abrir detalles de encomienda](#abrir-detalles-de-encomienda)
4. [Realizar entrega](#realizar-entrega)
5. [Cofirmar entrega](#confirmar-entrega)

### Ir a entrega encomiendas

![Entrega de encomiendas menu](../img/departure_packages.png)

### Buscar encomienda

> Se puede buscar por ruta y fecha, para buscar por otros parametros click en "busqueda avanzada".

![filtros de busqueda](../img/departure_delivery_packages_filters.png)

#### Busqueda avanzada

> Parametros de busqueda:

> * Doc. Empresa remitente
> * Nombre empresa remitente
> * Doc. Cliente remitente
> * Nombre cliente remitente
> * Doc. Destinatario
> * Nombre destinatario

![busqueda avanzada](../img/departure_delivery_packages_advanced_search.png)

### Abrir detalles de encomienda

> * Ubicado la encomienda a entregar.
> * Verificar "Estado" (en destino) y "Viaje/Entrega" (pendiente de entrega).
> * Click en el boton al inicio de la fila.

![boton redirección formulario](../img/departure_delivery_packages_form_button.png)

### Realizar entrega

> Click boton "Realizar entrega".

![formulario salida de encomiendas](../img/departure_delivery_packages_form.png)

### Confirmar entrega

![panel de cofirmación entrega](../img/departure_delivery_packages_confirm.png)
