# 🚕 CONTEXTO MAESTRO DEL PROYECTO TAXI — PLATAFORMA INTEGRAL DE MOVILIDAD
> **Documento Canónico de Transferencia de Contexto para Modelos de Lenguaje (Gemini / Claude / GPT)**  
> **Fecha de Emisión:** 21 de Noviembre de 2026 | **Versión:** `v3.0.0+1`  
> **Repositorio:** `c:\Workspaces\taxi` | **Proyecto Base:** `synergia_movil`  
> **Organización / Cliente:** FUNDETAXCOL (Cartagena de Indias, Colombia)  
> **Metodología:** Constitución Inviolable de "La Tripleta" (SDD + Tríada Bitácoras + LLM Wiki + Engram)

---

## 📌 1. Ficha Técnica y Resumen Ejecutivo

| Parámetro | Detalle Técnico |
| :--- | :--- |
| **Nombre del Proyecto** | **Taxi** (Evolución de alta cobertura de *Synergia Móvil*) |
| **Framework Frontend** | Flutter SDK `^3.12.2` / Lenguaje Dart |
| **Gestor de Estado y DI** | GetX `^4.7.3` (`GetxController`, `Obx`, `Get.put`, `Get.find`) |
| **Backend Objetivo** | **Google Firebase** (Cloud Firestore, Firebase Auth, Cloud Functions, Cloud Messaging, Remote Config, Storage) |
| **Backend Legacy (Referencia)**| Odoo 11 EE (Python 2.7/3.5, PostgreSQL) en `fundetaxcol.co` + Node.js Socket.IO en puerto 3000 (**Totalmente desacoplado para la nueva app**) |
| **Modo Acceso Servidor Prod**| **ESTRICTAMENTE SOLO LECTURA (READ-ONLY)**. Prohibida toda mutación en el servidor remoto. Copia descargada en `reference/`. |
| **Plataformas Soportadas** | Android Smartphones (Conductores y Clientes), Android Tablets (Garitas), Windows Desktop (Consola Administrativa) |
| **Monetización** | Google AdMob (`google_mobile_ads`) + Publicidad directa de convenios locales con restricción estricta de seguridad vial |

---

## 🎯 2. Misión, Visión y Evolución del Sistema

### De "Synergia Móvil" a "Taxi":
1. **El Sistema Legacy (`synergia_movil`):** Nació como una terminal operativa interna para operadores de garita de FUNDETAXCOL. Permitía registrar manualmente la llegada de un taxi (*enturnar*), asignarlo a una bahía de salida según una cola FIFO (*despachar*), emitir tiquetes térmicos en impresoras ESC/POS y registrar recaudos contables diarios hacia un ERP Odoo 11.
2. **La Limitación Central:** La app anterior era estrictamente **mononivel** (solo para administradores/operadores de garita). El conductor no tenía app propia y dependía de gritos, pantallas físicas o radiofrecuencia. El cliente final (pasajero) era completamente ajeno al sistema y tomaba el taxi en la calle sin trazabilidad digital.
3. **La Nueva Misión de `Taxi`:**
   - **Alta Cobertura:** Escalar la operación desde bahías cerradas hacia toda la ciudad y múltiples terminales.
   - **Emancipación de Odoo 11:** Reemplazar las llamadas JSON-RPC lentas, las cookies de sesión expiradas y los bloqueos de base de datos de Odoo 11 por una infraestructura reactiva, escalable y en tiempo real sobre **Firebase**.
   - **Transición sin Fricción:** Los operadores veteranos de garita deben encontrar una interfaz familiar con sus flujos habituales (cero curva de aprendizaje hostil), mientras los conductores y pasajeros adoptan experiencias modernas.

