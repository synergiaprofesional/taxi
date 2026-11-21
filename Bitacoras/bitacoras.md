# Índice de Bitácoras — Taxi

Registro cronológico resumido de análisis, diseño e implementaciones técnicas bajo la Constitución de La Tripleta.

### [2026-11-21 12:45] Tripleta Sprint B: Despacho en Bahía con Enlace WhatsApp para Pasajeros sin App
* **Problema:** Los pasajeros en bahías físicas (centros comerciales, terminales, aeropuertos) abordan a pie sin haber descargado la app móvil; Uber e inDrive no pueden atenderlos sin obligarlos a registrarse.
* **Solución:** Campo opcional de celular en `TurnoFormView` durante el despacho en garita con autocompletado +57; generación automática del viaje en Firestore (`categoria: bahiaPrioritaria`) en `FirestoreRepository`; helper `WhatsAppTrackingHelper` para formatear el mensaje enriquecido y generar el enlace web de tracking canónico `https://taxi.fundetaxcol.co/t/{viajeId}`; pantalla responsive de ticket digital `WebTicketTrackingView` con sello de verificación, placa colombiana, tarifa decretada desglosada y botón de auxilio SOS; suite TDD `test/services/despacho_whatsapp_test.dart` y catalogación en `tests/COMPENDIO_TESTS.md`; memoria en Engram registrada con ID `#660`.
* **Enlaces:** [Bitácora Monolito Mensual](file:///c:/Workspaces/taxi/Bitacoras/2026/11/bitacora.md) | [Bitácora Diaria 21/11/2026](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121.md) | [Bitácora Sesión 124500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20124500.md) | [OpenSpec Sprint B](file:///c:/Workspaces/taxi/openspec/changes/sprint-b-despacho-bahia-whatsapp-tracking/)

---

### [2026-11-21 11:45] Tripleta Sprint A: Categorías, Oferta con Ancla Legal y Selección de Conductor
* **Problema:** Diseñar e implementar el flujo de solicitud de carreras incorporando la simplicidad de categorías de Uber y la negociación transparente de inDrive sin caer en tarifas predatorias.
* **Solución:** Especificación formal OpenSpec en `sprint-a-categorias-ofertas-seleccion-conductor`; modelos `CategoriaViaje` y `ConductorOfertaModel` en `lib/models/viaje_model.dart`; métodos de marketplace en `FirestoreRepository`; hoja reactiva `DriverOffersSheet` para elegir conductor en tiempo real; ajuste de oferta interactiva con ancla legal por decreto en `PassengerHomeView`; suite TDD `test/models/categoria_oferta_test.dart` pasando 14/14 tests al 100%.
* **Enlaces:** [Bitácora Monolito Mensual](file:///c:/Workspaces/taxi/Bitacoras/2026/11/bitacora.md) | [Bitácora Diaria 21/11/2026](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121.md) | [Bitácora Sesión 114500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20114500.md) | [OpenSpec Sprint A](file:///c:/Workspaces/taxi/openspec/changes/sprint-a-categorias-ofertas-seleccion-conductor/)

---

### [2026-11-21 11:15] Desarrollo e Implementación de Modelos Firestore, Vistas Conductor/Pasajero, Pantalla Espejo y TDD 100%
* **Problema:** Materializar en código el desacoplamiento de Odoo hacia Firebase y dotar a la plataforma de las capacidades del Modelo Cebolla (Capa 0 Garita, Capa 1 Conductor, Capa 2 Pasajero), vistas nativas para taxista y usuario, cotizador de tarifas legales y enclavamiento de seguridad vial para AdMob.
* **Solución:** Creación de modelos NoSQL puros en `lib/models/` (`UserModel`, `ViajeModel`, `OrganizacionModel`, `TarifaSectorModel`, `RecaudoModel`) y adaptación con Firestore de `TurnoModel`, `BahiaModel` y `VehiculoModel`; implementación de `FirestoreRepository` y `firestore.rules`; integración reactiva en `TurnoController`; desarrollo de `DriverHomeView` (cola de turno, ahorro programado, radar de calle y botón de auxilio) y `PassengerHomeView` / `PassengerTripTrackingView` (cotizador previo por sectores oficiales, pantalla espejo y calificación); widget `AdmobBannerWidget` con destrucción de anuncios durante la conducción; y ejecución del Compendio TDD con 46 pruebas pasando al 100% (cero fallos).
* **Enlaces:** [Bitácora Monolito Mensual](file:///c:/Workspaces/taxi/Bitacoras/2026/11/bitacora.md) | [Bitácora Diaria 21/11/2026](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121.md) | [Bitácora Sesión 111500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20111500.md) | [Wiki Maestro](file:///c:/Workspaces/taxi/docs/wiki/index.md)

---

### [2026-11-21 09:15] Independización Taxi, Constitución La Tripleta, Respaldo de Referencia (Read-Only) y Toolkit Unificado
* **Problema:** Necesidad de independizar el sistema a una aplicación con mayor cobertura y propósito ampliado (`taxi`), desacoplada de Odoo 11 hacia Firebase, conservando la ergonomía y familiaridad UX para los usuarios actuales. Acceso de solo lectura al servidor de producción para extraer el código legacy de referencia.
* **Solución:** Descarga vía streaming en memoria de `/opt/server_rt_odoo`, `/opt/synergia/addons_fundetaxcol` y configs hacia `reference/` sin escribir nada en el servidor; instanciación de la Constitución Inviolable en `AGENTS.md` y `GEMINI.md`; creación del Toolkit Unificado `Consolidados/cli.py` con mapeo de 38 modelos Odoo a migrar; inicialización de la LLM Wiki ontológica en `docs/wiki/`; compendio TDD en `tests/COMPENDIO_TESTS.md`; y custodia de 259 scripts en `scripts/back/20261121/`.
* **Enlaces:** [Bitácora Monolito Mensual](file:///c:/Workspaces/taxi/Bitacoras/2026/11/bitacora.md) | [Bitácora Diaria 21/11/2026](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121.md) | [Bitácora Sesión 091500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20091500.md) | [Wiki Maestro](file:///c:/Workspaces/taxi/docs/wiki/index.md)

---

### [2026-11-18 14:36] Arquitectura de Expansión: Desacoplamiento de Odoo ERP, Supabase Self-Hosted y Salida a Play Store
* **Problema:** Necesidad de escalar Synergia Móvil a la Google Play Store y eliminar la dependencia y latencia impuesta por Odoo 11 Community (ERP de 2017) en el flujo de despacho en tiempo real.
* **Solución:** Análisis comparativo de Telegram Desktop (`tdesktop`) y frameworks híbridos (Tauri v2 vs Electron vs Flutter); ratificación de Flutter como runtime nativo multiplataforma (GPU sin WebViews ni DOM); rechazo de Firebase (NoSQL sin ACID, costos desmedidos de lectura y carencia de PostGIS); selección estratégica de **Supabase Self-Hosted** (PostgreSQL 15+ puro, PostGIS, Realtime WebSockets, GoTrue y PostgREST) en servidor propio bajo Docker Compose; desacoplamiento estricto del ERP contable Odoo a un receptor asíncrono pasivo de cierres de caja.
* **Enlaces:** [Bitácora Diaria 18/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/18/Bitacora%2018112026.md) | [Bitácora Sesión 143600](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/18/Bitacora%2020261118%20143600.md)

---

### [2026-11-07 13:50] Reorganización Jerárquica de Bitácoras (YYYY/MM/DD) y Regla en Mármol #9
* **Problema:** Existían más de 50 archivos de bitácoras dispersos en la raíz de `Bitacoras/`, provocando saturación visual y dificultando la navegación por fecha.
* **Solución:** Creación de la estructura determinista para el año 2026 (12 meses y 365 días: Febrero con 28 días, meses de 30 y 31 días); migración de 58 archivos existentes a sus carpetas exactas `Bitacoras/YYYY/MM/DD/`; normalización completa de enlaces en `bitacoras.md`; creación de scripts canónicos permanentes `scripts/organize_bitacoras.py` y `scripts/normalize_bitacoras_links.py`; e instauración formal de la **Regla Inviolable #9** en `AGENTS.md`, `GEMINI.md` y en las skills globales `bitacora` y `tripleta`.
* **Enlaces:** [Bitácora Diaria 07/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2007112026.md) | [Bitácora Sesión 135000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20135000.md)

---

### [2026-11-07 13:35] Documentación Integral de Sesión: Anti-Carrera en Búsqueda, Reset Tarifas, Layout Settings y Botón Salir v2.1.29+31
* **Problema:** Múltiples inconsistencias de experiencia de usuario en producción: búsquedas de placas como `842` y `776` mostraban placas irrelevantes al frente por desorden y condición de carrera en red; persistencia de tarifas al borrar destinos en despacho; desbordamientos visuales en ajustes; y ausencia de botón de salida en login.
* **Solución:** Implementado debounce de 250ms con token anti-carrera y ranking de relevancia en búsqueda; reseteo forzoso de tarifas a $0 al limpiar destino en `TurnoFormView`; rediseño fluido con `Wrap` en `SettingsView`; botón y modal de salida multiplataforma (`SystemNavigator.pop()` en Android, `exit(0)` en Windows); bump a `v2.1.29+31`; desplegado físicamente en Windows (`synergia_movil.exe`, PID 29212) y en Xiaomi Redmi Note 13 Pro (`versionName=2.1.29`, `versionCode=31`).
* **Enlaces:** [Bitácora Diaria 07/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2007112026.md) | [Bitácora Sesión 133500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20133500.md)

---

### [2026-11-07 11:10] Botón de Salir Multiplataforma (Móvil y Desktop) y Despliegue Dual v2.1.29+31
* **Problema:** En la pantalla de inicio de sesión (`LoginView`), el usuario requiere un botón para salir de la aplicación tanto en dispositivos móviles como en desktop.
* **Solución:** Implementado botón formal `SALIR DE LA APLICACIÓN` debajo de `INGRESAR A BAHÍA` y botón rápido en el encabezado (`_buildHeader`); diálogo modal de confirmación con tema oscuro; salida nativa de plataforma (`SystemNavigator.pop()` en Android e iOS, `exit(0)` en Windows); `flutter analyze` 0 issues; bump de versión a `v2.1.29+31`; compilado y desplegado físicamente en Windows Desktop (`synergia_movil.exe`, PID 29212) y en Xiaomi Redmi Note 13 Pro (`versionName=2.1.29`, `versionCode=31`, `11:08:51`).
* **Enlaces:** [Bitácora Diaria 07/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2007112026.md) | [Bitácora Sesión 111000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20111000.md)

---

### [2026-11-07 09:48] Hotfix Pantalla Gris en Despacho, Título Windows "SYNERGIA MOVIL" y Hardening E2E v2.1.25+27
* **Problema:** Pantalla gris (*Grey Screen of Death*) en formulario de Despacho al tocar cualquier turno por mutación ilegal de `TextEditingController` dentro de `fieldViewBuilder` y desbordamiento de `Autocomplete`. El usuario solicita además cambiar el título de Windows a `SYNERGIA MOVIL` y auditoría forense E2E de los 7 puntos y deuda técnica.
* **Solución:** Reemplazado `Autocomplete` por `TextFormField` nativo con sugerencias dinámicas no bloqueantes y chips rápidos en `TurnoFormView` y `PaymentFormView`; título cambiado en `windows/runner/main.cpp` y `Runner.rc`; interceptor Odoo 11 Code 100/SessionExpiredException en caliente; preservación de texto libre en `nota`; eliminación de métricas en Turnos en `home_view.dart` (Tablet/Desktop); canal Bluetooth SPP nativo en `MainActivity.kt`; bump a `v2.1.25+27`.
* **Enlaces:** [Bitácora Diaria 07/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2007112026.md) | [Bitácora Sesión 094800](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20094800.md) | [OpenSpec Change](file:///c:/Workspaces\synergia_movil\openspec\changes\realtime-bluetooth-hardening-v2-1-25\)

---

### [2026-11-07 07:52] Auditoría Punto a Punto del Informe de Novedades + Generación Documento de Contexto Técnico
* **Problema:** El cliente suministra que los 7 puntos del Informe de Novedades del 02/11/2026 se siguen presentando. Se solicita verificación empírica punto a punto si están resueltos en el código real (no por declaración del agente). Adicionalmente se solicita un documento de contexto técnico completo para compartir con otra IA que ayude a identificar fallas.
* **Solución:** Auditoría empírica ejecutando 18 comandos de inspección directa sobre el código fuente en disco. Resultado: 6/7 ítems confirmados en código ✅; 1/7 (sesión) implementado en código pero sin confirmación empírica del cliente (depende del timeout real del servidor Odoo ~30 min inactividad). Generación del documento `docs/contexto_tecnico_synergia_movil.md` (21 KB) con arquitectura, stack, flujo de datos, modelos, estado actual y deuda técnica. Bitácoras duales completas para transferencia a otra IA.
* **Hallazgo clave:** El único ítem pendiente de confirmar es el Punto 1 (sesión automática). El código de `reautenticarSilencioso()` es correcto; sin embargo, requiere validación física del cliente: esperar 30-45 min de inactividad y confirmar que la app no pide login de nuevo.
* **Deuda técnica identificada:** Bluetooth stub (`MissingPluginException`), WebSocket parcialmente integrado con TurnoController, Tablet Lenovo `HA27VLYC` sin despliegue verificado, OpenSpec `solucion-novedades-fundetaxcol` sin archivar.
* **Archivos creados:** `docs/contexto_tecnico_synergia_movil.md` (21 KB), `Bitacoras/2026/11/07/Bitacora 07112026.md`, `Bitacoras/2026/11/07/Bitacora 20261107 075253.md`
* **Enlaces:** [Bitácora Diaria 07/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2007112026.md) | [Bitácora Sesión 075253](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20075253.md) | [Contexto Técnico](file:///c:/Workspaces/synergia_movil/docs/contexto_tecnico_synergia_movil.md)

---

### [2026-11-07 07:28] Solución Integral de Novedades Fundetaxcol, QA Gates y Despliegue Multi-Dispositivo v2.1.24+26 (Tripleta Automática)
* **Problema:** El cliente reportó 7 novedades críticas en producción (02 de noviembre de 2026): 1. Sesión se cierra automáticamente; 2. En pagos no se visualiza el tipo de pago ("Recaudo $15.000"); 3. No se podía escribir manualmente el tipo de pago; 4. No se podían escribir manualmente los destinos en turnos; 5. Destinos con letras M, P, S no aparecían (Manga, Manzanillo, Pedro Salazar, San Pedro, San Francisco); 6. Recargo nocturno debe ser de $1.100 desde las 7:00 PM; 7. Eliminar el cuadro de métricas de la vista de turnos.
* **Solución:** Reautenticación silenciosa en background (`reautenticarSilencioso`) en `OdooService`; deserialización de `concepto_ids` en `PagoRecaudoModel` y proyección de `Conductor • Concepto` en Fila 2 de `PagoCardWidget`; entrada manual con `Autocomplete` de conceptos en `PaymentFormView` y `PaymentConceptForm`; entrada manual con `Autocomplete` de destinos en `TurnoFormView`; catálogo ampliado a 1000 registros en `getTarifasSector`; recargo nocturno forzado a `$1.100` estricto; cuadro de métricas condicionado a pestaña de Pagos en `BahiaSelectedView`; verificación de 0 issues en `flutter analyze` y 22/22 tests pasando en `flutter test`; bump a `v2.1.24+26`; compilación y despliegue físico verificado en Teléfono Xiaomi (`6tl7gupn9tnjdapb`) y Windows Desktop (`synergia_movil.exe`).
* **Enlaces:** [Bitácora Diaria 07/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2007112026.md) | [Bitácora Sesión 072800](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20072800.md) | [OpenSpec solucion-novedades-fundetaxcol](file:///c:/Workspaces/synergia_movil/openspec/changes/solucion-novedades-fundetaxcol/)

---

### [2026-11-02 13:27] Documentación e Integración de Grafos de Conocimiento (Graphify) y Restricción FIX-013
* **Problema:** Necesidad de aprovechar los grafos generados por Graphify (`lib/graphify-out/` con 695 nodos AST y `Bitacoras/graphify-out/` con 32 nodos semánticos), disponer de herramientas programáticas de análisis de impacto (blast radius) y blindar la restricción contra el borrado de scripts.
* **Solución:** Creación del script canónico `scripts/query_graphify.py` para análisis de impacto y estadísticas; elaboración de la guía de arquitectura `docs/guia_uso_grafos_graphify.md`; incorporación de FIX-013 en `ERRORES.md` con prohibición absoluta de purga de scripts; persistencia en Engram (`architecture/graphify-integration`).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 132700](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20132700.md) | [Guía de Grafos Graphify](file:///c:/Workspaces/synergia_movil/docs/guia_uso_grafos_graphify.md)

---

### [2026-11-02 11:48] Fila Dedicada para Tiempo de Espera en Turnos y Despliegue Multi-Dispositivo v2.1.23+25 (Tripleta Automática)
* **Problema:** En `TurnoCardWidget`, el nombre del conductor y el tiempo de espera compartían la misma fila horizontal, haciendo que nombres largos como "DUGLAS NERIO VARGAS QUINTERO" ocuparan todo el ancho y truncaran la espera a `•` o `• E...`.
* **Solución:** Separación en filas dedicadas: Fila 2 exclusiva para el conductor (`✓ OSWALDO MUÑOZ BUENDIA`) y Fila 3 nueva para el tiempo de espera (`⏱ Espera: 38 min`); verificación con 22/22 tests pasando y 0 issues en `flutter analyze`; bump a `v2.1.23+25`; despliegue verificado en Teléfono Xiaomi (`6tl7gupn9tnjdapb`), Tablet Lenovo (`HA27VLYC`) y Windows Desktop (`synergia_movil.exe`).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 114800](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20114800.md)

---

### [2026-11-02 11:37] Reubicación de Bahía al Lado de la Placa en Turnos y Despliegue Multi-Dispositivo v2.1.22+24 (Tripleta Automática)
* **Problema:** En `TurnoCardWidget`, el nombre de la bahía ("Garita") se mostraba en la columna lateral a la altura de la fila del conductor, robando espacio horizontal y truncando el tiempo de espera a `• Es...`.
* **Solución:** Reubicación de la bahía como badge elegante al lado de la placa en la Fila 1 (`WGM007 [Garita]`); liberación completa de la Fila 2 para que el conductor y la espera (`• Espera: 38 min`) respiren con el 100% del ancho de pantalla; eliminación del texto redundante en la columna trailing; verificación con 22/22 tests pasando y 0 issues en `flutter analyze`; bump a `v2.1.22+24`; despliegue verificado en Teléfono Xiaomi (`6tl7gupn9tnjdapb`), Tablet Lenovo (`HA27VLYC`) y Windows Desktop (`synergia_movil.exe`).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 113700](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20113700.md)

---

### [2026-11-02 11:23] Limpieza de Fila 1 en Despachos (Eliminación de Sobre-saturación) y Despliegue Multi-Dispositivo v2.1.21+23 (Tripleta Automática)
* **Problema:** En `DespachoCardWidget` se renderizaba `turno.name` (`"Turno #5 [WGN899 - JOHAN DARIO COLINA]"`), consumiendo todo el ancho de pantalla y expulsando la hora y el valor fuera de la vista en móviles, además de duplicar la placa y el conductor.
* **Solución:** Eliminación total del contenedor de `turno.name` en la Fila 1 de `DespachoCardWidget`; maquetación limpia: Placa a la izquierda, Hora a su lado y Valor al extremo derecho; verificación con 22/22 tests pasando y 0 issues en `flutter analyze`; bump a `v2.1.21+23`; despliegue verificado en Teléfono Xiaomi (`6tl7gupn9tnjdapb`), Tablet Lenovo (`HA27VLYC`) y Windows Desktop (`synergia_movil.exe`).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 112300](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20112300.md)

---

### [2026-11-02 11:12] Calibración Canónica de Horas Odoo (COT), Fecha de Despacho y Despliegue Multi-Dispositivo v2.1.20+22 (Tripleta Automática)
* **Problema:** Discrepancia horaria de 5 horas en las tarjetas de la app (mostraba 05:11 AM cuando el reloj del teléfono y de Colombia marcaba 10:25 AM) y visualización de hora de llegada a la cola en vez de la hora real en que se despachó el vehículo.
* **Solución:** Diagnóstico empírico en servidor Odoo 11 revelando que `get_fecha_actual` ya entrega hora local Colombia (COT); corrección de `parseDate` y `parseOdooDateTime` eliminando la adición forzada de `'Z'` que provocaba una doble resta de 5 horas; deserialización de `fecha_despacho` en `TurnoModel` y priorización en `DespachoCardWidget`; registro de FIX-012 en `ERRORES.md`; formalización OpenSpec `calibracion-horas-despacho-odoo`; verificación estática (0 issues `flutter analyze`) y unitaria (22/22 tests pasando); bump a `v2.1.20+22`; compilación y despliegue físico verificado en Teléfono Xiaomi (`6tl7gupn9tnjdapb`), Tablet Lenovo (`HA27VLYC`) y Windows Desktop (`synergia_movil.exe`).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 111200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20111200.md) | [OpenSpec calibracion-horas-despacho-odoo](file:///c:/Workspaces/synergia_movil/openspec/changes/calibracion-horas-despacho-odoo/)

---

### [2026-11-02 10:15] Desacoplamiento Estricto de Tarjetas (Restauración de Turnos & DespachoCardWidget) (Tripleta Automática)
* **Problema:** Al aplicar el diseño de 3 filas en `TurnoCardWidget` se había afectado involuntariamente la tarjeta de turnos en cola (Pestaña 1), causando sobre-saturación y repetición de datos cuando el usuario solo solicitó cambios en Pagos y Despachos.
* **Solución:** Desacoplamiento formal en tres componentes especializados: `TurnoCardWidget` restaurado 100% a su diseño original intacto con columna trailing; creación de `DespachoCardWidget` dedicado para despachos (Pestaña 2 e Historial) con estructura de 3 filas (Fila 1: Placa, Turno, Hora, Valor; Fila 2: Conductor; Fila 3: Destino y Dirección/Nota); preservación de `PagoCardWidget` con sus 3 filas (Fila 1: Placa, Tiquete, Hora, Valor; Fila 2: Conductor; Fila 3: Bahía); verificación con 0 issues en `flutter analyze` y 21/21 tests pasando en `flutter test`; bump a `v2.1.19+21`; compilación y despliegue físico verificado en Teléfono Xiaomi, Tablet Lenovo y Windows Desktop.
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 101500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20101500.md) | [OpenSpec redisenio-tarjetas-pagos-despachos](file:///c:/Workspaces/synergia_movil/openspec/changes/redisenio-tarjetas-pagos-despachos/)

---

### [2026-11-02 10:05] Calibración Novedades Fundetaxcol y Rediseño de 3 Filas en Pagos y Despachos (Tripleta Automática)
* **Problema:** Desfase horario de 5 horas entre Odoo UTC y Hora Colombia en pagos/turnos reportado en novedades; saturación visual provocada si se añade la sigla "COT"; compresión de datos y falta de espacio para dirección/nota en tarjetas de despacho y bahía en pagos.
* **Solución:** Normalización UTC a Hora Local de Colombia (`parseOdooDateTime` / `parseDate`) sin el texto "COT"; destino por defecto "Caribe Plaza" y recargo nocturno $1.100 desde las 19:00 en `TurnoFormView`; rediseño simétrico de 3 filas en `PagoCardWidget` (Fila 1: Placa, Tiquete, Hora, Valor; Fila 2: Conductor; Fila 3: Bahía) y `TurnoCardWidget` (Fila 1: Placa, Turno, Hora, Valor; Fila 2: Conductor; Fila 3: Destino y Dirección/Nota); formalización OpenSpec `redisenio-tarjetas-pagos-despachos`; verificación estática (0 issues `flutter analyze`) y unitaria (21/21 tests `flutter test`); bump a `v2.1.18+20`; compilación y despliegue físico verificado en Teléfono Xiaomi, Tablet Lenovo y Windows Desktop.
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 100500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20100500.md) | [OpenSpec redisenio-tarjetas-pagos-despachos](file:///c:/Workspaces/synergia_movil/openspec/changes/redisenio-tarjetas-pagos-despachos/)

---

### [2026-11-02 08:12] Visibilidad Canónica de Versión, Trazabilidad y Despliegue Físico Multi-Dispositivo (Tripleta Automática)
* **Problema:** En campo no había certeza inmediata de qué compilación estaba activa en terminales móviles y de escritorio, propiciando confusiones con versiones legadas; la versión estaba confinada a `pubspec.yaml` sin presencia en el AppBar ni en los tiquetes impresos.
* **Solución:** Implementación de clase SSOT `AppVersion` (`v2.1.16+18`); chip interactivo en AppBar de `BahiaSelectedView` (acceso a diagnóstico); badge en `LoginView` con layout adaptativo `Wrap`; sincronización en `SettingsView`, `SettingInfoExtraView` y pie de tiquetes térmicos en `PrinterService`; formalización OpenSpec `visibilidad-version-trazabilidad`; verificación estática (0 issues `flutter analyze`) y unitaria (21/21 tests `flutter test`); compilación y despliegue físico verificado con scripts de la raíz en Móvil Xiaomi (`deploy_phone.bat`), Tablet Lenovo (`deploy_tablet.bat`) y Windows Desktop (`deploy_windows.bat`).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 081200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20081200.md) | [OpenSpec visibilidad-version-trazabilidad](file:///c:/Workspaces/synergia_movil/openspec/changes/visibilidad-version-trazabilidad/)

---

### [2026-11-02 07:07] Rectificación Canónica de Tarifas de Despacho, Sincronización de Bahías y Pagar y Enturnar contra Odoo 11 (Tripleta Automática)
* **Problema:** Los turnos despachados no se marcaban con `fecha_despacho` ni emitían al canal WebSocket `/dispatch` en Odoo 11 debido a tarifas estáticas hardcodeadas en la UI sin transmisión de `tarifa_id`; la bahía activa del backend quedaba desfasada al no invocar `set_state(current_bay)`; y `pagarYEnturnar` no creaba el pago formal en `fundetaxcol.pago`.
* **Solución:** Implementación de `TarifaSectorModel` y RPC `getTarifasSector()` / `setBahiaActiva()` en `OdooService`; integración reactiva en `TurnoController` y `TurnoFormView`; formalización OpenSpec `rectificacion-tarifas-despacho-odoo`; registro de FIX-011 en `ERRORES.md`; bump a `v2.1.15+17`; verificación empírica con `flutter analyze` (0 issues) y `flutter test` (21/21 tests passed).
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 070700](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20070700.md) | [OpenSpec rectificacion-tarifas-despacho-odoo](file:///c:/Workspaces/synergia_movil/openspec/changes/rectificacion-tarifas-despacho-odoo/)

---

### [2026-11-02 06:25] Auditoría y Reconstrucción Forense de Bases y Referencias Fundacionales (gstack + SDD + Engram)
* **Problema:** Necesidad de auditar y consolidar formalmente las fuentes primarias, repositorios de referencia preexistentes (`fundetaxcol_flutter`, `addons_fundetaxcol`, `fundetaxcol`, `server_rt_odoo`, `proxyServer`) y compromisos de arquitectura sobre los que se fundó el proyecto Synergia Móvil.
* **Solución:** Reconstrucción forense cruzando memorias persistentes en Engram (#472, #485, #497, #500, #554), bitácoras fundacionales de Octubre 2026 y especificaciones OpenSpec; documentación del linaje multiplataforma (Flutter 3, Android + Windows Desktop, Tema Dual Claro/Oscuro y capa de impresión híbrida); generación de bitácora diaria y atómica; persistencia en Engram.
* **Enlaces:** [Bitácora Diaria 02/11/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2002112026.md) | [Bitácora Sesión 062500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/02/Bitacora%2020261102%20062500.md)

---

### [2026-10-25 11:30] Resolución de Visibilidad de Despachos y Turnos en Cola — Paridad con Tableros Web (Tripleta Automática)
* **Problema:** En los tableros web de Odoo (`/tablero_turnos`) se visualizaban correctamente los turnos en atención, en espera y los despachos realizados en Garita y 29D, pero en la Tablet y el Teléfono la cola y los despachos aparecían 100% vacíos debido a la disparidad entre el ID de la sesión operativa diaria (`bahia_sesion_id`, ej: 8843) y el ID de la bahía física estática (`bahia_id`, ej: 4).
* **Solución:** Soporte dual en `TurnoModel` (`bahiaSesionId` y `bahiaBaseId`) y filtrado con correspondencia dual indestructible `(t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value)` en `TurnoController`; registro de FIX-010 en `ERRORES.md`; bump a `v2.1.14+16`; compilación y despliegue físico verificado en Tablet Lenovo, Teléfono Xiaomi y Windows Desktop.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 124100](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20124100.md) | [Bitácora Sesión 113000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20113000.md)

---

### [2026-10-25 11:05] Corrección de Enturnamiento, Despacho y Deserialización de Bahías (Tripleta Automática)
* **Problema:** En Sótano / Caribe Plaza, los vehículos enturnados (ej. `WGM405`) no se reflejaban en la cola de turnos en espera ni podían despacharse debido a que `TurnoController` enviaba `'anonimo': true` (provocando auto-despacho inmediato en Odoo 11) y `TurnoModel.fromJson` evaluaba `json['bahia_id'] is int` (resultando en 0 al recibir un Map).
* **Solución:** Deserialización polimórfica en `TurnoModel.fromJson` para `bahia_id`, `vehiculo_id` y `conductor_id`; resolución de vehículos y envío de `anonimo: false` y `state: 'espera'` en `TurnoController.enturnarVehiculo`; soporte de despacho con notas; bump a `v2.1.13+15`; compilación y despliegue físico verificado en Tablet Lenovo, Teléfono Xiaomi y Windows Desktop.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 110500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20110500.md) | [OpenSpec enturnamiento-despacho-coordinacion](file:///c:/Workspaces/synergia_movil/openspec/changes/enturnamiento-despacho-coordinacion/)

---

### [2026-10-25 09:55] Compilación y Despliegue de Ejecutable Nativo Windows Release (Tripleta Automática)
* **Problema:** Generación y verificación del binario nativo `.exe` para Windows cumpliendo FIX-001 (timestamp fresco) y FIX-006 (sincronización de fuentes C++ efímeros).
* **Solución:** Creación de `scripts/verify_and_deploy_windows.ps1` y runner `deploy_windows.bat`; purga previa del binario viejo; copia de fuentes C++ del motor; compilación con `flutter build windows --release`; verificación y lanzamiento en primer plano.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 095500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20095500.md)

---

### [2026-10-25 09:25] Despliegue Físico de Release APK v2.1.12+14 en Teléfono Móvil Xiaomi (Tripleta Automática)
* **Problema:** Despliegue de la versión `v2.1.12+14` (con búsqueda híbrida y deserialización polimórfica de pagos) en el teléfono móvil de pruebas.
* **Solución:** Detección de dispositivo Xiaomi Redmi Note 13 (`6tl7gupn9tnjdapb`); instalación automatizada con `deploy_phone.bat` (53.86 MB); lanzamiento en primer plano con `am start`; validación empírica con `dumpsys package` (`versionName=2.1.12`, `versionCode=14`).
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 092500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20092500.md)

---

### [2026-10-25 09:05] Deserialización Polimórfica y Búsqueda Híbrida de Pagos en Odoo (Tripleta Automática)
* **Problema:** En la sesión activa del 24 de Octubre no se mostraban los 58 pagos registrados (a pesar de ver turnos y despachos) debido a una excepción de tipado al deserializar diccionarios `Map` devueltos por `_get_data()`. Además, se requería opción de buscar pagos históricos de días anteriores reportada por Jairo Acosta.
* **Solución:** Deserialización polimórfica en `PagoRecaudoModel.fromJson`; método `buscarPagosHistoricosRemotos()` en `TurnoController`; botón interactivo en `PagoListView`; formalización OpenSpec `busqueda-hibrida-pagos-historicos`; bump a `v2.1.12+14`; compilación y despliegue físico verificado en Tablet `HA27VLYC`.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 090500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20090500.md) | [OpenSpec busqueda-hibrida-pagos-historicos](file:///c:/Workspaces/synergia_movil/openspec/changes/busqueda-hibrida-pagos-historicos/)

---

### [2026-10-25 08:33] Despliegue Físico en Tablet HA27VLYC y Optimización de la Suite de Despliegue (Tripleta Automática)
* **Problema:** La tablet Lenovo estaba en estado `unauthorized`; los scripts `.bat` al invocar `adb` dentro de `for /f` sufrían deadlock por herencia de pipes con el daemon en segundo plano (`tcp:5037`); y se requería actualizar la tablet a `v2.1.11+13` y auditar todos los deploy scripts.
* **Solución:** Autorización de la tablet vía ADB; despliegue físico verificado de `app-release.apk` con `dumpsys package` (`versionName=2.1.11`); rediseño de `.bat` como runners que delegan directamente a PowerShell (FIX-008); creación de `detect_tablet.ps1`; actualización de `deploy_all.ps1` y `run_windows_exe.bat` bajo FIX-001 y FIX-002; registro en `ERRORES.md`.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 083300](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20083300.md)

---

### [2026-10-25 08:05] Compilación y Despliegue Físico Release APK v2.1.11+13 en Teléfono Móvil (Tripleta Automática)
* **Problema:** Despliegue e instalación de los cambios de paridad funcional en el dispositivo móvil de pruebas asegurando cumplimiento estricto del Gate FIX-002 de ERRORES.md.
* **Solución:** Incremento de versión a `2.1.11+13` en `pubspec.yaml`; compilación limpia de `app-release.apk` (53.83 MB); instalación vía ADB y lanzamiento en primer plano en Xiaomi Redmi Note 13 (`6tl7gupn9tnjdapb`); validación empírica con `dumpsys package`.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 080500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20080500.md)

