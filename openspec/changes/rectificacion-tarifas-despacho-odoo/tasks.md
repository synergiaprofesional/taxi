# Tasks: Rectificación Canónica de Tarifas de Despacho, Sincronización de Bahías y Pagar y Enturnar

## 1. Modelado de Datos
- [x] 1.1 Crear el DTO `TarifaSectorModel` en `lib/models/tarifa_sector_model.dart` con soporte de deserialización de `fundetaxcol.tarifa.sector`.

## 2. Capa de Servicios Odoo
- [x] 2.1 Agregar el método `getTarifasSector()` en `lib/services/odoo_service.dart`.
- [x] 2.2 Agregar el método `setBahiaActiva(int bahiaId)` en `lib/services/odoo_service.dart`.

## 3. Capa de Controladores (TurnoController)
- [x] 3.1 Incorporar la lista reactiva `tarifasDisponibles` y el método `cargarTarifasDesdeServidor()` en `lib/controllers/turno_controller.dart`.
- [x] 3.2 Invocar `odooService.setBahiaActiva(bahia.id)` dentro de `cambiarBahia(...)`.
- [x] 3.3 Asegurar que `despacharTurno(...)` transmita `tarifa_id` a `fundetaxcol.turno` en Odoo.
- [x] 3.4 Actualizar `pagarYEnturnar(...)` para crear el pago formal en `fundetaxcol.pago` garantizando trazabilidad contable.

## 4. Interfaz de Usuario (TurnoFormView & Vistas)
- [x] 4.1 Reemplazar el Dropdown hardcodeado en `lib/ui/views/form/turno_form_view.dart` por la lista de tarifas oficiales de Odoo con selección de `TarifaSectorModel`.
- [x] 4.2 Enlazar el total dinámicamente con la tarifa seleccionada y su recargo nocturno.
- [x] 4.3 Pasar `tarifaId: _tarifaSeleccionada?.id` en `_ejecutarDespacho()`.

## 5. Verificación, Versionamiento y Despliegue
- [x] 5.1 Incrementar versión a `v2.1.15+17` en `pubspec.yaml` cumpliendo FIX-002 de `ERRORES.md`.
- [x] 5.2 Ejecutar `flutter analyze` y asegurar 0 issues.
- [x] 5.3 Ejecutar `flutter test` y certificar aprobación total de tests.

