# ➕ Especificación de Vista 06: `TurnoFormView` — Modo "Enturnar"
## Registro y Formulario de Ingreso de Taxis a la Cola

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\views\form\turno_form_view.dart`
- **Controlador:** `lib/controllers/models/turno.controller.dart` (`TurnController` con `isTurn: true`, `entity.id == 0`)
- **Tipo de Componente:** `StatefulWidget` con `GetBuilder<TurnController>`

---

### 1. Propósito y Responsabilidad
Registrar la llegada de un taxi a la bahía. Asocia el vehículo y su conductor, valida que el vehículo no esté ya en turno activo, autocompleta el conductor principal asignado al taxi y envía la creación a Odoo 11.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Nuevo Turno                                 │
├──────────────────────────────────────────────┤
│                                              │
│  Anónimo:                              [ O ] │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ Placa: [ WGN121                      ] │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ Conductor: [ CARLOS RAMIREZ          ] │  │
│  └────────────────────────────────────────┘  │
│                                              │
│                                       ┌───┐  │
│                                       │ 💾│  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```

#### 2.1 Switch de Modo Anónimo (`CupertinoSwitch`)
- Si está activo:
  - Oculta el selector de vehículos registrados.
  - Muestra un campo de texto `TextFormField` libre con fondo morado suave (`Colors.purple.shade50`), `maxLength: 6` y `TextCapitalization.characters` para ingresar placas foráneas o de apoyo.
  - Asigna automáticamente el conductor genérico del sistema (`settings.driver`).
- Si está inactivo: Despliega el autocompletado formal sobre la flota de Fundetaxcol.

#### 2.2 Selector de Placa (`SearchGenericWidget<CarSearchController>`)
- Campo de sólo lectura que al hacer tap abre la búsqueda incremental modal.
- **Regla de Exclusión Inviolable:**
  ```dart
  final carsToExclude = entities
      .where((e) => e.state != 'cancelado')
      .where((e) => e.tarifaId.id == 0)
      .map((e) => e.vehiculoId.id)
      .toList();
  ```
  Los taxis que ya tienen un turno en espera no aparecen en la lista de búsqueda.
- **Autocompletado de Conductor:** Al seleccionar el taxi, el controlador inspecciona `vehiculo.conductorIds`. Si tiene conductores registrados, **asigna y autocompleta inmediatamente al primer conductor de la lista**.

#### 2.3 Selector de Conductor (`SearchGenericWidget<DriverSearchController>`)
- Si el taxi tiene conductores asociados, los muestra en una sección superior destacada titulada **"Conductores principales"**. Abajo muestra **"Otros conductores"**.

---

### 3. Guardado e Invocación Odoo RPC
Al presionar el botón flotante `Guardar` (`Icons.save`):
```dart
final data = {
  'bahia_id': settings.currentBay,
  'anonimo': entity.anonimo,
  'placa_anonima': entity.placaAnonima,
  'vehiculo_id': entity.anonimo ? false : entity.vehiculoId.id,
  'conductor_id': entity.conductorId.id,
  'tarifa_id': false,
};
await BaseController.actualizar('fundetaxcol.turno', data);
```
Odoo ejecuta `set_sequence()`, actualiza el turno actual de la bahía y emite un broadcast Socket.IO al canal `fundetaxcol.turno.channel`.
