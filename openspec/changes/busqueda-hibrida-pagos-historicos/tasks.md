# Tareas de Implementación: Búsqueda Híbrida y Deserialización de Pagos

- [x] Task 1: Refactorizar `PagoRecaudoModel.fromJson` en `lib/models/payment_model.dart` para soportar `Map`, `List` y primitivos de forma polimórfica sin excepciones de tipado.
- [x] Task 2: Actualizar `TurnoController.cargarPagosDesdeServidor()` asegurando mapeo de `bahiaSesionId` y métricas de recaudos.
- [x] Task 3: Implementar método `buscarPagosHistoricosRemotos(String query)` en `TurnoController` con fallback inteligente cuando no haya coincidencias locales.
- [x] Task 4: Conectar `PagoListView` con la búsqueda híbrida y soporte para pull-to-refresh.
- [x] Task 5: Validar estáticamente con `flutter analyze` (0 errores).
- [x] Task 6: Incrementar versión en `pubspec.yaml` a `2.1.12+14` cumpliendo FIX-002 de `ERRORES.md`.
- [x] Task 7: Compilar Release APK y desplegar en teléfono móvil (`deploy_phone.bat`) y tablet (`deploy_tablet.bat`).
- [x] Task 8: Validar con `dumpsys package`, documentar en Bitácora Dual y persistir en Engram.
