## ADDED Requirements

### Requirement: Control de Acceso Raíz por Gatekeeper
El sistema DEBE evaluar de forma reactiva el estado de autenticación en Odoo y bloquear completamente la interfaz operativa (`HomeView`) si no existe una sesión válida autenticada.

#### Scenario: Inicio en frío sin sesión autenticada
- **WHEN** la aplicación inicia en Windows o Android y no hay credenciales válidas
- **THEN** el sistema DEBE mostrar la pantalla `LoginView` e impedir la visualización del panel operativo o de turnos.

#### Scenario: Autenticación exitosa desbloquea el panel operativo
- **WHEN** el usuario ingresa credenciales válidas de Odoo o el auto-login tiene éxito
- **THEN** el Gatekeeper DEBE transicionar automáticamente hacia `HomeView` e iniciar la descarga de turnos y eventos de Socket.IO.

### Requirement: Pantalla Dedicada de Inicio de Sesión
El sistema DEBE proveer una vista dedicada `LoginView` con branding de Fundetaxcol, soporte táctil para tabletas POS y soporte de teclado para escritorio.

#### Scenario: Selección rápida de Bahía de despacho
- **WHEN** el operador pulsa uno de los botones de bahía preconfigurada (`Bahía 29D`, `Garita`, `Av. Lago`, etc.)
- **THEN** el sistema DEBE autocompletar el identificador del usuario de la bahía seleccionada.

#### Scenario: Intento de inicio de sesión fallido
- **WHEN** el usuario ingresa una contraseña incorrecta en `fundetaxcol.co`
- **THEN** el sistema DEBE mostrar un mensaje descriptivo de error y permanecer en `LoginView` sin abrir la interfaz operativa.

### Requirement: Retorno Inmediato a Login al Cerrar Sesión
El sistema DEBE destruir la sesión de memoria y retornar de inmediato a la pantalla de login cuando el usuario decida salir o cerrar sesión.

#### Scenario: Cierre voluntario de sesión o turno
- **WHEN** el usuario presiona "Cerrar Sesión", "Cerrar Turno" o "Salir del Sistema"
- **THEN** el sistema DEBE limpiar las credenciales volátiles en memoria, desconectar eventos y redirigir atómicamente a `LoginView`.
