# OpenSpec: View Turno Management (Gestión de Turnos en Bahía)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con el módulo de turnos de `fundetaxcol_flutter`, integrando:
- **Vista de Lista**: `lib/ui/views/list/turno_list_view.dart` (`TurnoListView`)
- **Vista de Formulario**: `lib/ui/views/form/turno_form_view.dart` (`TurnoFormView` en modo "Enturnar")
- **Controladores**:
  - `TurnListController` (`lib/controllers/list/turn_list.controller.dart` con `isTurnValue: true`)
  - `TurnController` (`lib/controllers/models/turno.controller.dart` con `isTurn: true`, `entity.id == 0`)
- **Tarjeta Visual**: `TurnoCardWidget` (`lib/ui/widgets/turno_card_widget.dart`)
- **Controladores de Búsqueda Integrados**:
  - `CarSearchController` (`lib/controllers/search/vehiculo.search.controller.dart`)
  - `DriverSearchController` (`lib/controllers/search/conductor.search.controller.dart`)
- **Modelos DTO**: `TurnModel` (`lib/classes/turno.dart`), `CarModel` (`lib/classes/vehiculo.dart`), `DriverModel` (`lib/classes/conductor.dart`)
- **Almacenamiento Local**: `TurnStorage` (`lib/storage/turn.storage.dart`)

---

## Modelado de Datos y Contratos Odoo 11

### Modelo Odoo: `fundetaxcol.turno` (Estado En Cola / Progreso)
- `id` (`integer`): ID del turno
- `name` (`char`): Nombre descriptivo (`Turno #X [PLACA - BAHIA]`)
- `secuencia` / `sequence` (`integer`): Posición en la fila (1, 2, 3...)
- `fecha` (`datetime`): Timestamp de asignación del turno
- `state` (`selection`): `'progreso'` (en espera de despacho)
- `anonimo` (`boolean`): Bandera para taxis foráneos o de apoyo
- `placa_anonima` (`char`): Texto libre de la placa en mayúsculas (hasta 6 caracteres)
- `bahia_id` (`many2one`): Bahía operativa de la sesión
- `vehiculo_id` (`many2one`): Taxi registrado (`false` si `anonimo == true`)
- `conductor_id` (`many2one`): Conductor asignado
- `tarifa_id` (`many2one`): `false` o `0` mientras esté en cola de espera
- `user_id` (`many2one`): Operador de bahía que registró el turno

### Invocación RPC para Enturnar:
```json
{
  "model": "fundetaxcol.turno",
  "method": "actualizar",
  "args": [],
  "kwargs": {
    "bahia_id": "<currentBayId>",
    "anonimo": false,
    "placa_anonima": false,
    "vehiculo_id": 125,
    "conductor_id": 48,
    "tarifa_id": false
  }
}
```

---

## Componentes UI y Layout

### 1. `TurnoListView` (Cola de Espera)
- **Contenedor**: `SmartRefresher` con `WaterDropMaterialHeader(color: Colors.blue)` y `loadTurns(reload: true)`.
- **Estado Vacío**: Centrado con mensaje: `"No hay turnos en [Nombre Bahía]"`.
- **Tarjeta `TurnoCardWidget`**:
  - `CircleAvatar` amarillo con el número secuencial (`1`, `2`, `3`).
  - Título: **Placa en negrita y mayúsculas** (`WGN121`), hora formateada (`formatDateTime(fecha)`).
  - Subtítulo 1: Conductor en itálica + Bahía en azul.
  - Subtítulo 2: Nombre del usuario operador que enturnó.
  - Fondo: Blanco para turnos regulares; gris tenue (`Colors.grey.shade200`) para turnos anónimos.
- **Acciones**:
  - Floating Action Button `(+)`: Abre `TurnoFormView` en modo "Enturnar" (`id == 0`).
  - Tap en tarjeta: Abre `TurnoFormView` en modo "Despachar" (`id != 0`).

