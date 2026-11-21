# 🏛️ Especificación Funcional Exhaustiva: Vistas, Controladores, Modelos y Reglas de Negocio (1 a 1)
## Proyecto Canónico de Referencia: `fundetaxcol_flutter` para `synergia_movil`

- **Fecha:** 2026-10-17 23:45 COT
- **Estado:** Especificación Formal de Ingeniería (Modo Exploración `/openspec-explore`)
- **Ubicación Canónica:** `docs/especificacion_funcional_vistas_fundetaxcol.md`
- **Código Fuente Auditado:** `C:\Workspaces\fundetaxcol_flutter`
- **Destino de Implementación:** `c:\Workspaces\synergia_movil`

---

## 🗺️ Índice de Vistas del Sistema

| # | Identificador de Vista | Tipo | Archivo en `fundetaxcol_flutter` | Controlador Asociado |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `SplashWidget` / `RootWidget` | Raíz / Splash | `lib/ui/widgets/root/splash_widget.dart` | `RootController` |
| **2** | `LoginWidget` | Formulario Auth | `lib/ui/widgets/root/login_widget.dart` | `LoginController` |
| **3** | `BahiaListView` / `BahiaView` | Listado Selector | `lib/ui/views/list/bahia_list_view.dart` | `BayListController` |
| **4** | `BahiaSelectedView` | Shell Maestro (Tabs) | `lib/ui/views/main/bahia_selected_view.dart` | `BahiaSelectedController` |
| **5** | `TurnoListView` | Listado Reactivo | `lib/ui/views/list/turno_list_view.dart` | `TurnListController` |
| **6** | `TurnoFormView` [Enturnar] | Formulario Registro | `lib/ui/views/form/turno_form_view.dart` | `TurnController` (`isTurn: true`) |
| **7** | `TurnoFormView` [Despachar] | Formulario Despacho | `lib/ui/views/form/turno_form_view.dart` | `TurnController` (`isTurn: false`) |
| **8** | `DespachoListView` | Listado Histórico | `lib/ui/views/list/despacho_list_view.dart` | `DispatchListController` |
| **9** | `PagoListView` | Listado Recaudos | `lib/ui/views/list/pago_list_view.dart` | `PaymentListController` |
| **10** | `PaymentFormView` | Formulario Maestro | `lib/ui/views/form/pago_form_view.dart` | `PaymentController` |
| **11** | `PaymentConceptForm` | Modal Renglón Cobro | `lib/ui/views/form/pago_concepto_form_view.dart` | `PaymentConceptController` |
| **12** | `SearchPageWidget` | Modal Autocomplete | `lib/ui/views/search/search_widget.dart` | `ISearchBaseController` |
| **13** | `SettingsView` | Formulario Ajustes | `lib/ui/views/settings_view.dart` | `SettingsController` |
| **14** | `SettingInfoExtra` | Diagnóstico Lectura | `lib/ui/views/settings_view.dart` (Línea 150) | `PreferencesController` |

---

## 📋 Especificación Detallada Vista por Vista

---

### VISTA 1: `SplashWidget` y `RootWidget` (Arranque y Enrutador Inicial)

