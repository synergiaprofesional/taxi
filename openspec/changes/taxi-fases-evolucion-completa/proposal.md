## Why

La aplicación actual (`synergia_movil`) está confinada a una operación mononivel de garita acoplada a un servidor Odoo 11 legacy (2017) con altas latencias y sin interacción con conductores ni pasajeros. 

Esta propuesta formaliza la evolución integral del ecosistema **Taxi** hacia una plataforma de movilidad de alta cobertura bajo el **Modelo Cebolla**, desacoplando el backend hacia **Google Firebase** (Cloud Firestore, Auth, Functions) y soportando tres perfiles (Administradores, Conductores, Pasajeros) en múltiples dispositivos (Android Smartphones, Tablets y Windows Desktop), con autosostenibilidad por publicidad integrada y dignificación del oficio del taxista.

## What Changes

- **Desacoplamiento Total de Odoo 11:** Reemplazo de llamadas JSON-RPC y cookies de sesión por streams reactivos en tiempo real con Cloud Firestore y Firebase Auth.
- **Implementación del Modelo Cebolla (RBAC):**
  - **Capa 0 (Administración y Garita):** Mantenimiento de la paridad operativa en tablets y nueva consola Windows Desktop con impresión térmica ESC/POS.
  - **Capa 1 (Conductores):** Aplicación móvil para turnos en vivo, despacho directo, consulta de ahorros programados y botón de pánico vial.
  - **Capa 2 (Pasajeros):** Solicitud geolocalizada, cotización automática según tarifas por sector y seguimiento en vivo.
- **Motor de Despacho Híbrido:** Algoritmo que balancea la cola FIFO física de bahías con el radar geolocalizado en calle para eliminar el rodamiento en vacío ("tiempos muertos").
- **Monetización Sostenible (AdMob + Convenios):** Publicidad no invasiva gobernada por Firebase Remote Config con la regla inviolable de cero anuncios durante la conducción activa.
- **Rebranding y Publicación Oficial:** Transición a package ID unificado y preparación para Google Play Store y binario Windows nativo.

## Capabilities

### New Capabilities
- `fase-0-rebranding-config`: Estandarización de identidad, variables desacopladas en `.env` y configuración tipada.
- `fase-1-firebase-data-architecture`: Modelado NoSQL de 38 entidades heredadas en Firestore, reglas de seguridad RBAC y Cloud Functions de colas.
- `fase-2-capa0-admin-garita`: Consola operativa de garita en Tablet (Landscape Split-View) y Desktop con impresión de tickets ESC/POS nativa.
- `fase-3-capa1-driver-ecosystem`: Experiencia móvil del conductor (cola en vivo, alerta sonora de despacho, billetera de ahorro programado y seguridad vial).
- `fase-4-capa2-client-passenger`: Solicitud de taxi por pasajeros, cotización transparente por sector y radar de aproximación en mapa.
- `fase-5-hybrid-dispatch-engine`: Máquina de estados del vehículo y despacho híbrido inteligente entre bahías físicas y llamadas en calle.
- `fase-6-monetization-admob-alliances`: Integración de Google AdMob y plataforma de convenios locales con restricción de seguridad al volante.
- `fase-7-hardening-playstore-deploy`: Compendio TDD, auditoría de seguridad y pipeline para Play Store (`.aab`) y Windows Desktop (`.exe`).
- `jerarquia-gremial-flota-dual`: Organigrama gremial en 5 niveles, conductores públicos vs privados y modalidades de vinculación de pasajeros.
- `tarifas-legales-estandarizadas`: Matriz oficial de sectores por decreto, recargos calculados en servidor, pantalla espejo y prohibición de tarifas arbitrarias.

### Modified Capabilities
- `view-turno-management`: Migración del flujo de enturnamiento y despacho de Odoo 11 hacia streams en tiempo real de Firebase Firestore.
- `view-bahia-selected-shell`: Soporte de interfaz adaptativa para tablet garita y control de turnos en caliente.
- `view-pago-recaudo`: Mapeo de pagos y conceptos hacia documentos Firestore con visualización del ahorro del conductor.

## Impact

- **Código Afectado:** `lib/services/` (creación de servicios Firebase, retiro gradual de OdooService), `lib/controllers/`, `lib/models/`, `lib/ui/views/`.
- **Dependencias:** Incorporación de `firebase_core`, `cloud_firestore`, `firebase_auth`, `firebase_messaging`, `firebase_remote_config` y `google_mobile_ads`.
- **Infraestructura:** Creación del proyecto Firebase en la nube; el servidor `fundetaxcol.co` permanece en modo estricto de SOLO LECTURA como referencia histórica.
