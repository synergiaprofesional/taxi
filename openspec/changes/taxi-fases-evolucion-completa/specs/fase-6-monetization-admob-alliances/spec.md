## ADDED Requirements

### Requirement: Publicidad No Intrusiva con Google AdMob
El sistema SHALL mostrar banners adaptativos e intersticiales gobernados por frecuencia (*capping*) en momentos de reposo del usuario, protegiendo la experiencia y los flujos críticos.

#### Scenario: Visualización de Banner en Cotización
- **WHEN** el pasajero está en la pantalla de cotización o seguimiento del mapa
- **THEN** se renderiza un banner inferior adaptativo sin bloquear los controles de solicitud

### Requirement: Regla Inviolable de Seguridad Vial en Conducción
El sistema SHALL inhibir completamente la presentación de anuncios emergentes, videos o pop-ups interactivos mientras el vehículo se encuentre en movimiento o en una carrera activa.

#### Scenario: Vehículo en Marcha
- **WHEN** los sensores GPS detectan velocidad superior a 5 km/h o el estado es `En Carrera`
- **THEN** el subsistema publicitario bloquea cualquier solicitud de despliegue de anuncios
