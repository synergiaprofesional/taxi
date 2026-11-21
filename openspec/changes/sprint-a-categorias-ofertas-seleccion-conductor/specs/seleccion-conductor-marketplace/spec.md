# Especificación: Selección de Conductor en Marketplace Transparente

## Requerimientos Normativos

### Requerimiento 1: Recepción Reactiva de Ofertas de Taxistas
Cuando los conductores aceptan o contraofertan una carrera, el pasajero debe ver las opciones aparecer en tiempo real sin recargar la pantalla.

#### Escenario: Conductores envían ofertas a la carrera
- **GIVEN** una carrera en estado `solicitado`
- **WHEN** dos taxistas responden mediante su app (uno aceptando el precio y otro contraofertando)
- **THEN** `DriverOffersSheet` renderiza dos tarjetas ordenadas por cercanía o precio
- **AND** muestra para cada uno: nombre, foto, calificación, vehículo, placa, tiempo estimado de llegada y precio propuesto.

---

### Requerimiento 2: Selección y Confirmación del Conductor
El pasajero tiene el control absoluto para decidir cuál conductor tomar. Al pulsar "Aceptar", el viaje queda asignado exclusivamente a ese móvil.

#### Escenario: Pasajero elige un conductor de la lista
- **GIVEN** la lista de ofertas en pantalla
- **WHEN** el pasajero presiona "Elegir Conductor" sobre la oferta seleccionada
- **THEN** el sistema ejecuta una transacción que actualiza el viaje a estado `asignado`
- **AND** asigna los datos definitivos del conductor y la tarifa pactada
- **AND** navega automáticamente a la pantalla de seguimiento `PassengerTripTrackingView`.
