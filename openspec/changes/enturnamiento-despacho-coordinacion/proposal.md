# Propuesta de Cambio: Corrección de Enturnamiento, Despacho y Deserialización de Bahías

## 🎯 Justificación y Problema
En la operación de campo de Fundetaxcol (coordinadoras de Sótano / Caribe Plaza), se reportó que al realizar un nuevo turno mediante "Enturnar Vehículo" (por ejemplo, el taxi `WGM405` ingresado 4 veces), el vehículo no se reflejaba en la cola de turnos en espera y no se permitía despacharlo.

### Causa Raíz Diagnosticada
1. **Deserialización Polimórfica Incompleta en `TurnoModel.fromJson`:**
   En Odoo 11, `fundetaxcol.turno.get_all` devuelve el campo Many2one `bahia_id` como un diccionario `Map<String, dynamic>` (`{'id': 8843, 'name': 'Garita Sesión [2026-10-25]'}`). `TurnoModel.fromJson` evaluaba `json['bahia_id'] is int ? json['bahia_id'] : 0`, resultando en `bahiaSesionId = 0`. Al filtrar en `TurnoController` por la bahía activa de la sesión (`bahiaSesionId == 8843`), la cola de turnos quedaba completamente vacía `[]`.
2. **Bandera `anonimo: true` Hardcodeada en `TurnoController.pagarYEnturnar` / `enturnarVehiculo`:**
   Al crear un turno, se enviaba al RPC `fundetaxcol.turno.actualizar` los parámetros `'anonimo': true` y `'vehiculo_id': false`. En el backend de Odoo (`TurnoMovil` en `fundetaxcol_movil/models/models.py`), existe la regla `if anonimo or tarifa_id: values['state'] = 'despachado'; values['fecha_despacho'] = fields.Datetime.now()`. Esto forzaba a que todo vehículo enturnado fuera inmediatamente auto-despachado por el servidor, naciendo con `state = 'despachado'` y nunca entrando a la cola de espera (`state = 'espera'`).
3. **Imposibilidad de Despachar:**
   Al no aparecer en la cola de turnos en espera, no había elemento en pantalla para ejecutar la acción de despacho.

## 📦 Alcance
- **`lib/models/turno_model.dart`**: Implementar parser polimórfico en `TurnoModel.fromJson` para extraer `bahiaSesionId`, `vehiculo_id` y `conductor_id` desde `Map`, `List` o `int`.
- **`lib/controllers/turno_controller.dart`**: Refactorizar `enturnarVehiculo` y `pagarYEnturnar` para enviar `anonimo: false`, `vehiculo_id` y `conductor_id` reales (o resolverlos por placa), estableciendo `state: 'espera'` para que ingrese en cola. En `despacharTurno`, invocar `actualizar` con `state: 'despachado'`.
- **`lib/ui/views/form/turno_form_view.dart`**: Pasar `vehiculoId` y `conductorId` al invocar `enturnarVehiculo`.
- **`pubspec.yaml`**: Incrementar versión a `2.1.13+15`.

## 🛡️ Impacto y Regresión
- No afecta las vistas ni los pagos existentes.
- Garantiza que los turnos asignados permanezcan en fila visible hasta que el operador los despache voluntariamente.
