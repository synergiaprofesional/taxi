# Propuesta: Calibración Canónica de Horas y Fecha de Despacho Nativa

## 1. Justificación y Causa Raíz
A partir de la confrontación empírica en vivo contra el servidor `fundetaxcol.co` (PostgreSQL y código Python Odoo 11), se descubrieron dos causas fundamentales de inconsistencia horaria:
1. **Doble Conversión Horaria:** Odoo 11 ejecuta internamente `get_fecha_actual(fecha)` en los métodos `_get_data()` de turnos y pagos, restando ya el offset de -5 horas (Hora Colombia, America/Bogota). En Flutter, al forzar un sufijo `'Z'` y ejecutar `.toLocal()`, Dart interpretaba la hora local como UTC y restaba 5 horas adicionales, produciendo que un turno enturnado a las `10:11 AM` se visualizara como `05:11 AM`.
2. **Ausencia de `fecha_despacho` en el Modelo:** La tarjeta `DespachoCardWidget` mostraba `turno.fechaCreacion` (la hora de llegada a la cola) en vez de `turno.fechaDespacho` (la hora real en la que el vehículo fue despachado al destino).

## 2. Alcance
- `lib/models/turno_model.dart`: Eliminar la adición forzada de `'Z'` en `parseDate` e incorporar el campo `fechaDespacho`.
- `lib/models/payment_model.dart`: Eliminar la adición forzada de `'Z'` en `parseOdooDateTime`.
- `lib/ui/widgets/despacho_card_widget.dart`: Visualizar `turno.fechaDespacho ?? turno.fechaCreacion`.
- Versionamiento: Bump a `v2.1.20+22`.
- Verificación: `flutter analyze` (0 issues) y `flutter test` (21/21 passing).
- Despliegue: Teléfono Xiaomi, Tablet Lenovo y Windows Desktop.

