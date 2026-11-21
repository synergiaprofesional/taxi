# 📝 Registro de Mutaciones - LLM Wiki (Append-Only)

Historial inmutable de actualizaciones, ingestas y modificaciones ontológicas en la Wiki de Taxi.

---

## [2026-11-21] ingest | Constitución Inicial del Proyecto Taxi y Repositorio de Referencia
- **Alcance:** Creación de la Wiki Maestro para el proyecto `Taxi`.
- **Entidades registradas:** `servidor_produccion.md` (Modo Solo Lectura), `firebase_backend.md` (Arquitectura Objetivo).
- **Conceptos registrados:** `arquitectura_taxi.md` (Desacoplamiento de Odoo hacia Firebase, Alta Cobertura), `transicion_ux_usuarios.md` (Continuidad operativa).
- **Estado:** Ingesta inicial validada con el Toolkit Unificado (`Consolidados/cli.py`).

---

## [2026-11-21] update | Definición de Perfiles RBAC y Ecosistema Multi-Plataforma
- **Alcance:** Especificación formal de los tres perfiles de usuario del sistema (Administrador, Conductor, Cliente/Pasajero) y de los dispositivos de despliegue (Android Teléfonos, Android Tablets y Windows Desktop).
- **Entidades registradas:** [`perfiles_usuarios.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/perfiles_usuarios.md), [`plataformas_dispositivos.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/plataformas_dispositivos.md).
- **Conceptos actualizados:** [`arquitectura_taxi.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/arquitectura_taxi.md) incorporando el ecosistema de 3 perfiles sobre Firebase.
- **Estado:** Gobernanza ontológica sincronizada y validada.

---

## [2026-11-21] update | Formalización del Modelo Cebolla de Arquitectura
- **Alcance:** Definición del Modelo Cebolla (Capas Concéntricas de Acceso): Núcleo Administrativo/Garita (Capa 0) -> Conductores (Capa 1) -> Clientes Pasajeros (Capa 2).
- **Concepto registrado:** [`modelo_cebolla_arquitectura.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/modelo_cebolla_arquitectura.md).
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Especificación del Modelo de Monetización y Publicidad
- **Alcance:** Definición de la estrategia de autosostenibilidad económica mediante publicidad integrada (Google AdMob + publicidad local directa de convenios gremiales).
- **Invariante crítico:** Prohibición estricta de publicidad intrusiva durante la conducción activa para proteger la seguridad vial.
- **Concepto registrado:** [`modelo_monetizacion_publicidad.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/modelo_monetizacion_publicidad.md).
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Generación de Documento Maestro de Contexto para Gemini
- **Alcance:** Creación del archivo canónico [`CONTEXTO_MAESTRO_PROYECTO_TAXI.md`](file:///c:/Workspaces/taxi/docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md) recopilando la totalidad de la documentación, bitácoras, código legacy de referencia, modelo cebolla, perfiles, plataformas y directrices de monetización.
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Incorporación del Destino Estratégico y Visión de Futuro
- **Alcance:** Actualización de [`CONTEXTO_MAESTRO_PROYECTO_TAXI.md`](file:///c:/Workspaces/taxi/docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md) y [`arquitectura_taxi.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/arquitectura_taxi.md) con la Sección 11 sobre el horizonte a largo plazo (SuperApp gremial, despacho híbrido bahía/calle, fidelización del conductor, ahorro programado, publicación en Play Store y SaaS multi-empresa).
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Integración del Manifiesto Conceptual del Ecosistema Taxi
- **Alcance:** Catalogación e integración del manifiesto [`conceptualizaci_n_del_ecosistema_taxi.md`](file:///c:/Workspaces/taxi/docs/conceptualizaci_n_del_ecosistema_taxi.md) y creación del concepto ontológico [`proposito_humano_y_ecosistema_urbano.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/proposito_humano_y_ecosistema_urbano.md).
- **Invariantes:** El taxista como primer y último anfitrión de la ciudad, eje vertical con hoteles, restaurantes y sitios recreativos, el valor del cliente de a pie y recomendación mutua de confianza.
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Depuración y Organización del Proyecto en Cesta de Custodia
- **Alcance:** Creación del directorio [`cesta/`](file:///c:/Workspaces/taxi/cesta/) para segregar archivos históricos y no correspondientes al alcance de `Taxi`:
  - `cesta/root_legacy/`: volcados de código anteriores (`codigo_completo_synergia.md`, `codigo_solo_lib_synergia.md`, `synergia_movil.iml`).
  - `cesta/scripts_legacy_odoo/`: 274 scripts heredados de minería y optimización de Odoo 11.
  - `cesta/docs_legacy_odoo/`: 17 informes y análisis anteriores de servidores.
- **Resultado:** Raíz, `scripts/` y `docs/` limpios y enfocados 100% en el nuevo desarrollo de `Taxi`.
- **OpenSpec:** Propuesta integral [`taxi-fases-evolucion-completa`](file:///c:/Workspaces/taxi/openspec/changes/taxi-fases-evolucion-completa/) completada al 100% (Proposal, Design, Specs y Tasks listos para Apply).

---

## [2026-11-21] update | Especificación de Gremios, Jerarquías y Tipología de Conductores
- **Alcance:** Definición del modelo multi-tenant de Gremios/Organizaciones con organigrama jerárquico (Gerencia -> Coordinadores -> Garita -> Propietarios -> Conductores).
- **Entidades registradas:** [`gremios_y_organizaciones.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/gremios_y_organizaciones.md) y concepto [`jerarquia_gremial_y_visibilidad_flota.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/jerarquia_gremial_y_visibilidad_flota.md).
- **Invariantes clave:**
  1. Conductores Públicos (flota abierta visible para cualquier ciudadano en calle).
  2. Conductores Privados (flota corporativa asignada a convenios exclusivos de hoteles, clínicas o industrias, oculta del despacho público general).
  3. Pasajeros Públicos con 3 modalidades de vinculación: General, Corporativo (convenio) y Referido por Conductor.
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Estandarización Legal de Tarifas y Cero Arbitrariedad
- **Alcance:** Creación de la entidad [`tarifas_legales_y_sectores.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/tarifas_legales_y_sectores.md).
- **Invariante no negociable:** Las tarifas deben ser 100% legales, verificables y basadas en decretos distritales.
- **Prohibición expresa:** Cero tarifas dinámicas especulativas (multiplicadores por lluvia), cero cobros discrecionales del conductor y cero regateos.
- **Transparencia bidireccional:** El desglose (base + recargo nocturno/festivo + terminal) se visualiza idéntico en las pantallas del pasajero y del conductor.
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Especificaciones OpenSpec de Jerarquías Gremiales y Tarifas Legales
- **Alcance:** Creación de especificaciones formales normativas con escenarios `WHEN/THEN` en OpenSpec:
  - [`jerarquia-gremial-flota-dual`](file:///c:/Workspaces/taxi/openspec/specs/jerarquia-gremial-flota-dual/spec.md): Organigrama gremial, conductores públicos vs privados, y 3 modalidades de vinculación de pasajeros.
  - [`tarifas-legales-estandarizadas`](file:///c:/Workspaces/taxi/openspec/specs/tarifas-legales-estandarizadas/spec.md): Tarifas basadas en decretos distritales, recargos calculados en servidor, pantalla espejo y auditoría de sobrecostos.
- **Estado OpenSpec:** Cambio [`taxi-fases-evolucion-completa`](file:///c:/Workspaces/taxi/openspec/changes/taxi-fases-evolucion-completa/) sincronizado con 13 especificaciones y 37 tareas (`isComplete: true`).

---

## [2026-11-21] update | Limpieza de Raíz y Estandarización Minimalista
- **Alcance:** Depuración de la raíz del proyecto. Traslado de los 8 scripts `.bat` y `.ps1` sueltos anteriores hacia [`cesta/scripts_deploy_legacy/`](file:///c:/Workspaces/taxi/cesta/scripts_deploy_legacy/).
- **Resultado:** La raíz conserva estrictamente 13 archivos canónicos de configuración, gobernanza y manifiesto Flutter.

---

## [2026-11-21] update | Implementación de Modelos Firestore, Vistas Conductor/Pasajero y TDD
- **Alcance:** Creación de la capa de datos NoSQL pura (`UserModel`, `ViajeModel`, `OrganizacionModel`, `TarifaSectorModel`, `RecaudoModel`), repositorio `FirestoreRepository` y `firestore.rules`.
- **UI:** Desarrollo de `DriverHomeView` (Capa 1: cola, ahorro programado, radar calle, SOS) y `PassengerHomeView` / `PassengerTripTrackingView` (Capa 2: cotizador oficial, pantalla espejo, calificación).
- **Seguridad Vial:** `AdmobBannerWidget` con enclavamiento de destrucción de anuncios durante la conducción activa.
- **TDD:** 46 pruebas unitarias y de widgets pasando al 100% (cero fallos).
- **Estado:** Gobernanza ontológica sincronizada.

---

## [2026-11-21] update | Sprint A: Categorías, Oferta con Ancla Legal y Selección de Conductor
- **Alcance:** Especificación formal en OpenSpec [`sprint-a-categorias-ofertas-seleccion-conductor`](file:///c:/Workspaces/taxi/openspec/changes/sprint-a-categorias-ofertas-seleccion-conductor/).
- **Modelos:** Ingesta de `CategoriaViaje` y `ConductorOfertaModel` en `ViajeModel`.
- **UI & Marketplace:** Hoja interactiva `DriverOffersSheet` en tiempo real y selector con ancla legal e incrementos en `PassengerHomeView`.
- **TDD:** 14/14 tests pasando al 100% en `test/models/categoria_oferta_test.dart`.
- **Estado:** Gobernanza ontológica sincronizada.
