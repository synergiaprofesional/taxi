# OpenSpec: View Despacho List (Historial General de Despachos del Conductor)

## Requirements

### Requirement: Búsqueda Transversal de Servicios Despachados
El sistema DEBE permitir consultar todos los despachos realizados por un conductor o vehículo a través de cualquier bahía de la ciudad en la jornada actual.

#### Scenario: Visualización por defecto de despachos de la bahía actual
- **GIVEN** que el operador está en Bahía Garita y el buscador está vacío
- **WHEN** consulta la pestaña Despachos
- **THEN** la lista DEBE mostrar los vehículos despachados en Bahía Garita en orden cronológico inverso.

#### Scenario: Búsqueda global de servicios de un conductor
- **GIVEN** que un conductor realizó servicios desde varias bahías (ej. Garita, 29D y Lago)
- **WHEN** el operador busca por el nombre del conductor o placa del vehículo (ej. `985`)
- **THEN** la lista DEBE mostrar todos los despachos realizados por dicho vehículo/conductor en el día sin importar la bahía de partida.
