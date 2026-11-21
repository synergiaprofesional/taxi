# Tasks: Implementación de Visibilidad de Versión y Despliegue Físico

## 1. Configuración y Fuente Única de Verdad
- [x] 1.1 Crear `lib/core/config/app_version.dart` con `AppVersion.display` y `AppVersion.ticketFooter`.
- [x] 1.2 Incrementar `version: 2.1.16+18` en `pubspec.yaml` cumpliendo FIX-002 de `ERRORES.md`.

## 2. Integración en Interfaz de Usuario
- [x] 2.1 Añadir chip interactivo de versión en el AppBar de `lib/ui/views/main/bahia_selected_view.dart`.
- [x] 2.2 Exponer versión en `lib/ui/views/auth/login_view.dart`.
- [x] 2.3 Sincronizar versión en `lib/ui/views/settings/settings_view.dart` y `setting_info_extra_view.dart`.

## 3. Trazabilidad en Impresión
- [x] 3.1 Incorporar `AppVersion.ticketFooter` en el pie de página de `lib/services/printer_service.dart`.

## 4. Verificación Estática y Pruebas
- [x] 4.1 Ejecutar `flutter analyze` y asegurar 0 issues.
- [x] 4.2 Ejecutar `flutter test` y certificar aprobación total de la suite (21/21 tests).

## 5. Compilación y Despliegue Físico (Root Scripts)
- [x] 5.1 Compilar APK Release fresca con `flutter build apk --release`.
- [x] 5.2 Desplegar y verificar en Móvil Xiaomi mediante `deploy_phone.bat` (o `scripts/verify_and_deploy_phone.ps1`).
- [x] 5.3 Desplegar y verificar en Tablet Lenovo mediante `deploy_tablet.bat` (o `scripts/verify_and_deploy_tablet.ps1`).
- [x] 5.4 Compilar, verificar y lanzar ejecutable Windows mediante `deploy_windows.bat` (o `scripts/verify_and_deploy_windows.ps1`).
