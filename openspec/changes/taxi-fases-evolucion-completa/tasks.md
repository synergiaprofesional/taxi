## 1. Rebranding, Infraestructura y Dependencias

- [x] 1.1 Actualizar `pubspec.yaml` con dependencias de Firebase (`firebase_core`, `cloud_firestore`, `firebase_auth`, `firebase_messaging`, `firebase_remote_config`), `google_mobile_ads` y bump a versión `3.0.0+1`.
- [x] 1.2 Actualizar `AndroidManifest.xml` (package ID, nombre de app `Taxi`, permisos de ubicación y conectividad).
- [x] 1.3 Actualizar runner de Windows en `windows/runner/main.cpp` y `Runner.rc` para fijar el título y nombre a `Taxi`.
- [x] 1.4 Configurar inicialización de Firebase multiplataforma en `lib/main.dart` con soporte offline habilitado.

## 2. Capa de Modelos y Repositorios Firestore

- [x] 2.1 Crear modelos de datos puros con serialización Firestore en `lib/models/` (`UserModel`, `VehiculoModel`, `ConductorModel`, `BahiaModel`, `TurnoModel`, `TarifaSectorModel`, `RecaudoModel`, `ViajeModel`).
- [x] 2.2 Implementar `FirebaseService` y `FirestoreRepository` para reemplazar los métodos RPC de `OdooService`.
- [x] 2.3 Redactar y validar `firestore.rules` con control estricto de acceso RBAC para las tres capas del Modelo Cebolla.

## 3. Capa 0 — Núcleo Garita, Bahías y Cajas (Tablet y Desktop)

- [x] 3.1 Conectar `TurnoController` a streams en tiempo real de Firestore (`snapshots()`).
- [ ] 3.2 Adaptar `BahiaSelectedView` para layout responsive split-view en tablets y desktop.
- [x] 3.3 Migrar el formulario de enturne y despacho (`TurnoFormView`) hacia transacciones atómicas de Firestore.
- [x] 3.4 Migrar el formulario de recaudos (`PaymentFormView`) a la colección `/recaudos`.
- [ ] 3.5 Verificar el pipeline de impresión térmica ESC/POS multiplataforma (Bluetooth en tablet, Win32 en Windows).

## 4. Capa 1 — Módulo del Conductor (Android Móvil)

- [x] 4.1 Implementar pantalla de inicio del conductor con visualización de turno activo, posición en cola y bahía asignada.
- [ ] 4.2 Integrar notificaciones push y alertas sonoras de llamada cuando el vehículo es despachado a bahía.
- [x] 4.3 Desarrollar vista de billetera y ahorro programado acumulado para el taxista.
- [x] 4.4 Implementar botón de auxilio / pánico vial con geolocalización en tiempo real hacia garita.

## 5. Capa 2 — Módulo del Pasajero / Cliente (Android Móvil)

- [x] 5.1 Implementar flujo de geolocalización de recogida y selección de destino.
- [x] 5.2 Implementar cotizador anticipado de tarifa basado en la matriz de sectores de Firestore.
- [x] 5.3 Implementar pantalla de seguimiento en mapa en vivo con datos del taxi y conductor asignado.
- [x] 5.4 Implementar pantalla de finalización de viaje con valoración y calificación del servicio.

## 6. Motor de Despacho Híbrido (Bahía + Calle)

- [ ] 6.1 Implementar máquina de estados del taxi (`fuera_turno`, `en_cola`, `despachado`, `en_carrera`, `libre_calle`).
- [ ] 6.2 Implementar geofencing de proximidad para sugerencia de enturne virtual al acercarse libre a una bahía.
- [ ] 6.3 Implementar lógica de emparejamiento equitativo entre solicitudes en calle y turnos de bahía.

## 7. Monetización, Google AdMob y Convenios

- [x] 7.1 Integrar SDK `google_mobile_ads` e inicializar banners adaptativos en vistas de pasajero.
- [x] 7.2 Implementar enclavamiento de seguridad vial: bloqueo estricto de anuncios mientras el móvil esté en movimiento.
- [ ] 7.3 Configurar Firebase Remote Config para calibración dinámica de frecuencias y anunciantes locales.

## 8. Compendio TDD, Verificación y Compilación Dual (.apk y .exe)

- [x] 8.1 Escribir suites de pruebas unitarias para modelos y repositorios en `test/` y catalogar en `tests/COMPENDIO_TESTS.md`.
- [ ] 8.2 Ejecutar `flutter test` garantizando 0 fallos.
- [ ] 8.3 Compilar y validar el ejecutable de Windows Desktop (`taxi.exe`).
- [ ] 8.4 Compilar y validar el APK de Android Release (`app-release.apk`).

## 9. Jerarquía Gremial, Flota Dual y Vinculación

- [x] 9.1 Modelar la entidad `/organizaciones` con los 5 niveles jerárquicos y Custom Claims de rol gremial.
- [x] 9.2 Implementar filtro de visibilidad algorítmica: ocultar conductores privados del radar público de pasajeros.
- [x] 9.3 Desarrollar módulo de vinculación de pasajeros por código de convenio corporativo (voucher) y código de conductor referido.

## 10. Motor Tarifario Oficial y Pantalla Espejo

- [ ] 10.1 Implementar Cloud Function para cálculo oficial de tarifas por sector y evaluación de recargos legales en servidor.
- [x] 10.2 Implementar componente de UI "Pantalla Espejo" que garantiza la visualización del mismo desglose tarifario en conductor y pasajero.
- [x] 10.3 Implementar sistema de auditoría y reporte de discrepancia tarifaria con bloqueo preventivo ante cobros arbitrarios.
