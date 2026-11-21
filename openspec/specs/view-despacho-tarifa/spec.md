# OpenSpec: View Despacho & Tarifa (Despachos y Salidas con Pasajero)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con el módulo de despachos de `fundetaxcol_flutter`, integrando:
- **Vista de Lista**: `lib/ui/views/list/despacho_list_view.dart` (`DespachoListView`)
- **Vista de Formulario**: `lib/ui/views/form/turno_form_view.dart` (`TurnoFormView` en modo despacho)
- **Controladores**:
  - `DispatchListController` (`lib/controllers/list/turn_list.controller.dart` con `isTurnValue: false`)
  - `TurnController` (`lib/controllers/models/turno.controller.dart` con `isTurn: true`, `entity.id != 0`)
- **Tarjeta UI**: `TurnoCardWidget` (`lib/ui/widgets/turno_card_widget.dart`)
- **Buscador de Destinos**: `PathSearchController` (`lib/controllers/search/tarifa.search.controller.dart`)
- **Modelos DTO**: `TurnModel` (`lib/classes/turno.dart`), `PathModel` (`lib/classes/path.dart`)
- **Servicios de Impresión**: `Printer` con `printTurn(turn)` vía Win32 spooler en Windows o Bluetooth en Android

---

## Modelado de Datos y Contratos Odoo 11

### Modelo Odoo: `fundetaxcol.tarifa.sector`
- `id` (`integer`): ID del sector o destino
- `name` (`char`): Nombre de la ruta (ej. `Aeropuerto`, `Bocagrande`, `Terminal de Transportes`)
- `valor` (`float`): Tarifa base en pesos colombianos
- `valor_recargo` (`float`): Valor adicional por recargo nocturno
- `nota` (`char`): Observaciones (ej. `Tarifa fija reglamentaria`)

### Modelo Odoo: `fundetaxcol.turno` (Estado Despachado)
- `id` (`integer`): ID del turno
- `name` (`char`): Descripción autogenerada (`Turno #X [PLACA - BAHIA]`)
- `secuencia` / `sequence` (`integer`): Número consecutivo en bahía
- `state` (`selection`): `'despachado'` (excluye `'cancelado'` y `'progreso'`)
- `bahia_id` (`many2one`): Bahía operativa de la sesión
- `vehiculo_id` (`many2one`): Vehículo despachado
- `conductor_id` (`many2one`): Conductor asignado
- `tarifa_id` (`many2one`): Sector/tarifa liquidada (`tarifa_id != 0`)
- `total` (`float`): Monto liquidado (`tarifa.valor + recargo`)
- `fecha_despacho` (`datetime`): Timestamp oficial de salida
- `user_id` (`many2one`): Usuario despachador que emitió la salida

---

## Requirements

### Requirement: Historial Cronológico de Despachos en DespachoListView
El sistema DEBE proveer en `DespachoListView` la lista cronológica de todos los vehículos despachados en la bahía activa durante la jornada actual (`tarifaId.id != 0` y `state != 'cancelado'`), ordenados descendentemente por secuencia/hora de salida (`result.sort((a, b) => b.sequence.compareTo(a.sequence))`).

#### Scenario: Carga y renderizado del historial de despachos
- **WHEN** el despachador selecciona la pestaña "Despachos" en el Shell operativo
- **THEN** el sistema DEBE consultar `TurnStorage.getAll()` filtrando turnos donde `bahiaSesionId == settings.currentBay && tarifaId.id != 0 && state != 'cancelado'` y presentarlos en un `ListView.separated` con `SmartRefresher`.

#### Scenario: Visualización detallada en TurnoCardWidget
- **WHEN** se renderiza un despacho en la lista
- **THEN** la tarjeta DEBE mostrar un `CircleAvatar` amarillo con el número de secuencia, la placa en mayúscula negrita, la hora de salida (`fechaDespacho`), el conductor en itálica, la bahía en azul, el destino (`tarifaId.name`) en negrita, el valor con formato de moneda (`$ 18.000`) y el nombre del usuario despachador.

#### Scenario: Reimpresión térmica desde la lista de despachos
- **WHEN** el despachador pulsa sobre una tarjeta de despacho
- **THEN** el sistema DEBE abrir `TurnoFormView` en modo consulta permitiendo visualizar el desglose del despacho y disparar la reimpresión del comprobante de salida mediante el botón de imprimir.

#### Scenario: Búsqueda reactiva de despachos
- **WHEN** el usuario escribe en el buscador universal de la AppBar mientras la pestaña activa es Despachos
- **THEN** el sistema DEBE filtrar la lista en memoria evaluando coincidencias en la placa (`vehiculoId.name` o `placaAnonima`), conductor (`conductorId.name`) o destino (`tarifaId.name`).

---

### Requirement: Liquidación de Tarifa y Salida de Turno en TurnoFormView
El sistema DEBE proveer una pantalla dedicada para despachar el taxi en turno, bloqueando la placa y conductor en solo lectura, proveyendo un buscador de sectores (`PathSearchController`), calculando el recargo nocturno según `settings.horaRecargo`, soportando la cancelación de turno y disparando la impresión térmica.

#### Scenario: Bloqueo de datos del vehículo y conductor
- **WHEN** se abre `TurnoFormView` para un turno existente (`entity.id != 0`)
- **THEN** los selectores de placa y conductor DEBEN aparecer bloqueados en solo lectura (`enabled: false`), impidiendo su modificación.

#### Scenario: Selección de tarifa y cálculo de recargo diurno
- **WHEN** el operador selecciona un destino en `PathSearchController` antes de la hora configurada en `settings.horaRecargo` (ej. antes de las 18:00:00)
- **THEN** el sistema DEBE asignar `entity.total = tarifa.valor`, actualizar la nota del sector si existe y reflejar el valor en el footer persistente sin recargo.

#### Scenario: Selección de tarifa y cálculo de recargo nocturno
- **WHEN** el operador selecciona un destino después o a la hora configurada en `settings.horaRecargo`
- **THEN** el sistema DEBE evaluar la hora del sistema contra `settings.horaRecargo`, asignar `entity.total = tarifa.valor + tarifa.valorRecargo` y desplegar el total con recargo nocturno en el footer en formato monetario.

#### Scenario: Confirmación de despacho con auto-impresión
- **WHEN** el operador pulsa el botón de despachar turno (`Icons.save`) con tarifa seleccionada
- **THEN** el sistema DEBE enviar a Odoo vía RPC:
  ```json
  {
    "id": entity.id,
    "tarifa_id": entity.tarifaId.id,
    "nota": entity.nota
  }
  ```
  y al confirmar el guardado, si `settings.autoPrint == true`, DEBE disparar de inmediato la impresión física del comprobante en la impresora térmica configurada.

#### Scenario: Cancelación de turno con diálogo de confirmación
- **WHEN** el operador pulsa el botón rojo de cancelar turno
- **THEN** el sistema DEBE mostrar un diálogo de confirmación `¿Desea cancelar el turno?`, y si se confirma, invocar RPC `fundetaxcol.turno.cancelar(id: entity.id)`, removiendo el taxi de la cola y notificando vía WebSocket.
