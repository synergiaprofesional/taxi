# 🏛️ CONTEXT.md — Contexto Central de Arquitectura y Reglas

**Proyecto:** Synergia Móvil (FUNDETAXCOL)  
**Versión Actual:** `v2.1.25+27`  
**Framework:** Flutter SDK `^3.12.2` / Dart  
**Gestor de Estado:** GetX (`^4.7.3`)  
**Backend:** Odoo 11 EE (`fundetaxcol.co`, JSON-RPC) + Node.js Socket.IO (`fundetaxcol.co:3000`)

---

## 📦 Paquetes y Versiones Clave (`pubspec.yaml`)
- `get: ^4.7.3` (Gestión de estado reactivo, inyección de dependencias `Get.put`/`Get.find`, enrutamiento)
- `http: ^1.6.0` (Cliente HTTP para JSON-RPC hacia Odoo 11)
- `socket_io_client: ^1.0.2` (WebSockets en tiempo real hacia `server_rt_odoo`)
- `shared_preferences: ^2.5.6` (Persistencia local en disco)
- `intl: ^0.20.3` (Formateo de moneda `es_CO` y fechas)
- `cupertino_icons: ^1.0.8`

---

## 🧱 Estructura Canónica de Directorios
- `lib/core/` -> Configuración, red (`NetworkConfig`), tema (`AppColors`, `AppTheme`), utilidades (`LocalStorage`).
- `lib/models/` -> Modelos puros e inmutables (`TurnoModel`, `PagoRecaudoModel`, `TarifaSectorModel`, etc.).
- `lib/services/` -> Servicios de comunicación y hardware (`OdooService`, `SocketService`, `PrinterService`).
- `lib/controllers/` -> Lógica de negocio reactiva (`TurnoController`, `ThemeController`).
- `lib/ui/views/` -> Pantallas de la aplicación (`auth/`, `bahia/`, `form/`, `home/`, `list/`, `main/`, `settings/`).
- `lib/ui/widgets/` -> Tarjetas y componentes reutilizables (`pago_card_widget.dart`, `turno_card_widget.dart`, etc.).
- `scripts/` -> Scripts de compilación y despliegue automatizado (**PROHIBIDO BORRAR**).
- `Bitacoras/` -> Documentación dual de sesiones (`Bitacora ddmmaaa.md` y `Bitacora YYYYMMDD HHmmss.md`).
- `docs/` -> Documentación técnica persistente (`contexto_tecnico_synergia_movil.md`).

---

## 🛡️ Reglas Inviolables de Arquitectura y Código
1. **Regla GetX Obx:** En cualquier `Obx(() { ... })`, la variable observable `.value` **DEBE LEERSE EN LA PRIMERA LÍNEA** antes de cualquier `if` o `return` condicional para evitar `improper use of GetX`.
2. **Prohibido `setState()` en `build()`:** Nunca mutar controladores (`TextEditingController.text = ...`) dentro de constructores de vista o `fieldViewBuilder`.
3. **Colores y Tipografía:** Usar siempre `AppColors` y `AppTheme` (prohibido quemar colores hexadecimales).
4. **Odoo 11 Legacy:** Autenticación exclusiva por cookies `session_id`. Detección de sesión expirada mediante `error['code'] == 100` y `SessionExpiredException` en HTTP 200 con re-autenticación en caliente.
5. **Hardware en Hilo de Fondo:** Cualquier operación de hardware (impresión térmica, Bluetooth RFCOMM, TCP) debe ejecutarse en hilos de fondo (`Executors.newSingleThreadExecutor()` / `Dispatchers.IO`) con timeout de 3.5s para no congelar la UI.
6. **Versionamiento Continuo:** Incrementar obligatoriamente `pubspec.yaml` y `lib/core/config/app_version.dart` en cada ciclo.