---

### [2026-10-25 07:45] Paridad Funcional Canónica con fundetaxcol_flutter y Gobernanza OpenSpec (Tripleta Automática)
* **Problema:** Los coordinadores de terminal reportaron que la app no permitía buscar pagos ni turnos de otras bahías, no permitía buscar despachos transversalmente, mostraba "Conductor Desconocido" al ingresar placas (ej: `WGM776`) y se cerraba sola al suspender la pantalla en Android.
* **Solución:** Implementación de consultas multi-bahía en `TurnoController` con búsqueda transversal por texto; resolución de conductores reales en Odoo 11 mediante `fundetaxcol.vehiculo.partner`; autocompletado de conceptos y conductor en `PaymentFormView`; eliminación de `android:taskAffinity=""` en `AndroidManifest.xml`; formalización en OpenSpec y verificación 0 errores con `flutter analyze`.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 074500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20074500.md) | [OpenSpec paridad-funcional-fundetaxcol](file:///c:/Workspaces/synergia_movil/openspec/changes/paridad-funcional-fundetaxcol/)

---

### [2026-10-18 21:12] Fix de TURNO Repetido, Caddy en :80, Scripts en Raíz y Despliegue v2.1.10+12 (Tripleta Automática)
* **Problema:** En recibos de despacho se duplicaba "TURNO: TURNO # 12"; Caddy con IP a secas requería certificados SSL inválidos para Android; faltaban fuentes C++ en `cpp_client_wrapper` para Windows (.exe); y se requería acceso directo a todos los scripts `.bat` y `.ps1` en la raíz.
* **Solución:** Regex en `_extraerTurnoEnUnaLinea` para limpiar prefijos; Caddyfile configurado en `:80` limpio; fuentes C++ sincronizadas desde SDK Flutter (FIX-006); scripts `.bat` y `.ps1` en la raíz (FIX-008); despliegue verificado de `v2.1.10+12` en móvil y Windows.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 211200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20211200.md)

