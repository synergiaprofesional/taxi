## ADDED Requirements

### Requirement: Máquina de Estados del Vehículo y Despacho Híbrido
El sistema SHALL gestionar el ciclo de vida operativo del taxi transitando entre los estados `Fuera de Turno`, `En Cola Bahía`, `Despachado`, `En Carrera` y `Libre en Calle`.

#### Scenario: Transición de Carrera a Libre
- **WHEN** el conductor finaliza un viaje activo
- **THEN** su estado cambia a `Libre en Calle` y queda disponible para el radar de solicitudes cercanas o enturne virtual

### Requirement: Enturne Virtual por Proximidad Geográfica
El sistema SHALL detectar mediante geofencing cuando un taxi libre se aproxima a una bahía con cupos disponibles y permitirle ingresar a la cola sin contacto manual.

#### Scenario: Detección en Rango de Bahía
- **WHEN** el taxi libre entra en el radio de 300 metros de una bahía regulada
- **THEN** el sistema le ofrece enturnarse digitalmente respetando el orden estricto de llegada
