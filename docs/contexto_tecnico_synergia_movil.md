# Documento de Contexto Técnico y Estado Actual
# Proyecto: Synergia Móvil — Sistema de Despacho y Recaudo FUNDETAXCOL
**Generado:** 2026-11-07 | **Versión en producción:** `v2.1.24+26`
**Repositorio:** `c:\Workspaces\synergia_movil` | **Cliente:** FUNDETAXCOL (NIT 900.542.188-4)

---

## 1. Resumen Ejecutivo del Proyecto

Synergia Móvil es una **aplicación Flutter multiplataforma** (Android móvil, Android tablet, Windows Desktop) que actúa como **terminal de operación** para los despachadores y cajeros de FUNDETAXCOL, una fundación de taxis en Cartagena, Colombia.

**Problema que resuelve:**
- Digitalizar la gestión de bahías de taxis: inscripción de vehículos en fila (*enturnar*), despacho a destino con tarifa y cobro de recargos automáticos.
- Registrar y visualizar el recaudo de pagos de conductores (cuotas de sostenimiento, planillas, ahorros).
- Emitir tiquetes físicos ESC/POS en impresoras térmicas en el momento del despacho.
- Sincronizar el estado de bahías y turnos en tiempo real con el servidor Odoo del cliente.

**Infraestructura del cliente:** Odoo 11 (EE) corriendo en `fundetaxcol.co` sobre Linux. Base de datos PostgreSQL `fundetaxcol`.

---

## 2. Stack Tecnológico y Entorno

### Frontend / Mobile / Desktop
| Componente | Tecnología | Versión |
|---|---|---|
| Framework UI | Flutter / Dart | SDK `^3.12.2` |
| State Management | GetX | `^4.7.3` |
| HTTP Client | `package:http` | `^1.6.0` |
| WebSocket Client | `socket_io_client` | `^1.0.2` |
| Persistencia Local | `shared_preferences` | `^2.5.6` |
| Internacionalización | `intl` | `^0.20.3` |
| Iconos | `cupertino_icons` | `^1.0.8` |
| Linting | `flutter_lints` | `^6.0.0` |

### Backend / Servicios Externos
| Servicio | Rol | Protocolo |
|---|---|---|
| **Odoo 11 EE** (`fundetaxcol.co`) | ERP central; fuente de verdad de vehículos, conductores, bahías, pagos, turnos | JSON-RPC 2.0 vía HTTP (`/web/dataset/call_kw`) |
| **server_rt_odoo** (`fundetaxcol.co:3000`) | Servidor Node.js de eventos en tiempo real (WebSocket) | Socket.IO (WebSocket + polling fallback) |
| Caddy (Reverse Proxy) | Sirve HTTPS y rutea WebSocket al puerto 3000 | HTTPS/WSS estándar |

### Plataformas de Destino
- **Android APK** (Teléfono Xiaomi `6tl7gupn9tnjdapb` y Tablet Lenovo M11 `HA27VLYC`)
- **Windows Desktop EXE** (`build/windows/x64/runner/Release/synergia_movil.exe`)

---

## 3. Arquitectura y Estructura de Directorios

