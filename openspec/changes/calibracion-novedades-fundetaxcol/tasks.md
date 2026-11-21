# Tasks: Calibración Fina según Informe de Novedades Fundetaxcol

## 1. Utilidades y Modelos de Datos
- [x] 1.1 Implementar función canónica de parseo UTC a Local (`parseOdooUtcDateTime`) en utilidades o directamente en los DTOs.
- [x] 1.2 Actualizar `PagoRecaudoModel.fromJson` en `lib/models/payment_model.dart` con la conversión horaria.
- [x] 1.3 Actualizar `TurnoModel.fromJson` en `lib/models/turno_model.dart` con la conversión horaria.

## 2. Lógica de Despacho y Tarifas
- [x] 2.1 En `lib/ui/views/form/turno_form_view.dart`, preseleccionar prioritariamente "Caribe Plaza".
- [x] 2.2 En `lib/ui/views/form/turno_form_view.dart`, calibrar horario de recargo nocturno a las 19:00 (7:00 p.m.) y valor a $1.100.

## 3. Versionamiento Canónico
- [x] 3.1 Incrementar versión a `v2.1.17+19` en `lib/core/config/app_version.dart`.
- [x] 3.2 Incrementar versión a `2.1.17+19` en `pubspec.yaml`.

## 4. Verificación y Calidad
- [x] 4.1 Ejecutar `flutter analyze` y asegurar 0 issues.
- [x] 4.2 Ejecutar `flutter test` y certificar aprobación de la suite.

## 5. Compilación y Despliegue Físico Multi-Dispositivo
- [ ] 5.1 Compilar APK Release con `flutter build apk --release`.
- [ ] 5.2 Desplegar y verificar en Teléfono Móvil Xiaomi con `deploy_phone.bat`.
- [ ] 5.3 Desplegar y verificar en Tablet Lenovo con `deploy_tablet.bat`.
- [ ] 5.4 Compilar, verificar y lanzar ejecutable Windows con `deploy_windows.bat`.
