# Design: Calibración Fina según Informe de Novedades Fundetaxcol

## 1. Mapeo y Normalización de Fechas UTC a Local (COT UTC-5)
En Odoo 11, los campos de fecha como `fecha`, `create_date` y `write_date` se transmiten en formato ISO-8601 sin zona horaria:
`YYYY-MM-DD HH:MM:SS` (ej. `2026-11-02 22:12:00`).

Para neutralizar el desfase de 5 horas:
```dart
DateTime parseOdooUtcDateTime(dynamic raw) {
  if (raw == null || raw == false) return DateTime.now();
  var str = raw.toString().trim();
  if (str.isEmpty) return DateTime.now();
  // Normalizar espacio a separador T
  str = str.replaceFirst(' ', 'T');
  // Si no especifica offset ni Z, asumir UTC incondicionalmente
  if (!str.endsWith('Z') && !str.contains('+') && !RegExp(r'-\d\d:?\d\d$').hasMatch(str)) {
    str = '${str}Z';
  }
  final dt = DateTime.tryParse(str);
  return dt != null ? dt.toLocal() : DateTime.now();
}
```
Esto asegura que las 22:11:00 UTC se conviertan de inmediato a las 17:11:00 (5:11 p.m.) hora Colombia.

## 2. Preselección Heurística de Tarifa ("Caribe Plaza")
Al inicializar `TurnoFormView` en modo despacho:
```dart
_tarifaSeleccionada = turnoController.tarifasDisponibles.firstWhereOrNull(
  (t) => t.name.toUpperCase().contains('CARIBE PLAZA')
) ?? turnoController.tarifasDisponibles.first;
```

## 3. Calibración del Recargo Nocturno
* Umbral de hora: `now.hour >= 19 || now.hour < 5` (7:00 p.m. a 5:00 a.m.).
* Monto de contingencia: `_valorRecargo = 1100.0`.

