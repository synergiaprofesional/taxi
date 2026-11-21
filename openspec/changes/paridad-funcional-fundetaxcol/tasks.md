# Tasks: Paridad Funcional Absoluta con fundetaxcol_flutter

- [x] Tarea 1: Remover `android:taskAffinity=""` en `android/app/src/main/AndroidManifest.xml` para evitar cierre de app en segundo plano.
- [x] Tarea 2: Robustecer `OdooService` con `finally` en `isLoggingIn`, manejo seguro de timeouts y soporte de lectura multi-bahía para pagos y turnos.
- [x] Tarea 3: Modificar `VehiculoModel` y `ConductorModel` para resolver conductores correctamente desde IDs o mapas y asociar conceptos por defecto.
- [x] Tarea 4: Actualizar `TurnoController` implementando el patrón dual (vista local por bahía en reposo, búsqueda global en todas las bahías con texto).
- [x] Tarea 5: Actualizar `PagoListView`, `TurnoListView` y `DespachoListView` para consumir la búsqueda global y mostrar la bahía correspondiente en cada tarjeta.
- [x] Tarea 6: Actualizar `PaymentFormView` para auto-seleccionar conductor real al ingresar placa (solucionar "Conductor Desconocido") y poblar conceptos.
- [x] Tarea 7: Validar compilación con `flutter analyze` y verificar ausencia de regresiones.
- [x] Tarea 8: Documentación dual obligatoria (`Bitacora 25102026.md`, `Bitacora 20261025 HHmmss.md`, `bitacoras.md`) y persistencia en Engram (`mem_save`).
