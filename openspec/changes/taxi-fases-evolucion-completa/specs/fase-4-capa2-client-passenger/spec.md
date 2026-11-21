## ADDED Requirements

### Requirement: Cotización Transparente de Tarifa por Sector
El sistema SHALL calcular y mostrar al pasajero el valor estimado del viaje antes de solicitar el servicio, basado en la matriz oficial de sectores y barrios de la ciudad.

#### Scenario: Estimación de Tarifa
- **WHEN** el pasajero selecciona su destino en el formulario
- **THEN** el sistema calcula la tarifa base más recargos vigentes y la presenta de forma clara en pantalla

### Requirement: Seguimiento en Vivo del Vehículo Asignado
El sistema SHALL renderizar en un mapa interactivo la posición en tiempo real del taxi asignado, junto con la placa, número móvil y datos verificados del conductor.

#### Scenario: Aceptación de Servicio
- **WHEN** un taxi es asignado a la solicitud del pasajero
- **THEN** el mapa actualiza la posición del móvil cada 3 segundos hasta su llegada al punto de recogida
