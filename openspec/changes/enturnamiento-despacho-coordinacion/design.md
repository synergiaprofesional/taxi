# Documento de Diseño: Ciclo de Vida de Enturnamiento, Despacho y Deserialización

## 🏗️ Arquitectura y Contratos de Datos

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      FLUJO DE ENTURNAMIENTO Y DESPACHO CORREGIDO                       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [TurnoFormView / BahiaSelectedView]                                                   │
│               │                                                                        │
│               │ (placa, conductor, vehiculoId, conductorId)                            │
│               ▼                                                                        │
│  [TurnoController.enturnarVehiculo]                                                    │
│               │                                                                        │
│               ▼                                                                        │
│  RPC fundetaxcol.turno.actualizar:                                                     │
│  {                                                                                     │
│    'bahia_id': bahiaIdActual (ej: 8843),                                               │
│    'vehiculo_id': vehiculoId,                                                          │
│    'conductor_id': conductorId,                                                        │
│    'anonimo': false,          <-- Permite que Odoo mantenga el estado 'espera'          │
│    'tarifa_id': false,        <-- Sin tarifa inicial para no auto-despachar            │
│    'state': 'espera'                                                                   │
│  }                                                                                     │
│               │                                                                        │
│               ▼                                                                        │
│  [Backend Odoo: fundetaxcol.turno]                                                     │
│  Crea el registro con state = 'espera'.                                                │
│               │                                                                        │
│               ▼                                                                        │
│  [App: TurnoModel.fromJson]                                                            │
│  bahiaSesionId extraído polimórficamente:                                              │
│  if (rawBahia is Map) -> rawBahia['id']                                                │
│  else if (rawBahia is List) -> rawBahia[0]                                             │
│  else if (rawBahia is int) -> rawBahia                                                 │
│               │                                                                        │
│               ▼                                                                        │
│  [Fila de Turnos Activos]                                                              │
│  turnos.where((t) => t.enFila && t.bahiaSesionId == 8843) -> Muestra WGM405 en cola.   │
│               │                                                                        │
│               ▼  (Al presionar "Despachar" en la tarjeta de turno)                     │
│  [TurnoController.despacharTurno(turnoId)]                                             │
│  RPC fundetaxcol.turno.actualizar:                                                     │
│  {                                                                                     │
│    'id': turnoId,                                                                      │
│    'state': 'despachado',                                                              │
│    'fecha_despacho': Datetime.now()                                                    │
│  }                                                                                     │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## 📐 Decisiones de Diseño

1. **Resolución de `vehiculo_id` y `conductor_id`:**
   Si el operador digita la placa manualmente sin seleccionar de la lista sugerida, el controlador buscará en `vehiculoController.vehiculos` por placa. Si existe, tomará su `id` y su `conductor_id`. Si no se encuentra, buscará en Odoo vía `searchRead` o creará/asignará con `placa_anonima` pero con `anonimo: false` para que no se autodespache.
2. **Parser Seguro en `TurnoModel`:**
   Normalizar extracción de `bahiaSesionId`:
   ```dart
   int bahiaIdParsed = 0;
   final rawBahia = json['bahia_id'];
   if (rawBahia is Map) {
     bahiaIdParsed = parseInt(rawBahia['id']);
   } else if (rawBahia is List && rawBahia.isNotEmpty) {
     bahiaIdParsed = parseInt(rawBahia[0]);
   } else if (rawBahia is int) {
     bahiaIdParsed = rawBahia;
   }
   ```
   Y asignar `bahiaSesionId: bahiaIdParsed`.
3. **Mantenimiento del Historial:**
   Los turnos despachados pasan a `turnosDespachados` donde la coordinadora puede auditarlos en la pestaña correspondiente.
