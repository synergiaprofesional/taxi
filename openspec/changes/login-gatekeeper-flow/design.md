## Context

En Synergia Móvil, la aplicación inicializaba directamente `HomeView`, dejando la autenticación como un diálogo modal opcional. El usuario requiere que tanto en Windows (.exe) como en Android (.apk en la tablet Lenovo), la interfaz operativa no sea accesible bajo ninguna circunstancia si el usuario no ha iniciado sesión, y que al cerrar sesión se retorne obligatoriamente a la pantalla de Login.

## Goals / Non-Goals

**Goals:**
- Bloquear el acceso a `HomeView` hasta que `OdooService.isAuthenticated` sea `true`.
- Proveer una pantalla de inicio de sesión (`LoginView`) adaptada a pantallas táctiles (Tablet POS) y PC de escritorio.
- Facilitar el inicio de sesión rápido para los despachadores de Fundetaxcol (`29d`, `garita`, `lago`, `santa_marta`).
- Redirigir inmediatamente a `LoginView` al invocar `cerrarSesion()` o salir del sistema.

**Non-Goals:**
- Modificar el backend de Odoo o los métodos de autenticación (`/web/session/authenticate`).
- Crear nuevos usuarios o roles en la base de datos de producción `fundetaxcol`.

## Decisions

### 1. Gatekeeper Reactivo en la Raíz vs. Navegación Imperativa
- **Decisión:** Implementar un widget raíz `AuthGatekeeper` en `lib/ui/views/auth/auth_gatekeeper.dart` que envuelve la aplicación y reacciona con `Obx` a `odooService.isAuthenticated`.
- **Alternativa Descartada:** Usar `Get.to()` / `Get.offAll()` dispersos en múltiples botones. Esto suele dejar rutas huérfanas en la pila o permitir volver atrás con el botón retroceso de Android.
- **Razón:** El patrón reactivo garantiza que si `isAuthenticated` pasa a `false` (por expiración de sesión, error 401 o clic en Logout), la vista operativa se desmonta atómicamente y se muestra el Login.

### 2. Auto-login con Estado de Carga Neutro
- **Decisión:** `OdooService` expone `isLoggingIn = false.obs`. Si hay credenciales guardadas y `isLoggingIn` es `true`, el Gatekeeper muestra una pantalla de bienvenida/splash con el logo institucional de Fundetaxcol mientras Odoo valida la sesión. Si falla o no hay credenciales, muestra el formulario de login.

### 3. Interfaz Táctil para Tablet POS M11
- **Decisión:** Diseñar `LoginView` con tarjetas táctiles de selección rápida para las terminales activas de Fundetaxcol (`Bahía 29D`, `Garita`, `Av. Lago`, etc.), permitiendo que el operador toque su bahía, ingrese su PIN/contraseña y entre con un botón amplio de alta visibilidad.

## Risks / Trade-offs

- **[Riesgo] Pérdida de conectividad al intentar auto-login:** Si el dispositivo está sin red al arrancar, el auto-login fallará.
  - *Mitigación:* Se captura el error de red, se muestra un mensaje claro ("Sin conexión a fundetaxcol.co") y se deja la pantalla de login disponible con botón de reintento.
- **[Riesgo] Botón de retroceso de Android en la tablet:**
  - *Mitigación:* El Gatekeeper es el nodo raíz; no hay rutas anteriores en el historial de navegación para retroceder una vez cerrada la sesión.
