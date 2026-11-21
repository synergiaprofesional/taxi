# OpenSpec: View Pago List (Historial de Pagos y Recaudos Diarios)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/list/pago_list_view.dart` (`PagoListView`)
- **Controlador**: `PaymentListController` (`lib/controllers/list/payment_list.controller.dart`)
- **Tarjeta Visual**: `PagoCardWidget` (`lib/ui/widgets/pago_card_widget.dart`)
- **Modelo DTO**: `PaymentModel` (`lib/classes/pago.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/09_pago_list_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Pagos — Bahía 29D                           │
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │ REC-00124                  10:14 PM    │  │
│  │ WGN121 — CARLOS RAMIREZ                │  │
│  │ Bahía: 29D                             │  │
│  │ Total: $ 25.000                        │  │
│  │ Cajero: operador1                      │  │
│  └────────────────────────────────────────┘  │
│                                       ┌───┐  │
│                                       │ + │  │
│                                       └───┘  │
└──────────────────────────────────────────────┘
```
- **Contenedor**: `SmartRefresher` con `WaterDropMaterialHeader` y `FundetaxcolCustomFooter`.
- **Estado Vacío**: `"No hay pagos en [Nombre Bahía]"`.
- **Tarjeta `PagoCardWidget`**:
  - Consecutivo contable (ej. `REC-00124`) y fecha/hora.
  - Placa del vehículo en negrita, conductor en itálica y nombre de la bahía.
  - Total cobrado formateado monetariamente (`formatMonetary(total)`).
  - Nombre del usuario cajero.
- **Acciones**:
  - Floating Action Button `(+)`: Abre `PaymentFormView` en modo nuevo cobro (`id == 0`).
  - Tap en tarjeta: Abre `PaymentFormView` en modo consulta (`id != 0`) para reimpresión térmica.

---

## Controlador y Filtro Local
- Filtro en memoria:
  ```dart
  final result = entities.where((e) => e.bahiaSesionId == settings.currentBay).toList();
  result.sort((a, b) => b.consecutivo.compareTo(a.consecutivo));
  ```
- Búsqueda incremental por placa (`vehiculoId.name`) o conductor (`conductorId.name`).

---

## Requirements

### Requirement: Consulta y Registro de Recaudos Diarios en PagoListView
El sistema DEBE proveer en `PagoListView` la consulta en tiempo real de todos los pagos registrados en la bahía activa mediante el modelo Odoo `fundetaxcol.pago`, ordenados de forma descendente por número consecutivo contable.

#### Scenario: Visualización de pagos en bahía activa
- **WHEN** el usuario ingresa a la pestaña de Pagos
- **THEN** el sistema DEBE listar los recibos con su consecutivo oficial (`REC-00124`), placa, conductor, total recaudado y fecha/hora, ordenados con el más reciente de primero.

#### Scenario: Consulta y reimpresión de recibo existente
- **WHEN** el usuario pulsa sobre una tarjeta de pago
- **THEN** el sistema DEBE abrir `PaymentFormView` en modo consulta (`id != 0`), bloqueando los campos y habilitando el botón verde de reimpresión térmica.
