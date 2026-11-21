# Proposal: Calibración Fina según Informe de Novedades Fundetaxcol

## 1. Contexto y Problema
Tras la auditoría del documento oficial "INFORME DE NOVEDADES - SISTEMA FUNDETAXCOL" emitido por la administración de Fundetaxcol, se constataron 3 desajustes específicos de reglas de negocio en la aplicación:
1. **Desfase Horario de 5 Horas en Pagos y Turnos:** Odoo almacena `datetime` en PostgreSQL bajo zona horaria UTC (`2025-10-25 22:11:00`). Como el string carece de sufijo `Z`, Dart lo parsea como hora local, mostrando las 10:11 p.m. en lugar de las 5:11 p.m. (hora legal de Colombia, UTC-5).
2. **Destino de Despacho por Defecto:** Los operadores en las bahías despachan mayoritariamente hacia "Caribe Plaza". La app seleccionaba ciegamente el primer registro del catálogo Odoo en lugar de priorizar Caribe Plaza.
3. **Regla de Recargo Nocturno de Transporte:** La app aplicaba recargo a partir de las 20:00 (8:00 p.m.) con valor de $2.500, mientras que el tarifario oficial de Fundetaxcol rige desde las 19:00 (7:00 p.m.) con un valor reglamentario de $1.100.

## 2. Solución Propuesta
1. Implementar la función utilitaria de parseo `DateTimeUtils.parseOdooUtc(raw)` que garantiza la interpretación estricta de las marcas de tiempo de Odoo como UTC y su conversión transparente a la zona horaria local del dispositivo (`.toLocal()`) en `PagoRecaudoModel` y `TurnoModel`.
2. Modificar la inicialización de tarifas en `TurnoFormView` para preseleccionar automáticamente la tarifa que contenga `"CARIBE PLAZA"` como destino predeterminado.
3. Actualizar la regla de recargo nocturno en `TurnoFormView` fijando el horario desde las 19:00 (7:00 p.m.) hasta las 05:00 a.m., y el valor base de recargo de contingencia en $1.100.
4. Incrementar la versión canónica a `v2.1.17+19` en `pubspec.yaml` y `AppVersion`.
5. Ejecutar compilación y despliegue físico verificado en Teléfono Móvil, Tablet Lenovo y Windows Desktop.

