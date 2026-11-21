# Design: Rectificación Canónica de Tarifas de Despacho, Sincronización de Bahías y Pagar y Enturnar

## Contexto y Arquitectura

El ecosistema transaccional de Fundetaxcol se apoya en modelos Many2one estrictos en PostgreSQL/Odoo 11:
1. `fundetaxcol.tarifa.sector`: Define los sectores urbanos e interurbanos con su valor base y recargo nocturno.
2. `fundetaxcol.turno`: Requiere `tarifa_id` para transicionar formalmente a `state: 'despachado'` y registrar la fecha de salida.
3. `fundetaxcol.settings.mobile`: Almacena `current_bay` para cada operador; consultado por `get_current_bay()` en el backend.
4. `fundetaxcol.pago`: Posee el booleano `enturnar`. Cuando es `True`, Odoo invoca `crear_turno()` de manera transaccional.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FLUJO DE DESPACHO CANÓNICO                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [TurnoFormView]                                                            │
│         │                                                                   │
│         ▼                                                                   │
│  Seleccionar Tarifa de Odoo ───▶ [fundetaxcol.tarifa.sector]               │
│         │                         (id, name, valor, valor_recargo)          │
│         ▼                                                                   │
│  Calcular Total = valor + (esNocturno ? valor_recargo : 0)                  │
│         │                                                                   │
│         ▼                                                                   │
│  [TurnoController.despacharTurno]                                           │
│         │                                                                   │
│         ▼                                                                   │
│  Odoo RPC fundetaxcol.turno.actualizar:                                     │
│  kwargs: { id: turnoId, tarifa_id: tarifa.id, valor: total, nota: dir }     │
│         │                                                                   │
│         ▼                                                                   │
│  [Odoo 11 Backend]                                                          │
│  if anonimo or tarifa_id:                                                   │
│      state = 'despachado'                                                   │
│      fecha_despacho = now()                                                 │
│  send_data() ───▶ WebSocket emite a '/dispatch'                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Decisiones de Diseño

### 1. DTO `TarifaSectorModel`
```dart
class TarifaSectorModel {
  final int id;
  final String name;
  final double valor;
  final double valorRecargo;
  final String nota;

  TarifaSectorModel({
    required this.id,
    required this.name,
    required this.valor,
    required this.valorRecargo,
    this.nota = '',
  });

  factory TarifaSectorModel.fromJson(Map<String, dynamic> json) { ... }
}
```

### 2. Sincronización de Bahía Activa (`set_state`)
Al invocar `cambiarBahia(BahiaModel bahia)`:
```dart
await odooService.setBahiaActiva(bahia.id);
```
Invocando Odoo:
```json
{
  "model": "fundetaxcol.settings.mobile",
  "method": "set_state",
  "kwargs": {
    "uid": userId,
    "current_bay": bahiaId
  }
}
```

### 3. Pagar y Enturnar Integrado
Al ejecutar `pagarYEnturnar(placa, conductor, valor)`:
Si el usuario está autenticado, registrar el pago en `fundetaxcol.pago` enviando `enturnar: true`, o registrar el pago contable asociando el concepto por defecto y garantizando la presencia del turno.

### 4. Tarifa Selector en `TurnoFormView`
Reemplazar el dropdown estático por un selector reactivo alimentado por `turnoController.tarifasDisponibles`. Al seleccionar un destino, actualizar reactivamente la tarifa base, la nota y el valor de recargo correspondiente.