---

### [2026-10-18 20:12] Activación de Endpoint Directo RAW en C:\proxyServer e Impresión Nativa desde Tablet (Tripleta Automática)
* **Problema:** La tablet enviaba tiquetes a `C:\proxyServer` vía `/hw_proxy/print_xml_receipt` (HTML), pasando por `wkhtmltopdf` y Ghostscript con `-dPDFFitPage`, provocando que el tiquete saliera enano, reducido y demorado, en contraste con el PC que imprimía a tamaño real nativo.
* **Solución:** Implementado endpoint `/hw_proxy/print_raw` en `C:\proxyServer\src\routes.py` con inyección directa `win32print` RAW; actualizado `PrinterService` en Flutter para enviar prioritariamente los bytes ESC/POS en base64; bump a `v2.1.9+11` y despliegue físico verificado en la tablet con `./deploy_tablet.bat`.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 201200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20201200.md)

---

### [2026-10-18 19:50] Scripts de Despliegue en Raíz, Fuente B en Tiquetes y Actualización de Login (Tripleta Automática)
* **Problema:** Necesidad de comandos directos para compilar y lanzar Windows .exe y desplegar a Tablet y Móvil desde la terminal sin comandos manuales complejos; tamaño de fuente del conductor en tiquete aún muy visible y usuarios obsoletos en login.
* **Solución:** Creación de `run_windows_exe.bat`, `deploy_tablet.bat` y `deploy_phone.bat` en la raíz (y en `scripts/`); comando ESC/POS `ESC M 1` (Fuente B condensada) y reducción a 9px en HTML para el conductor; actualización de accesos rápidos de Login; compilación y verificación física en tablet con `dumpsys package` (v2.1.8+10).
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 195000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20195000.md)

