# Especificación Técnica de Vista: SettingInfoExtra

## 1. Identificación y Ubicación
- **Archivo en fundetaxcol_flutter**: `lib/ui/views/settings_view.dart#L150`
- **Controlador Principal**: `PreferencesController` (`lib/controllers/global/preferences.controller.dart`)

---

## 2. Propósito y Flujo Operativo
`SettingInfoExtra` es una pantalla de diagnóstico técnico y auditoría para que los operadores o administradores de infraestructura puedan verificar de inmediato los parámetros de conexión al backend de Odoo y la identidad de la sesión activa en el dispositivo móvil.

---

## 3. Campos y Métricas Visualizadas (Solo Lectura)
1. **Conexión al Servidor**:
   - **Host / Servidor**: `fundetaxcol.co`
   - **Puerto**: `80` (HTTP / JSON-RPC)
   - **Base de Datos**: `fundetaxcol`
   - **Puerto WebSocket**: `3000` (`server_rt_odoo`)
2. **Identidad del Usuario**:
   - **Nombre de Usuario**: Nombre completo del despachador o cajero logueado.
   - **Correo Electrónico**: Email del usuario de Odoo.
3. **Versión de la Aplicación**:
   - Número de versión oficial y código de compilación (ej. `v1.0.8+15`).
