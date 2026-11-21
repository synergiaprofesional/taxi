# Especificación Técnica de Vista: SettingsView

## 1. Identificación y Ubicación
- **Archivo en fundetaxcol_flutter**: `lib/ui/views/settings_view.dart`
- **Controlador Principal**: `SettingsController` (`lib/controllers/global/settings.controller.dart`)
- **Almacenamiento Local**: `SettingsStorage` (`lib/storage/settings.storage.dart`)
- **Botón de Cierre de Sesión**: `LogoutWidget` (`lib/ui/widgets/root/logout_widget.dart`)

---

## 2. Propósito y Flujo Operativo
`SettingsView` permite al operador y personal técnico configurar las opciones operativas y de hardware de la aplicación móvil en la tableta o terminal POS: concepto contable de ingreso por defecto, conductor genérico de apoyo para modo anónimo, dirección física MAC de la impresora térmica Bluetooth, interruptor de auto-impresión de despachos y recibos, y acceso a la pantalla de diagnóstico adicional.

---

## 3. Secciones del Formulario
1. **Sección General (`CupertinoFormSection`)**:
   - **Concepto por Defecto**: `SearchGenericWidget` sobre `fundetaxcol.concepto`. Determina cuál concepto se precarga automáticamente en el formulario de pagos si el conductor no tiene conceptos específicos asignados.
   - **Conductor de Apoyo**: Muestra en solo lectura el conductor genérico asignado en el sistema para enturnar vehículos foráneos en modo anónimo.
2. **Sección Impresión**:
   - **MAC Impresora Bluetooth**: Campo de texto para la dirección MAC de la impresora térmica portátil (ej. `66:32:00:1A:4C:E8`). En Windows se enlaza además con la cola del spooler de impresión local.
   - **Auto-Impresión (`CupertinoSwitch`)**: Switch booleano `Imprimir pagos y despachos automáticamente`. Si está en `true`, al guardar un pago o confirmar un despacho se dispara la impresión física sin requerir pulsar el botón de imprimir.
3. **Acciones**:
   - **Botón "Información adicional"**: Abre `SettingInfoExtra`.
   - **Botón Flotante Guardar (`Icons.save`)**: Persiste los ajustes en `SettingsStorage` y actualiza la sesión.
   - **LogoutWidget en AppBar**: Cierra la sesión activa y retorna a `LoginWidget`.
