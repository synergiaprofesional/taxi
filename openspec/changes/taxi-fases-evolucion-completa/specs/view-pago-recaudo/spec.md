## MODIFIED Requirements

### Requirement: Recaudo y Registro de Ahorros sobre Firestore
El sistema SHALL registrar los pagos de sostenimiento, planillas y aportes de ahorro como documentos en la colección `/recaudos`, actualizando en tiempo real el saldo de la billetera del conductor.

#### Scenario: Cobro y Acreditación de Ahorro
- **WHEN** se procesa un recaudo con concepto de ahorro en garita
- **THEN** Firestore registra el comprobante contable y actualiza de inmediato el balance en la app del conductor
