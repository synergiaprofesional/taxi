# Spec: Requerimientos de Visibilidad de Versión

## REQ-001: Centralización Canónica de Versión
* El sistema DEBE exponer en `lib/core/config/app_version.dart` las propiedades estáticas `versionName`, `versionCode`, `display` y `ticketFooter`.
* El valor de `versionName` y `versionCode` DEBE corresponder exactamente con `version` en `pubspec.yaml` (`2.1.16+18`).

## REQ-002: Indicador Visible en Pantalla Principal
* `BahiaSelectedView` DEBE renderizar en su AppBar un badge con el texto formateado de `AppVersion.display`.
* El badge DEBE ser interactivo; al pulsarlo, el sistema DEBE abrir la vista `SettingInfoExtraView`.

## REQ-003: Identificación en Pantalla de Acceso
* `LoginView` DEBE mostrar la versión visible en el encabezado o pie de la pantalla para confirmar la versión antes de iniciar sesión.

## REQ-004: Trazabilidad en Tiquetes Físicos
* Toda impresión térmica generada por `PrinterService` DEBE incluir al pie del recibo la cadena `AppVersion.ticketFooter`.

