# Proposal: Visibilidad Canónica de Versión y Trazabilidad en Synergia Móvil

## 1. Contexto y Problema
En entornos operativos de transporte de pasajeros en campo (bahías de Garita, 29D, Av. Lago, etc.), los operadores manejan terminales móviles (Xiaomi), tablets fijas (Lenovo) y estaciones Windows de escritorio. Frecuentemente conviven compilaciones previas o aplicaciones heredadas de 2025. 
Hasta la versión `v2.1.15+17`, la versión del software estaba confinada a `pubspec.yaml` y al interior de los menús de diagnóstico, sin presencia visual en la pantalla principal de trabajo, ni en la pantalla de acceso, ni en los tiquetes térmicos emitidos a los taxistas. Esto generaba incertidumbre para el operador y para el equipo de soporte sobre qué revisión exacta del código estaba operando en cada terminal.

## 2. Solución Propuesta
Establecer una Fuente Única de la Verdad (SSOT) para el versionamiento de Synergia Móvil:
1. Crear la clase canónica `AppVersion` en `lib/core/config/app_version.dart`.
2. Exponer una píldora visual e interactiva en el AppBar de `BahiaSelectedView` mostrando `v2.1.16+18` con acceso táctil directo a la pantalla de diagnóstico técnico (`SettingInfoExtraView`).
3. Exhibir la versión en la pantalla de autenticación `LoginView`.
4. Integrar la versión en el pie de página de `SettingsView` y sincronizarla en `SettingInfoExtraView`.
5. Estampar la versión en el pie de los tiquetes físicos generados por `PrinterService`.
6. Incrementar la versión canónica a `v2.1.16+18` cumpliendo FIX-002 de `ERRORES.md`.
7. Ejecutar el ciclo completo de despliegue físico verificado en el teléfono móvil, la tablet y el ejecutable Windows.

## 3. Criterios de Aceptación
- `AppVersion` centraliza de manera síncrona y tipada `versionName`, `versionCode`, `display` y `ticketFooter`.
- La pantalla principal `BahiaSelectedView` muestra la versión visible en el AppBar sin comprometer el espacio en pantallas pequeñas.
- `flutter analyze` reporta 0 issues y `flutter test` aprueba el 100% de la suite.
- APK release compilado y desplegado exitosamente con `deploy_phone.bat` y `deploy_tablet.bat`.
- Binario nativo Windows compilado, verificado con timestamp reciente y lanzado con `deploy_windows.bat`.