### 💖 2.1. Propósito Humano, Urbano y Gremial (El Alma del Proyecto)
*Documento canónico:* [`conceptualizaci_n_del_ecosistema_taxi.md`](file:///c:/Workspaces/taxi/docs/conceptualizaci_n_del_ecosistema_taxi.md)

El proyecto **Taxi** no es solo software de despacho; es una iniciativa para **rescatar, dignificar y posicionar la profesión del taxista** como una labor esencial, formal y respetada:
* **El Taxista como Anfitrión Urbano:** Es el primer y último anfitrión de la ciudad; quien recibe al visitante en el aeropuerto o terminal, conoce cada rincón y acompaña el regreso seguro a casa del ciudadano.
  * *Eslóganes de identidad:* *"El primer y último anfitrión de la ciudad"*, *"El oficio que mueve la ciudad con seriedad y respaldo"*, *"Del barrio al destino, con la seriedad de siempre"*.
* **El Taxi como Eje Vertical de la Economía Urbana:** No es un simple transporte de punto A a punto B, sino un conector vital que articula:
  1. **El Cliente de a Pie (El Latido Diario):** El ciudadano cotidiano que va al trabajo, salud o estudio.
  2. **Hoteles y Hospedaje:** Confianza y respaldo al huésped con conductores identificados.
  3. **Restaurantes y Ocio:** Movilidad segura para comensales en horarios nocturnos.
  4. **Sitios Recreativos, Playas y Comercio:** Acceso confiable para familias y turistas.
* **Dinámica de Confianza y Recomendación Mutua:** Hoteles, restaurantes y comercios aliados recomiendan el servicio porque saben que sus clientes viajan en manos seguras, cerrando un círculo virtuoso de demanda formal sin comisiones abusivas.

---

## 🧅 3. El "Modelo Cebolla" (Arquitectura de Capas Concéntricas)

El sistema se estructura en tres capas concéntricas de información, acceso y servicios:

```text
               ┌────────────────────────────────────────────────────────┐
               │              CAPA 2: CLIENTES FINALES                  │
               │                   (Pasajeros)                          │
               │   ┌────────────────────────────────────────────────┐   │
               │   │             CAPA 1: CONDUCTORES                │   │
               │   │                (Flota Móvil)                   │   │
               │   │   ┌────────────────────────────────────────┐   │   │
               │   │   │     CAPA 0: NÚCLEO ADMINISTRATIVO      │   │   │
               │   │   │         (Garitas y Despacho)           │   │   │
               │   │   │                                        │   │   │
               │   │   │ - Control de bahías y colas FIFO       │   │   │
               │   │   │ - Censo de vehículos y conductores     │   │   │
               │   │   │ - Tarifas maestras y sectores          │   │   │
               │   │   │ - Cajas, liquidación y auditoría       │   │   │
               │   └────────────────────────────────────────────┘   │   │
               │   │                                                │   │
               │   │ - Enturne digital y posición en cola           │   │
               │   │ - Aceptación de despachos y carreras           │   │
               │   │ - Monitoreo de aportes y recaudos              │   │
               │   │ - Navegación y contacto con cliente            │   │
               │   └────────────────────────────────────────────────┘   │
               │                                                        │
               │ - Solicitud de taxi (origen / destino)                 │
               │ - Cotización anticipada de tarifa por sector           │
               │ - Seguimiento en tiempo real del vehículo asignado     │
               │ - Calificación, seguridad e historial de viajes        │
               └────────────────────────────────────────────────────────┘
```

### Capa 0: Núcleo Administrativo (Garitas, Operadores, Administradores)
* **Funciones:** Regulación de bahías, ordenamiento de colas, altas/bajas de vehículos y conductores, definición de tarifas y recargos, auditoría contable y resolución de incidencias.
* **Dispositivos:** Windows Desktop y Android Tablets de garita.

### Capa 1: Capa Intermedia de Conductores (Flota de Taxis)
* **Funciones:** Enturne digital automático o asistido, visualización de posición en turno, alerta sonora/visual al ser despachado a una bahía, aceptación de carreras solicitadas por clientes, consulta de estado de cuenta de recaudos y botón de auxilio.
* **Dispositivos:** Android Smartphones.

### Capa 2: Capa Externa de Clientes Finales (Pasajeros)
* **Funciones:** Solicitud de taxi geolocalizado, cotización previa basada en la matriz de sectores de la empresa, radar en vivo del móvil asignado, validación de seguridad (placa, móvil, nombre) y calificación post-servicio.
* **Dispositivos:** Android Smartphones.

### 🏢 3.1. Estructura Gremial, Flota Pública/Privada y Vinculación de Pasajeros
*Documento canónico:* [`docs/wiki/entities/gremios_y_organizaciones.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/gremios_y_organizaciones.md) y [`docs/wiki/concepts/jerarquia_gremial_y_visibilidad_flota.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/jerarquia_gremial_y_visibilidad_flota.md)

El sistema contempla la realidad organizativa de los **Gremios y Agremiaciones de Transporte** (cooperativas, asociaciones, sindicatos y empresas de taxi):
1. **Organigrama Jerárquico Interno:**
   - **Nivel 1 (Gerencia/Presidencia):** Políticas globales, tarifas y convenios institucionales.
   - **Nivel 2 (Coordinadores de Zona):** Supervisores de bahías estratégicas y puestos de control.
   - **Nivel 3 (Operadores de Garita y Cajeros):** Despacho operativo y recaudos diarios.
   - **Nivel 4 (Propietarios de Flota):** Dueños de vehículos afiliados con liquidación consolidada.
   - **Nivel 5 (Conductores):** Operación en calle y atención de servicios.
2. **Dualidad de Flota: Conductores Públicos vs Privados:**
   - **🚖 Conductor Público (Flota Abierta):** Atiende a cualquier ciudadano en la calle o en bahías públicas; visible en el radar general de la app de pasajeros.
   - **🔒 Conductor Privado (Flota Corporativa / Convenios):** Conductor asignado exclusivamente a convenios institucionales (hoteles 5 estrellas, clínicas, empresas portuarias/petroleras). **No recibe carreras de la calle**; su despacho está reservado para los clientes vinculados a ese convenio específico con estándares VIP o facturación centralizada.
3. **Pasajeros Públicos y sus Modalidades de Vinculación:**
   - El pasajero es por definición público (descarga la app con su número celular y OTP SMS).
   - **Modalidad 1: Público General:** Solicita taxi en la ciudad; es atendido por la flota pública estándar.
   - **Modalidad 2: Corporativo / Hotel (Convenio):** Se vincula mediante código de convenio o correo institucional; accede con prioridad a la **flota privada del gremio** con opción de pago por voucher empresarial.
   - **Modalidad 3: Vinculado por Conductor Referido:** El pasajero escanea el QR o ingresa el código del taxista que le prestó un buen servicio. Cuando pide un taxi, el sistema notifica primero a su conductor preferido si está libre y cerca, fidelizando al taxista.

---

## 📱 4. Ecosistema de Dispositivos y Plataformas

1. **Android Smartphones:**
   - Para **Conductores:** Optimizado para bajo consumo de batería, GPS continuo en segundo plano, soporte offline cuando atraviesa túneles o zonas sin cobertura celular, interfaz con botones táctiles grandes para interactuar rápido en semáforos.
   - Para **Pasajeros:** Interfaz limpia, mapa interactivo, selección de destino por autocompletado y cotización inmediata.
2. **Android Tablets (Garitas y Bahías):**
   - Para **Operadores de Punto Fijo:** Diseño apaisado (*Landscape*) con vista partida (*Split-View*): columna izquierda con las bahías y cola de vehículos en tiempo real; columna derecha con botones rápidos de despacho, cobro de recaudo e impresión automática.
   - **Hardware integrado:** Conexión Bluetooth SPP nativa o TCP hacia impresoras térmicas de 58mm/80mm para expedición de tickets de salida.
3. **Windows Desktop (`taxi.exe`):**
   - Para **Administración Central y Cajas:** Consola administrativa densa en datos, filtros avanzados, auditoría en vivo, conciliación de caja diaria y exportación de reportes a PDF y Excel.

---

## ☁️ 5. Arquitectura Backend Objetivo: Google Firebase

El nuevo backend descarta Odoo 11 por completo. Se modela sobre el ecosistema Firebase:

### 1. Cloud Firestore (Base de Datos NoSQL Reactiva)
Colecciones estructuradas:
* `/usuarios/{uid}`: Perfil, rol (`admin`, `driver`, `client`), teléfono, estado activo, token FCM.
* `/vehiculos/{placa}`: Móvil, marca, modelo, tarjeta de control, SOAT, tecnomecánica, conductor activo asignado.
* `/conductores/{conductorId}`: Cédula, licencia, foto, teléfono, saldo de ahorros, calificación promedio.
* `/bahias/{bahiaId}`: Nombre (ej: Aeropuerto, Terminal, Garita 1), capacidad, orden, activa.
* `/turnos/{turnoId}`: Vehículo, conductor, bahía, posición en cola, estado (`en_cola`, `despachado`, `cancelado`), marcas de tiempo (`fecha_ingreso`, `fecha_despacho`).
* `/solicitudes_viaje/{viajeId}`: Cliente, origen (lat/lng/texto), destino (lat/lng/texto), sector_id, tarifa_estimada, conductor_id, estado (`solicitado`, `asignado`, `en_camino`, `a_bordo`, `finalizado`, `cancelado`).
* `/tarifas_sector/{sectorId}`: Nombre del sector, valor base, valor recargo nocturno/festivo, descripción.
* `/recaudos/{recaudoId}`: Consecutivo, conductor_id, vehiculo_id, valor_total, fecha, conceptos (ahorro, cuota sostenimiento, planilla), cajero_id.
* `/campanas_publicitarias/{campanaId}`: Banners locales, cliente anunciante, vigencia, métricas de clics e impresiones.

### 2. Firebase Authentication
* Autenticación basada en JWT. Soporte para teléfono/SMS (OTP) para conductores y pasajeros, y correo/contraseña para operadores y administradores.
* Asignación de *Custom Claims* (`role: 'admin' | 'driver' | 'client'`) para gobernar las reglas de seguridad de Firestore.

### 3. Cloud Functions (TypeScript / Node.js)
* **Gestor de Turnos FIFO:** Algoritmo atómico que asigna el siguiente taxi disponible en bahía cuando un cliente solicita carrera o cuando la garita despacha una unidad.
* **Notificaciones Push (FCM):** Despacho instantáneo de alertas a la app del conductor cuando sale su turno ("¡Móvil 240, acérquese a Bahía 1!").
* **Liquidación de Cierres:** Consolidación automática de cajas y recaudos al final de cada turno.

### 4. Firebase Remote Config
* Control dinámico de flags de negocio: activación de recargo nocturno, umbral de distancia para enturne por GPS, y frecuencia de publicidad.

---

## 📢 6. Modelo de Monetización y Publicidad

Para sustentar los costos de infraestructura (Firebase, Cloud Functions, APIs de mapas) sin gravar excesivamente al taxista ni al usuario:

1. **Google AdMob Integrado (`google_mobile_ads`):**
   - **Banners Adaptativos:** En la parte inferior de la pantalla de cotización y durante el seguimiento de la carrera en el cliente.
   - **Intersticiales Post-Servicio:** Mostrados suavemente al pasajero tras finalizar y calificar un viaje (limitado con *frequency capping* a 1 cada 3 viajes).
   - **Anuncios en Reposo para Conductores:** Mostrados exclusivamente en la pantalla de espera de turno en bahía.
2. **⚠️ Regla Inviolable de Seguridad Vial:**
   - **PROHIBICIÓN TOTAL** de anuncios emergentes, videos o pop-ups interactivos mientras el conductor esté en movimiento o realizando una carrera activa. Cero distracciones al volante.
3. **Plataforma de Publicidad Local Directa:**
   - Espacio para convenios comerciales del gremio: talleres mecánicos, venta de llantas, repuestos, aseguradoras de transporte público y estaciones de combustible.

---

## 🏛️ 7. Síntesis del Repositorio de Referencia Legacy (`reference/`)

Descargado directamente del servidor de producción `fundetaxcol.co` en modo **100% solo lectura**:

### Componentes Descargados en Local:
1. `reference/addons_fundetaxcol/`:
   * `fundetaxcol`: Módulo principal de Odoo 11 con los modelos de transporte.
   * `fundetaxcol_movil`: Adaptaciones móviles legacy y endpoints RPC.
   * `fundetaxcol_whatsapp`: Notificaciones y automatización de mensajería.
   * `ft_informe`, `mensajeria`, `print_javascript`.
2. `reference/server_rt_odoo/`:
   * Servicio Node.js Express con `socket.io@2.4.1` que transmitía eventos de cambio en turnos por WebSocket.
3. `reference/config/`:
   * `Caddyfile`: Reverse proxy con manejo de SSL y ruteo de puertos 80, 443, 3000 y 8069.
   * `odoo_80.conf`: Parámetros de conexión a PostgreSQL de Odoo 11.
   * `odoo_80.service`: Demonio de systemd.

### Modelos de Negocio Mapeados (38 modelos detectados por `Consolidados/cli.py`):
* **Turnos y Despacho:** `fundetaxcol.turno`, `fundetaxcol.bahia`, `fundetaxcol.sesion.bahia`, `fundetaxcol.secuencia.ticket`.
* **Flota:** `fundetaxcol.vehiculo`, `fundetaxcol.vehiculo.marca`, `fundetaxcol.vehiculo.partner`, `res.partner.contacto`.
* **Tarifario:** `fundetaxcol.tarifa`, `fundetaxcol.tarifa.sector`, `fundetaxcol.barrio`, `fundetaxcol.barrio.sector`.
* **Recaudos y Pagos:** `fundetaxcol.pago`, `fundetaxcol.pago.concepto`, `fundetaxcol.concepto`, `fundetaxcol.ahorro`, `fundetaxcol.ahorro.detalle`.

---

## 🛠️ 8. Estado del Código Frontend Flutter (Heredado de `synergia_movil`)

El código base en `lib/` cuenta con componentes maduros y probados en campo:
* **Tema y Colores (`lib/core/theme/`):** Paleta corporativa de taxi (amarillo canario `#FFC107`, negro profundo `#121212`, gris oscuro `#1E1E1E`, blanco puro). Soporte nativo para modo claro y oscuro persistido.
* **Control de Flujo con GetX (`lib/controllers/`):** Controladores reactivos (`TurnoController`, `ThemeController`). Regla crítica: en cualquier `Obx(() { ... })`, la variable observable `.value` se lee en la primera línea.
* **Impresión Térmica ESC/POS (`lib/services/printer_service.dart`):** Drivers probados para impresoras de tickets en red (TCP 9100), Bluetooth SPP nativo en Android (vía `MethodChannel` en Kotlin) y spooler de Windows Desktop (`raw_print_windows.ps1` / Win32).
* **Vistas Existentes (`lib/ui/views/`):**
  - `auth/login_view.dart`: Pantalla de autenticación y selección de entorno.
  - `home/home_view.dart`: Shell responsivo que commuta automáticamente entre vistas móviles, tablets y desktop.
  - `main/bahia_selected_view.dart`: Shell principal con navegación por pestañas (Turnos en cola, Despachos realizados, Recaudos de pago).
  - `form/turno_form_view.dart`: Formulario ágil de enturne y despacho con autocompletado y recargos.
  - `form/payment_form_view.dart`: Formulario de cobro de recaudo por chips rápidos de conceptos.
  - `settings/settings_view.dart`: Ajustes de conectividad, selección de impresora y preferencias.

---

## ⚖️ 9. La Constitución Inviolable del Proyecto ("La Tripleta")

Cualquier cambio, sesión o desarrollo en `Taxi` obedece estrictamente las leyes definidas en [`AGENTS.md`](file:///c:/Workspaces/taxi/AGENTS.md):

1. **SDD + OpenSpec Híbrido (`artifact_store: hybrid`):**
   - Planificar antes de codificar (`propose` → `spec` → `design` → `tasks`).
   - Persistencia dual: Engram MCP (`topic_key: sdd/{change-name}/*`) y archivos Markdown locales en `openspec/changes/{change-name}/`.
   - TDD obligatorio: Pruebas unitarias sin tolerar un solo fallo.
2. **Tríada de Bitácoras Obligatoria (3 Archivos en Disco en cada sesión):**
   - Monolito Mensual: `Bitacoras/{YYYY}/{MM}/bitacora.md`
   - Diario del Día: `Bitacoras/{YYYY}/{MM}/{DD}/Bitacoras YYYYMMDD.md`
   - Snapshot Atómico: `Bitacoras/{YYYY}/{MM}/{DD}/Bitacoras YYYYMMDD HHmmss.md` (con Resumen Ejecutivo, Tool Attribution con enlaces `file://...`, Decisiones, Estado de Memoria y Próximos Pasos).
3. **Curación Obligatoria de LLM Wiki (`docs/wiki/`):**
   - Memoria ontológica viva: Entidades (`docs/wiki/entities/`), Conceptos (`docs/wiki/concepts/`), Índice Central (`index.md`) y Log append-only (`log.md`).
4. **Desacoplamiento Absoluto de Configuración:**
   - Capa 1: `.env` y `.env.example`.
   - Capa 2: Matrices declarativas `config_*.json`.
   - Capa 3: Capa tipada de carga [`Consolidados/core/config.py`](file:///c:/Workspaces/taxi/Consolidados/core/config.py).
5. **Toolkit Unificado y Custodia Histórica:**
   - Todo comando o utilidad centralizada en [`Consolidados/cli.py`](file:///c:/Workspaces/taxi/Consolidados/cli.py).
   - Scripts históricos preservados inmutablemente en `scripts/back/{YYYYMMDD}/`.
6. **Perímetro de Servidor de Producción (Solo Lectura Estricto):**
   - Prohibido terminantemente ejecutar comandos de modificación o escritura en el servidor remoto `fundetaxcol.co`.

---

## 🗺️ 10. Hoja de Ruta de Implementación (Roadmap)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      ROADMAP PROYECTO TAXI                            │
├────────────────────────────────────────────────────────────────────────┤
│ FASE 1: Cimientos Firebase y Modelado de Datos                         │
│ - Configuración de Firebase Auth, Firestore y Security Rules           │
│ - Implementación de repositorios Dart para los 38 modelos de negocio   │
│ - Reemplazo de OdooService por FirebaseService reactivo                │
├────────────────────────────────────────────────────────────────────────┤
│ FASE 2: Adaptación Capa 0 (Administración y Garita)                   │
│ - Garantizar paridad total de interfaz y flujos para operadores        │
│ - Impresión de tickets ESC/POS nativa sincronizada con Firestore       │
│ - Consola Desktop Windows para administración y reportes               │
├────────────────────────────────────────────────────────────────────────┤
│ FASE 3: Despliegue Capa 1 (Módulo Conductor Android)                   │
│ - Vista móvil de turno en vivo y posición en bahía                     │
│ - Notificaciones push (FCM) de despacho y asignación de carrera        │
│ - Consulta de estado de recaudo y saldo de ahorro                      │
├────────────────────────────────────────────────────────────────────────┤
│ FASE 4: Despliegue Capa 2 (Módulo Pasajero y Monetización)             │
│ - Solicitud de taxi geolocalizada con cotización por sector            │
│ - Radar de seguimiento en vivo del vehículo asignado                   │
│ - Integración de Google AdMob y módulo de publicidad local             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 11. Hacia Dónde Queremos Llevar la Aplicación (Visión Estratégica, Futuro y Alcance)

La meta de **Taxi** trasciende la simple digitalización de una garita. El propósito fundamental es convertir esta solución en la **plataforma líder y soberana de movilidad para el gremio de taxis**, integrando tecnología de vanguardia, legalidad y beneficios tangibles para todos los actores:

### 1. La "SuperApp" Gremial Frente a las Plataformas Transnacionales
* **El Reto:** Plataformas extranjeras (Uber, Didi, InDrive, Cabify) operan al margen de muchas normativas locales, con tarifas dinámicas especulativas que perjudican al usuario y comisiones abusivas (20% a 30%) que precarizan al conductor.
* **La Respuesta de Taxi:** Crear una alternativa digital de igual o superior calidad técnica, pero apalancada en las fortalezas del transporte público formal:
  * **Tarifas Reguladas y Transparentes:** Cotización anticipada por sectores geográficos y taxímetro digital validado, eliminando disputas y cobros excesivos.
  * **Legalidad Plena y Seguridad Jurídica:** Flota 100% legal bajo el marco del Ministerio de Transporte (Decreto 1079 de Colombia: tarjetas de operación, tarjetas de control vigentes, seguros obligatorios SOAT y pólizas de responsabilidad contractual y extracontractual).
  * **Monopolio Natural de Bahías Exclusivas:** Solo los taxis formalmente afiliados tienen derecho de estacionamiento y recogida prioritaria en aeropuertos, terminales marítimas/terrestres, centros comerciales y grandes cadenas hoteleras.

### 2. Despacho Híbrido Inteligente (Fusión de Bahía Física + Radar en Calle)
* **El Problema Actual:** El taxista pasa horas esperando en una bahía física o rueda consumiendo gasolina sin rumbo buscando pasajeros.
* **Hacia Dónde Vamos:** Un motor de despacho híbrido:
  * Si el taxi está estacionado en una bahía (Aeropuerto, Terminal), el sistema respeta la cola física FIFO y le emite su ticket o confirmación digital.
  * Cuando el taxi sale a prestar un servicio y queda libre en la calle, el sistema activa su **radar digital geolocalizado**: puede tomar servicios solicitados por pasajeros cercanos o recibir un "enturne virtual" anticipado cuando se aproxima a una bahía con alta demanda, **eliminando los tiempos muertos y el kilometraje en vacío**.

### 3. Ecosistema de Bienestar y Fidelización del Conductor
* La aplicación está diseñada para que el taxista la ame y la sienta suya, no como un explotador digital:
  * **Billetera de Ahorro Digital Programado:** Visualización diaria del ahorro acumulado (la tradición del gremio de guardar un porcentaje diario para las primas decembrinas o mantenimiento correctivo), con liquidación transparente.
  * **Autoliquidación y Pagos sin Fricción:** Pago de cuotas diarias de sostenimiento y planilla de viaje mediante billeteras móviles (Nequi, Daviplata, PSE), erradicando las filas físicas en garita al final de la jornada.
  * **Club de Beneficios y Alianzas Comerciales:** A través de la red publicitaria y convenios gremiales, los conductores acceden a tarifas preferenciales y descuentos en servitecas, llantas, cambio de aceite, lavaderos, baterías y repuestos.
  * **Red de Seguridad y Auxilio Inmediato:** Botón de pánico conectado en tiempo real con la central de monitoreo y con la red de taxistas cercanos ante cualquier situación de peligro o accidente.

### 4. Publicación Oficial en Tiendas y Escalabilidad Masiva
* **Google Play Store & Apple App Store:** Salida del esquema de instalación artesanal de APKs para pasar a distribución masiva con compilaciones en formato App Bundle (`.aab`), actualizaciones automáticas transparentes y estricto cumplimiento de políticas de privacidad de Google y Apple.
* **Modelo SaaS Multi-Empresa / Multi-Ciudad:** La arquitectura modular sobre Firebase permite activar nuevas empresas de taxi o cooperativas en otras ciudades (Barranquilla, Santa Marta, Medellín, Bogotá) operando bajo la misma infraestructura con particionamiento de datos multi-tenant.

### 5. Autosostenibilidad Financiera a Costo Cero para la Operación
* Gracias a la estrategia de monetización no invasiva (Google AdMob gobernado dinámicamente + publicidad directa del sector automotor local), la plataforma genera ingresos recurrentes que costean el 100% del consumo de Firebase Firestore, Cloud Functions y APIs de mapas. La tecnología deja de ser un costo para convertirse en una fuente de sustentabilidad y modernización gremial.

---

*Documento consolidado y generado automáticamente para asistencia de IA por Antigravity bajo metodología gstack y SDD.*
