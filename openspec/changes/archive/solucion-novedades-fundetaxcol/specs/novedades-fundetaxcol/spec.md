# Spec: Novedades Oficiales Fundetaxcol

## REQ-001: Persistencia de Sesión y Auto-Reconexión Silenciosa
* **GIVEN** que el operador ha iniciado sesión y tiene credenciales guardadas en `LocalStorage`.
* **WHEN** la sesión de Odoo expira en el servidor o la app vuelve de segundo plano y una llamada RPC recibe un fallo de autenticación o timeout.
* **THEN** el sistema DEBE re-autenticarse silenciosamente en segundo plano y reintentar la operación, sin expulsar al operador al `LoginView`.

## REQ-002: Visibilidad del Concepto de Pago en Tarjetas
* **GIVEN** un registro de pago recibido desde el backend Odoo o generado en caja.
* **WHEN** `PagoRecaudoModel.fromJson` procesa los datos del pago.
* **THEN** DEBE deserializar las líneas de `concepto_ids` y exponer el nombre del concepto principal (`conceptoNombre`).
* **AND** `PagoCardWidget` DEBE mostrar el nombre del concepto en la Fila 2 junto al nombre del conductor.

## REQ-003: Captura Rápida y Manual de Tipo de Pago
* **GIVEN** que el cajero se encuentra en `PaymentFormView` registrando un recaudo.
* **WHEN** necesita especificar el concepto de cobro.
* **THEN** DEBE poder escribir el nombre del concepto manualmente o seleccionarlo de las sugerencias de Odoo en la misma pantalla principal, sin obligación de usar un dropdown rígido en pantalla secundaria.

## REQ-004: Destinos Manuales y Sin Truncamiento Alfabético
* **GIVEN** la lista de tarifas sectoriales en `OdooService.getTarifasSector()`.
* **WHEN** se consulta el catálogo de destinos de Odoo.
* **THEN** la consulta DEBE solicitar un límite suficiente (≥ 1000) para asegurar la carga completa de sectores que inician con M, P, S y el resto del abecedario (incluyendo Manga, Manzanillo del Mar, Pedro Salazar, San Pedro, San Francisco).
* **AND** en `TurnoFormView`, el operador DEBE poder escribir libremente el destino con autocompletado en un campo de texto, asociando automáticamente la tarifa si coincide o registrando el destino personalizado.

## REQ-005: Tarifa Oficial de Recargo Nocturno de $1.100
* **GIVEN** un despacho registrado entre las 19:00 horas (7:00 p.m.) y las 04:59:59 horas.
* **WHEN** se calcula el valor total del servicio con recargo nocturno.
* **THEN** el valor adicional por recargo DEBE ser exactamente de $1.100 COP, sin ser sobreescrito por valores desactualizados de la base de datos.

## REQ-006: Supresión del Cuadro de Métricas en Vistas de Turnos
* **GIVEN** que el operador se encuentra en `BahiaSelectedView`.
* **WHEN** selecciona la pestaña de Turnos en Cola (`_currentIndex == 1`) o Turnos Despachados (`_currentIndex == 2`).
* **THEN** el cuadro de métricas ("Recaudo Empresa" y "Servicios Clientes") DEBE ocultarse para dejar el 100% de la altura de la pantalla disponible a las tarjetas de turnos.
* **AND** el cuadro de métricas solo DEBE visualizarse en la pestaña de Pagos (`_currentIndex == 0`).

