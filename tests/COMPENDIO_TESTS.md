# 🧪 Compendio TDD y Catálogo de Pruebas - Proyecto Taxi

Este compendio cataloga todas las suites de prueba unitarias, de integración y de widgets bajo el estándar TDD del proyecto `Taxi`.

---

## 📋 Catálogo de Pruebas Unitarias y de Widgets

| Suite / Archivo | Dominio | Propósito Técnico | Comando de Ejecución |
| :--- | :--- | :--- | :--- |
| [`test/models/categoria_oferta_test.dart`](file:///c:/Workspaces/taxi/test/models/categoria_oferta_test.dart) | Categorías y Ofertas | Valida `CategoriaViaje`, modelo de contraoferta `ConductorOfertaModel` y tarifas propuestas | `flutter test test/models/categoria_oferta_test.dart` |
| [`test/models/user_model_test.dart`](file:///c:/Workspaces/taxi/test/models/user_model_test.dart) | Usuarios y Roles | Valida serialización de `UserModel`, custom claims, roles gremiales y conductor privado | `flutter test test/models/user_model_test.dart` |
| [`test/models/viaje_model_test.dart`](file:///c:/Workspaces/taxi/test/models/viaje_model_test.dart) | Viajes y Pantalla Espejo | Valida ciclo de vida de `ViajeModel`, estados y desglose transparente de tarifas | `flutter test test/models/viaje_model_test.dart` |
| [`test/models/organizacion_model_test.dart`](file:///c:/Workspaces/taxi/test/models/organizacion_model_test.dart) | Gremios y Flota Dual | Valida organigrama gremial, convenios corporativos y flags de flota pública/privada | `flutter test test/models/organizacion_model_test.dart` |
| [`test/models/tarifa_sector_model_test.dart`](file:///c:/Workspaces/taxi/test/models/tarifa_sector_model_test.dart) | Tarifas Oficiales | Valida `TarifaSectorModel`, decretos distritales y recargos legales | `flutter test test/models/tarifa_sector_model_test.dart` |
| [`test/services/despacho_whatsapp_test.dart`](file:///c:/Workspaces/taxi/test/services/despacho_whatsapp_test.dart) | Despacho Bahía WhatsApp | Valida formateo de celular, URL de WhatsApp, tracking web y viaje de bahía para pasajero sin app | `flutter test test/services/despacho_whatsapp_test.dart` |
| [`test/services/firestore_tarifa_test.dart`](file:///c:/Workspaces/taxi/test/services/firestore_tarifa_test.dart) | Motor Tarifario | Valida cálculo legal estandarizado en `FirestoreRepository` (cero arbitrariedad) | `flutter test test/services/firestore_tarifa_test.dart` |
| [`test/turno_model_test.dart`](file:///c:/Workspaces/taxi/test/turno_model_test.dart) | Turnos y Bahías | Valida estados de fila, deserialización polimórfica y propiedades computadas | `flutter test test/turno_model_test.dart` |
| [`test/fundetaxcol_parity_views_test.dart`](file:///c:/Workspaces/taxi/test/fundetaxcol_parity_views_test.dart) | Paridad UI Garita | Valida layout, widgets y flujos de paridad visual de garita y bahía | `flutter test test/fundetaxcol_parity_views_test.dart` |
| [`test/responsive_layout_test.dart`](file:///c:/Workspaces/taxi/test/responsive_layout_test.dart) | Responsive | Valida split-view en tablets/desktop y single-view en smartphones | `flutter test test/responsive_layout_test.dart` |
| [`test/session_recovery_test.dart`](file:///c:/Workspaces/taxi/test/session_recovery_test.dart) | Resiliencia | Valida recuperación de estado offline y reconexión | `flutter test test/session_recovery_test.dart` |

---

## 🛡️ Cero Tolerancia a Fallos
Ninguna tarea o cambio en OpenSpec se considerará completado si existe algún fallo en la suite de pruebas. Todas las suites deben ejecutarse con:
```bash
flutter test
```
garantizando 100% de aserciones exitosas.
