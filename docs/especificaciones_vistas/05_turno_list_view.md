# 🚕 Especificación de Vista 05: `TurnoListView`
## Cola de Turnos en Bahía (Taxis en Espera de Pasajero)

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\views\list\turno_list_view.dart`
- **Controlador:** `lib/controllers/list/turn_list.controller.dart` (`TurnListController`)
- **Widget de Tarjeta:** `lib/ui/widgets/turno_card_widget.dart` (`TurnoCardWidget`)
- **Tipo de Componente:** `StatefulWidget` con `GetBuilder<TurnListController>`

---

### 1. Propósito y Responsabilidad
Desplegar la fila reactiva de taxis en espera de servicio en la bahía activa. Los vehículos se muestran ordenados cronológicamente por su número de turno (`sequence`) y cambian de posición a medida que se despachan o cancelan.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Bahía 29D                                   │
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │ ( 1 ) WGN121               10:15 PM    │  │
│  │       CARLOS RAMIREZ       Bahía 29D   │  │
│  │       Usuario: operador1               │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ ( 2 ) FXS830               10:18 PM    │  │
│  │       JUAN PEREZ           Bahía 29D   │  │
│  │       Usuario: operador1               │  │
│  └────────────────────────────────────────┘  │
│                                              │
│                                       ┌───┐  │
│                                       │ + │  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Pull-To-Refresh:** `SmartRefresher` conectado a `_.loadTurns(reload: true)`.
- **Estado Vacío:** Mensaje centrado: `"No hay turnos en [Nombre Bahía]"`.
- **Tarjeta [`TurnoCardWidget`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/turno_card_widget.dart):**
  - Leading: `CircleAvatar` amarillo con el número secuencial (`1`, `2`, `3`).
  - Title: **Placa en mayúsculas y negrita** a la izquierda (`WGN121`), y hora formateada a la derecha (`formatDateTime(fecha)`).
  - Subtitle: Nombre del conductor en negrita/itálica, nombre de la bahía en azul, y operador que lo enturnó.
  - Color: Blanco para turnos normales; gris tenue (`Colors.grey.shade200`) para turnos anónimos.
- **Floating Action Button `(+)`:** Abre `TurnoFormView` en modo "Enturnar".
- **Tap en una Tarjeta:** Abre `TurnoFormView` en modo "Despachar".

---

### 3. Controlador Asociado: `TurnListController`
- **Filtro Local:**
  ```dart
  bool find(TurnModel turn) {
    return turn.bahiaSesionId == settings.currentBay && turn.tarifaId.id == 0 && turn.state != 'cancelado';
  }
  ```
- **Ordenamiento:**
  ```dart
  result.sort((a, b) => a.sequence.compareTo(b.sequence));
  ```
- **Búsqueda Incremental (`search`):**
  Permite filtrar al instante por placa, placa anónima o nombre del conductor.

---

### 4. Modelo DTO: `TurnModel` (`lib/classes/turno.dart`)
- `id`: `int`
- `sequence`: `int` (Posición en la fila)
- `fecha`: `String` (Fecha/hora de asignación)
- `anonimo`: `bool`
- `placaAnonima`: `String`
- `vehiculoId`: `CarModel` (con `name` y `conductorIds`)
- `conductorId`: `DriverModel` (con `name`)
- `bahiaId`: `BayModel`
- `tarifaId`: `PathModel` (`id == 0` mientras está en espera)
