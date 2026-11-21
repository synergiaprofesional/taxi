# OpenSpec: View Turno Form Despacho (Salida de Turno con Pasajero)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/form/turno_form_view.dart` (`TurnoFormView` con `isTurn: true`, `entity.id != 0`)
- **Controlador**: `TurnController` (`lib/controllers/models/turno.controller.dart`)
- **Buscador de Destinos**: `PathSearchController` (`lib/controllers/search/tarifa.search.controller.dart` sobre `fundetaxcol.tarifa.sector`)
- **Impresión Térmica**: `Printer.printTurn(turn)`
- **Referencia Técnica**: `docs/especificaciones_vistas/07_turno_form_despacho_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  [1] WGN121                                  │
├──────────────────────────────────────────────┤
│  Placa: WGN121                [SOLO LECTURA] │
│  Conductor: CARLOS RAMIREZ    [SOLO LECTURA] │
│  Destino: [ Aeropuerto                     ] │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │       [ CANCELAR TURNO ] (Rojo)        │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│  Nota: Tarifa fija nocturna                  │
│  Valor: $ 18.000                      ┌───┐  │
│                                       │ 🖨️│  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Campos Bloqueados**: Placa y Conductor con `enabled: false`.
- **Selector de Destino**: `SearchGenericWidget<PathSearchController>`.
- **Cálculo de Recargo Nocturno (`handleOnChangeTarifa`)**:
  - Si la hora actual es posterior o igual a `settings.horaRecargo` (ej. `18:00:00`):
    `entity.total = tarifa.valor + tarifa.valorRecargo;`
  - De lo contrario:
    `entity.total = tarifa.valor;`
- **Botón Cancelar Turno**: `CupertinoButton(color: Colors.red)` con confirmación e invocación RPC `fundetaxcol.turno.cancelar`.
- **Footer Persistente**: Nota del sector y Valor con formato monetario oficial (`$ 18.000`).

---

## Invocación Odoo 11 RPC y Auto-Impresión
```json
{
  "model": "fundetaxcol.turno",
  "method": "actualizar",
  "args": [],
  "kwargs": {
    "id": 1420,
    "tarifa_id": 12,
    "nota": "Tarifa fija nocturna"
  }
}
```
Si `settings.autoPrint == true`, dispara inmediatamente `printer.printTurn(turn)`.

---

## Requirements

### Requirement: Liquidación de Tarifa y Salida de Turno en TurnoFormView
El sistema DEBE proveer una pantalla dedicada para despachar el taxi en turno, bloqueando la placa y conductor en solo lectura, proveyendo un buscador de sectores, calculando el recargo nocturno según `settings.horaRecargo`, soportando la cancelación de turno y disparando la impresión térmica.

#### Scenario: Cálculo de recargo nocturno automático
- **WHEN** el operador selecciona un destino después de la hora estipulada en `settings.horaRecargo`
- **THEN** el sistema DEBE sumar automáticamente el valor base de la tarifa más el campo `valorRecargo` y reflejarlo en el campo total del footer.

#### Scenario: Confirmación de despacho con auto-impresión
- **WHEN** el operador pulsa el botón de despachar turno y `settings.autoPrint` está activo
- **THEN** el sistema DEBE actualizar el turno en Odoo con `tarifa_id` y disparar de forma automática la impresión del comprobante en la impresora térmica.

#### Scenario: Cancelación de turno con diálogo de confirmación
- **WHEN** el operador pulsa el botón rojo de cancelar y confirma la acción
- **THEN** el sistema DEBE invocar el método RPC `fundetaxcol.turno.cancelar` en Odoo y remover el taxi de la cola.
