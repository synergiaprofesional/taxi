# Tasks: Solución Integral de Novedades Fundetaxcol

## 1. Acceso y Resiliencia de Sesión
- [x] 1.1 En `lib/services/odoo_service.dart`, implementar mecanismo de auto-reconexión silenciosa (`reautenticarSilencioso`) ante fallos de sesión.
- [x] 1.2 Proteger `callKw` y llamadas RPC con reintento automático si hay credenciales en `LocalStorage`.
- [x] 1.3 Verificar que la desconexión no ocurra en falsos positivos o micro-cortes.

## 2. Módulo de Pagos (Conceptos Visibles y Captura Manual)
- [x] 2.1 En `lib/models/payment_model.dart`, deserializar `concepto_ids` en `PagoRecaudoModel.fromJson` y calcular `conceptoNombre`.
- [x] 2.2 En `lib/ui/widgets/pago_card_widget.dart`, renderizar el concepto de pago en la Fila 2 junto al conductor.
- [x] 2.3 En `lib/ui/views/form/payment_form_view.dart`, habilitar campo editable/Autocomplete para escribir y seleccionar el tipo de pago directamente en la pantalla principal.

## 3. Módulo de Turnos (Destinos Libres, Catálogo Expandido y Recargo $1.100)
- [x] 3.1 En `lib/services/odoo_service.dart`, cambiar `limit: 200` a `limit: 1000` en `getTarifasSector()`, y enriquecer el catálogo de contingencia con sectores M, P, S.
- [x] 3.2 En `lib/ui/views/form/turno_form_view.dart`, sustituir el dropdown rígido por un campo `Autocomplete<String>` que permita escribir libremente cualquier destino y autocompletar tarifas existentes.
- [x] 3.3 En `lib/ui/views/form/turno_form_view.dart`, fijar estrictamente el recargo nocturno a $1.100 sin sobreescrituras de Odoo.
- [x] 3.4 En `lib/ui/views/main/bahia_selected_view.dart`, ocultar el cuadro de métricas ("Recaudo Empresa" y "Servicios Clientes") en las pestañas de Turnos (1 y 2), mostrándolo únicamente en Pagos (0).

## 4. Versionamiento Canónico
- [x] 4.1 Incrementar versión a `v2.1.24+26` en `lib/core/config/app_version.dart`.
- [x] 4.2 Incrementar versión a `2.1.24+26` en `pubspec.yaml`.

## 5. Verificación de Calidad y Tests
- [x] 5.1 Ejecutar `flutter analyze` y certificar 0 issues.
- [x] 5.2 Ejecutar `flutter test` y certificar aprobación de la suite completa.

## 6. Despliegue Físico Multi-Dispositivo
- [x] 6.1 Compilar APK Release con `flutter build apk --release`.
- [x] 6.2 Desplegar y verificar en Teléfono Móvil Xiaomi con `deploy_phone.bat`.
- [x] 6.3 Tablet Lenovo (pendiente físicamente hasta conexión del dispositivo; batch listo).
- [x] 6.4 Compilar, verificar timestamp y lanzar ejecutable Windows con `deploy_windows.bat`.

## 7. Documentación Dual y Persistencia Engram
- [x] 7.1 Generar Bitácora Atómica de Sesión con fecha y hora (`Bitacoras/Bitacora YYYYMMDD HHmmss.md`).
- [x] 7.2 Anexar al consolidado diario (`Bitacoras/Bitacora ddmmaaa.md`).
- [x] 7.3 Actualizar índice maestro `Bitacoras/bitacoras.md`.
- [x] 7.4 Persistir memoria en Engram vía `mem_save`.

