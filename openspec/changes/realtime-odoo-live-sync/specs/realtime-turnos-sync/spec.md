## ADDED Requirements

### Requirement: Consulta y Sincronización de Turnos Reales
The system MUST query and display real turnos from the Odoo database table `fundetaxcol_turno` for the selected bay, and SHALL NOT use mock or hardcoded turnos.

#### Scenario: Carga de turnos al autenticar o cambiar de bahía
- **WHEN** el operador inicia sesión exitosamente o selecciona una bahía activa (`29D`, `Garita`, `Av. Lago`)
- **THEN** el sistema invoca el método RPC `fundetaxcol.turno.get_all` con el ID de la sesión de bahía y puebla la lista de turnos en espera y en atención con las placas y conductores reales.

#### Scenario: Recepción de eventos en tiempo real vía WebSocket
- **WHEN** el servidor Node.js emite un evento `turn` o `dispatch` a través del puerto 3000
- **THEN** el sistema actualiza inmediatamente la lista de turnos sin requerir recargar la pantalla manualmente.

### Requirement: Selección Dinámica de Sesión de Bahía
The system MUST list open bay sessions for the current date (`fundetaxcol_sesion_bahia`) and SHALL allow operators to switch between them.

#### Scenario: Conmutación de bahía activa
- **WHEN** el operador selecciona una bahía diferente desde el AppBar o el diálogo de selección
- **THEN** el sistema actualiza `bahiaIdActual` y descarga inmediatamente la cola de turnos correspondiente a dicha bahía.
