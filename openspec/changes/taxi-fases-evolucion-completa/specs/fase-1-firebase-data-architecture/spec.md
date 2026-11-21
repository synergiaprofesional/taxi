## ADDED Requirements

### Requirement: Modelado Documental en Cloud Firestore
El sistema SHALL persistir las entidades de transporte en colecciones NoSQL optimizadas con desnormalización estratégica de metadatos de vehículos y conductores.

#### Scenario: Creación y Consulta de Turno
- **WHEN** un vehículo ingresa a la cola de una bahía
- **THEN** el documento `/turnos/{id}` se almacena con su placa, móvil y conductor incrustados, permitiendo su lectura reactiva en una única operación

### Requirement: Control de Acceso Basado en Roles (RBAC) en Firebase Auth
El sistema SHALL autenticar usuarios asignando Custom Claims (`admin`, `driver`, `client`) y restringir las mutaciones mediante Firestore Security Rules.

#### Scenario: Aislamiento de Datos por Rol
- **WHEN** un usuario con rol `client` intenta leer la colección `/recaudos`
- **THEN** el motor de reglas de Firestore deniega el acceso de forma inmediata
