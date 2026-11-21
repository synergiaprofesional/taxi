# OpenSpec: View Setting Info Extra (Auditoría Técnica y Parámetros del Servidor)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/settings_view.dart#L150` (`SettingInfoExtra`)
- **Controlador**: `PreferencesController` (`lib/controllers/global/preferences.controller.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/14_setting_info_extra_view.md`

---

## Componentes UI y Layout
- **AppBar**: Título `"Información adicional"`.
- **Lista de Parámetros en Solo Lectura**:
  - **Servidor / Host**: `fundetaxcol.co`
  - **Puerto HTTP / JSON-RPC**: `80`
  - **Base de Datos Odoo**: `fundetaxcol`
  - **Puerto WebSocket**: `3000` (`server_rt_odoo`)
  - **Usuario Operador**: Nombre completo del despachador autenticado.
  - **Correo Electrónico**: Email del usuario en Odoo.
  - **Versión de la App**: Versión y código de compilación (ej. `v1.0.8+15`).

---

## Requirements

### Requirement: Panel de Auditoría y Diagnóstico en SettingInfoExtra
El sistema DEBE proveer en `SettingInfoExtra` una pantalla de solo lectura con los datos de conexión al servidor de Odoo 11 y la información del usuario autenticado.

#### Scenario: Consulta de parámetros del servidor
- **WHEN** el operador o administrador pulsa el botón "Información adicional"
- **THEN** el sistema DEBE mostrar el host (`fundetaxcol.co`), puerto (`80`), base de datos (`fundetaxcol`), puerto de sockets (`3000`), usuario logueado y versión de la aplicación.