### 2. `TurnoFormView` (Modo Enturnar)
- **Switch Anónimo (`CupertinoSwitch`)**:
  - Si está activo: Oculta el selector de vehículos del padrón, habilita campo `TextFormField` con fondo morado suave (`Colors.purple.shade50`), `maxLength: 6`, `TextCapitalization.characters` y asigna automáticamente el conductor genérico del sistema (`settings.driver`).
  - Si está inactivo: Muestra el selector de placa modal.
- **Selector de Placa (`SearchGenericWidget<CarSearchController>`)**:
  - Excluye vehículos que ya se encuentren en cola (`carsToExclude`).
  - Al seleccionar un vehículo, inspecciona `vehiculo.conductorIds` y precarga inmediatamente el primer conductor de la lista.
- **Selector de Conductor (`SearchGenericWidget<DriverSearchController>`)**:
  - Divide la lista modal en dos secciones: **"Conductores principales"** (asociados al taxi) y **"Otros conductores"** (resto del padrón).
- **Botón Flotante Guardar (`Icons.save`)**: Valida formulario, envía RPC y regresa a la cola.

---

## Requirements

### Requirement: Cola de Espera de Turnos en Tiempo Real
El sistema DEBE presentar en `TurnoListView` la lista ordenada ascendentemente de todos los vehículos en espera asignados a la bahía activa cuyo campo `tarifaId.id == 0` y `state != 'cancelado'`, renderizando cada elemento en una tarjeta `TurnoCardWidget` con su número de turno, placa, conductor y hora.

#### Scenario: Visualización de vehículos en cola
- **WHEN** el despachador abre la pestaña de Turnos
- **THEN** el sistema DEBE mostrar los turnos no despachados ordenados por secuencia (1, 2, 3...) con la placa destacada en negrita y avatar amarillo.

#### Scenario: Filtrado local estricto de la bahía activa
- **WHEN** el controlador carga los turnos en memoria
- **THEN** DEBE aplicar el filtro `turn.bahiaSesionId == settings.currentBay && turn.tarifaId.id == 0 && turn.state != 'cancelado'`, excluyendo turnos de otras bahías o ya despachados.

#### Scenario: Selección de turno para despacho
- **WHEN** el operador pulsa sobre una tarjeta de turno en cola
- **THEN** el sistema DEBE abrir `TurnoFormView` en modo despacho con los datos del taxi bloqueados.

---

### Requirement: Registro de Nuevo Turno (Enturnar)
El sistema DEBE proveer un formulario en `TurnoFormView` para registrar la llegada de un vehículo a la bahía, soportando tanto modo anónimo como búsqueda autocompletable con exclusión de vehículos en turno y precarga de conductor habitual.

#### Scenario: Enturnar vehículo regular con conductor habitual
- **WHEN** el operador busca y selecciona una placa en `CarSearchController`
- **THEN** el sistema DEBE autocompletar automáticamente el conductor principal asignado a ese vehículo y preparar el envío a Odoo.

#### Scenario: Prevención de duplicidad de turnos
- **WHEN** el operador abre el selector de placas
- **THEN** el selector DEBE excluir de los resultados cualquier vehículo que ya posea un turno activo en cola (`carsToExclude`).

#### Scenario: Modo Anónimo para vehículos foráneos o de apoyo
- **WHEN** el operador activa el switch de "Modo Anónimo"
- **THEN** el sistema DEBE habilitar un campo de texto libre para digitar la placa foránea (hasta 6 caracteres en mayúsculas) y asignar automáticamente el conductor genérico preconfigurado.

#### Scenario: Guardado y emisión de evento WebSocket
- **WHEN** el operador pulsa "Guardar" en `TurnoFormView`
- **THEN** el sistema DEBE invocar `fundetaxcol.turno.actualizar` por RPC, asignar el consecutivo oficial de la bahía, emitir el evento `turn` por WebSocket y refrescar la lista.
