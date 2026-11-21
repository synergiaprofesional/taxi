# Especificación: Categorías y Oferta con Ancla Legal

## Requerimientos Normativos

### Requerimiento 1: Selección de Categoría de Viaje
La aplicación debe permitir al pasajero alternar entre categorías de viaje en un solo toque, adaptando la tarifa base y el tipo de vehículo.

#### Escenario: Pasajero selecciona categoría de viaje
- **GIVEN** el pasajero se encuentra en `PassengerHomeView`
- **WHEN** toca el chip de "Bahía Prioritaria" o "Ejecutivo VIP"
- **THEN** la interfaz actualiza la categoría activa en el estado
- **AND** recalcula la tarifa sugerida aplicando las reglas de la categoría correspondiente.

---

### Requerimiento 2: Ancla Legal y Ajuste de Oferta
La tarifa base mostrada al usuario debe provenir estrictamente de la matriz de sectores aprobada por decreto distrital. El pasajero puede ajustar su oferta voluntaria mediante incrementos predefinidos.

#### Escenario: Pasajero ajusta el valor ofertado
- **GIVEN** un sector seleccionado con tarifa oficial de $14.000 COP
- **WHEN** el pasajero pulsa el botón `[ + $2.000 ]`
- **THEN** la oferta del pasajero se establece en $16.000 COP
- **AND** la interfaz muestra el desglose: "Tarifa Oficial Decreto: $14.000 + Propina/Ajuste voluntario: $2.000".

#### Escenario: Publicación de la oferta a la flota
- **GIVEN** una oferta configurada por el pasajero
- **WHEN** pulsa "Pedir Taxi / Publicar Oferta"
- **THEN** se crea el documento en `/viajes` con estado `solicitado`
- **AND** se abre de inmediato la hoja interactiva `DriverOffersSheet` a la espera de postulaciones.
