# OpenSpec: View Settings & Config (Ajustes y Configuración del Sistema)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con los módulos de ajustes y diagnóstico de `fundetaxcol_flutter`, integrando:
- **Vista de Ajustes**: `lib/ui/views/settings_view.dart` (`SettingsView` y `SettingsViewWidget`)
- **Vista de Diagnóstico Técnico**: `lib/ui/views/settings_view.dart#L150` (`SettingInfoExtra`)
- **Controladores**:
  - `SettingsController` (`lib/controllers/global/settings.controller.dart`)
  - `PreferencesController` (`lib/controllers/global/preferences.controller.dart`)
- **Componentes**: `CupertinoFormSection`, `CupertinoFormRow`, `CupertinoTextField`, `CupertinoSwitch`, `LogoutWidget`
- **Almacenamiento Local**: `SettingsStorage` (`lib/storage/settings.storage.dart`)

---

## Componentes UI y Layout

### 1. `SettingsView` (Pantalla de Ajustes Operativos)
- **AppBar**:
  - Título centrado "Ajustes".
  - Acción en la derecha: `LogoutWidget` (`lib/ui/widgets/root/logout_widget.dart`), permitiendo cerrar sesión voluntariamente con diálogo de confirmación.
- **Sección 1: General (`CupertinoFormSection`)**:
  - Encabezado: `"General"` (tamaño 20 negrita).
  - Fila 1: `SearchGenericWidget` con `ConceptSearchController` para seleccionar el **Concepto de ingreso por defecto**.
  - Fila 2: `CupertinoTextField` de solo lectura mostrando el **Conductor de apoyo** configurado en Odoo para turnos anónimos.
- **Sección 2: Impresión (`CupertinoFormSection`)**:
  - Encabezado: `"Impresión"` (tamaño 20 negrita).
  - Fila 1: `CupertinoTextField` para ingresar o editar la **Dirección MAC de la impresora Bluetooth** (ej. `66:32:00:1A:4C:E8`), enlazada en Windows con el Spooler `TIQUETES` en `USB001`.
  - Fila 2: Fila con etiqueta `"Imprimir pagos y despachos automáticamente"` y switch interactivo `CupertinoSwitch(value: autoPrint, activeColor: Vx.blue400)`.
- **Botón Secundario**: `CupertinoButton` con texto `"Información adicional"`, navegando a `SettingInfoExtra`.
- **Botón Flotante Guardar (`Icons.save`)**: Persiste los valores modificados en `SettingsStorage` mediante `_.onSave()`.

### 2. `SettingInfoExtra` (Auditoría Técnica y Parámetros del Servidor)
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

### Requirement: Configuración de Parámetros Operativos en SettingsView
El sistema DEBE proveer en `SettingsView` una interfaz para la gestión del hardware de impresión, conceptos predeterminados y conductor genérico de apoyo.

#### Scenario: Configuración de dirección física MAC de impresora
- **WHEN** el operador ingresa la dirección MAC Bluetooth en el campo correspondiente y pulsa Guardar
- **THEN** el sistema DEBE almacenar el valor en `SettingsStorage` y utilizarlo para vincular la impresora térmica en cada intento de impresión.

#### Scenario: Activación de auto-impresión de tiquetes y recibos
- **WHEN** el operador activa el switch `Imprimir pagos y despachos automáticamente`
- **THEN** el sistema DEBE asignar `settings.autoPrint = true` de forma persistente, haciendo que cada cobro o salida confirmada imprima físicamente sin requerir un tap adicional.

#### Scenario: Modificación del concepto contable por defecto
- **WHEN** el operador busca y selecciona un nuevo concepto contable en la sección General
- **THEN** el sistema DEBE actualizar `settings.concept`, precargándolo en futuros pagos donde el conductor no tenga conceptos específicos asignados.

---

### Requirement: Panel de Auditoría y Diagnóstico en SettingInfoExtra
El sistema DEBE proveer en `SettingInfoExtra` una pantalla de solo lectura con los datos de conexión al servidor de Odoo 11 y la información del usuario autenticado.

#### Scenario: Consulta de parámetros del servidor
- **WHEN** el operador o administrador pulsa el botón "Información adicional"
- **THEN** el sistema DEBE mostrar el host (`fundetaxcol.co`), puerto (`80`), base de datos (`fundetaxcol`), puerto de sockets (`3000`), usuario logueado y versión de la aplicación.
