# Especificación Técnica de Vista: PaymentFormView

## 1. Identificación y Ubicación
- **Archivo en fundetaxcol_flutter**: `lib/ui/views/form/pago_form_view.dart`
- **Controlador Principal**: `PaymentController` (`lib/controllers/models/pago.controller.dart`)
- **Sub-Componente de Conceptos**: `PaymentDetail` (`pago_form_view.dart#L104`)
- **Controladores de Búsqueda Integrados**:
  - `CarSearchController` (`lib/controllers/search/vehiculo.search.controller.dart`)
  - `DriverSearchController` (`lib/controllers/search/conductor.search.controller.dart`)
- **Modal de Concepto**: `PaymentConceptForm` (`lib/ui/views/form/pago_concepto_form_view.dart`)

---

## 2. Propósito y Flujo Operativo
`PaymentFormView` es el formulario maestro de recaudo contable. Permite al cajero registrar un pago seleccionando el vehículo y conductor, precargando los conceptos por defecto (o agregando conceptos adicionales como rodamiento, seguro o aportes) y calculando en tiempo real la sumatoria en un footer persistente. Si el pago ya fue guardado, opera en modo de solo lectura y permite la reimpresión térmica.

---

## 3. Componentes Visuales y Estructura
1. **AppBar**:
   - Título: Muestra el `consecutivo` si ya está registrado (ej. `REC-00124`) o el texto `Nuevo pago`.
2. **Formulario Central**:
   - **Selector de Placa** (`SearchGenericWidget<CarSearchController>`):
     - Campo de texto bloqueado con tap para desplegar la búsqueda modal.
     - Obligatorio (`required: true`).
     - Al seleccionar taxi: extrae automáticamente `vehiculo.conductorIds` y precarga el primer conductor principal en el selector de conductor.
   - **Selector de Conductor** (`SearchGenericWidget<DriverSearchController>`):
     - Organizado con dos secciones: "Conductores principales" y "Otros conductores".
     - Al seleccionar conductor: precarga sus conceptos asignados (`conductor.conceptoIds`). Si no tiene, precarga el concepto por defecto configurado en el sistema (`settings.concept`).
   - **Sub-Lista de Conceptos (`PaymentDetail`)**:
     - Botón (+) en la cabecera de la sub-lista para abrir `PaymentConceptForm`.
     - `ListView.separated` con cada concepto: nombre, desglose `${cantidad}x $valor` y subtotal.
     - Botón de eliminación (icono `close`) por cada renglón.
3. **Footer Persistente**:
   - Muestra el texto reactivo: `Total: $ XX,XXX` formateado en moneda local.
4. **Floating Action Buttons**:
   - **Modo Creación (`id == 0`)**: Botón Guardar (`Icons.save`).
   - **Modo Consulta (`id != 0`)**: Botón Imprimir (`Icons.print`, color verde).

---

## 4. Contrato y Envío a Odoo
- **Método RPC**: `BaseController.actualizar('fundetaxcol.pago', data)`
- **Payload**:
  ```json
  {
    "bahia_id": settings.currentBay,
    "vehiculo_id": entity.vehiculoId.id,
    "conductor_id": entity.conductorId.id,
    "concepto_ids": [
      {
        "concepto_id": 12,
        "cantidad": 1,
        "valor": 15000.0
      }
    ]
  }
  ```
- **Auto-Impresión**: Si `settings.autoPrint == true`, al recibir la respuesta satisfactoria de Odoo se dispara inmediatamente `printer.printPayment(payment)`.
