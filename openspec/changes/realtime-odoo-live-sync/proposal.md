## Why

La aplicación actualmente muestra turnos y bahías simuladas (`cargarTurnosSimulados()`) debido a la ausencia de un flujo de autenticación formal con Odoo 11 y a que las peticiones se dirigían a HTTPS (puerto 443) antes de su activación en el servidor. Es mandatorio reemplazar por completo los datos ficticios conectando la app en tiempo real a la base de datos `fundetaxcol` en `fundetaxcol.co:80` y al WebSocket de Node.js en el puerto 3000 para sincronizar las bahías activas (`29D`, `Garita`, `Av. Lago`) y los turnos reales de los operadores.

## What Changes

- **Eliminación Total de Mock Data**: Remoción definitiva del método `cargarTurnosSimulados()` en `TurnoController`.
- **Autenticación Formal Odoo 11**: Integración de diálogo y controlador de inicio de sesión contra `/web/session/authenticate`, con persistencia segura de credenciales y cookie de sesión en almacenamiento local.
- **Detección y Configuración de Red**: Ajuste de `NetworkConfig` para operar por HTTP (puerto 80) y Socket.IO (puerto 3000) mientras se completa la migración a Caddy SSL, con fallback transparente.
- **Sincronización en Vivo de Bahías**: Consulta dinámica de sesiones de bahía activas (`fundetaxcol.sesion.bahia`) correspondientes al operador autenticado.
- **Gestión Reactiva de Turnos Reales**: Consumo de llamadas RPC `get_all` y escucha de eventos Socket.IO (`turn`, `dispatch`, `session`, `payment`) para refrescar la cola de turnos en vivo.

## Capabilities

### New Capabilities
- `odoo-auth-session`: Gestión de credenciales, autenticación en Odoo 11 `/web/session/authenticate` y persistencia de sesión de operador.
- `realtime-turnos-sync`: Extracción de turnos reales de PostgreSQL y sincronización bidireccional vía WebSocket (`server_rt_odoo`) en puerto 3000.

### Modified Capabilities
<!-- No existing formal specs in openspec/specs/ to modify -->

## Impact

- **Modelos y Servicios**: `OdooService`, `NetworkConfig`, `SocketService`, `TurnoController`.
- **UI / Vistas**: Integración de `LoginDialog` y actualización reactiva de `HomeView` y `BahiaSelectorDialog`.
- **Binarios**: Recompilación de ejecutables release para Windows (`synergia_movil.exe`) y Android (`app-release.apk`) libres de datos simulados.
