# Design: Paridad Funcional Absoluta con fundetaxcol_flutter

## Decisiones de Arquitectura

### 1. Modelo de Doble Estado en Colecciones Operativas (Local vs Global)
En `fundetaxcol_flutter`, las listas operativas manejan una separación clara entre:
- **`entities`**: El universo completo de registros descargados para la jornada (todas las bahías activas de la sesión).
- **`entitiesFound`**: El subconjunto proyectado en pantalla:
  - Si el buscador está vacío (`query.isEmpty`): Muestra únicamente los registros pertenecientes a la bahía seleccionada (`currentBay`).
  - Si el buscador contiene texto (`query.isNotEmpty`): Busca transversalmente sobre `entities` (todas las bahías) por placa, conductor, destino o consecutivo.

```
                  ┌──────────────────────────────────────────────┐
                  │ Odoo 11: `get_all` / search_read multi-bahía │
                  └──────────────────────┬───────────────────────┘
                                         ▼
                             entities (Caché Global)
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
           query.trim().isEmpty                      query.trim().isNotEmpty
                    │                                         │
                    ▼                                         ▼
         Filtro Bahía Seleccionada                  Filtro Global Transversal
           (Garita / 29D / Lago)                    (Todas las Bahías del Día)
```

### 2. Resolución de Vehículo y Conductor en Odoo RPC
- En Odoo 11, `search_read` en `fundetaxcol.vehiculo` retorna `conductor_ids: [int]`.
- Al seleccionar o autocompletar un vehículo, `VehiculoModel` debe soportar conductores tanto cuando vienen serializados como objetos `Map` (en `get_all`) como cuando vienen como IDs (`[int]`).
- Si vienen como IDs, el servicio debe resolver el nombre del conductor consultando `res.partner` / `fundetaxcol.conductor` o precargando el catálogo completo vía `Storage.getCars()` tal como lo hacía `fundetaxcol_flutter`.
- Al autoseleccionar el conductor, se inyectan automáticamente sus conceptos de cobro por defecto.

### 3. Ciclo de Vida Android y Persistencia de Tarea
- `android:taskAffinity=""` en `AndroidManifest.xml` fuerza al Activity Manager de Android a tratar cada instancia como una tarea aislada sin afinidad con el launcher del sistema, provocando que el OS mate el proceso al salir a segundo plano o apagar la pantalla.
- Remover `android:taskAffinity=""` restituye la afinidad natural con el paquete `com.synergia.synergia_movil`, manteniendo la app activa en RAM en segundo plano.
- En `OdooService`, asegurar bloques `finally` en `isLoggingIn` para evitar bloqueos en splash si la red es lenta.
