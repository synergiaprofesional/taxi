# Spec: Despacho con Tarifas Oficiales y Sincronización de Sesión

## Requirement: Despacho de Turnos con Tarifas Sectoriales de Odoo
El sistema DEBE permitir despachar un vehículo seleccionando un destino oficial del catálogo de Odoo 11 (`fundetaxcol.tarifa.sector`) y registrar el identificador relacional en el turno.

### Scenario: Despacho exitoso con destino y tarifa oficial
- **GIVEN** un turno en estado de espera o atención activa en la bahía actual
- **WHEN** el despachador abre el formulario de despacho y selecciona una tarifa del sector (ej. "Aeropuerto / Crespo")
- **THEN** la aplicación calcula el total sumando la tarifa base y el recargo correspondiente
- **AND** al presionar "DESPACHAR SALIDA", envía a Odoo el identificador `tarifa_id`, el valor total y las notas
- **AND** Odoo marca el turno como `despachado`, fija `fecha_despacho` y emite el evento WebSocket a `/dispatch`.

---

## Requirement: Sincronización de Bahía Activa en Backend
El sistema DEBE notificar a Odoo 11 la bahía física que el operador ha seleccionado en la interfaz.

### Scenario: Cambio de bahía activa
- **GIVEN** un operador autenticado en el sistema
- **WHEN** selecciona una nueva bahía en `BahiaSelectorDialog`
- **THEN** la aplicación invoca el método `set_state` en `fundetaxcol.settings.mobile` con `current_bay = bahia.id`
- **AND** cualquier método del backend que llame a `get_current_bay()` resuelve la bahía correcta sin lanzar errores de validación.

---

## Requirement: Recaudo Contable en "Pagar y Enturnar"
El sistema DEBE asegurar que la acción combinada de "Pagar y Enturnar" registre el recaudo contable en `fundetaxcol.pago`.

### Scenario: Pagar y enturnar genera pago y turno
- **GIVEN** un operador en el terminal de cobro
- **WHEN** ejecuta la acción "Pagar y Enturnar" ingresando placa, conductor y valor
- **THEN** se genera el registro contable en `fundetaxcol.pago`
- **AND** el vehículo queda posicionado en la cola de turnos en espera de la bahía.

