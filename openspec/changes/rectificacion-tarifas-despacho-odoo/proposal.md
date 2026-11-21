# Proposal: Rectificación Canónica de Tarifas de Despacho, Sincronización de Bahías y Pagar y Enturnar

## Why

La auditoría forense del sistema (`/opsx-explore`) reveló tres brechas estructurales críticas entre `synergia_movil` y el backend en producción de Odoo 11 (`fundetaxcol.co`):
1. **Despachos con Destinos Hardcodeados:** `TurnoFormView` posee un menú estático con 5 destinos quemados en texto (`Aeropuerto $18.000`, etc.) y nunca envía `tarifa_id` a Odoo. En consecuencia, Odoo no registra la fecha de despacho oficial, deja `tarifa_id` en nulo y emite el evento WebSocket a `/turn` en lugar de `/dispatch`.
2. **Desincronización de Bahía Activa (`current_bay`):** Al cambiar de bahía en Flutter, nunca se invoca `fundetaxcol.settings.mobile.set_state(uid, current_bay: id)`, dejando al servidor desfasado respecto a la bahía real del operador.
3. **"Pagar y Enturnar" Desacoplado de Caja:** La función `pagarYEnturnar` solo crea un turno ad-hoc sin generar el registro contable en `fundetaxcol.pago`, perdiendo el recaudo en la contabilidad de Odoo a pesar de que Odoo soporta nativamente `enturnar: True` en `fundetaxcol.pago`.

Para que la aplicación funcione como corresponde en producción (conforme a las reglas de la terminal de transporte), es mandatorio rectificar estos contratos y unificar la lógica con el backend Odoo 11.

## What Changes

- **Modelo `TarifaSectorModel`:** DTO formal para representar `fundetaxcol.tarifa.sector` (`id`, `name`, `valor`, `valor_recargo`, `nota`).
- **Servicio `OdooService`:** 
  - Incorporación de `getTarifasSector()` para consultar las rutas y tarifas reales de Odoo.
  - Incorporación de `setBahiaActiva(int bahiaId)` para notificar a `fundetaxcol.settings.mobile.set_state` al cambiar de bahía.
- **Controlador `TurnoController`:**
  - Carga reactiva de tarifas sectoriales en `tarifasDisponibles`.
  - Paso estricto de `tarifaId` en `despacharTurno(...)` garantizando activación de `state: 'despachado'` y emisión a `/dispatch`.
  - Integración contable en `pagarYEnturnar(...)` creando el pago formal en `fundetaxcol.pago`.
- **Vista `TurnoFormView`:**
  - Reemplazo del Dropdown estático por el catálogo real de tarifas de Odoo con cálculo dinámico de tarifa base y recargo nocturno.
- **Versionamiento:** Bump a `v2.1.15+17` en `pubspec.yaml` conforme a FIX-002 de `ERRORES.md`.

## Capabilities

### New Capabilities
- `despacho-tarifas-reales`: Consumo dinámico del modelo `fundetaxcol.tarifa.sector` en despacho y pase formal de `tarifa_id` a Odoo 11.
- `bahia-state-sync`: Sincronización bidireccional del estado de bahía activa del despachador en `fundetaxcol.settings.mobile`.
- `recaudo-enturnamiento-unificado`: Creación de pagos en `fundetaxcol.pago` con enturnamiento automático.

### Modified Capabilities
- `turno-management`: Actualización del ciclo de despacho para enviar identificadores relacionales exactos.

## Impact
- **Backend Odoo 11**: Sincronización 100% canónica con `fundetaxcol_movil/models/models.py`.
- **Frontend Flutter**: Eliminación de datos mock / hardcodeados, despacho fiel a la operación de la terminal y trazabilidad contable de recaudos.

