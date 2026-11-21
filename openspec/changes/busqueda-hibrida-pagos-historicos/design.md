# Diseño Arquitectónico: Búsqueda Híbrida y Deserialización de Pagos

## 1. Arquitectura de Deserialización Polimórfica (`PagoRecaudoModel`)

Para soportar de manera infalible tanto las respuestas RPC `fundetaxcol.pago.get_all` (que devuelven diccionarios `_get_data()`) como las de `search_read` (que devuelven listas `[id, name]`), se implementa extracción con validación estricta de tipos:

```text
Entrada JSON de Odoo
       │
       ├── 'bahia_id' ────┬── is Map   ──> id = map['id'],   nombre = map['name']
       │                  ├── is List  ──> id = list[0],     nombre = list[1]
       │                  └── is int   ──> id = int,         nombre = 'Bahía'
       │
       ├── 'vehiculo_id' ─┬── is Map   ──> id = map['id'],   placa  = map['name']
       │                  ├── is List  ──> id = list[0],     placa  = list[1]
       │                  └── fallback ──> id = int/0,       placa  = json['placa']
       │
       ├── 'conductor_id' ┬── is Map   ──> id = map['id'],   nombre = map['name']
       │                  ├── is List  ──> id = list[0],     nombre = list[1]
       │                  └── fallback ──> id = int/0,       nombre = json['conductor']
       │
       └── 'total' / 'valor' ─────────> (json['total'] ?? json['valor'] ?? 0.0).toDouble()
```

## 2. Flujo de Búsqueda Híbrida en `TurnoController`

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FLUJO DE BÚSQUEDA HÍBRIDA (UI)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Operador escribe en SearchBar: query]                                     │
│                     │                                                       │
│                     ▼                                                       │
│  ¿query está vacío? ─────── SI ────▶ Mostrar pagos de bahía activa          │
│         │                                                                   │
│         NO                                                                  │
│         ▼                                                                   │
│  Filtrar pagos locales de la sesión activa (transversal multi-bahía)        │
│         │                                                                   │
│         ▼                                                                   │
│  ¿Hay resultados locales?                                                   │
│    ├── SI ──▶ Mostrar resultados inmediatamente (< 5 ms)                    │
│    └── NO ──▶ Si query.length >= 3:                                         │
│               Consultar Odoo en segundo plano (searchRead histórico)        │
│               Domain: ['|', ['vehiculo_id.name', 'ilike', query],          │
│                             ['conductor_id.name', 'ilike', query],         │
│                        '|', ['consecutivo', 'ilike', query]]                │
│               Renderizar resultados remotos enriquecidos                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3. Contratos de Datos
* `bahiaSesionId`: Permite discriminar la sesión de bahía asignada.
* `fecha`: Formato ISO parseado con `DateTime.tryParse`.
* `PagoListView`: Muestra indicador si el pago corresponde a una fecha o sesión histórica.
