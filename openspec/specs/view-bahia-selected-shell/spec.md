# OpenSpec: View Bahía Selected Shell (Centro de Comando de Bahía)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/main/bahia_selected_view.dart` (`BahiaSelectedView`)
- **Controlador**: `BahiaSelectedController` (`lib/controllers/root/bahia_selected.controller.dart`)
- **Controlador de WebSocket**: `SocketController` (`server_rt_odoo` en puerto 3000)
- **Componente de Búsqueda**: `TitleSearchWidget` (`lib/ui/widgets/title_search_widget.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/04_bahia_selected_shell_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│ [🔍 Buscar turno/pago...]             (⋮)    │
├──────────────────────────────────────────────┤
│             [ BODY DINÁMICO ]                │
│       (IndexedStack con vista activa)        │
├──────────────────────────────────────────────┤
│    💳 Pagos   │   🚕 Turnos   │  🚪 Despachos │
└──────────────────────────────────────────────┘
```
- **3 Pestañas Fijas**:
  1. `PagoListView` (`Icons.payment`)
  2. `TurnoListView` (`Icons.login`)
  3. `DespachoListView` (`Icons.logout`)
- **AppBar Dinámico**:
  - `TitleSearchWidget` que delega la búsqueda reactiva a la pestaña activa (`search(value)`).
  - Menú contextual `(⋮)`: Bahías (`set_state(go_to_bays: true)`), Ajustes (`SettingsView`), Salir (cierre de sesión).
- **Socket.IO en Vivo (Puerto 3000)**: Escucha `turn`, `dispatch`, `payment` y `session`.

---

## Requirements

### Requirement: Arquitectura Shell con Tres Pestañas Nativas
El sistema DEBE proveer un contenedor maestro `BahiaSelectedView` que organice la operativa diaria mediante un `BottomNavigationBar` de tres pestañas fijas: Pagos (`PagoListView`), Turnos (`TurnoListView`) y Despachos (`DespachoListView`), conservando el estado de cada vista al alternar entre ellas.

#### Scenario: Cambio de pestaña operativa instantáneo
- **WHEN** el despachador pulsa cualquiera de las tres pestañas en la barra inferior
- **THEN** el sistema DEBE alternar la vista correspondiente en pantalla completa de forma instantánea sin perder los datos cargados ni la posición de desplazamiento.

### Requirement: Buscador Universal en AppBar
El sistema DEBE proveer en la AppBar del Shell un componente de búsqueda interactivo (`TitleSearchWidget`) que delegue la consulta en tiempo real al controlador de la pestaña que se encuentre actualmente activa.

#### Scenario: Búsqueda reactiva en pestaña activa
- **WHEN** el usuario escribe un término en el buscador de la AppBar
- **THEN** la vista activa DEBE filtrar sus tarjetas de inmediato (por placa o conductor) aplicando la función `search(value)`.

### Requirement: Sincronización WebSocket en Tiempo Real
El contenedor maestro DEBE suscribirse al servidor WebSocket (`server_rt_odoo` en el puerto 3000) y reaccionar ante los eventos de actualización del sistema.

#### Scenario: Recepción de evento de turno o despacho
- **WHEN** el servidor emite un evento `turn` o `dispatch`
- **THEN** el sistema DEBE actualizar automáticamente las listas en memoria de turnos y despachos reflejando los cambios sin requerir recarga manual.

#### Scenario: Cierre remoto de sesión
- **WHEN** el servidor emite el evento `session` indicando cierre de jornada en Odoo
- **THEN** el sistema DEBE notificar al operador, limpiar la sesión y redirigir atómicamente a `LoginWidget`.