```
c:\Workspaces\synergia_movil\
│
├── lib/                          # Código fuente Dart
│   ├── main.dart                 # Punto de entrada: inicializa LocalStorage, registra OdooService y ThemeController
│   │
│   ├── core/                     # Infraestructura transversal
│   │   ├── config/app_version.dart   # AppVersion: versionName='2.1.24', versionCode=26
│   │   ├── network/network_config.dart  # Gestión de URLs: host, puerto, HTTPS, sanitización
│   │   ├── theme/app_colors.dart     # Paleta de colores (amarillo taxi / negro)
│   │   ├── theme/app_theme.dart      # ThemeData Light + Dark
│   │   └── utils/local_storage.dart  # Wrapper SharedPreferences (clave/valor)
│   │
│   ├── models/                   # Modelos de datos (puros, sin lógica)
│   │   ├── bay_model.dart            # BahiaModel: id, name, codigo, activa
│   │   ├── payment_model.dart        # AhorroModel, CompanyModel, ConceptoCobroModel, PaymentConceptLine, PagoRecaudoModel
│   │   ├── printer_config_model.dart # TipoImpresora (enum), PrinterConfigModel
│   │   ├── tarifa_sector_model.dart  # TarifaSectorModel: id, name, valor, valorRecargo, nota
│   │   ├── ticket_data_model.dart    # TicketDataModel: datos para imprimir tiquete ESC/POS
│   │   ├── turno_model.dart          # EstadoTurno (enum), TurnoModel
│   │   └── vehicle_model.dart        # ConductorModel, VehiculoModel
│   │
│   ├── services/                 # Capa de acceso a datos y hardware
│   │   ├── odoo_service.dart         # JSON-RPC a Odoo: auth, callKw, CRUD de turnos/pagos/bahías/tarifas
│   │   ├── printer_service.dart      # Generación ESC/POS y envío: emulador, TCP, Bluetooth, Spooler Windows, URL
│   │   └── socket_service.dart       # Socket.IO: conexión a server_rt_odoo para eventos en tiempo real
│   │
│   ├── controllers/              # Lógica de negocio reactiva (GetX)
│   │   ├── turno_controller.dart     # Controller principal: orquesta OdooService + SocketService + PrinterService
│   │   └── theme_controller.dart     # Gestión Light/Dark mode persistido
│   │
│   └── ui/                       # Capa de presentación
│       ├── views/
│       │   ├── auth/
│       │   │   ├── auth_gatekeeper.dart  # Widget raíz: bloquea acceso hasta isAuthenticated==true
│       │   │   ├── login_view.dart       # Pantalla de login (usuario, contraseña, host, BD)
│       │   │   └── login_dialog.dart     # Modal de re-login en contexto de sesión expirada
│       │   ├── home/home_view.dart       # Shell responsive: detecta mobile/tablet/desktop → routing de layout
│       │   ├── main/bahia_selected_view.dart  # Shell de bahía: BottomNav 3 pestañas (Pagos, Turnos, Despachos)
│       │   ├── bahia/bahia_selector_dialog.dart  # Diálogo para elegir bahía activa
│       │   ├── form/
│       │   │   ├── payment_form_view.dart    # Formulario nuevo recaudo (Autocomplete + chips conceptos)
│       │   │   ├── payment_concept_form.dart  # Formulario concepto de cobro (texto libre)
│       │   │   └── turno_form_view.dart      # Formulario enturnar/despachar (Autocomplete destino + recargo nocturno)
│       │   ├── list/
│       │   │   ├── pago_list_view.dart        # Lista de pagos filtrada/buscable
│       │   │   ├── turno_list_view.dart        # Fila activa de vehículos en bahía
│       │   │   ├── despacho_list_view.dart     # Historial de despachos
│       │   │   └── despacho_history_view.dart  # Vista histórica expandida
│       │   ├── pago/pago_dialog.dart          # Diálogo detalle de un pago
│       │   └── settings/
│       │       ├── settings_view.dart          # Config: host Odoo, BD, credenciales, impresora, socket, tema
│       │       └── setting_info_extra_view.dart # Info de versión, latencia, sesión
│       └── widgets/
│           ├── pago_card_widget.dart      # Tarjeta de pago: placa, monto, conductor • concepto, hora
│           ├── turno_card_widget.dart     # Tarjeta de turno en fila
│           ├── despacho_card_widget.dart  # Tarjeta de despacho con destino y tarifa
│           ├── ticket_preview_dialog.dart  # Vista previa del tiquete antes de imprimir
│           └── search_generic_widget.dart  # Widget de búsqueda reutilizable
│
├── test/                         # Suite de pruebas (22 tests, todos pasando)
│   ├── fundetaxcol_parity_views_test.dart   # Tests de paridad de UI: PagoCard, DespachoCard, BahiaSelectedView
│   ├── login_gatekeeper_test.dart           # Tests de flujo auth: gatekeeper muestra login/home
│   ├── responsive_layout_test.dart          # Tests de layout responsive (mobile/tablet/desktop)
│   ├── services_test.dart                   # Tests de NetworkConfig y PrinterService (ESC/POS, ticket)
│   ├── turno_model_test.dart                # Tests de parsing TurnoModel desde JSON Odoo
│   ├── user_preferences_landscape_test.dart # Tests de persistencia de config de impresora por usuario
│   └── widget_test.dart                     # Test de humo del widget raíz
│
├── android/                      # Config Android: package=com.synergia.synergia_movil
├── windows/                      # Config Desktop Windows (CMake runner)
├── assets/img/                   # Logos e imágenes estáticas (fundetaxcol_logo.png, etc.)
│
├── scripts/                      # Scripts de automatización (NUNCA ELIMINAR)
│   ├── deploy_phone.bat          # Launcher → verify_and_deploy_phone.ps1
│   ├── deploy_tablet.bat         # Launcher → verify_and_deploy_tablet.ps1 (Lenovo HA27VLYC)
│   ├── deploy_windows.bat        # Launcher → verify_and_deploy_windows.ps1
│   ├── verify_and_deploy_phone.ps1    # Compila APK, instala vía ADB, lanza en Xiaomi, valida dumpsys
│   ├── verify_and_deploy_tablet.ps1   # Ídem para Tablet Lenovo
│   └── verify_and_deploy_windows.ps1  # Compila EXE, valida timestamp, lanza proceso
│
├── openspec/                     # Especificaciones y cambios bajo metodología OpenSpec
│   ├── changes/                  # Changes activos e históricos
│   └── specs/                    # Especificaciones de vistas individuales
│
├── Bitacoras/                    # Bitácoras duales de sesión (obligatorio)
├── docs/                         # Documentación técnica (architecture/, specs/, especificaciones_vistas/)
├── AGENTS.md / GEMINI.md         # Reglas inviolables del workspace para agentes IA
├── ERRORES.md                    # Registro de gotchas y fixes obligatorios (leer ANTES de compilar)
└── pubspec.yaml                  # version: 2.1.24+26 | sdk: ^3.12.2
```

