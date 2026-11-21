# OpenSpec: View Pago Form (Resolución Automática de Conductor y Conceptos)

## Requirements

### Requirement: Resolución Automática de Conductor y Conceptos al Digitar Placa
El sistema DEBE resolver inmediatamente el nombre real del conductor asociado al vehículo digitado (erradicando "Conductor Desconocido") y precargar automáticamente los conceptos de cobro asociados.

#### Scenario: Digitación de placa existente
- **GIVEN** que el vehículo `WGM776` tiene asignado un conductor en la base de datos
- **WHEN** el operador digita o selecciona `WGM776` en "Nuevo Recaudo de Caja"
- **THEN** el campo conductor DEBE poblarse automáticamente con el nombre del conductor titular (y no "Conductor Desconocido").
- **AND** los conceptos a cobrar DEBEN inicializarse con los conceptos parametrizados para ese conductor o con el concepto obligatorio general.
