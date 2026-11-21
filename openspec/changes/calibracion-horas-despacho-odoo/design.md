# Diseño: Calibración Canónica de Horas y Deserialización de Fecha de Despacho

## 1. Arquitectura de Datos y Flujo de Fechas

```
┌─────────────────────────────────┐
│     PostgreSQL / Odoo 11        │
│   create_date (UTC en BD)       │
│  "2026-11-02 15:11:58"          │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Odoo Python: get_fecha_actual() │
│ UTC - 5 horas (America/Bogota)  │
│ Retorna: "2026-11-02 10:11:58"  │
└────────────────┬────────────────┘
                 │
                 ▼ JSON RPC (_get_data)
┌─────────────────────────────────┐
│ Flutter DateTime Parsing        │
│ parseDate("2026-11-02 10:11:58")│
│ Parseo directo sin forzar 'Z'   │
│ DateTime(2026, 11, 2, 10, 11)   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ UI Widgets (DateFormat 'hh:mm') │
│ Muestra: 10:11 AM (Hora COT)    │
└─────────────────────────────────┘
```

## 2. Decisiones de Diseño

1. **Parseo Directo sin 'Z':**
   - Odoo ya entrega las fechas pre-convertidas a la zona horaria del usuario/empresa (`America/Bogota`, UTC-5).
   - Si `DateTime.tryParse(str)` recibe una cadena sin indicador de zona horaria (ej: `2026-11-02 10:11:58`), Dart la interpreta como fecha en hora local del sistema.
   - Si la cadena ya incluye `Z` o un offset explícito (`+00:00`, `-05:00`), Dart preserva el offset o permite convertir con `.toLocal()`.
   - Por tanto, no se debe agregar forzosamente `'Z'`.

2. **Deserialización de `fecha_despacho` en `TurnoModel`:**
   - Odoo entrega `json['fecha_despacho']` cuando el turno transiciona al estado `'despachado'`.
   - Si el turno aún está en espera, `fecha_despacho` viene en `false` o `null`.
   - `TurnoModel` añade el campo `final DateTime? fechaDespacho`.
   - `DespachoCardWidget` prioriza `turno.fechaDespacho ?? turno.fechaCreacion` para mostrar la hora en la que realmente se realizó el despacho, alineándose con el momento de cobro y salida.

3. **Compatibilidad con Pagos:**
   - `parseOdooDateTime` en `PaymentModel` adopta la misma regla limpia para garantizar que los tiquetes de pago muestren exactamente la hora de emisión sin desfase.

