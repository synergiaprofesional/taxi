## Why

Actualmente la aplicación (.exe y .apk) muestra la interfaz operativa (`HomeView`) incluso cuando el usuario no se ha autenticado en Odoo, exponiendo una pantalla con turnos vacíos y forzando a abrir diálogos secundarios. Es imperativo que la terminal permanezca completamente bloqueada tras una pantalla de autenticación formal hasta que se establezca una sesión real en Odoo (`fundetaxcol.co`), y que al cerrar sesión o salir del sistema se retorne de inmediato al login.

## What Changes

- **Controlador Gatekeeper de Raíz (`AuthGatekeeper`):** Intercepta la navegación principal en `main.dart`. Si no hay sesión válida activa, bloquea el acceso y muestra la pantalla de inicio de sesión.
- **Pantalla Dedicada de Inicio de Sesión (`LoginView`):** Nueva vista premium responsive para Tablet POS y Desktop con identidad institucional de Fundetaxcol, botones táctiles de acceso rápido por Bahía (`29d`, `garita`, `lago`, `santa_marta`) y formulario de usuario/contraseña.
- **Flujo de Cierre de Sesión Inmediato:** Al seleccionar "Cerrar Sesión", "Cerrar Turno" o "Salir del Sistema", se limpian las credenciales volátiles de memoria y la aplicación regresa instantáneamente a `LoginView`.
- **Auto-login Seguro:** Si existen credenciales recordadas en `LocalStorage`, la app intenta la autenticación automática en segundo plano mostrando un splash sutil; si falla o expira, cae limpiamente en el formulario de login.

## Capabilities

### New Capabilities
- `login-gatekeeper`: Control de acceso y bloqueo reactivo de la interfaz operativa basado en el estado de autenticación de Odoo 11.

### Modified Capabilities
<!-- No requirement changes to existing specs -->

## Impact

- `lib/main.dart`: El widget raíz ahora evalúa `odooService.isAuthenticated`.
- `lib/ui/views/auth/login_view.dart`: Nueva pantalla completa de inicio de sesión táctil/desktop.
- `lib/services/odoo_service.dart`: Limpieza de sesión y notificación reactiva a la UI en `cerrarSesion()`.
- `lib/ui/views/home/home_view.dart`: Acciones de cierre de sesión vinculadas al retorno inmediato al login.
