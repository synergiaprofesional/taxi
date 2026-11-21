# OpenSpec: View Pago & Recaudo (Recaudos y Cobros Diarios)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con el módulo de pagos y recaudos contables de `fundetaxcol_flutter`, integrando:
- **Vista de Lista**: `lib/ui/views/list/pago_list_view.dart` (`PagoListView`)
- **Vista de Formulario Maestro**: `lib/ui/views/form/pago_form_view.dart` (`PaymentFormView`)
- **Sub-Componente de Conceptos**: `PaymentDetail` (`pago_form_view.dart#L104`)
- **Modal de Captura de Conceptos**: `lib/ui/views/form/pago_concepto_form_view.dart` (`PaymentConceptForm`)
- **Controladores**:
  - `PaymentListController` (`lib/controllers/list/payment_list.controller.dart`)
  - `PaymentController` (`lib/controllers/models/pago.controller.dart`)
  - `PaymentConceptController` (`lib/controllers/models/pago_concepto.controller.dart`)
- **Controladores de Búsqueda Integrados**:
  - `CarSearchController` (`lib/controllers/search/vehiculo.search.controller.dart`)
  - `DriverSearchController` (`lib/controllers/search/conductor.search.controller.dart`)
  - `ConceptSearchController` (`lib/controllers/search/concepto.search.controller.dart`)
- **Tarjeta Visual**: `PagoCardWidget` (`lib/ui/widgets/pago_card_widget.dart`)
- **Modelos DTO**:
  - `PaymentModel` (`lib/classes/pago.dart`)
  - `PaymentConceptModel` (`lib/classes/pago_concepto.dart`)
  - `ConceptModel` (`lib/classes/concept.dart`)
- **Almacenamiento Local**: `PaymentStorage` (`lib/storage/payment.storage.dart`)

---

## Modelado de Datos y Contratos Odoo 11

### Modelo Odoo: `fundetaxcol.pago`
- `id` (`integer`): ID del recibo de recaudo
- `consecutivo` (`char`): Número oficial contable (ej. `REC-00124`)
- `fecha` (`datetime`): Timestamp de cobro
- `bahia_id` / `bahia_sesion_id` (`many2one`): Bahía donde se cobró
- `vehiculo_id` (`many2one`): Taxi asociado al recaudo
- `conductor_id` (`many2one`): Conductor que realiza el pago
- `total` (`float`): Sumatoria total liquidada en pesos colombianos
- `user_id` / `user` (`many2one`): Nombre del cajero u operador
- `concepto_ids` (`one2many`): Lista de conceptos asociados

