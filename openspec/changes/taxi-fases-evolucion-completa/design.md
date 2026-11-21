## Context

El proyecto `Taxi` hereda la base de código de `synergia_movil`, una aplicación Flutter cliente que se comunicaba con un backend Odoo 11 EE en `fundetaxcol.co` mediante JSON-RPC sincrónico (`/web/dataset/call_kw`) y un socket intermedio en Node.js puerto 3000. 

El objetivo es transformar esta arquitectura en una plataforma reactiva multiplataforma sustentada en **Google Firebase**, organizando el sistema bajo el **Modelo Cebolla** (Capa 0: Garita/Admin, Capa 1: Conductores, Capa 2: Pasajeros) con un esquema de despacho híbrido (bahías físicas + radar en calle) y autosostenibilidad financiera por publicidad (Google AdMob y convenios locales).

## Goals / Non-Goals

**Goals:**
- Desacoplar por completo el código de Odoo 11, migrando los 38 modelos esenciales de transporte a colecciones estructuradas en Cloud Firestore.
- Implementar autenticación unificada RBAC con Firebase Auth (claims: `admin`, `driver`, `client`).
- Preservar la ergonomía, velocidad e impresión térmica de garita en tablets y Windows Desktop para evitar rechazo operativo.
- Desplegar la experiencia móvil del conductor (turnos en vivo, recepción de despacho, consulta de ahorros programados y botón de pánico vial).
- Desplegar la experiencia del pasajero (solicitud geolocalizada, cotización automática según tarifas por sector y seguimiento en vivo).
- Integrar monetización mediante Google AdMob garantizando cero anuncios invasivos durante la conducción activa.
- Diseñar la máquina de estados de despacho híbrido para reducir a cero los kilómetros y tiempos muertos.

**Non-Goals:**
- Conectar o sincronizar directamente la nueva base de datos con Odoo 11 (desacoplamiento total).
- Modificar o alterar el servidor de producción `fundetaxcol.co` (perímetro estricto de solo lectura).
- Implementar pasarelas de pago con tarjeta de crédito en la primera iteración (se mantiene efectivo y recaudos físicos/móviles).

## Decisions

### 1. Google Firebase como Backend Operativo
- *Decisión:* Seleccionar Cloud Firestore + Firebase Auth + Cloud Functions en lugar de actualizar Odoo o montar un backend REST custom.
- *Justificación:* Firestore provee sincronización reactiva en tiempo real (sub-100ms) mediante listeners nativos en Flutter (`Stream<QuerySnapshot>`), persistencia offline automática (crítica para túneles y áreas de baja cobertura), y escalabilidad automática sin administración de servidores.
- *Alternativas consideradas:* Odoo 18/19 (descartado por mantener cuellos de botella contables en el camino crítico de la movilidad), PostgreSQL propio con Supabase (descartado por requerir administración y mantenimiento de infraestructura).

### 2. Desnormalización Estratégica en Firestore
- *Decisión:* Incrustar metadatos esenciales del vehículo (`placa`, `numero_movil`) y conductor (`nombre`, `telefono`) directamente dentro del documento `/turnos/{id}`.
- *Justificación:* En NoSQL las lecturas se cobran por documento. La desnormalización permite a la garita y al conductor renderizar la lista completa de turnos con **1 sola lectura por turno**, eliminando N+1 consultas.

### 3. Modelo Cebolla con Reglas de Seguridad Granulares (`firestore.rules`)
- *Decisión:* Segregar el acceso mediante *Custom Claims* de Firebase Auth.
  - Claims `admin`: Lectura/escritura en `/bahias`, `/turnos`, `/recaudos`, `/tarifas_sector`.
  - Claims `driver`: Lectura de su turno y bahía, actualización de estado en viaje, consulta de sus propios ahorros.
  - Claims `client`: Creación de `/solicitudes_viaje`, lectura de datos just-in-time del conductor asignado y tarifas públicas. Cero acceso a `/recaudos` o balances de garita.

### 4. Seguridad Vial Inviolable en Monetización
- *Decisión:* La publicidad se activa únicamente en estados de reposo (conductor esperando turno en bahía; pasajero cotizando o tras calificar el servicio).
- *Justificación:* Cumplimiento estricto de normas de tránsito y protección de la vida humana. Cero pop-ups o intersticiales con el vehículo en movimiento.

## Risks / Trade-offs

- **[Riesgo: Costos de Lectura en Firestore]** → *Mitigación:* Desnormalización de datos, paginación con cursores (`startAfterDocument`), y uso intensivo de la caché local de Firestore (`PersistenceEnabled: true`).
- **[Riesgo: Dispositivos sin Conexión Celular]** → *Mitigación:* Firestore almacena las mutaciones en caché local SQLite y las sincroniza en background tan pronto recupera conectividad.
- **[Riesgo: Resistencia de Operadores de Garita]** → *Mitigación:* Se preservan los layouts idénticos en tablet (split-view) y atajos de teclado en Windows Desktop, manteniendo la impresión automática de tickets ESC/POS.
