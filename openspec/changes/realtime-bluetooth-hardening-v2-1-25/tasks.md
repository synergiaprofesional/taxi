# Tasks: Real-Time Sync & Bluetooth SPP Hardening (v2.1.25+27)

## 1. Versionamiento y Blast Radius
- [x] 1.1 Ejecutar análisis de blast radius con Graphify (`scripts/query_graphify.py`).
- [x] 1.2 Actualizar versión en `pubspec.yaml` a `2.1.25+27`.
- [x] 1.3 Actualizar versión en `lib/core/config/app_version.dart` a `versionName = '2.1.25'`, `versionCode = 27`.
- [x] 1.4 Archivar cambio OpenSpec anterior en `openspec/changes/archive/solucion-novedades-fundetaxcol/`.

## 2. Frente 1: Real-Time & Health Check Visual
- [ ] 2.1 En `lib/services/socket_service.dart`, implementar `eventSequence` observable y método `reconnect()`.
- [ ] 2.2 En `lib/controllers/turno_controller.dart`, vincular listeners con debounce (400ms) escuchando `eventSequence`.
- [ ] 2.3 En `lib/ui/views/main/bahia_selected_view.dart`, implementar indicador visual en `AppBar` respetando la regla temprana de GetX.

## 3. Frente 2: Impresión Bluetooth SPP Nativa en Android
- [ ] 3.1 En `android/app/src/main/kotlin/com/synergia/synergia_movil/MainActivity.kt`, implementar canal `com.synergia.synergia_movil/bluetooth_printer` con RFCOMM en hilo de fondo y timeout de 3.5s.
- [ ] 3.2 En `lib/services/printer_service.dart`, conectar la rama `TipoImpresora.bluetooth` al canal nativo con timeout y fallback controlado.

## 4. Gates de Verificación y Calidad
- [ ] 4.1 Ejecutar `flutter analyze` y asegurar 0 issues.
- [ ] 4.2 Ejecutar tests unitarios puntuales (`flutter test test/services_test.dart test/fundetaxcol_parity_views_test.dart`).

## 5. Compilación y Despliegue Físico
- [ ] 5.1 Desplegar en Windows con `scripts/deploy_windows.bat` y verificar timestamp del `.exe`.
- [ ] 5.2 Desplegar en Teléfono Móvil Xiaomi con `scripts/deploy_phone.bat` y verificar `adb dumpsys package`.

## 6. Documentación Dual y Memoria
- [ ] 6.1 Actualizar `contexto_tecnico_synergia_movil.md`.
- [ ] 6.2 Generar Bitácora Diaria (`Bitacoras/Bitacora 07112026.md`).
- [ ] 6.3 Generar Bitácora Atómica de Sesión (`Bitacoras/Bitacora YYYYMMDD HHmmss.md`).
- [ ] 6.4 Actualizar índice maestro `Bitacoras/bitacoras.md`.
- [ ] 6.5 Persistir en Engram vía `mem_save`.

