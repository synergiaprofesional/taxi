# Especificación: Búsqueda Híbrida de Pagos

## Capability: hybrid-payment-search

### Scenario 1: Búsqueda local de pagos en sesión activa
- **GIVEN** que existen 58 pagos cargados en memoria pertenecientes a las bahías activas de la sesión.
- **WHEN** el operador busca un texto de placa o conductor (ej: `'FXW558'`).
- **THEN** la vista debe filtrar y mostrar los pagos coincidentes de cualquier bahía de forma instantánea.

### Scenario 2: Búsqueda histórica remota en servidor
- **GIVEN** que el operador busca una placa o consecutivo que no fue registrado en la sesión activa (ej: `'214159'` o una placa de semanas anteriores).
- **WHEN** la búsqueda local no devuelve coincidencias y la consulta tiene al menos 3 caracteres.
- **THEN** el sistema debe consultar a Odoo en segundo plano y desplegar los pagos históricos encontrados.
