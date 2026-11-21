# 🚪 Especificación de Vista 08: `DespachoListView`
## Historial de Turnos Despachados del Día con Tarifa y Reimpresión

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\views\list\despacho_list_view.dart`
- **Controlador:** `lib/controllers/list/turn_list.controller.dart` (`DispatchListController` heredando de `TurnListBaseController`)
- **Widget de Tarjeta:** `lib/ui/widgets/turno_card_widget.dart` (`TurnoCardWidget`)
- **Tipo de Componente:** `StatefulWidget` con `GetBuilder<DispatchListController>`

---

### 1. Propósito y Responsabilidad
Listar cronológicamente todos los vehículos que ya fueron despachados con pasajero asignado desde la bahía activa durante el día de trabajo. Permite al despachador verificar las salidas, auditar la tarifa sugerida y reimprimir el comprobante térmico físico si el pasajero o conductor lo solicitan.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Despachos — Bahía 29D                       │
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │ ( 3 ) WGN121               10:22 PM    │  │
│  │       CARLOS RAMIREZ       Bahía 29D   │  │
│  │       AEROPUERTO           $ 18.000    │  │
│  │       Usuario: operador1               │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ ( 2 ) FXT911               10:10 PM    │  │
│  │       MARIO GOMEZ          Bahía 29D   │  │
│  │       BOCAGRANDE           $ 15.000    │  │
│  │       Usuario: operador1               │  │
│  └────────────────────────────────────────┘  │
│                                              │
└──────────────────────────────────────────────┘
```
- **Contenedor Principal:** `SmartRefresher` con `WaterDropMaterialHeader` y `FundetaxcolCustomFooter`.
- **Estado Vacío:** `Center(child: Text('No hay despachos en [Nombre Bahía]'))`.
- **Separador:** `ListView.separated` con `SizedBox(height: 6.0)`.
- **Tarjeta [`TurnoCardWidget`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/turno_card_widget.dart):**
  - Leading: `CircleAvatar` con fondo amarillo y el número de secuencia.
  - Título: Placa en mayúsculas negrita a la izquierda, fecha/hora de despacho (`fechaDespacho`) a la derecha en itálica.
  - Fila de Subtítulo 1: Conductor en itálica mayúscula + Nombre de la Bahía en azul.
  - Fila de Subtítulo 2: **Nombre de la Ruta / Destino (`tarifaId.name`)** en negrita a la izquierda, y **Valor cobrado con formato monetario oficial (`$ 18.000`)** alineado a la derecha.
  - Fila de Subtítulo 3: `Usuario: [cajero/despachador]`.
  - Color de fondo: Blanco para turnos regulares; gris (`Colors.grey.shade200`) para turnos anónimos.
- **Acción al hacer Tap:**
  Al tocar una tarjeta, ejecuta `_.selectEntity(e)`:
  Abre `TurnoFormView` en modo consulta para **visualizar el detalle y reimprimir el tiquete de salida**.

---

### 3. Controlador Asociado: `DispatchListController`
- **Herencia:** `TurnListBaseController` con `isTurnValue: false`.
- **Carga de Datos (`loadTurns`):**
  ```dart
  Future<void> loadTurns({bool reload = false}) async {
    await loadPage(() async {
      entities = await TurnStorage.getAll(reload: reload);
      entitiesFound = await turnsByDefault();
    }, isLoading: !reload);
  }
  ```
- **Filtro Estricto de Despachos (`turnsByDefault`):**
  ```dart
  bool find(TurnModel turn) {
    // tarifaId.id != 0 determina que ya tiene sector asignado y está despachado
    return turn.bahiaSesionId == settings.currentBay && turn.tarifaId.id != 0;
  }
  final result = entities.where((e) => e.state != 'cancelado').where(find).toList();
  result.sort((a, b) => b.sequence.compareTo(a.sequence)); // Más recientes primero
  return result;
  ```
- **Búsqueda Reactiva (`search`):**
  Filtra la lista de despachos en memoria por placa, placa anónima, nombre de conductor o nombre de ruta (`tarifaId.name`).

---

### 4. Modelos DTO
- **`TurnModel`** (`lib/classes/turno.dart`):
  - `fechaDespacho`: `String` (Fecha y hora oficial de salida en Odoo).
  - `tarifaId`: `PathModel` (con `id`, `name`, `valor`, `nota`, `valorRecargo`).
  - `total`: `double` (Valor total cobrado incluyendo recargo nocturno).
