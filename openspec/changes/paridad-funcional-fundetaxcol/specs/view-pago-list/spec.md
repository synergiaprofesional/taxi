# OpenSpec: View Pago List (Transversal Multi-Bahía)

## Requirements

### Requirement: Búsqueda Transversal de Pagos Multi-Bahía
El sistema DEBE presentar los pagos de la bahía seleccionada cuando el buscador esté vacío, pero cuando el operador digite un término de búsqueda (placa, conductor o consecutivo), el sistema DEBE buscar sobre TODOS los pagos de todas las bahías registrados en la jornada.

#### Scenario: Visualización por defecto de la bahía activa
- **GIVEN** que el operador está ubicado en la bahía Garita y el buscador está vacío
- **WHEN** se carga la pestaña de Pagos
- **THEN** la lista DEBE mostrar únicamente los recaudos efectuados en Garita ordenados por consecutivo descendente.

#### Scenario: Búsqueda transversal de recaudos en cualquier bahía
- **GIVEN** que un vehículo `WGO194` pagó en Bahía Lago o Bahía 29D
- **WHEN** el operador escribe `WGO194` en el buscador mientras tiene seleccionada la bahía Garita
- **THEN** el sistema DEBE encontrar y mostrar el pago del vehículo `WGO194`, indicando claramente la bahía de origen en la tarjeta.