---

### [2026-10-18 17:55] Armonización Visual Global Amarillo Taxi y Negro (Tripleta Automática)
* **Problema:** Necesidad de reflejar la identidad oficial del gremio taxista (Amarillo y Negro) con máximo contraste tanto en Modo Oscuro (noche) como en Modo Claro (sol) cumpliendo estándares de accesibilidad WCAG.
* **Solución:** Incorporación de tokens `taxiYellow` y `taxiBlackPure` en `AppColors`; avatares del turno en atención estilo placa oficial (Amarillo Taxi con número en Negro Puro `FontWeight.w900`); botones primarios y FAB ("PAGAR Y ENTURNAR") con contraste de 12.8:1 (WCAG AAA); armonización en `AppTheme`, `TurnoCardWidget`, `PagoCardWidget` y `BahiaSelectedView`.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 175500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20175500.md) | [OpenSpec taxi-yellow-black-palette](file:///c:/Workspaces/synergia_movil/openspec/changes/taxi-yellow-black-palette/)

---

### [2026-10-18 17:46] Persistencia Local por Usuario de Impresión y Scroll en Landscape (Tripleta Automática)
* **Problema:** Pérdida de ajustes de impresora térmica al reiniciar o cambiar sesión (Odoo 11 no maneja hardware térmico cliente); bloqueo de scroll en panel lateral izquierdo en smartphones horizontales (`_buildTabletLayout`).
* **Solución:** Implementación de Key Scoping `user_pref_${usuario}_printer_config` en `PrinterService` y `SettingsView`; carga reactiva en `TurnoController`; incorporación de `SingleChildScrollView` y eliminación de `Spacer()` en `home_view.dart`; creación de `DespachoHistoryView` con buscador WhatsApp.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 174600](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20174600.md) | [OpenSpec user-preferences-landscape-scroll](file:///c:/Workspaces/synergia_movil/openspec/changes/user-preferences-landscape-scroll/)

---

### [2026-10-18 07:50] Filtrado Estricto de Cola de Turnos y Sesión Activa Odoo 11 (Tripleta Automática)
* **Problema:** En `HomeView`, "COLA DE TURNOS EN BAHÍA" mostraba 211 vehículos mezclando turnos ya despachados con tarifa ($12.000, $15.000) y cancelados de toda la jornada.
* **Solución:** Implementados getters reactivos `turnosEnCola` (`!esDespacho && !cancelado`), `turnosDespachados` y `turnoEnAtencion`. Integrada consulta de `fundetaxcol.settings.mobile.get_data` para sincronizar `current_session` y `current_bay`. Columna central de `HomeView` exclusiva para fila activa y botón directo de Historial de Despachos en AppBar.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 075000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20075000.md) | [SDD Cola de Turnos](file:///c:/Workspaces/synergia_movil/docs/sdd-cola-turnos-sesion-activa-20261018.md)

---

### [2026-10-18 00:50] Paridad Integral de Vistas Fundetaxcol (Tripleta Automática)
* **Problema:** Paridad 1 a 1 de todas las vistas, shell de 3 pestañas (Pagos, Turnos, Despachos), selector de bahías corregido y soporte contable completo.
* **Solución:** Implementación de `BahiaSelectedView`, `TurnoListView`, `DespachoListView`, `PagoListView`, `TurnoFormView`, `PaymentFormView`, `PaymentConceptForm`, `SearchGenericWidget` y suite de 19 tests unitarios.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 005000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20005000.md)

