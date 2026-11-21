# OpenSpec: View Turno List (Cola de Turnos en Bahía)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/list/turno_list_view.dart` (`TurnoListView`)
- **Controlador**: `TurnListController` (`lib/controllers/list/turn_list.controller.dart`)
- **Tarjeta Visual**: `TurnoCardWidget` (`lib/ui/widgets/turno_card_widget.dart`)
- **Modelo DTO**: `TurnModel` (`lib/classes/turno.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/05_turno_list_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Bahía 29D                                   │
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │ ( 1 ) WGN121               10:15 PM    │  │
│  │       CARLOS RAMIREZ       Bahía 29D   │  │
│  │       Usuario: operador1               │  │
│  └────────────────────────────────────────┘  │
│                                       ┌───┐  │
│                                       │ + │  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Contenedor**: `SmartRefresher` conectado a `loadTurns(reload: true)`.
- **Estado Vacío**: `"No hay turnos en [Nombre Bahía]"`.
- **Tarjeta `TurnoCardWidget`**:
  - `CircleAvatar` amarillo con número de secuencia (`1`, `2`, `3...`).
  - Placa en negrita mayúscula (`WGN121`), hora formateada a la derecha.
  - Conductor en itálica, bahía en azul y operador que enturnó.
  - Fondo blanco para turnos normales; gris tenue para turnos anónimos.
- **Acciones**:
  - Floating Action Button `(+)`: Abre `TurnoFormView` en modo "Enturnar".
  - Tap en tarjeta: Abre `TurnoFormView` en modo "Despachar".

---

## Controlador y Filtro Local
- Filtro en memoria:
  ```dart
  bool find(TurnModel turn) {
    return turn.bahiaSesionId == settings.currentBay && turn.tarifaId.id == 0 && turn.state != 'cancelado';
  }
  ```
- Ordenamiento ascendente: `result.sort((a, b) => a.sequence.compareTo(b.sequence));`.

---

## Requirements

### Requirement: Cola de Espera de Turnos en Tiempo Real
El sistema DEBE presentar en `TurnoListView` la lista ordenada ascendentemente de todos los vehículos en espera asignados a la bahía activa cuyo campo `tarifaId.id == 0` y `state != 'cancelado'`, renderizando cada elemento en una tarjeta `TurnoCardWidget`.

#### Scenario: Visualización de vehículos en cola
- **WHEN** el despachador abre la pestaña de Turnos
- **THEN** el sistema DEBE mostrar los turnos no despachados ordenados por secuencia con avatar amarillo, placa en negrita y conductor.

#### Scenario: Selección de turno para despacho
- **WHEN** el operador pulsa sobre una tarjeta de turno en cola
- **THEN** el sistema DEBE abrir `TurnoFormView` en modo despacho con los datos del taxi bloqueados.