#### 1. Archivos Fuente
- Vista: [`lib/ui/widgets/root/splash_widget.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/root/splash_widget.dart) y [`root_widget.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/root/root_widget.dart).
- Controlador: [`lib/controllers/root/root.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/root/root.controller.dart).

#### 2. Objetos y DTOs
- `SettingModel`: Modelo que almacena `currentSession`, `currentBay`, `currentView`, `autoPrint`, `mac`.

#### 3. Interacción Odoo / LocalStorage
- Al montar, `LocalStorage.initialize()` abre la persistencia local.
- Invoca `authController.validateToken()` $\rightarrow$ Envía `checkSession()` al cliente Odoo con el `session_id` almacenado en SharedPreferences.

#### 4. Reglas de Negocio y Transiciones
```
                                ¿Token Válido?
                                 /          \
                             NO /            \ SÍ
                               ▼              ▼
                          LoginWidget     Consulta Odoo `fundetaxcol.settings.mobile.get_data`
                                          ├── currentView == 'bay'   ──> BahiaSelectedView (Abre directo)
                                          ├── currentView == 'bays'  ──> BahiaListView (Elige bahía)
                                          └── default                ──> HomeWidget / BahiaListView
```
- Tiempo de splash: `Duration(milliseconds: 1500)`.

---

### VISTA 2: `LoginWidget` (Autenticación Formal en Odoo 11)

#### 1. Archivos Fuente
- Vista: [`lib/ui/widgets/root/login_widget.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/root/login_widget.dart).
- Controlador: [`lib/controllers/root/login.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/root/login.controller.dart).

#### 2. Componentes UI
- Logotipo oficial de Fundetaxcol (`LogoWidget(size: 200)`).
- Input `TextFormField` Usuario (`login`).
- Input `TextFormField` Contraseña (`password`) con toggle de ocultar/mostrar.
- Botón principal de acceso "Iniciar Sesión" con spinner de carga (`BlurLoadingWidget`).
- Botón de engranaje o selector de ajustes de conexión (Host, Puerto, Base de Datos).

#### 3. Invocación RPC
- Endpoint Odoo: `/web/session/authenticate`.
- Payload: `{"db": "fundetaxcol", "login": username, "password": password}`.
- Almacenamiento: Guarda `session_id`, `uid`, `name`, `email` y limpia cachés de sesión previa.

---

### VISTA 3: `BahiaListView` / `BahiaView` (Selector de Bahías Activas)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/list/bahia_list_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/list/bahia_list_view.dart) y [`bahia_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/main/bahia_view.dart).
- Controlador: [`lib/controllers/list/bay_list.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/list/bay_list.controller.dart).
- Widget de Tarjeta: [`lib/ui/widgets/bahia_card_widget.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/bahia_card_widget.dart).

#### 2. Objetos y DTOs
- `BayModel`:
  ```dart
  class BayModel {
    int id = 0;
    String name = ''; // Asigna json['name_sec'] ?? json['name']
  }
  ```

#### 3. Invocación Odoo RPC Exacta
```dart
model: 'fundetaxcol.sesion.bahia',
method: 'search_read',
fields: ['id', 'name_sec'], // <-- OBLIGATORIO: name_sec trae el nombre corto
domain: [
  ['sesion_id', '=', settings.currentSession] // <-- OBLIGATORIO: solo la sesión de hoy
]
```

#### 4. UI y Comportamiento
- Lista con pull-to-refresh (`SmartRefresher`).
- Tarjetas limpias rectangulares mostrando el nombre corto en negrita (`29D`, `Garita`, `Av. Lago`) y el icono de ingreso `Icons.login`.
- **PROHIBIDO:** No debe mostrar fechas de sesiones pasadas ni avatares redondos con el ID numérico (`B8816`).
- Al seleccionar una bahía:
  - Invoca Odoo: `fundetaxcol.settings.mobile.set_state(uid: userId, current_bay: selected.id)`.
  - Actualiza `SettingsStorage`.
  - Navega mediante `Get.offAll(() => BahiaSelectedView(...))`.

---

