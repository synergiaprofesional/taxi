## Context

Actualmente en `c:\Workspaces\synergia_movil`, `TurnoController` carga una lista fija de turnos hardcodeados (`cargarTurnosSimulados()`) debido a que la app arranca sin autenticarse contra Odoo 11, y `NetworkConfig` intentaba comunicarse por defecto a través de HTTPS (puerto 443), el cual se encuentra aún en proceso de despliegue antes de las 22:00 COT. Como resultado, las llamadas RPC no se ejecutaban y la UI mostraba datos ficticios desconectados de la base de datos `fundetaxcol` de `fundetaxcol.co`.

## Goals / Non-Goals

**Goals:**
- Autenticar formalmente al operador contra `/web/session/authenticate` en Odoo 11 (`fundetaxcol.co:80`).
- Guardar de forma persistente y segura las credenciales y la cookie de sesión (`session_id`) en `LocalStorage`.
- Configurar dinámicamente `NetworkConfig` para utilizar HTTP directo (puerto 80) y Socket.IO (puerto 3000) con fallback automático.
- Eliminar de raíz y permanentemente `cargarTurnosSimulados()`.
- Consultar las sesiones de bahía activas (`fundetaxcol_sesion_bahia`) de la jornada y permitir conmutar entre `29D`, `Garita` y `Av. Lago`.
- Obtener los turnos reales de la bahía seleccionada invocando `fundetaxcol.turno.get_all` y escuchar los eventos de Socket.IO (`turn`, `dispatch`, `session`, `payment`).

**Non-Goals:**
- No alterar el esquema de base de datos de PostgreSQL en producción ni modificar los módulos backend de Odoo.
- No depender de configuraciones externas ajenas a `fundetaxcol.co`.

## Decisions

### 1. Detección Inteligente de Transporte (HTTP vs HTTPS)
- **Decisión:** `NetworkConfig` intentará por defecto HTTP directo en puerto 80 (y socket en puerto 3000) si HTTPS (443) rechaza la conexión, permitiendo transición transparente una vez Caddy active los certificados SSL.
- **Alternativas:** Forzar HTTPS causaba un fallo de `Connection reset` bloqueando la comunicación.

### 2. Flujo de Autenticación con Diálogo Reactivo y Auto-Login
- **Decisión:** Al iniciar, si existen credenciales válidas en `LocalStorage`, la app ejecuta un auto-login en segundo plano. Si no existen o fallan, muestra inmediatamente un `LoginDialog` con selector rápido de usuarios de bahía (`29d@fundetaxcol.co`, `garita@fundetaxcol.co`, etc.).
- **Alternativas:** Dejar credenciales quemadas en el código (inseguro e inflexible para diferentes operadores).

### 3. Sincronización en Tiempo Real vía Socket.IO y Polling de Respaldo
- **Decisión:** Escuchar en `SocketService` los eventos nativos de `server_rt_odoo`: `turn`, `dispatch`, `session`, `payment`. Si el socket se desconecta temporalmente, un temporizador ligero consulta `fundetaxcol.turno.to_update` para sincronización sin saturar el ancho de banda.
- **Alternativas:** Polling agresivo cada segundo (satura la CPU del servidor).

## Risks / Trade-offs

- [Desconexión de Socket.IO por inestabilidad de red 3G/4G] → Mitigación: Mecanismo de reconexión exponencial y respaldo con `to_update`.
- [Sesión expirada en Odoo] → Mitigación: Detección de código de error de sesión en `OdooService` con re-autenticación automática silenciosa si hay credenciales guardadas.
- [Múltiples bahías asignadas a un mismo operador] → Mitigación: Selector visual reactivo de bahías en el AppBar con actualización instantánea de la lista de turnos.
