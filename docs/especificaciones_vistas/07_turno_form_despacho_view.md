# 🚀 Especificación de Vista 07: `TurnoFormView` — Modo "Despachar Turno"
## Asignación de Ruta, Recargo Nocturno, Cancelación e Impresión de Salida

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\views\form\turno_form_view.dart`
- **Controlador:** `lib/controllers/models/turno.controller.dart` (`TurnController` con `isTurn: true`, `entity.id != 0`)
- **Tipo de Componente:** `StatefulWidget` con `GetBuilder<TurnController>`

---

### 1. Propósito y Responsabilidad
Despachar un taxi que se encuentra en la bahía asignándole la ruta solicitada por el usuario/pasajero. Calcula automáticamente si aplica recargo nocturno, permite cancelar el turno con confirmación y emite el comprobante térmico físico de salida.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  [1] WGN121                                  │
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │ Placa: WGN121           [SOLO LECTURA] │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ Conductor: CARLOS RAM.  [SOLO LECTURA] │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ Destino: [ Aeropuerto                ] │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │       [ CANCELAR TURNO ] (Rojo)        │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│  Nota: Tarifa fija nocturna                  │
│  Valor: $ 18.000                             │
│                                       ┌───┐  │
│                                       │ 🖨️│  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```

#### 2.1 Datos Bloqueados en Solo Lectura
- Placa y Conductor permanecen fijos con `enabled: false`.

#### 2.2 Selector de Destino / Tarifa (`SearchGenericWidget<PathSearchController>`)
- Campo activo obligatorio para despachar.
- Consulta el catálogo de sectores en Odoo: `fundetaxcol.tarifa.sector`.
- **Cálculo Automático de Recargo Nocturno (`handleOnChangeTarifa`):**
  ```dart
  final now = DateTime.now();
  final times = settings.horaRecargo.split(':'); // Ej: "18:00:00"
  final h = int.parse(times[0]);
  final m = int.parse(times[1]);
  final s = int.parse(times[2]);
  
  bool conRecargo = false;
  if (now.hour > h || (now.hour == h && now.minute > m) || (now.hour == h && now.minute == m && now.second > s)) {
    conRecargo = true;
  }
  
  entity.tarifaId = PathModel.fromJson(json);
  final recargo = conRecargo ? entity.tarifaId.valorRecargo : 0;
  entity.total = entity.tarifaId.valor + recargo;
  entity.nota = entity.tarifaId.nota;
  ```

#### 2.3 Botón Cancelar Turno (Rojo)
- `CupertinoButton(color: Colors.red)`
- Despliega diálogo de confirmación:
  - Si el despachador confirma: Invoca RPC `fundetaxcol.turno.cancelar(id: entity.id)`. El turno desaparece de la cola en tiempo real.

#### 2.4 Footer Persistente (`persistentFooterButtons`)
- Muestra la nota del sector si existe.
- Muestra el valor en tipografía de tamaño 20 con formato monetario oficial (`$ 18.000`).

---

### 3. Guardado, Despacho e Impresión Física
Al presionar el botón flotante verde (`Icons.save` / `Icons.print`):
```dart
final data = {
  'id': entity.id,
  'tarifa_id': entity.tarifaId.id,
  'nota': entity.nota,
};
final result = await BaseController.actualizar('fundetaxcol.turno', data);
if (result != null) {
  final turn = TurnModel.fromJson(result);
  if (settings.autoPrint) {
    await printer.printTurn(turn); // <-- Dispara el tiquete físico
  }
  Get.back(result: result);
}
```
Odoo pasa el estado del turno a `'despachado'`, asigna `fecha_despacho = now()` y emite el evento WebSocket.