### VISTA 4: `BahiaSelectedView` (Shell Central de Operaciones)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/main/bahia_selected_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/main/bahia_selected_view.dart).
- Controlador: [`lib/controllers/root/bahia_selected.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/root/bahia_selected.controller.dart).

#### 2. Componentes UI
- **AppBar Integrado (`TitleSearchWidget`):**
  - Campo de búsqueda reactivo: filtra la lista activa al tipear.
  - Menú contextual desplegable (`PopupMenuButton`):
    - `Bahías` (vuelve a `BahiaListView`).
    - `Ajustes` (abre `SettingsView`).
    - `Salir` (cierra sesión en Odoo y limpia almacenamiento local).
- **Body Dinámico:** Renderiza el widget de la pestaña activa.
- **BottomNavigationBar:** Barra inferior con exactamente **3 pestañas**:
  1. `Pagos` (`Icons.payment`) $\rightarrow$ `PagoListView`.
  2. `Turnos` (`Icons.login`) $\rightarrow$ `TurnoListView`.
  3. `Despachos` (`Icons.logout`) $\rightarrow$ `DespachoListView`.

#### 3. Escucha de Eventos WebSocket (Socket.IO Puerto 3000)
El controlador mantiene abierto un stream continuo con `server_rt_odoo`:
- Evento `'turn'` $\rightarrow$ Recarga automáticamente `TurnListController.loadTurns()`.
- Evento `'dispatch'` $\rightarrow$ Recarga automáticamente `DispatchListController.loadTurns()`.
- Evento `'payment'` $\rightarrow$ Recarga automáticamente `PaymentListController.loadPayments()`.
- Evento `'session'` $\rightarrow$ Cierra la sesión si el administrador la cerró en el servidor.

---

### VISTA 5: `TurnoListView` (Cola de Turnos en Bahía)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/list/turno_list_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/list/turno_list_view.dart).
- Controlador: [`lib/controllers/list/turn_list.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/list/turn_list.controller.dart).
- Widget de Tarjeta: [`lib/ui/widgets/turno_card_widget.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/turno_card_widget.dart).

#### 2. Invocación Odoo RPC y Filtrado
- Invoca RPC: `model: 'fundetaxcol.turno'`, `method: 'get_all'`, `kwargs: {'bahia_ids': settings.bahiaIds}`.
- Filtro local estricto:
  ```dart
  bool find(TurnModel turn) {
    return turn.bahiaSesionId == settings.currentBay && turn.tarifaId.id == 0 && turn.state != 'cancelado';
  }
  ```
- Ordenamiento: `result.sort((a, b) => a.sequence.compareTo(b.sequence));` (secuencia 1, 2, 3...).

#### 3. Renderizado de la Tarjeta (`TurnoCardWidget`)
- Círculo leading: Número de turno secuencial (`#sequence`).
- Título: **Placa en mayúsculas y negrita** (extraída del `vehiculoId.name` o `placaAnonima`), con la fecha/hora alineada a la derecha.
- Subtítulo: Nombre del conductor en mayúsculas, nombre de la bahía en azul, y usuario operador que enturnó.
- Color de fondo: Blanco para turnos normales, gris claro (`Colors.grey.shade200`) para turnos anónimos.

#### 4. Acciones del Operador
- **Botón Flotante `(+)`:** Abre `TurnoFormView` en modo "Enturnar".
- **Tap en una Tarjeta:** Abre `TurnoFormView` en modo "Despachar" para el turno seleccionado.

---

### VISTA 6: `TurnoFormView` — Modo "Enturnar" (Crear Turno en Cola)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/form/turno_form_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/form/turno_form_view.dart).
- Controlador: [`lib/controllers/models/turno.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/models/turno.controller.dart) instanciado con `TurnModel()` vacío y `isTurn: true`.

#### 2. Campos del Formulario
1. **Switch de Anónimo (`CupertinoSwitch`):**
   - Si `true`: Oculta el buscador de placa y muestra un campo `TextFormField` de texto libre con `maxLength: 6` y `TextCapitalization.characters` (ej. para vehículos de apoyo o foráneos). Asigna automáticamente el `conductor_id` genérico de la configuración.
2. **Selector de Placa (`SearchGenericWidget<CarSearchController>`):**
   - Solo visible si no es anónimo.
   - Lista vehículos de `fundetaxcol.vehiculo`.
   - **Regla de Exclusión:** `carsToExclude` filtra todos los vehículos que ya tengan un turno activo en cola (`state != 'cancelado' && tarifaId.id == 0`).
   - Al seleccionar la placa: **Autocompleta de inmediato el conductor principal asociado al vehículo** (`vehiculo.conductorIds[0]`).
3. **Selector de Conductor (`SearchGenericWidget<DriverSearchController>`):**
   - Divide la lista en dos secciones:
     - "Conductores principales" (los asignados al taxi seleccionado).
     - "Otros conductores" (el resto del padrón).

#### 3. Botón Guardar (Floating Action Button)
- Envía a Odoo vía RPC:
  ```dart
  data = {
    'bahia_id': settings.currentBay,
    'anonimo': entity.anonimo,
    'placa_anonima': entity.placaAnonima,
    'vehiculo_id': entity.anonimo ? false : entity.vehiculoId.id,
    'conductor_id': entity.conductorId.id,
    'tarifa_id': false,
  };
  BaseController.actualizar('fundetaxcol.turno', data);
  ```
- Odoo le asigna el consecutivo en base a `bahia.turno_actual`, emite broadcast por WebSocket y retorna el turno creado.

---

### VISTA 7: `TurnoFormView` — Modo "Despachar Turno" (Asignación de Ruta y Salida)

#### 1. Activación
- Se abre al hacer tap sobre un turno en `TurnoListView`.
- El controlador recibe el `TurnModel` existente (`entity.id != 0`, `isTurn: true`).

#### 2. Campos y Comportamiento UI
1. **Datos del Vehículo y Conductor en Solo Lectura:** El despachador visualiza la placa y el conductor ya enturnados.
2. **Selector de Destino / Tarifa (`SearchGenericWidget<PathSearchController>`):**
   - Consulta `fundetaxcol.tarifa.sector`.
   - Al seleccionar una ruta:
     - Extrae `tarifa.valor` y `tarifa.valorRecargo`.
     - **Cálculo Automático de Recargo Nocturno:**
       ```dart
       final times = settings.horaRecargo.split(':'); // Ej: "18:00:00"
       if (horaActual >= horaRecargo) {
         entity.total = tarifa.valor + tarifa.valorRecargo;
       } else {
         entity.total = tarifa.valor;
       }
       ```
     - Muestra la nota del sector si existe (`entity.nota`).
3. **Footer Persistente:** Muestra en texto grande destacado:
   - `Nota: [Texto nota]` (si aplica).
   - `Valor: $ 18,000` (con formato monetario).
4. **Botón Rojo "Cancelar Turno" (`CupertinoButton`):**
   - Muestra diálogo de confirmación: "¿Por favor confirme la cancelación del turno?".
   - Si confirma: Invoca RPC `fundetaxcol.turno.cancelar(id: entity.id)`.
5. **Botón Guardar / Despachar (Floating Action Button verde con icono de Guardar/Imprimir):**
   - Invoca `BaseController.actualizar('fundetaxcol.turno', {'id': entity.id, 'tarifa_id': entity.tarifaId.id, 'nota': entity.nota})`.
   - Si `settings.autoPrint == true`, **dispara de inmediato la impresión física del tiquete de salida en papel térmico de 58mm**.

---

### VISTA 8: `DespachoListView` (Historial de Despachos del Día)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/list/despacho_list_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/list/despacho_list_view.dart).
- Controlador: [`DispatchListController`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/list/turn_list.controller.dart) (`isTurnValue: false`).

#### 2. Funcionalidad y Filtrado
- Filtra turnos donde `tarifaId.id != 0` (turnos que ya fueron despachados).
- Tarjetas `TurnoCardWidget` mostrando:
  - Número de turno de salida.
  - Placa y Conductor.
  - **Ruta / Destino (ej. Aeropuerto, Bocagrande)**.
  - **Valor cobrado ($)**.
  - Fecha y hora exacta del despacho (`fechaDespacho`).
- **Acción al hacer Tap:** Abre el turno en `TurnoFormView` para **reimprimir el tiquete de salida** en cualquier momento del día.

---

### VISTA 9: `PagoListView` (Historial de Recaudos Diarios)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/list/pago_list_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/list/pago_list_view.dart).
- Controlador: [`PaymentListController`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/list/payment_list.controller.dart).
- Modelo: [`PaymentModel`](file:///C:/Workspaces/fundetaxcol_flutter/lib/classes/pago.dart).
- Widget de Tarjeta: [`PagoCardWidget`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/pago_card_widget.dart).

#### 2. Invocación Odoo RPC
- Consulta `fundetaxcol.pago` para la bahía actual:
  ```dart
  fields: ['id', 'consecutivo', 'fecha', 'total', 'ingreso', 'ahorro', 'bahia_id', 'vehiculo_id', 'conductor_id', 'concepto_ids']
  ```
- Ordenamiento: Descendente por consecutivo (`b.consecutivo.compareTo(a.consecutivo)`).

#### 3. Renderizado de la Tarjeta (`PagoCardWidget`)
- Leading: Número de índice del pago.
- Título: Placa y Fecha formateada.
- Subtítulo: Nombre del conductor, Consecutivo contable oficial (ej. `REC-0452`) y Total pagado en pesos (`$ 12,500`).
- Botón flotante `(+)`: Abre `PaymentFormView` para registrar un nuevo cobro.
- Tap en la tarjeta: Abre el pago para consultar el detalle de los conceptos y **reimprimir el comprobante térmico**.

---

### VISTA 10: `PaymentFormView` (Formulario Maestro de Cobro de Pagos)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/form/pago_form_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/form/pago_form_view.dart).
- Controlador: [`PaymentController`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/models/pago.controller.dart).

#### 2. Estructura y Flujo de Cobro
1. **Selector de Placa (`CarSearchController`):**
   - Selecciona el taxi a cobrar.
   - Autocompleta automáticamente el conductor habitual.
2. **Selector de Conductor (`DriverSearchController`):**
   - Al seleccionar conductor, **precarga automáticamente los conceptos configurados por defecto para ese conductor o el concepto de ingreso predeterminado** (ej. Rodamiento Diario $5.000).
3. **Sub-lista de Conceptos (`PaymentDetail`):**
   - Muestra cada renglón cobrado: Nombre del concepto, Cantidad x Valor unitario y Subtotal.
   - Botón `(X)` para eliminar renglones.
   - Botón `(+)` en AppBar: Abre `PaymentConceptForm` para agregar más conceptos (ej. Aportes sociales, Seguros, Cuota de administración).
4. **Footer Persistente:** Muestra la suma en tiempo real:
   - `Total: $ XX,XXX` calculado dinámicamente con `reduce((a, b) => a + b)`.
5. **Botón Guardar:**
   - Envía a Odoo la estructura relacional Many2many:
     ```dart
     'concepto_ids': [[0, 0, {'concepto_id': id, 'cantidad': cant, 'valor': val}]]
     ```
   - Odoo genera el recibo contable con su consecutivo.
   - Si `autoPrint == true`, **dispara la impresión física del recibo térmico contable**.

---

### VISTA 11: `PaymentConceptForm` (Modal de Adición de Concepto)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/form/pago_concepto_form_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/form/pago_concepto_form_view.dart).
- Controlador: [`PaymentConceptController`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/models/pago_concepto.controller.dart).
- Modelo: [`PaymentConceptModel`](file:///C:/Workspaces/fundetaxcol_flutter/lib/classes/pago_concepto.dart).

#### 2. Campos
1. **Selector de Concepto (`ConceptSearchController`):**
   - Consulta el catálogo `fundetaxcol.concepto` (`fields: ['id', 'name', 'valor', 'tipo']`).
   - Al seleccionar un concepto, **precarga automáticamente su valor unitario por defecto** en el campo de valor.
2. **Campo de Cantidad (`TextFormField` numérico):**
   - Por defecto: `1`.
   - Validación: Debe ser numérico y mayor a 0.
3. **Campo de Valor (`TextFormField` numérico):**
   - Precargado con el valor del concepto.
   - Validación: Debe ser numérico y mayor o igual a 0.
4. **Botón Hecho (`FloatingActionButton` con icono `Icons.done`):**
   - Valida el formulario y retorna el objeto `PaymentConceptModel` a `PaymentFormView`, sumándolo al total.

---

### VISTA 12: `SearchPageWidget` / `SearchGenericWidget` (Buscador Incremental Universal)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/search/search_widget.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/search/search_widget.dart).
- Controlador Base: [`lib/controllers/search/search.base.controller.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/search/search.base.controller.dart).

#### 2. Arquitectura de Autocompletado
Es un componente genérico altamente reutilizable `SearchGenericWidget<T extends ISearchBaseController>`:
- Se abre a pantalla completa con foco automático en el teclado.
- **Filtrado Incremental en Memoria:** Filtra mientras el usuario escribe sin saturar el servidor de peticiones.
- **Sección de Elementos Habituales (`firstSectionWidget`):**
  - Para conductores: Permite mostrar primero "Conductores principales del vehículo" en una sección gris destacada y abajo "Otros conductores".
- **Botón de Limpiar:** Borra el texto de búsqueda o cierra con `-1` (deseleccionar).
- **Controladores Especializados:**
  1. `CarSearchController` (`fundetaxcol.vehiculo` con exclusión de taxis en turno).
  2. `DriverSearchController` (`res.partner` con filtro Many2many).
  3. `PathSearchController` (`fundetaxcol.tarifa.sector`).
  4. `ConceptSearchController` (`fundetaxcol.concepto`).

---

### VISTA 13: `SettingsView` (Configuración del Sistema y Hardware)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/settings_view.dart`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/settings_view.dart).
- Controlador: [`SettingsController`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/global/settings.controller.dart).

#### 2. Opciones de Configuración
1. **Concepto de Ingreso por Defecto:** Permite seleccionar cuál concepto se agregará automáticamente al crear un nuevo cobro.
2. **Conductor de Apoyo / Genérico:** Conductor asignado a los turnos anónimos.
3. **Hardware de Impresión:**
   - Campo para ingresar la **Dirección MAC de la Impresora Bluetooth** (ej. `00:11:22:33:44:55`).
   - Switch de **"Imprimir pagos y despachos automáticamente"** (`autoPrint`).
4. **Botón Guardar:** Guarda en `LocalStorage` y sincroniza en Odoo `fundetaxcol.settings.mobile`.

---

### VISTA 14: `SettingInfoExtra` (Auditoría Técnica y Diagnóstico)

#### 1. Archivos Fuente
- Vista: [`lib/ui/views/settings_view.dart#L150`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/views/settings_view.dart#L150).
- Controlador: [`PreferencesController`](file:///C:/Workspaces/fundetaxcol_flutter/lib/controllers/global/preferences.controller.dart).

#### 2. Campos en Solo Lectura
- **Sección Conexión:** Servidor (`fundetaxcol.co`), Puerto (`80`), Base de Datos (`fundetaxcol`).
- **Sección Usuario:** Nombre del cajero/despachador y Correo electrónico.
- **Sección Aplicación:** Nombre de versión (`VERSION_NAME`) y Revisión de compilación (`REVISION_NAME`).

---

## 🖨️ Componente de Impresión Universal: `Printer` (`lib/utils/printer.dart`)

Genera tramas binarias exactas ESC/POS para papel de 58mm:

1. **Tiquete de Turno / Despacho (`_printTurn`):**
   - Número de Turno (`Turno: #125`).
   - Usuario despachador.
   - Destino / Ruta (`Destino: Aeropuerto`).
   - Valor sugerido monetario (`Valor sugerido: $ 18,000`).
   - Placa (`Placa: WGN121` o placa anónima).
   - Conductor.
   - Fecha y Hora de despacho.
   - Nota (si aplica).
   - Pie institucional de Fundetaxcol: Teléfonos, Email, Web, Report Footer y Timestamp.
   - Comando de corte automático (`generator.cut()`).

2. **Recibo de Pago / Recaudo (`_printPayment`):**
   - Consecutivo contable (`Consecutivo: REC-0452`).
   - Fecha, Usuario, Placa y Conductor.
   - **Tabla de Conceptos:** Columnas alineadas de Concepto y Valor.
   - Total Pago.
   - Desglose de Ahorros y Total Ahorros (si aplica).
   - Número de Ingresos.
   - Pie institucional y corte automático.

---

## 🚀 Plan de Adopción para `synergia_movil`

Para que `synergia_movil` alcance la paridad impecable que exige producción sin inventar nada nuevo:

1. **Replicar la navegación por 3 Tabs de `BahiaSelectedView`:**
   - Pestaña 1: **Pagos** (`PagoListView` + `PaymentFormView` + `PaymentConceptForm`).
   - Pestaña 2: **Turnos** (`TurnoListView` + `TurnoFormView` en modo Enturnar).
   - Pestaña 3: **Despachos** (`DespachoListView` + `TurnoFormView` en modo Despachar con recargo nocturno).
2. **Reemplazar el selector actual de bahías:** Usar `['id', 'name_sec']` y filtrar por la sesión de hoy (`sesion_id = currentSession`), eliminando la lista de 4 años de sesiones viejas.
3. **Mantener el soporte multiplataforma:** La misma lógica modular operará tanto en la tablet Lenovo Android como en el ejecutable Windows Desktop con la impresora térmica local.
