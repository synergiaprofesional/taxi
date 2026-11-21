## ADDED Requirements

### Requirement: Autenticación de Operador en Odoo 11
The system SHALL authenticate operators against Odoo 11 endpoint `/web/session/authenticate` using database `fundetaxcol`, login, and password.

#### Scenario: Autenticación exitosa
- **WHEN** el operador ingresa credenciales válidas y presiona "Iniciar Sesión"
- **THEN** el sistema envía la petición JSON-RPC a Odoo 11, almacena la cookie de sesión en memoria y `LocalStorage`, marca `isAuthenticated = true` y cierra el diálogo de autenticación.

#### Scenario: Fallo de autenticación
- **WHEN** el operador ingresa credenciales inválidas o la contraseña es errónea
- **THEN** el sistema muestra un mensaje de error claro en pantalla sin bloquear la aplicación y permite reintentar el ingreso.

### Requirement: Persistencia de Sesión y Auto-Login
The system SHALL persist operator credentials and session state in local storage to support automatic login on application launch.

#### Scenario: Auto-login al iniciar la aplicación
- **WHEN** la aplicación inicia y encuentra credenciales guardadas en `LocalStorage`
- **THEN** el sistema intenta autenticarse automáticamente en segundo plano sin desplegar el diálogo modal a menos que la autenticación falle.

#### Scenario: Cierre de sesión manual
- **WHEN** el operador selecciona la opción "Cerrar Sesión" en Ajustes o en el menú de usuario
- **THEN** el sistema borra la cookie activa y los tokens almacenados, establece `isAuthenticated = false` y despliega la pantalla de autenticación.
