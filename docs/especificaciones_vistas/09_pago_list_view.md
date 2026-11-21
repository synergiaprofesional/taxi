# Especificación Técnica de Vista: PagoListView

## 1. Identificación y Ubicación
- **Archivo en fundetaxcol_flutter**: `lib/ui/views/list/pago_list_view.dart`
- **Controlador Principal**: `PaymentListController` (`lib/controllers/list/payment_list.controller.dart`)
- **Tarjeta Visual**: `PagoCardWidget` (`lib/ui/widgets/pago_card_widget.dart`)
- **Modelo de Datos**: `PaymentModel` (`lib/classes/pago.dart`)
- **Almacenamiento Local / Caché**: `PaymentStorage` (`lib/storage/payment.storage.dart`)

---

## 2. Propósito y Flujo Operativo
`PagoListView` es la primera pestaña operativa del shell `BahiaSelectedView`. Permite al despachador/cajero consultar el historial de todos los cobros y recaudos realizados durante la sesión activa en la bahía seleccionada. Permite filtrar en tiempo real por placa o conductor, consultar el detalle de un cobro previo para su reimpresión térmica y abrir el formulario de creación de nuevos recaudos.

---

## 3. Modelo de Datos y Contrato con Odoo
- **Modelo Odoo**: `fundetaxcol.pago`
- **Campos Consultados**:
  - `id`: Identificador único del pago en PostgreSQL.
  - `consecutivo`: Consecutivo contable oficial generado por la secuencia de Odoo (ej. `REC-00124`).
  - `vehiculo_id`: Relación Many2one con `fundetaxcol.vehiculo` (`[id, name]`).
  - `conductor_id`: Relación Many2one con `res.partner` (`[id, name]`).
  - `total`: Monto total recaudado en pesos colombianos ($).
  - `user_id` / `user`: Nombre del cajero u operador que registró el recaudo.
  - `fecha`: Fecha y hora de expedición del recibo.
  - `bahia_id` / `bahia_sesion_id`: Identificador de la bahía operativa.
  - `concepto_ids`: Lista de conceptos contables asociados al recibo.

---

## 4. Lógica de Negocio y Reglas Operativas
1. **Filtro de Bahía**: Solo muestra los pagos cuyo `bahiaSesionId == settings.currentBay`.
2. **Ordenamiento**: Descendente por `consecutivo` (`result.sort((a, b) => b.consecutivo.compareTo(a.consecutivo))`), garantizando que el último pago aparezca de primero.
3. **Búsqueda Incremental**:
   - Evalúa coincidencias en `vehiculoId.name` o `conductorId.name`.
   - Se activa dinámicamente desde el `TitleSearchWidget` de la AppBar.
4. **Pull-to-Refresh**: Utiliza `SmartRefresher` para recargar pagos desde el servidor forzando `reload: true`.
5. **Acciones Operativas**:
   - **Tap en Tarjeta**: Abre `PaymentFormView` en modo consulta (`controller.entity.id != 0`), habilitando el botón verde de reimpresión térmica.
   - **Botón Flotante (+)**: Abre `PaymentFormView` en modo creación con la lista de vehículos y conductores a excluir.
