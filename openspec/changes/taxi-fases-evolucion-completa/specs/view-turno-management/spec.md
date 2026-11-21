## MODIFIED Requirements

### Requirement: Gestión de Turnos Reactiva sobre Firestore
El sistema SHALL gestionar la fila de vehículos en bahía utilizando streams en tiempo real de Cloud Firestore (`collection('turnos').snapshots()`), eliminando el acoplamiento a llamadas JSON-RPC de Odoo 11.

#### Scenario: Enturnar Vehículo sin Odoo
- **WHEN** el operador registra la placa o móvil en la bahía activa
- **THEN** el turno se almacena como documento en Firestore y se propaga instantáneamente a todas las pantallas conectadas

#### Scenario: Despacho Atómico en Cola
- **WHEN** se confirma el despacho de una unidad
- **THEN** una transacción de Firestore actualiza el estado a `despachado` y reordena la secuencia de los turnos siguientes
