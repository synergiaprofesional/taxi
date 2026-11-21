# 📅 Diario del Día — 21 de Noviembre de 2026
# Proyecto: Taxi
**Responsable:** Antigravity (Staff Engineer AI) + Usuario
**Fecha:** 2026-11-21
**Versión Inicial:** `3.0.0+1`

---

## 🎯 Resumen de la Jornada

1. **Constitución e Independización del Proyecto Taxi:**
   - Separación formal desde `synergia_movil` hacia `c:\Workspaces\taxi`.
   - Adopción de la Constitución Inviolable de **La Tripleta** en [`AGENTS.md`](file:///c:/Workspaces/taxi/AGENTS.md) y [`GEMINI.md`](file:///c:/Workspaces/taxi/GEMINI.md).
2. **Inspección y Descarga de Referencia de Producción (Solo Lectura):**
   - Conexión SSH read-only hacia `fundetaxcol.co` sin modificar nada en el servidor.
   - Extracción de `/opt/server_rt_odoo`, `/opt/synergia/addons_fundetaxcol` y configs hacia `reference/`.
3. **Puesta en Marcha del Toolkit Unificado (`Consolidados/`):**
   - Creación de CLI maestro [`Consolidados/cli.py`](file:///c:/Workspaces/taxi/Consolidados/cli.py) con menú interactivo y subcomandos (`status`, `models`, `health`, `config`).
   - Mapeo automatizado de 38 modelos de negocio heredados para su diseño en Firebase.
4. **Gobernanza Ontológica (LLM Wiki en `docs/wiki/`):**
   - Entidades: Servidor Producción (`servidor_produccion.md`), Backend Firebase (`firebase_backend.md`).
   - Conceptos: Arquitectura Taxi (`arquitectura_taxi.md`), Transición UX (`transicion_ux_usuarios.md`).
   - Catálogo e histórico en `index.md` y `log.md`.
5. **Preservación Inmutable:**
   - 259 scripts archivados en `scripts/back/20261121/`.

---

## 📌 Snapshots Atómicos de la Fecha
- [Sesión 20261121 091500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20091500.md)
- [Sesión 20261121 111500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20111500.md)
- [Sesión 20261121 114500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20114500.md)
- [Sesión 20261121 124500](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20124500.md)


---

### [2026-11-21 09:22:00] Sesión de Arquitectura: Definición Multi-Perfil y Multi-Plataforma
* **Problema:** Establecer la frontera de funcionalidades y los actores del sistema Taxi para ampliar la cobertura de servicio más allá del despacho interno de garita.
* **Solución:**
  1. Definición formal de 3 perfiles en [`perfiles_usuarios.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/perfiles_usuarios.md):
     - **Administradores:** Configuración global, parametrización de tarifas, flota, bahías y liquidación contable (Windows Desktop / Tablet).
     - **Conductores:** Turnos digitales, cola en tiempo real, alertas de despacho a bahía, estado de recaudos y pagos (Android Móvil).
     - **Clientes (Pasajeros):** Solicitud de taxi, cotización de tarifa por sector, tracking en vivo del móvil asignado e historial (Android Móvil).
  2. Definición formal de 3 plataformas en [`plataformas_dispositivos.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/plataformas_dispositivos.md): Android Teléfonos, Android Tablets y Windows Desktop.
  3. Sincronización ontológica en la LLM Wiki (`docs/wiki/`) y persistencia en Engram (`topic_key: architecture/taxi-profiles-and-platforms`, ID `#644`).


---

### [2026-11-21 09:25:00] Arquitectura de Cobertura: Modelo Cebolla (Núcleo Garita -> Conductor -> Pasajero)
* **Problema:** En el sistema legacy la app era mononivel (exclusivamente para garita/administrador); en Taxi se requiere expandir hacia los conductores y hasta los clientes finales.
* **Solución:**
  1. Diseño y especificación del **Modelo Cebolla** en [`modelo_cebolla_arquitectura.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/modelo_cebolla_arquitectura.md):
     - **Capa 0 (Núcleo):** Administradores/Garitas (censo de flota, bahías, tarifas maestras, cajas).
     - **Capa 1 (Intermedia):** Conductores (enturne digital, despacho a bahía, aceptación de carreras, aportes).
     - **Capa 2 (Perímetro):** Clientes finales (solicitud de taxi, cotización previa, tracking en vivo, calificación).
  2. Protocolo de seguridad y privacidad: aislamiento estricto de datos con Firestore Security Rules (Capa 2 no tiene acceso a balances ni reglas de Capa 0).
  3. Memoria persistente en Engram registrada con ID `#645`.


---

### [2026-11-21 09:27:00] Arquitectura de Monetización: Publicidad y Sostenibilidad Financiera
* **Problema:** Financiar los costos de infraestructura (Firebase Firestore, Functions, APIs de mapas) sin encarecer la operación para taxistas ni pasajeros.
* **Solución:**
  1. Especificación del subsistema de publicidad en [`modelo_monetizacion_publicidad.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/modelo_monetizacion_publicidad.md):
     - **Google AdMob:** Banners adaptativos e intersticiales gobernados por frecuencia (*capping*).
     - **Publicidad Local Directa:** Espacios para patrocinios de marcas y comercios locales (talleres mecánicos, repuestos, estaciones de combustible, aseguradoras).
  2. **Regla Inviolable de Seguridad Vial:** Cero anuncios intrusivos durante el viaje activo del conductor.
  3. Control dinámico de encendido/apagado y límites mediante Firebase Remote Config.
  4. Persistido en Engram con ID `#646`.


---

### [2026-11-21 09:38:00] Generación de Documento Maestro de Contexto para Gemini
* **Problema:** El usuario requiere un archivo `.md` exhaustivo y autocontenido para alimentar cualquier chat de Gemini con el 100% del contexto del proyecto.
* **Solución:**
  1. Recopilación integral de todos los documentos en `docs/`, `docs/wiki/`, `reference/` y bitácoras históricas.
  2. Generación del documento maestro [`docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md`](file:///c:/Workspaces/taxi/docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md) en 10 secciones estructuradas: Ficha técnica, Misión y evolución, Modelo Cebolla (3 capas), Ecosistema multiplataforma (Móvil, Tablet, Desktop), Arquitectura Firebase, Monetización/Publicidad, Síntesis del backend de referencia (38 modelos), Estado del código Flutter, Constitución de La Tripleta y Roadmap.
  3. Catalogación en el índice de la LLM Wiki y memoria persistente en Engram (ID `#647`).


---

### [2026-11-21 09:43:00] Visión de Futuro y Destino Estratégico de Taxi
* **Problema:** Enriquecer el documento maestro de contexto con la visión estratégica integral hacia dónde se dirige el producto.
* **Solución:**
  1. Adición de la **Sección 11** en [`CONTEXTO_MAESTRO_PROYECTO_TAXI.md`](file:///c:/Workspaces/taxi/docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md) cubriendo los 5 ejes estratégicos:
     - **SuperApp Gremial:** Competencia legal y regulada frente a apps transnacionales (Uber, InDrive), tarifas justas y exclusividad de bahías (Aeropuerto, Terminal, Hoteles).
     - **Despacho Híbrido:** Fusión de cola física en bahía con radar en calle para erradicar tiempos muertos y rodamiento en vacío.
     - **Fidelización del Taxista:** Billetera de ahorro programado decembrino, autoliquidación digital de recaudos, botón de auxilio y club de descuentos automotrices.
     - **Distribución en Tiendas:** Salida formal a Google Play Store con actualizaciones continuas.
     - **SaaS Multi-Empresa:** Escalabilidad multi-tenant para expandirse a otras ciudades y empresas de taxi con autosostenibilidad por publicidad.
  2. Actualización en LLM Wiki y memoria persistente en Engram (ID `#648`).


---

### [2026-11-21 10:11:00] Integración del Manifiesto Conceptual: El Taxista como Anfitrión Urbano
* **Problema:** Articular la dimensión humana, gremial y urbana contenida en [`conceptualizaci_n_del_ecosistema_taxi.md`](file:///c:/Workspaces/taxi/docs/conceptualizaci_n_del_ecosistema_taxi.md) dentro de la memoria maestra del sistema.
* **Solución:**
  1. Lectura e integración completa del archivo conceptual.
  2. Adición de la subsección `2.1. Propósito Humano, Urbano y Gremial` en [`CONTEXTO_MAESTRO_PROYECTO_TAXI.md`](file:///c:/Workspaces/taxi/docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md).
  3. Creación del concepto [`proposito_humano_y_ecosistema_urbano.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/proposito_humano_y_ecosistema_urbano.md) en la LLM Wiki y actualización de `index.md` y `log.md`.
  4. Persistido en Engram con ID `#649`.


---

### [2026-11-21 10:27:00] Depuración de Workspace en Cesta y Formalización OpenSpec
* **Problema:** Despejar la raíz, scripts y documentación técnica de los archivos no asociados al nuevo proyecto Taxi, respetando la política de Cero Pérdida de Código.
* **Solución:**
  1. Creación de la estructura [`cesta/`](file:///c:/Workspaces/taxi/cesta/) y segregación limpia:
     - `cesta/root_legacy/`: volcados de código antiguos (`codigo_completo_synergia.md`, `codigo_solo_lib_synergia.md`, `synergia_movil.iml`).
     - `cesta/scripts_legacy_odoo/`: 274 scripts individuales de diagnóstico de Odoo 11.
     - `cesta/docs_legacy_odoo/`: 17 informes y análisis anteriores de servidores.
     - Documentación de custodia en [`cesta/README.md`](file:///c:/Workspaces/taxi/cesta/README.md).
  2. Finalización formal de la propuesta OpenSpec [`taxi-fases-evolucion-completa`](file:///c:/Workspaces/taxi/openspec/changes/taxi-fases-evolucion-completa/):
     - `proposal.md`: Done.
     - `design.md`: Done.
     - `specs/`: 11 especificaciones para todas las fases (Done).
     - `tasks.md`: Lista completa de tareas verificables (Done).
  3. Estado de OpenSpec: `isComplete: true`, lista para arrancar la implementación (`/opsx-apply`).


---

### [2026-11-21 10:31:00] Invariante de Tarifas Legales Estandarizadas (Cero Arbitrariedad)
* **Problema:** En el mercado informal y en apps transnacionales existen cobros arbitrarios, regateos y tarifas dinámicas abusivas que perjudican al usuario y dañan la reputación del gremio.
* **Solución:**
  1. Definición formal de la entidad [`tarifas_legales_y_sectores.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/tarifas_legales_y_sectores.md):
     - **Base Legal:** Matriz oficial de sectores y barrios autorizada por decreto distrital de transporte (DATT).
     - **Cálculo Automático de Recargos:** Nocturno (20:00 - 05:00), festivo/dominical y bahía especial/aeropuerto evaluados por servidor.
     - **Pantalla Espejo:** Pasajero y conductor ven exactamente el mismo valor desglosado antes de iniciar y al finalizar la carrera.
     - **Sanciones:** Prohibición estricta de cobros discrecionales bajo pena de bloqueo en la agremiación.
  2. Actualización de la LLM Wiki y memoria persistente en Engram (ID `#652`).


---

### [2026-11-21 10:38:00] Limpieza Integral de la Raíz del Proyecto
* **Problema:** En la raíz persistían 8 scripts antiguos `.bat` y `.ps1` que apuntaban a binarios y paquetes legacy de `synergia_movil`.
* **Solución:**
  1. Traslado de los 8 scripts a [`cesta/scripts_deploy_legacy/`](file:///c:/Workspaces/taxi/cesta/scripts_deploy_legacy/).
  2. Actualización de [`cesta/README.md`](file:///c:/Workspaces/taxi/cesta/README.md).
  3. La raíz del proyecto queda reducida a los 13 archivos canónicos indispensables (manifiestos, `.env`, `.env.example`, lockfile, linter y constitución).


---

### [2026-11-21 11:45:00] Tripleta Sprint A: Categorías, Oferta con Ancla Legal y Selección de Conductor
* **Problema:** Diseñar e implementar el flujo de solicitud de carreras incorporando la simplicidad de categorías de Uber y la negociación transparente de inDrive sin caer en tarifas predatorias.
* **Solución:**
  1. Especificación formal OpenSpec en [`sprint-a-categorias-ofertas-seleccion-conductor`](file:///c:/Workspaces/taxi/openspec/changes/sprint-a-categorias-ofertas-seleccion-conductor/).
  2. Implementación de `CategoriaViaje` y `ConductorOfertaModel` en `lib/models/viaje_model.dart`.
  3. Métodos de marketplace en `FirestoreRepository` (`proponerOfertaConductor`, `streamOfertasViaje`, `seleccionarConductorViaje`).
  4. Hoja modal reactiva `DriverOffersSheet` para que el pasajero elija su conductor en tiempo real.
  5. Componente interactivo de ajuste de oferta con ancla legal de decreto distrital en `PassengerHomeView`.
  6. Suite TDD `test/models/categoria_oferta_test.dart` pasando 14/14 tests al 100%.
  7. Memoria en Engram registrada con ID `#658`.

---

### [2026-11-21 12:45:00] Tripleta Sprint B: Despacho en Bahía con Enlace WhatsApp para Pasajeros sin App
* **Problema:** Los pasajeros en bahías físicas (centros comerciales, terminales, aeropuertos) abordan a pie sin haber descargado la app móvil; Uber e inDrive no pueden atenderlos sin obligarlos a registrarse.
* **Solución:**
  1. Campo opcional de celular en `TurnoFormView` durante el despacho en garita con autocompletado +57.
  2. Generación automática del viaje en Firestore (`categoria: bahiaPrioritaria`) en `FirestoreRepository`.
  3. Helper `WhatsAppTrackingHelper` para formatear el mensaje enriquecido y generar el enlace web de tracking canónico `https://taxi.fundetaxcol.co/t/{viajeId}`.
  4. Pantalla responsive de ticket digital `WebTicketTrackingView` con sello de verificación, placa colombiana, tarifa decretada desglosada y botón de auxilio SOS.
  5. Suite TDD `test/services/despacho_whatsapp_test.dart` y catalogación en `tests/COMPENDIO_TESTS.md`.
  6. Memoria en Engram registrada con ID `#660`.