---

## 4. Flujo de Datos y Comunicación

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SYNERGIA MÓVIL (Flutter App)                │
│                                                                     │
│  UI Layer (Widgets/Views)                                           │
│       │  Obx() reactive bindings                                    │
│       ▼                                                             │
│  TurnoController (GetxController)   ◄──── SocketService (Socket.IO)│
│       │                                        ▲                   │
│       │  async calls                           │ real-time events  │
│       ▼                                        │                   │
│  OdooService (GetxService)              server_rt_odoo (Node.js)   │
│       │                                   fundetaxcol.co:3000      │
│       │  JSON-RPC 2.0 (HTTP POST)               │                  │
│       ▼                                         │                  │
│  Odoo 11 EE ─────────────────────────── PostgreSQL (fundetaxcol)   │
│  fundetaxcol.co (/web/dataset/call_kw)                             │
│       │                                                             │
│  PrinterService                                                     │
│       │  ESC/POS bytes                                              │
│       ├─► Emulador (debug only)                                     │
│       ├─► TCP Socket (port 9100, impresoras Wi-Fi)                  │
│       ├─► Bluetooth SPP (MethodChannel nativo Android — STUB)       │
│       ├─► Spooler Windows (nombre de impresora compartida)          │
│       └─► HTTP URL (servicio proxy raw-escpos externo)              │
└─────────────────────────────────────────────────────────────────────┘
```

**Flujo de inicio:**
1. `main()` → `LocalStorage.initialize()` → `Get.put(OdooService)` → `OdooService.autoLogin()` (carga credenciales guardadas en SharedPreferences).
2. `AuthGatekeeper` observa `OdooService.isAuthenticated.obs`:
   - `false` → muestra `LoginView` (con splash durante auto-login).
   - `true` → navega a `HomeView`.
3. `HomeView` detecta `DeviceType` por ancho de pantalla → renderiza layout mobile (pantalla completa) o tablet/desktop (panel lateral + contenido).
4. El usuario selecciona una bahía → `TurnoController` llama a `OdooService.getBahias()` y `cargarTurnos()`.
5. `SocketService` conecta a `server_rt_odoo` y recibe eventos push para refrescar la UI sin polling.

**Autenticación a Odoo:**
- `POST /web/session/authenticate` → Odoo devuelve `session_id` cookie.
- Cookie persiste en SharedPreferences (`odoo_cookie`) para reutilización.
- En cada `callKw`: si respuesta tiene error `'session'`/`'expired'`/`'auth'` o HTTP 401/403 → `reautenticarSilencioso()` automático sin interrupción al usuario.

---

## 5. Modelos de Datos / Esquemas Clave

### `TurnoModel` — Vehículo en bahía
```
id, name (ej: "T-0142"), vehiculoPlaca, conductorNombre, bahiaNombre,
numeroTurno (secuencia en fila), estado: EstadoTurno {espera|actual|siguiente|despachado|cancelado},
fechaCreacion, fechaDespacho?, valorTotal, tarifaId, tarifaNombre,
nota, esAnonimo, placaAnonima, bahiaSesionId, bahiaBaseId, vehiculoId, conductorId
```
*Computed:* `enFila` (espera|actual|siguiente), `esDespacho` (tarifaId > 0).

### `PagoRecaudoModel` — Recaudo de un conductor
```
id, consecutivo, conductorNombre, vehiculoPlaca, fecha, total,
conceptoNombre (tipo de pago: "Cuota de Sostenimiento", etc.),
lineas: List<PaymentConceptLine> (concepto_id, nombre, valor),
ahorros: List<AhorroModel>,
bahiaSesionId, bahiaId, nota
```

### `TarifaSectorModel` — Destino/tarifa de despacho
```
id, name (ej: "Manga"), valor (ej: 14000.0), valorRecargo (fijo: 1100.0), nota
```
*Catálogo offline de 11 sectores con fallback si Odoo falla. `limit:1000` en query.*

### `BahiaModel` — Bahía operativa
```
id, name (ej: "Bahía 29D"), codigo (ej: "29D"), activa
```

### `TicketDataModel` — Datos del tiquete ESC/POS
```
empresaNombre, nit ("NIT 900.542.188-4"), bahiaNombre, turnoNumero,
placa, movilNumero, conductor, destino, direccion,
fechaHora, valorTotal, cajero, pieMensaje, turnoId
```

### `PrinterConfigModel` — Config de impresora (por usuario)
```
tipo: TipoImpresora {bluetooth|tcp|spoolerWindows|emulador|url},
nombreODireccion, puerto (default:9100), anchoPapel (58u80 mm), autoCorte
```
*Persiste por usuario con clave `user_pref_{user}_printer_config`.*

### `ConductorModel` / `VehiculoModel`
```
ConductorModel: id, name, cedula, telefono, conceptos: List<ConceptoCobroModel>
VehiculoModel:  id, placa, numero (movil), conductorId, conductorNombre, bahiaId
ConceptoCobroModel: id, nombre, valor
```

---

## 6. Estado Actual del Desarrollo

### ✅ Funcionalidades Implementadas y Operativas (v2.1.24+26)

| Módulo | Estado |
|---|---|
| Autenticación Odoo + auto-login desde SharedPreferences | ✅ |
| Re-autenticación silenciosa ante 401/403/session-expired | ✅ |
| AuthGatekeeper reactivo (splash → login → home) | ✅ |
| Selección de bahía activa con persistencia | ✅ |
| Enturnar vehículo (nuevo turno en fila) | ✅ |
| Despachar vehículo con destino y tarifa | ✅ |
| Autocomplete de destinos con texto libre + chips rápidos | ✅ |
| Recargo nocturno automático 7PM–5AM a \$1.100 fijo (no sobreescrito por Odoo) | ✅ |
| Lista de turnos en fila (filtrada por bahía) | ✅ |
| Historial de despachos de la sesión | ✅ |
| Registro de recaudo/pago de conductores | ✅ |
| Autocomplete de concepto de pago con texto libre + chips | ✅ |
| Visualización de tipo de pago en tarjeta (Conductor • Concepto) | ✅ |
| Búsqueda híbrida de pagos: local (bahía actual) + remota (histórico Odoo) | ✅ |
| Emisión de tiquetes ESC/POS (emulador, TCP, Bluetooth stub, Windows Spooler, URL) | ✅ |
| Config de impresora persistida por nombre de usuario | ✅ |
| Preview de tiquete antes de imprimir | ✅ |
| Tiempo real vía Socket.IO (server_rt_odoo) | ✅ |
| Layout responsive: mobile / tablet / desktop (tres perfiles distintos) | ✅ |
| Paleta taxi amarillo/negro, Light + Dark mode persistido | ✅ |
| Panel de configuración (host, BD, credenciales, impresora, socket) | ✅ |
| Métricas de recaudo y servicios visible solo en pestaña Pagos (oculta en Turnos/Despachos) | ✅ |
| Versión visible en AppBar y tiquetes (`v2.1.24+26`) | ✅ |
| Scripts de despliegue automatizado (Phone, Tablet, Windows) con validación `dumpsys` | ✅ |
| Suite de 22 tests (unitarios + widget) pasando al 100% | ✅ |

### ⚠️ Módulos Parciales / Pendientes de Integración

| Módulo | Estado | Detalle |
|---|---|---|
| **Despliegue Tablet Lenovo M11 (`HA27VLYC`)** | ⏳ Pendiente | Tablet no conectada en la última sesión. Ejecutar `.\deploy_tablet.bat` cuando se conecte. |
| **Confirmación cliente: sesión no se cierra** | ⏳ Sin confirmar | Código implementado. Depende del timeout del servidor Odoo (~30 min inactividad). No validado empíricamente por el cliente. |
| **WebSocket real-time push completo** | ⚠️ Parcial | `SocketService` conecta y recibe eventos. Integración full con `TurnoController` para auto-refresh de UI no finalizada para todos los eventos. |
| **Bluetooth SPP Android** | ⚠️ Stub | La rama `TipoImpresora.bluetooth` llama a un `MethodChannel` nativo que NO tiene implementación Java/Kotlin. Crashea con `MissingPluginException`. Workaround: usar TCP. |
| **OpenSpec `solucion-novedades-fundetaxcol`** | ⏳ Archivar | Change implementado y desplegado. Falta ejecutar archivo formal. |

---

## 7. Problemas Conocidos, Deuda Técnica y Bloqueos

### ERRORES.md — Gotchas Obligatorios (leer antes de compilar)

| ID | Problema | Fix Obligatorio |
|---|---|---|
| **FIX-001** | Windows EXE: `flutter build windows` NO actualiza el timestamp del `.exe` (solo el `app.so`). El usuario ve fecha vieja y cree que no compiló. | Eliminar `synergia_movil.exe` antes de compilar **o** tocar `windows/runner/main.cpp`. Validar con `mtime` real del archivo. |
| **FIX-002** | APK ADB: `adb install -r` instala en segundo plano sin relanzar app. Si versión no sube, el usuario ve la versión vieja. | Incrementar versión → compilar → instalar → `adb shell am start -n com.synergia.synergia_movil/.MainActivity` → validar con `adb shell dumpsys package com.synergia.synergia_movil`. |
| **FIX-003** | SSH remoto a Odoo: scripts Python largos en una línea vía `python3 -c "..."` fallan por parsing de Bash (comillas, paréntesis). | Subir script vía SFTP a `/tmp/`, ejecutar `python3 /tmp/script.py`. |

### Deuda Técnica y Gotchas Críticos

1. **GetX `Obx` + return temprano:** Si dentro de un `Obx` se hace un `return` condicional antes de leer alguna variable `.obs`, GetX no registra el observable y lanza excepción en runtime. **Regla:** siempre leer al menos una variable `Rx` antes de cualquier `return` condicional dentro de un `Obx`.

2. **`RichText`/`TextSpan` invisible a `find.text()`:** Los tests Flutter con `find.text('...')` no detectan texto dentro de `RichText`. Usar siempre widgets `Text` separados, o usar `find.byWidgetPredicate()`.

3. **`flutter test` suite completa:** Tarda ~2 minutos. Solo `flutter analyze` como gate de verificación + test puntual si se creó para el bug específico.

4. **Bluetooth Printer (Stub):** `TipoImpresora.bluetooth` declarado pero sin implementación nativa Android. Workaround activo: TCP (port 9100).

5. **server_rt_odoo sin health check:** Si el servicio Node.js en `fundetaxcol.co:3000` cae, `SocketService.isConnected` queda en `false` sin notificación visible al usuario (solo `debugPrint`).

6. **Odoo 11 EE (legacy 2017):** No soporta JSON-RPC v2.0 estándar moderno ni headers `Authorization: Bearer`. Autenticación exclusiva por cookies de sesión (`session_id`). Cualquier cambio que asuma autenticación moderna romperá la integración.

### Reglas Inviolables del Workspace

> Cumplimiento obligatorio para cualquier agente o sesión:
> 1. **Scripts en `scripts/`** — PROHIBIDO eliminar.
> 2. **Docs en `docs/`**, bitácoras duales en `Bitacoras/`.
> 3. **Leer `ERRORES.md`** antes de cualquier compilación o despliegue.
> 4. **Incrementar versión** en `pubspec.yaml` Y `lib/core/config/app_version.dart` en CADA ciclo.
> 5. **Gate empírico obligatorio:** `flutter analyze` → 0 issues antes de declarar tarea completa. Validar con `dumpsys`, timestamps y PID reales.
> 6. **Perímetro hermético:** exclusivo `synergia_movil` y `fundetaxcol.co`. Prohibido mezclar otros proyectos.
> 7. **RCA antes de parchar:** Si un bug reaparece, explicar qué falló exactamente antes de tocar una sola línea.
> 8. **Checklist manual de 3–5 pasos** al finalizar cada corrección para validación física del usuario.

---

*Fin del documento. Versión actual en disco: `v2.1.24+26`.*
*Desplegado: Teléfono Xiaomi (`2026-11-07 07:27:16`) ✅ | Windows Desktop (`2026-11-07 07:22:11`) ✅ | Tablet Lenovo `HA27VLYC` ⏳ pendiente.*
