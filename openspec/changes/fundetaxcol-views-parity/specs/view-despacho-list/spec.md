# OpenSpec: View Despacho List (Historial de Despachos del Día)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/list/despacho_list_view.dart` (`DespachoListView`)
- **Controlador**: `DispatchListController` (`lib/controllers/list/turn_list.controller.dart` con `isTurnValue: false`)
- **Widget de Tarjeta**: `TurnoCardWidget` (`lib/ui/widgets/turno_card_widget.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/08_despacho_list_view.md`

---

## Componentes UI y Layout
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
└──────────────────────────────────────────────┘
```
- **Contenedor**: `SmartRefresher` con `WaterDropMaterialHeader` y `FundetaxcolCustomFooter`.
- **Estado Vacío**: `Center(child: Text('No hay despachos en [Nombre Bahía]'))`.
- **Tarjeta `TurnoCardWidget`**:
  - `CircleAvatar` amarillo con número de secuencia.
  - Placa en negrita a la izquierda, hora de salida a la derecha.
  - Conductor en itálica + Bahía en azul.
  - Nombre de la ruta en negrita (`AEROPUERTO`) y valor con formato monetario (`$ 18.000`).
  - Nombre del usuario despachador.
- **Acción al hacer Tap**: Abre `TurnoFormView` en modo consulta para visualizar y reimprimir el tiquete físico.

---

## Controlador y Filtro Local
- Filtro en memoria:
  ```dart
  bool find(TurnModel turn) {
    return turn.bahiaSesionId == settings.currentBay && turn.tarifaId.id != 0 && turn.state != 'cancelado';
  }
  ```
- Ordenamiento descendente: `result.sort((a, b) => b.sequence.compareTo(a.sequence));`.

---

## Requirements

### Requirement: Historial Cronológico de Despachos en DespachoListView
El sistema DEBE proveer en `DespachoListView` la lista cronológica de todos los vehículos despachados en la bahía activa durante la jornada actual (`tarifaId.id != 0` y `state != 'cancelado'`), ordenados descendentemente por secuencia/hora de salida.

#### Scenario: Carga y renderizado del historial de despachos
- **WHEN** el despachador selecciona la pestaña "Despachos" en el Shell operativo
- **THEN** el sistema DEBE consultar `TurnStorage.getAll()` filtrando turnos donde `bahiaSesionId == settings.currentBay && tarifaId.id != 0 && state != 'cancelado'` y presentarlos en un `ListView.separated`.

#### Scenario: Visualización detallada en TurnoCardWidget
- **WHEN** se renderiza un despacho en la lista
- **THEN** la tarjeta DEBE mostrar avatar de secuencia, placa, hora de salida, conductor, bahía, destino, valor monetario formateado y usuario despachador.

#### Scenario: Reimpresión térmica desde la lista de despachos
- **WHEN** el despachador pulsa sobre una tarjeta de despacho
- **THEN** el sistema DEBE abrir `TurnoFormView` en modo consulta permitiendo reimprimir el comprobante térmico.
