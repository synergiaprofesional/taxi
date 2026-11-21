# OpenSpec: View Pago Concepto Form (Captura de Renglón Contable)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/form/pago_concepto_form_view.dart` (`PaymentConceptForm`)
- **Controlador**: `PaymentConceptController` (`lib/controllers/models/pago_concepto.controller.dart`)
- **Buscador de Concepto**: `ConceptSearchController` (`lib/controllers/search/concepto.search.controller.dart` sobre `fundetaxcol.concepto`)
- **Modelo de Retorno**: `PaymentConceptModel` (`lib/classes/pago_concepto.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/11_pago_concepto_form_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Agregar concepto                            │
├──────────────────────────────────────────────┤
│  Concepto: [ Rodamiento                    ] │
│  Cantidad: [ 1                             ] │
│  Valor:    [ 15000                         ] │
│                                       ┌───┐  │
│                                       │ ✔ │  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Campos**:
  - `SearchGenericWidget<ConceptSearchController>`: Selector de concepto contable obligatorio. Al seleccionar, precarga cantidad = 1 y valor sugerido de Odoo.
  - `TextFormField` Cantidad (`cantidadCtrl`): Teclado numérico, validación de entero mayor estricto a 0.
  - `TextFormField` Valor (`valorCtrl`): Teclado numérico, validación de decimal mayor o igual a 0.
- **Botón Flotante (`Icons.done`)**: Valida y ejecuta `Get.back(result: entity)`.

---

## Requirements

### Requirement: Modal de Captura de Conceptos Contables
El sistema DEBE proveer un formulario modal en `PaymentConceptForm` que permita al cajero seleccionar un concepto de Odoo, definir cantidad y valor unitario, y retornarlo estructurado a la vista principal de recaudo.

#### Scenario: Selección de concepto y precarga de tarifa sugerida
- **WHEN** el cajero selecciona un concepto en el buscador
- **THEN** el sistema DEBE precargar automáticamente el campo cantidad en 1 y el campo valor con el monto configurado en `fundetaxcol.concepto`.

#### Scenario: Validación estricta de cantidad y valor
- **WHEN** el cajero intenta guardar con cantidad menor o igual a 0 o valor negativo
- **THEN** el sistema DEBE bloquear el envío y mostrar un mensaje de validación correspondiente.
