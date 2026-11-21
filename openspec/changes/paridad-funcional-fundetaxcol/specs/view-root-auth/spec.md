# OpenSpec: View Root Auth (Persistencia de Ciclo de Vida y Tolerancia a Red)

## Requirements

### Requirement: Persistencia de Tarea en Android sin Cierre por Inactividad
El sistema DEBE mantener el proceso de la aplicación en segundo plano sin ser purgado por Android al suspender la pantalla o alternar entre aplicaciones.

#### Scenario: Cambio de aplicación o reposo
- **GIVEN** que el despachador está usando la app y bloquea la pantalla o abre WhatsApp
- **WHEN** desbloquea el teléfono o regresa a Synergia Móvil después de varios minutos
- **THEN** la aplicación DEBE conservar su estado y permanecer abierta en la vista correspondiente sin cerrarse repentinamente ni forzar re-autenticación.
