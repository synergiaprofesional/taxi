# Tareas de Implementación: enturnamiento-despacho-coordinacion

- [x] 1. Refactorizar `lib/models/turno_model.dart` para extraer polimórficamente `bahiaSesionId`, `vehiculo_id` y `conductor_id` desde `Map`, `List` o `int`.
- [x] 2. Modificar `lib/controllers/turno_controller.dart` para implementar resolución de `vehiculo_id` y `conductor_id` a partir de la placa antes de enviar la creación de turno.
- [x] 3. Eliminar el parámetro `anonimo: true` en `pagarYEnturnar` / `enturnarVehiculo`, enviando `anonimo: false`, `state: 'espera'` y `tarifa_id: false`.
- [x] 4. Actualizar `lib/ui/views/form/turno_form_view.dart` para pasar `vehiculoId` y `conductorId` al llamar `turnoController.enturnarVehiculo`.
- [x] 5. Incrementar versión en `pubspec.yaml` a `2.1.13+15`.
- [x] 6. Ejecutar verificación de tipos y sintaxis con `flutter analyze`.
- [x] 7. Compilar APK y Windows Release, y desplegar vía `deploy_all.ps1`.
- [x] 8. Generar Bitácora Dual y persistir en Engram.
