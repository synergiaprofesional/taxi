## ADDED Requirements

### Requirement: Estandarización de Identidad y Rebranding
El sistema SHALL unificar la identidad visual, el nombre visible y el package identifier bajo la denominación oficial `Taxi` en todas las plataformas soportadas (Android y Windows Desktop).

#### Scenario: Compilación e Identificación de Aplicación
- **WHEN** se compila el ejecutable en Windows o el paquete en Android
- **THEN** el título de ventana, el applicationId y los metadatos visibles del sistema deben reflejar `Taxi` sin residuos de nombres anteriores

### Requirement: Desacoplamiento de Configuración en Tres Capas
El sistema SHALL cargar las variables de infraestructura y credenciales desde `.env` y exponerlas a través de clases tipadas inmutables en tiempo de ejecución.

#### Scenario: Carga de Credenciales en Inicio
- **WHEN** la aplicación inicializa en cualquier plataforma
- **THEN** la configuración tipada valida la presencia de los parámetros de Firebase y modo de ejecución antes de habilitar la interfaz
