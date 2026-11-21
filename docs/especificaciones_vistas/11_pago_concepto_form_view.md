# Especificación Técnica de Vista: PaymentConceptForm

## 1. Identificación y Ubicación
- **Archivo en fundetaxcol_flutter**: `lib/ui/views/form/pago_concepto_form_view.dart`
- **Controlador Principal**: `PaymentConceptController` (`lib/controllers/models/pago_concepto.controller.dart`)
- **Buscador de Concepto**: `ConceptSearchController` (`lib/controllers/search/concepto.search.controller.dart`)
- **Modelo de Retorno**: `PaymentConceptModel` (`lib/classes/pago_concepto.dart`)

---

## 2. Propósito y Flujo Operativo
`PaymentConceptForm` es una vista modal de captura rápida que permite al cajero añadir un nuevo concepto contable al formulario de recaudo. Cuenta con un buscador del catálogo oficial de conceptos de Odoo, campo para la cantidad (por defecto 1) y campo para el valor unitario (precargado desde la tarifa del concepto pero modificable si se requiere).

---

## 3. Campos y Validación
1. **Selector de Concepto** (`SearchGenericWidget<ConceptSearchController>`):
   - Consulta `fundetaxcol.concepto` (`fields: ['id', 'name', 'valor']`).
   - Al seleccionar un concepto:
     - `entity.conceptoId = concepto`
     - `entity.cantidad = 1`
     - `entity.valor = concepto.valor`
     - Asigna automáticamente los valores a los controladores de texto `cantidadCtrl` y `valorCtrl`.
2. **Campo de Cantidad (`cantidadCtrl`)**:
   - Tipo de teclado numérico (`TextInputType.number`).
   - Validación: Debe ser mayor estricto a 0 y de tipo numérico entero.
3. **Campo de Valor (`valorCtrl`)**:
   - Tipo de teclado numérico (`TextInputType.number`).
   - Validación: Debe ser mayor o igual a 0 y de formato numérico decimal.
4. **Botón Flotante (`Icons.done`)**:
   - Valida el formulario (`form.validate()`).
   - Invoca `Get.back(result: entity)`, devolviendo el objeto al formulario padre `PaymentFormView`.
