# OpenSpec: View Turno Form Enturnar (Ingreso de Taxi a Cola)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/form/turno_form_view.dart` (`TurnoFormView` con `isTurn: true`, `entity.id == 0`)
- **Controlador**: `TurnController` (`lib/controllers/models/turno.controller.dart`)
- **Buscadores**: `CarSearchController`, `DriverSearchController`
- **Referencia Técnica**: `docs/especificaciones_vistas/06_turno_form_enturnar_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Nuevo Turno                                 │
├──────────────────────────────────────────────┤
│  Anónimo:                              [ O ] │
│  ┌────────────────────────────────────────┐  │
│  │ Placa: [ WGN121                      ] │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ Conductor: [ CARLOS RAMIREZ          ] │  │
│  └────────────────────────────────────────┘  │
│                                       ┌───┐  │
│                                       │ 💾│  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Switch Anónimo (`CupertinoSwitch`)**:
  - Si activo: Campo de texto libre `TextFormField` morado (`Colors.purple.shade50`), `maxLength: 6`, `TextCapitalization.characters`. Conductor genérico de apoyo (`settings.driver`).
  - Si inactivo: Selector de flota formal con exclusión de taxis en turno.
- **Selector de Placa**: `SearchGenericWidget<CarSearchController>`. Excluye `carsToExclude`. Autocompleta primer conductor habitual.
- **Selector de Conductor**: `SearchGenericWidget<DriverSearchController>`. Divide en "Conductores principales" y "Otros conductores".
- **Botón Flotante Guardar (`Icons.save`)**.

---

## Invocación Odoo 11 RPC
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

## Requirements

### Requirement: Registro de Nuevo Turno en Cola
El sistema DEBE proveer un formulario en `TurnoFormView` para registrar la llegada de un vehículo a la bahía, soportando tanto modo anónimo como búsqueda autocompletable con exclusión de vehículos en turno y precarga de conductor habitual.

#### Scenario: Enturnar vehículo regular con conductor habitual
- **WHEN** el operador busca y selecciona una placa en `CarSearchController`
- **THEN** el sistema DEBE autocompletar automáticamente el conductor principal asignado a ese vehículo y preparar el envío a Odoo.

#### Scenario: Prevención de duplicidad de turnos
- **WHEN** el operador abre el selector de placas
- **THEN** el selector DEBE excluir de los resultados cualquier vehículo que ya posea un turno activo en cola (`carsToExclude`).

#### Scenario: Modo Anónimo para vehículos foráneos o de apoyo
- **WHEN** el operador activa el switch de "Modo Anónimo"
- **THEN** el sistema DEBE habilitar un campo de texto libre para digitar la placa foránea y asignar automáticamente el conductor genérico preconfigurado.
