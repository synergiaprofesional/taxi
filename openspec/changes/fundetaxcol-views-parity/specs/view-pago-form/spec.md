# OpenSpec: View Pago Form (Formulario Maestro de Cobro de Recaudos)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/form/pago_form_view.dart` (`PaymentFormView`)
- **Controlador**: `PaymentController` (`lib/controllers/models/pago.controller.dart`)
- **Sub-Componente de Conceptos**: `PaymentDetail` (`pago_form_view.dart#L104`)
- **Referencia Técnica**: `docs/especificaciones_vistas/10_pago_form_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Nuevo pago                                  │
├──────────────────────────────────────────────┤
│  Placa: [ WGN121                           ] │
│  Conductor: [ CARLOS RAMIREZ               ] │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ Conceptos                          (+) │  │
│  ├────────────────────────────────────────┤  │
│  │ Rodamiento                 (x) Eliminar│  │
│  │ 1x $ 15.000                            │  │
│  │ $ 15.000                               │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│  Total: $ 15.000                      ┌───┐  │
│                                       │ 💾│  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Selectores Superiores**:
  - `SearchGenericWidget<CarSearchController>`: Selector de taxi obligatorio. Precarga conductor y conceptos.
  - `SearchGenericWidget<DriverSearchController>`: Conductor con división principales vs padrón.
- **Sub-Lista `PaymentDetail`**:
  - AppBar con botón `(+)` para abrir `PaymentConceptForm`.
  - ListView con desglose de ítems: `${cantidad}x $valor` y subtotal `${cantidad * valor}`.
  - Botón de eliminación individual (`Icons.close`).
- **Footer Persistente**:
  - Total reactivo: `Total: ${formatMonetary(totalConcepts)}` en fuente grande negrita e itálica.
- **Acciones Flotantes**:
  - Modo Consulta (`id != 0`): Botón verde de impresión (`Icons.print`).
  - Modo Creación (`id == 0`): Botón Guardar (`Icons.save`).

---

## Invocación Odoo 11 RPC y Auto-Impresión
```json
{
  "model": "fundetaxcol.pago",
  "method": "actualizar",
  "args": [],
  "kwargs": {
    "bahia_id": "<currentBayId>",
    "vehiculo_id": 125,
    "conductor_id": 48,
    "concepto_ids": [
      {
        "concepto_id": 10,
        "cantidad": 1,
        "valor": 15000.0
      }
    ]
  }
}
```
Si `settings.autoPrint == true`, dispara de inmediato `printer.printPayment(entity)`.

---

## Requirements

### Requirement: Formulario Maestro de Pago con Conceptos en PaymentFormView
El sistema DEBE proveer un formulario de recaudo que vincule vehículo, conductor y una lista dinámica de conceptos contables (`PaymentDetail`), calculando de forma reactiva la sumatoria total en un footer persistente.

#### Scenario: Autocompletado de conductor y conceptos al seleccionar taxi
- **WHEN** el cajero selecciona una placa en `PaymentFormView`
- **THEN** el sistema DEBE autocompletar el primer conductor principal y cargar sus conceptos contables habituales, actualizando de inmediato el total en el footer.

#### Scenario: Guardado, emisión y auto-impresión
- **WHEN** el cajero pulsa "Guardar" y el formulario es válido
- **THEN** el sistema DEBE invocar `actualizar('fundetaxcol.pago', data)`, retornar el pago registrado a la lista y disparar la impresión térmica si `settings.autoPrint == true`.
