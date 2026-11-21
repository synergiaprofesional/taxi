# OpenSpec: View Settings (Ajustes Operativos y de Hardware)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/settings_view.dart` (`SettingsView` y `SettingsViewWidget`)
- **Controlador**: `SettingsController` (`lib/controllers/global/settings.controller.dart`)
- **Componentes**: `CupertinoFormSection`, `CupertinoSwitch`, `LogoutWidget`
- **Referencia Técnica**: `docs/especificaciones_vistas/13_settings_view.md`

---

## Componentes UI y Layout
- **AppBar**: Título centrado "Ajustes", botón `LogoutWidget` a la derecha.
- **Sección General**:
  - `SearchGenericWidget` para Concepto de ingreso por defecto (`settings.concept`).
  - Campo de solo lectura para Conductor de apoyo (`settings.driver`).
- **Sección Impresión**:
  - Campo para MAC Impresora Bluetooth (enlazada con Spooler Win32 `TIQUETES` en `USB001` en Windows).
  - Switch `CupertinoSwitch` para `"Imprimir pagos y despachos automáticamente"`.
- **Botón "Información adicional"**: Abre `SettingInfoExtra`.
- **Botón Flotante Guardar (`Icons.save`)**.

---

## Requirements

### Requirement: Configuración de Parámetros Operativos en SettingsView
El sistema DEBE proveer en `SettingsView` una interfaz para la gestión del hardware de impresión, conceptos predeterminados y conductor genérico de apoyo.

#### Scenario: Configuración de hardware de impresión
- **WHEN** el usuario ingresa la dirección MAC de la impresora Bluetooth y activa el interruptor de auto-impresión
- **THEN** el sistema DEBE persistir dichos valores en `SettingsStorage` y utilizarlos en cada despacho y cobro registrado.

#### Scenario: Asignación de concepto contable por defecto
- **WHEN** el operador selecciona un concepto contable en el buscador de la sección General
- **THEN** el sistema DEBE guardarlo como concepto por defecto para autocompletar pagos a conductores que no posean conceptos asignados.