---

### [2026-10-17 17:40] Análisis de Empaquetado APK y Conexión de Datos
* **Problema:** Determinar cuál proyecto de referencia genera APK y cómo se conectan al backend (IP vs Dominio).
* **Solución:** Identificado `fundetaxcol_flutter` como el proyecto móvil APK con conexión vía dominio (`fundetaxcol.co:80` + port `3000`), mientras `fundetaxcol` es Python/Flet.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 174030](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20174030.md)

---

### [2026-10-17 17:54] Arquitectura de Caddy Server y Soporte Dual HTTPS
* **Problema:** Habilitar HTTPS en `fundetaxcol.co` sin romper terminales legacy ni depender de cron jobs manuales de SSL.
* **Solución:** Elección de Caddy v2 como reverse proxy con TLS automático y modo dual (HTTP para legacy, HTTPS para Synergia Móvil) redirigiendo a Odoo en `127.0.0.1:8069`.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 175430](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20175430.md) | [Doc Caddy](file:///c:/Workspaces/synergia_movil/docs/ARQUITECTURA_CADDY_SERVER.md)

---

### [2026-10-17 18:32] Diagnóstico de Rendimiento (CPU 98%) e Integración de Fail2ban
* **Problema:** CPU al 98.1% por escaneo masivo de bots en puerto 80 sin proxy; necesidad de blindar el servidor con Fail2ban sin riesgo de bloqueo a IPs de gestión.
* **Solución:** Incorporación de Fail2ban con lista blanca inmutable (`190.253.19.26`, `190.242.47.74`), Caddy como escudo y `workers = 2` en Odoo.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 183200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20183200.md) | [Plan Despliegue](file:///c:/Workspaces/synergia_movil/docs/PLAN_DESPLIEGUE_CADDY_FAIL2BAN.md) | [Diagnóstico](file:///c:/Workspaces/synergia_movil/docs/DIAGNOSTICO_RENDIMIENTO_Y_LOGS.md)

---

### [2026-10-17 18:35] Diagnóstico de Timezone, Servicio de Sockets y Descarga de Producción
* **Problema:** Desfase de 1 hora en tiquetes impresos; necesidad de identificar el servicio de conexión móvil y traer los módulos reales de producción.
* **Solución:** Identificada zona `America/Montreal` como causa raíz; localizado y auditado `server_rt_odoo` (Node.js/Socket.IO en puerto 3000 con typo en systemd); descargados localmente `addons_fundetaxcol` y `server_rt_odoo`.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 183549](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20183549.md) | [Diagnóstico Timezone](file:///c:/Workspaces/synergia_movil/docs/DIAGNOSTICO_TIMEZONE_Y_SERVICIOS_PRODUCCION.md)

---

### [2026-10-17 19:01] Implementación del Core Multiplataforma Flutter 3 (Android y Windows)
* **Problema:** Fragmentación tecnológica entre app móvil legacy HTTP y sistema de escritorio Odoo.
* **Solución:** Creación de Synergia Móvil (`com.synergia.movil`) en Flutter 3 con SDD formal, `NetworkConfig` sanitizado, tema visual dark y controlador GetX.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 190133](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20190133.md) | [SDD Core](file:///c:/Workspaces/synergia_movil/docs/sdd-core-multiplataforma-20261017.md)

---

### [2026-10-17 19:25] Tripleta Completa: Servicios Odoo, Sockets, Impresión Térmica Dual y Adaptabilidad Tri-Dispositivo
* **Problema:** Dotar al sistema de todos los componentes operativos (Odoo JSON-RPC, Sockets, Impresión ESC/POS con corte) y asegurar responsividad 100% en los 3 factores de forma (Smartphone, Tablet/POS, PC).
* **Solución:** Implementados `PrinterService` (bytes binarios y emulador visual), `OdooService`, `SocketService`, `SettingsView`, y diseño adaptativo tri-dispositivo verificado con 8 tests al 100%.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 192500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20192500.md) | [SDD Servicios](file:///c:/Workspaces/synergia_movil/docs/sdd-servicios-odoo-impresion-realtime-20261017.md)

---

### [2026-10-17 19:40] Compilación de Binarios Nativos e Instalación Directa v2.0.0+1
* **Problema:** Generar ejecutables nativos para PC de escritorio (`.exe`) y paquete APK universal para móvil/tablet, actualizando versión a `2.0.0+1` e instalando en dispositivo físico.
* **Solución:** Compilado `synergia_movil.exe` (Windows x64 Release), ensamblado `app-release.apk` (v2.0.0+1, 50.9 MB) e instalado exitosamente vía ADB en Xiaomi `23117RA68G`.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Ejecutable Windows](file:///c:/Workspaces/synergia_movil/build/windows/x64/runner/Release/synergia_movil.exe) | [APK Release](file:///c:/Workspaces/synergia_movil/build/app/outputs/flutter-apk/app-release.apk)
---

### [2026-10-17 20:25] Tripleta Automática: Paridad Funcional Exacta, Dual Theme y Modelos Odoo 11
* **Problema:** Dotar a Synergia Móvil de paridad funcional exacta 1:1 con la app anterior, resolver el requerimiento mandatorio de Tema Claro y Oscuro, e integrar modelos DTO idénticos a producción.
* **Solución:** Implementado sistema dual de temas (`AppTheme.lightTheme` & `darkTheme`) con `ThemeController`, creados modelos `TurnModel`, `PaymentModel`, `CarModel`, `BayModel` y métodos RPC ampliados en `OdooService`. Verificado 100% con 8 pruebas.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 202500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20202500.md) | [SDD Paridad](file:///c:/Workspaces/synergia_movil/docs/sdd-funcionalidad-paridad-temas-recaudo-20261017.md) | [Dashboard HTML](file:///c:/Workspaces/synergia_movil/docs/analisis_comparativo.html)
---

### [2026-10-17 20:45] Compilación Release Exitosa (.exe y .apk) y Paridad 100% Funcional Entregada
* **Problema:** Compilación final y entrega directa de binarios nativos Release con paridad funcional completa Odoo 11 y soporte de temas Claro/Oscuro sin dependencias pendientes.
* **Solución:** Generados con 0 errores y 100% tests pasados los binarios nativos Release de Windows (`synergia_movil.exe`) y Android universal para móvil y tablet (`app-release.apk`, 54.6 MB).
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 204500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20204500.md) | [Ejecutable Windows](file:///c:/Workspaces/synergia_movil/build/windows/x64/runner/Release/synergia_movil.exe) | [APK Release](file:///c:/Workspaces/synergia_movil/build/app/outputs/flutter-apk/app-release.apk)
---

### [2026-10-17 21:30] Tripleta Completa: OpenSpec Apply `realtime-odoo-live-sync`
* **Problema:** Erradicar mock data de la app, conectar la sesión formal con Odoo 11, sincronizar las bahías activas de hoy (`29D`, `Garita`, `Av. Lago`) y consumir turnos reales en tiempo real vía WebSocket.
* **Solución:** Implementado cambio OpenSpec `realtime-odoo-live-sync` (12/12 tareas completadas). Eliminado `cargarTurnosSimulados()`, agregado `LoginDialog`, soporte dual de transporte HTTP/Sockets y compilados binarios release Windows y Android libres de simulación.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 213000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20213000.md) | [OpenSpec Change](file:///c:/Workspaces/synergia_movil/openspec/changes/realtime-odoo-live-sync/)
---

### [2026-10-17 22:20] Solución Socket.IO 2.4.1, Métricas Reales y OpenSpec `login-gatekeeper-flow`
* **Problema:** Estado "Desconectado" en Socket.IO, métricas fijas maquetadas en la interfaz de escritorio y necesidad de un Gatekeeper para impedir el acceso a la app si no se ha iniciado sesión en Odoo.
* **Solución:** Alineado protocolo Socket.IO a v2.4.1 con `socket_io_client: ^1.0.2` (enlace en vivo exitoso con `fundetaxcol.co:3000`), sustitución de cifras estáticas por reactivas sobre turnos reales, corrección de casteo en Odoo 11 e implementación del Gatekeeper de autenticación raíz con pantalla `LoginView` dedicada y retorno obligatorio al cerrar sesión.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 222000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20222000.md) | [OpenSpec Change](file:///c:/Workspaces/synergia_movil/openspec/changes/login-gatekeeper-flow/)



---

### [2026-10-17 23:05] Parseo Polimórfico de Placas (Odoo get_all Map) e Inyección Binaria RAW Spooler Windows ("TIQUETES" USB001)
* **Problema:** Los turnos mostraban el conductor pero salían con `'SIN-PLACA'` debido a que Odoo retorna Many2one como Diccionarios (`Map`) en `get_all` y no Listas; y la impresora física no expulsaba papel porque `TipoImpresora.spoolerWindows` tenía un stub vacío.
* **Solución:** Implementado parseo polimórfico en `TurnoModel.fromJson` soportando `Map`, `List`, `String`, anónimos y regex fallback en `name`. Implementada inyección RAW directa al spooler Win32 (`winspool.drv` / `WritePrinter`) verificada con prueba física real en la impresora `"TIQUETES"` (código de salida 0). Actualizados binarios Windows y APK instalado en tablet.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2017102026.md) | [Bitácora Sesión 230500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/17/Bitacora%2020261017%20230500.md) | [SDD](file:///c:/Workspaces/synergia_movil/docs/sdd-turnos-placas-impresion-20261017.md)

---

### [2026-10-18 08:20] Diagnóstico gstack de Lentitud Crítica y Estabilización Servidor Odoo 11 fundetaxcol.co
* **Problema:** El servidor de producción `fundetaxcol.co` presentaba lentitud extrema (CPU al 98-100%, tiempos de respuesta HTTP de 30 a 60 segundos y caídas por timeout 504/408).
* **Solución:** Trazado de pila completa identificó transacciones zombi en PostgreSQL bloqueadas durante 52 días que inhabilitaban el `autovacuum`, provocando table bloat masivo (> 99%), un bucle infinito en el cron de correos (`interval_number = 0`) y contención continua del GIL de Python 3.6. Se terminaron las transacciones zombi, se corrigió el cron a 15 min, se ejecutó `VACUUM ANALYZE` en tablas críticas (reduciendo tuplas muertas de 350K a 0) y se reinició el servicio.
* **Métricas:** La CPU cayó de **98% a 0-3%**, el load average disminuyó a **0.16** y la latencia HTTP pasó de **60s a 64 milisegundos (mejora de 99.8%)**.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 082000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20082000.md) | [Diagnóstico Técnico](file:///c:/Workspaces/synergia_movil/docs/DIAGNOSTICO_LENTITUD_ODOO_Y_PLAN_ESTABILIZACION.md)

---

### [2026-10-18 09:30] Tripleta Completa: Resguardo de Código, 12 Índices B-Tree y Optimización Ficha Vehículos / Enturnado Odoo 11
* **Problema:** Al pasar entre vehículos en Odoo 11 o enturnar digitando la placa, el navegador se congelaba durante minutos con el spinner *"Todavía cargando... Por favor sea paciente."*. Además, no permitía buscar fácilmente conductores por Nombre cuando el conductor de hoy es un relevo.
* **Solución:** 
  1. **Resguardo Seguro:** Backup íntegro en `/opt/synergia/backups_addons/addons_fundetaxcol_backup_20261018_092514.tar.gz`.
  2. **12 Índices B-Tree Concurrentes:** Creados en PostgreSQL (`idx_turno_bahia_state`, `idx_turno_vehiculo_state`, `idx_vehiculo_name`, `idx_partner_identificacion`, `idx_partner_conductor`, etc.) sin bloqueos en producción.
  3. **Ficha de Vehículos Ultraliviana:** Reemplazadas tablas pesadas inline en notebook (2,071 pagos y 12,391 despachos) por Smart Buttons en la cabecera (`pago_count` y `turno_count`) con acciones de ventana bajo demanda.
  4. **Enturnado Instantáneo (Placa ➔ Conductor):** Reescribe `_onchange_vehiculo_id` usando `.mapped('conductor_id')` y fallback directo a propietario-conductor en 6.4 ms.
  5. **Búsqueda por Nombre:** Flexibilizado el dominio de `conductor_id` a `[('conductor','=',True)]` y sobreescrito `name_search` en `Conductor (res.partner)` para resolver en milisegundos por Nombre o Cédula.
  6. **Upgrade y Sincronización:** Ejecutado upgrade `odoo-bin -u fundetaxcol`, reiniciado servicio y sincronizado localmente en `C:\Workspaces\addons_fundetaxcol`.
* **Métricas:** 
  * Carga de vehículo: de **1.12 s a 24 ms** (**45x más rápido**).
  * Enturnado (Placa ➔ Conductor): de **minutos a 6.4 ms**.
  * Búsqueda por Nombre de conductor: **10 ms**.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 093000](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20093000.md) | [SDD Optimización Vehículos y Enturnado](file:///c:/Workspaces/synergia_movil/docs/SDD_OPTIMIZACION_VEHICULOS_Y_ENTURNADO_ODOO11.md)

### [2026-10-18 11:41] Auditoría de Pagos Odoo, Mapeo Contable Valor, Métricas Duales Cortas y ERRORES.md en Raíz
* **Problema:** En la app móvil el recibo de pago salía con `Monto: $ 0` a pesar de que el operador reportó 1 pago en el sistema. Además, la tarjeta de métricas mezclaba ingresos de caja de la empresa con tarifas de turnos despachados para pasajeros ($148.000 vs $45.000).
* **Solución:** 
  1. Identificada causa raíz en PostgreSQL Odoo 11: la columna de pago es `valor` (no `total`). Se ajustó `payment_model.dart` y `turno_controller.dart`.
  2. Desacopladas las métricas en UI con nombres cortos: `Recaudo Empresa` (ingresos de caja) y `Servicios Clientes` (tarifas despachos pasajeros) tanto en PC (`home_view.dart`) como en móvil (`BahiaSelectedView`).
  3. Reubicado `docs/errores.md` a la raíz como [`ERRORES.md`](file:///c:/Workspaces/synergia_movil/ERRORES.md) con FIX-005, FIX-006 y FIX-007.
  4. Compilado y validado empíricamente `synergia_movil.exe` (91.1 KB) y `app-release.apk` (v2.1.2+4).
### [2026-10-18 17:15] Rediseño Fiel de Listas WhatsApp/Telegram, OpenSpec en Tripleta y Verificación 19/19 Tests
* **Problema:** Listas con tarjetas cuadradas flotantes (`Card`) que reducían el área visible en móvil; buscador sin acceso directo y necesidad de formalizar especificaciones de Tripleta bajo OpenSpec.
* **Solución:** 
  1. Vinculada la skill `tripleta` a especificaciones formales mediante **OpenSpec** (`openspec/changes/`).
  2. Creado cambio OpenSpec `whatsapp-telegram-lists-redesign` (proposal, design, specs BDD, tasks).
  3. Rediseñadas las listas a formato plano continuo edge-to-edge con `ListView.separated` y divisores sangrados a 74px.
  4. Implementado número de turno en avatar (Opción 2) y `Conductor • Espera: X min` en tiempo real (Opción 1: Opción B).
  5. Buscador fijo en cápsula WhatsApp (`borderRadius: 24`) sin botones intermediarios debajo, ganando 40% de área útil.
  6. Soporte fiel para Modo Oscuro y Modo Claro con tokens nativos de WhatsApp en `AppColors`.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 171500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20171500.md) | [OpenSpec Change](file:///c:/Workspaces/synergia_movil/openspec/changes/whatsapp-telegram-lists-redesign/proposal.md)

---

### [2026-10-18 20:12] Endpoint RAW Directo en C:\proxyServer para Impresión Térmica Instantánea 80mm
* **Problema:** El proxy convertía los tiquetes HTML a PDF con wkhtmltopdf y luego a PostScript con Ghostscript, provocando impresiones lentas y reducidas a 58mm en papel de 80mm.
* **Solución:** Creado endpoint directo `/hw_proxy/print_raw` en `C:\proxyServer\src\routes.py` enviando bytes binarios ESC/POS directamente al Spooler Win32, eliminando dependencias de PDF y logrando salida instantánea a 80mm.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 201200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20201200.md)

---

### [2026-10-18 21:12] Optimización de Tiquete, Suite de Scripts Raíz y Proxy Caddy :80
* **Problema:** Palabra TURNO repetida en el encabezado del tiquete y necesidad de comandos simples de despliegue en Windows sin fallos de subshell batch.
* **Solución:** Sanitizado `_extraerTurnoEnUnaLinea` en `PrinterService`, creados scripts de automatización `.bat` y `.ps1` en la raíz, resuelto error C1083 en compilador C++ de Windows y desplegada v2.1.10+12.
* **Enlaces:** [Bitácora Diaria 18/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2018102026.md) | [Bitácora Sesión 211200](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/18/Bitacora%2020261018%20211200.md)

---

### [2026-10-18 21:51] Solución Integral Caddy Server HTTPS en Localhost y LAN con Bypass SSL en PrinterService
* **Problema:** Error `ERR_SSL_PROTOCOL_ERROR` / conexión rechazada en `https://localhost` y `https://192.168.6.227/` al omitir puerto 443 en Caddyfile, y rechazo de certificados locales por parte de Android/Dart al imprimir desde la app.
* **Solución:** Configurado `C:\proxyServer\Caddyfile` con `tls internal` para `192.168.6.227`, `localhost` y `127.0.0.1` en puertos 443 y 80, recargado Caddy en caliente (`caddy reload`). Adaptado `PrinterService` con `IOClient` (`badCertificateCallback = true`) y enrutamiento inteligente de IPs locales a `/hw_proxy/print_raw`. Verificado con prueba física de impresión térmica sobre HTTPS (`{"result": true}`), 21/21 tests OK y desplegado en Tablet `HA27VLYC`.
---

### [2026-10-25 07:45] Tripleta Completa: Paridad Funcional Absoluta con fundetaxcol_flutter
* **Problema:** En pruebas de campo con coordinadores (Jairo Acosta), la app solo buscaba pagos y turnos en la bahía Garita y no transversalmente en todas las bahías; los servicios despachados no mostraban el historial general del conductor; al ingresar placa salía "Conductor Desconocido" y la app se cerraba al demorar o suspender en Android.
* **Solución:** Implementada búsqueda transversal multi-bahía mediante patrón dual (`pagosFiltrados`, `turnosEnColaFiltrados`, `turnosDespachadosFiltrados`), auto-resolución de conductor y conceptos vía `fundetaxcol.vehiculo.partner`, catálogo oficial ampliado, y eliminación de `taskAffinity=""` en AndroidManifest para preservar la app en segundo plano. Cero errores en `flutter analyze`.
* **Enlaces:** [Bitácora Diaria 25/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2025102026.md) | [Bitácora Sesión 074500](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/10/25/Bitacora%2020261025%20074500.md) | [OpenSpec Change](file:///c:/Workspaces/synergia_movil/openspec/changes/paridad-funcional-fundetaxcol/)





- **20261107 102300**: [Bitacora 20261107 102300.md](file:///c:/Workspaces/synergia_movil/Bitacoras/2026/11/07/Bitacora%2020261107%20102300.md) - Hotfix Layout Settings, Reset de Tarifa en Despacho y Despliegue Dual v2.1.26+28 (Windows .exe + Xiaomi Redmi Note 13 Pro).
