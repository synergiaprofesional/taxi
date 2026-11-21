# Spec: Reglas de Negocio Oficiales Fundetaxcol

## REQ-001: Conversión Estricta UTC a Local
* `PagoRecaudoModel.fromJson` y `TurnoModel.fromJson` DEBEN interpretar las cadenas de fecha de Odoo como UTC y convertirlas a tiempo local del dispositivo.
* La fecha visualizada por el operador para un registro a las 17:12 COT (22:12 UTC en Odoo) DEBE ser estrictamente 5:12 p.m.

## REQ-002: Tarifa por Defecto Caribe Plaza
* Al abrir el formulario de despacho para un turno en cola, el sistema DEBE preseleccionar la tarifa que corresponda a "Caribe Plaza" si existe en el catálogo.

## REQ-003: Ventana y Tarifa de Recargo Nocturno
* El cálculo automático de recargo nocturno DEBE activarse a partir de las 19:00 horas (7:00 p.m.) y mantenerse hasta las 04:59:59 horas.
* El valor de recargo aplicado en ausencia de valor específico en la tarifa DEBE ser de $1.100 COP.

