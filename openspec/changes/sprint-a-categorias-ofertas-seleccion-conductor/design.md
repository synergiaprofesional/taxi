# Diseño Técnico: Sprint A — Categorías, Oferta con Ancla Legal y Selección de Conductor

## 1. Arquitectura de Datos y Máquina de Estados de Oferta

```text
┌────────────────────────────────────────────────────────┐
│             CICLO DE NEGOCIACIÓN DE LA OFERTA          │
└────────────────────────────────────────────────────────┘

 1. [Publicar Viaje]
    ViajeModel(estado: solicitado, tarifaPropuestaPasajero: $X, categoria: Y)
          │
          ▼
 2. [Flota Recibe Solicitud en Radar]
    Taxistas cercanos envían ofertas a subcolección:
    /viajes/{viajeId}/ofertas/{conductorId}
    ConductorOfertaModel(precioPropuesto: $Z, distanciaMetros, tiempoMinutos)
          │
          ▼
 3. [Pasajero Escucha Stream en Vivo]
    DriverOffersSheet renderiza en tiempo real cada oferta recibida
          │
          ▼
 4. [Pasajero Elige Conductor]
    Firestore Transaction:
    - Estado viaje pasa a `asignado`
    - conductor_id, placa, nombre fijados en ViajeModel
    - tarifa_total fijada al precio pactado
    - Se rechazan o descartan las demás ofertas
```

## 2. Definición de Categorías de Movilidad
- `taxiEstandar`: Taxi tradicional en calle o bahía.
- `bahiaPrioritaria`: Taxi despachado con prioridad física desde garita autorizada.
- `ejecutivoVip`: Vehículos de gama alta o convenios especiales con aire acondicionado permanente.
- `envioExpress`: Transporte de paquetes y encomiendas en baúl cerrado.
- `intermunicipal`: Viajes de ciudad a ciudad.

## 3. Trade-offs y Consideraciones
- **Subcolección vs Array embebido:** Se utiliza subcolección `/viajes/{id}/ofertas` para evitar colisiones de concurrencia y límites de 1MB por documento cuando múltiples taxistas ofertan al mismo tiempo.
- **Tiempos de expiración (TTL):** La solicitud de viaje expira automáticamente a los 2 minutos si no se selecciona ningún conductor, evitando carreras zombis.
