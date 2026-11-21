# OpenSpec: View Shell Navigation (Centro de Comando de Bahía)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con el contenedor Shell de `fundetaxcol_flutter`, integrando:
- **Vista Canónica**: `lib/ui/views/main/bahia_selected_view.dart` (`BahiaSelectedView`)
- **Controlador**: `BahiaSelectedController` (`lib/controllers/root/bahia_selected.controller.dart`)
- **Controlador de WebSocket**: `SocketController` (`server_rt_odoo` en puerto 3000)
- **Componente de Búsqueda**: `TitleSearchWidget` (`lib/ui/widgets/title_search_widget.dart`)
- **Pestaña 1**: `PagoListView` (`lib/ui/views/list/pago_list_view.dart`)
- **Pestaña 2**: `TurnoListView` (`lib/ui/views/list/turno_list_view.dart`)
- **Pestaña 3**: `DespachoListView` (`lib/ui/views/list/despacho_list_view.dart`)

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│ [🔍 Buscar turno/pago...]             (⋮)    │
├──────────────────────────────────────────────┤
│                                              │
│             [ BODY DINÁMICO ]                │
│       (IndexedStack con vista activa)        │
│                                              │
├──────────────────────────────────────────────┤
│    💳 Pagos   │   🚕 Turnos   │  🚪 Despachos │
└──────────────────────────────────────────────┘
```

### 1. AppBar con Buscador Universal Dinámico
- Contiene `TitleSearchWidget`, permitiendo escribir texto incrementalmente.
- Cada pestaña implementa la interfaz `WidgetList` con el método `search(String value)`. Al escribir en la AppBar, el Shell delega la búsqueda al controlador de la pestaña que esté activa en ese instante.
- **Menú Contextual `PopupMenuButton` (⋮)**:
  - **Bahías**: Ejecuta RPC `fundetaxcol.settings.mobile.set_state(go_to_bays: true)` y navega de regreso a `BahiaListView`.
  - **Ajustes**: Abre `SettingsView` para configuración de impresora y autoPrint.
  - **Salir**: Destruye la sesión en memoria y enruta a `LoginWidget`.

### 2. Barra de Navegación Inferior (`BottomNavigationBar`)
- **Item 0 - Pagos**: Icono `Icons.payment`, título "Pagos", renderiza `PagoListView`.
- **Item 1 - Turnos**: Icono `Icons.login`, título "Turnos", renderiza `TurnoListView`.
- **Item 2 - Despachos**: Icono `Icons.logout`, título "Despachos", renderiza `DespachoListView`.
- El cuerpo debe utilizar `IndexedStack` o `PageView` con `AutomaticKeepAliveClientMixin` para preservar el scroll y los datos cargados sin recargar al alternar.

---

## Sincronización en Tiempo Real (WebSocket Puerto 3000)
El controlador `BahiaSelectedController` escucha el stream de `SocketController`:
```dart
SocketController().streamController.stream.listen((event) async {
  if (event == sessionId) {
    GlobalControllers.getPreferences().closeSession();
    await Get.offAll(() => MainApp.rootApp);
  } else if (event == turnId || event == dispatchId) {
    await turnWidget.controller.loadTurns();
    await dispatchWidget.controller.loadTurns();
  } else if (event == paymentId) {
    await paymentWidget.controller.loadPayments();
  }
});
```

---

## Requirements

### Requirement: Arquitectura Shell con Tres Pestañas Nativas
El sistema DEBE proveer un contenedor maestro `BahiaSelectedView` que organice la operativa diaria mediante un `BottomNavigationBar` de tres pestañas fijas: Pagos (`PagoListView`), Turnos (`TurnoListView`) y Despachos (`DespachoListView`), conservando el estado de cada vista al alternar entre ellas.

#### Scenario: Cambio de pestaña operativa instantáneo
- **WHEN** el despachador pulsa cualquiera de las tres pestañas en la barra inferior
- **THEN** el sistema DEBE alternar la vista correspondiente en pantalla completa de forma instantánea sin perder los datos cargados ni la posición de desplazamiento.

#### Scenario: Preservación de estado entre pestañas
- **WHEN** el operador filtra o hace scroll en la pestaña de Turnos y cambia a la pestaña de Pagos y luego regresa a Turnos
- **THEN** la lista de Turnos DEBE conservar intacta la posición de scroll y el estado de la cola.

---

### Requirement: Buscador Universal en AppBar
El sistema DEBE proveer en la AppBar del Shell un componente de búsqueda interactivo (`TitleSearchWidget`) que delegue la consulta en tiempo real al controlador de la pestaña que se encuentre actualmente activa.

#### Scenario: Búsqueda reactiva en pestaña activa
- **WHEN** el usuario escribe un término en el buscador de la AppBar
- **THEN** la vista activa DEBE filtrar sus tarjetas de inmediato (por placa o conductor) aplicando la función `search(value)`.

#### Scenario: Cierre de búsqueda con botón atrás (WillPopScope)
- **WHEN** el usuario pulsa el botón atrás del hardware o de la barra de navegación mientras el buscador está desplegado
- **THEN** el sistema DEBE contraer el buscador y limpiar el filtro sin cerrar la aplicación.

---

### Requirement: Sincronización WebSocket en Tiempo Real
El contenedor maestro DEBE suscribirse al servidor WebSocket (`server_rt_odoo` en el puerto 3000) y reaccionar ante los eventos de actualización del sistema.

#### Scenario: Recepción de evento de turno o despacho
- **WHEN** el servidor emite un evento `turn` o `dispatch`
- **THEN** el sistema DEBE invocar `loadTurns()` en segundo plano tanto en `TurnListController` como en `DispatchListController`, actualizando la UI sin parpadeos.

#### Scenario: Recepción de evento de recaudo
- **WHEN** el servidor emite un evento `payment`
- **THEN** el sistema DEBE invocar `loadPayments()` en `PaymentListController`, refrescando el listado de cobros.

#### Scenario: Cierre remoto de sesión
- **WHEN** el servidor emite el evento `session` indicando cierre de jornada en Odoo
- **THEN** el sistema DEBE notificar al operador, limpiar las credenciales volátiles y redirigir atómicamente a `LoginWidget`.