### Invocación RPC para Guardar Pago:
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
      },
      {
        "concepto_id": 14,
        "cantidad": 1,
        "valor": 5000.0
      }
    ]
  }
}
```

---

## Componentes UI y Layout

### 1. `PagoListView` (Historial de Cobros)
- **Contenedor**: `SmartRefresher` con `WaterDropMaterialHeader` y `loadPayments(reload: true)`.
- **Estado Vacío**: Centrado con mensaje: `"No hay pagos en [Nombre Bahía]"`.
- **Tarjeta `PagoCardWidget`**:
  - Consecutivo oficial a la izquierda (ej. `REC-00124`).
  - Placa del taxi en negrita y conductor en itálica.
  - Valor total recaudado en pesos (`formatMonetary(total)`).
  - Fecha y hora de expedición.
  - Nombre del usuario cajero.
- **Acciones**:
  - Floating Action Button `(+)`: Abre `PaymentFormView` en modo nuevo pago (`id == 0`).
  - Tap en tarjeta: Abre `PaymentFormView` en modo consulta (`id != 0`) con botón de reimpresión.

### 2. `PaymentFormView` (Formulario Maestro de Cobro)
- **AppBar**: Muestra el consecutivo si `id != 0`, o `Nuevo pago` si `id == 0`.
- **Selectores Superiores**:
  - `SearchGenericWidget<CarSearchController>`: Selector de placa obligatorio. Al cambiar, precarga el conductor principal del vehículo y sus conceptos contables asignados.
  - `SearchGenericWidget<DriverSearchController>`: Selector de conductor con división entre habituales y padrón general.
- **Sub-Lista `PaymentDetail`**:
  - Barra de herramientas con título "Conceptos" y botón `(+)` para abrir `PaymentConceptForm`.
  - Lista de conceptos agregados mostrando `${cantidad}x $valor` y el subtotal `${cantidad * valor}`.
  - Botón de eliminación (`Icons.close`) en cada fila cuando `enabled == true`.
- **Footer Persistente**:
  - Alineado a la izquierda: `Total: ${formatMonetary(totalConcepts)}` en tipografía de tamaño 20 negrita e itálica.
- **Floating Action Buttons**:
  - Modo Consulta (`id != 0`): Botón verde de impresión (`Icons.print`) ejecutando `printer.printPayment(entity)`.
  - Modo Creación (`id == 0`): Botón Guardar (`Icons.save`) con validación de formulario.

### 3. `PaymentConceptForm` (Modal de Captura de Concepto)
- **Selector de Concepto**: `SearchGenericWidget<ConceptSearchController>` sobre `fundetaxcol.concepto`. Al elegir concepto, precarga `cantidadCtrl.text = "1"` y `valorCtrl.text = concepto.valor`.
- **Campo Cantidad**: `TextFormField` numérico entero mayor estricto a 0.
- **Campo Valor**: `TextFormField` numérico decimal mayor o igual a 0.
- **Botón `Hecho!` (`Icons.done`)**: Retorna el `PaymentConceptModel` a `PaymentFormView`.

---

## Requirements

### Requirement: Consulta y Registro de Recaudos Diarios en PagoListView
El sistema DEBE proveer en `PagoListView` la consulta en tiempo real de todos los pagos registrados en la bahía activa mediante el modelo Odoo `fundetaxcol.pago`, ordenados de forma descendente por número consecutivo contable (`result.sort((a, b) => b.consecutivo.compareTo(a.consecutivo))`).

#### Scenario: Visualización de pagos en bahía activa
- **WHEN** el usuario ingresa a la pestaña de Pagos
- **THEN** el sistema DEBE listar los recibos con su consecutivo oficial (`REC-00124`), placa, conductor, total recaudado y fecha/hora, ordenados con el más reciente de primero.

#### Scenario: Consulta y reimpresión de recibo existente
- **WHEN** el usuario pulsa sobre una tarjeta de pago
- **THEN** el sistema DEBE abrir `PaymentFormView` en modo consulta (`id != 0`), bloqueando los campos y habilitando el botón verde de reimpresión térmica.

#### Scenario: Búsqueda reactiva de pagos
- **WHEN** el usuario escribe en el buscador universal de la AppBar en la pestaña de Pagos
- **THEN** el sistema DEBE filtrar la lista evaluando coincidencias en la placa (`vehiculoId.name`) o conductor (`conductorId.name`).

---

### Requirement: Formulario Maestro de Pago con Conceptos en PaymentFormView
El sistema DEBE proveer un formulario de recaudo que vincule vehículo, conductor y una lista dinámica de conceptos contables (`PaymentDetail`), calculando de forma reactiva la sumatoria total en un footer persistente.

#### Scenario: Autocompletado de conductor y conceptos al seleccionar taxi
- **WHEN** el cajero selecciona una placa en `PaymentFormView`
- **THEN** el sistema DEBE autocompletar el primer conductor principal y cargar sus conceptos contables habituales (o el concepto por defecto de `settings.concept` si no posee ninguno), actualizando de inmediato el total en el footer.

#### Scenario: Agregación de conceptos contables dinámicos
- **WHEN** el cajero pulsa el botón (+) en la sub-lista `PaymentDetail`
- **THEN** el sistema DEBE abrir `PaymentConceptForm`, capturar concepto, cantidad y valor, y al pulsar `Hecho!`, agregarlo a la lista `conceptoIds` y recalcular el total general reactivamente.

#### Scenario: Eliminación de renglón de cobro
- **WHEN** el cajero pulsa el botón de eliminar (`Icons.close`) en un concepto
- **THEN** el sistema DEBE retirar el elemento de `conceptoIds` y recalcular de inmediato el total en el footer.

#### Scenario: Guardado, emisión y auto-impresión
- **WHEN** el cajero pulsa "Guardar" y el formulario es válido
- **THEN** el sistema DEBE invocar `actualizar('fundetaxcol.pago', data)`, retornar el pago registrado a la lista y disparar la impresión térmica si `settings.autoPrint == true`.
