# 📅 Monolito Mensual de Bitácoras — Noviembre de 2026
# Proyecto: Taxi
**Repositorio:** `c:\Workspaces\taxi`

Este archivo consolida todas las sesiones de trabajo técnico del mes de Noviembre de 2026 bajo la metodología de **La Tripleta** y SDD.

---

## 📌 Índice de Sesiones de Noviembre 2026

- **2026-11-21:** [Sesión 114500 - Tripleta Sprint A: Categorías, Oferta con Ancla Legal y Selección de Conductor](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20114500.md)
- **2026-11-21:** [Sesión 111500 - Desarrollo e Implementación de Modelos Firestore, Vistas Conductor/Pasajero y TDD](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20111500.md)
- **2026-11-21:** [Sesión 091500 - Instanciación de Constitución Taxi, Repositorio de Referencia y Gobernanza](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20091500.md)

---

## 📝 Sesión: 2026-11-21 11:45:00 — Tripleta Sprint A: Categorías, Oferta con Ancla Legal y Selección de Conductor

### 1. Resumen Ejecutivo
- **Contexto:** Fusión de lo mejor de Uber (categorías en 1 toque) e inDrive (negociación y marketplace de conductores) adaptado al taxi formal.
- **Acción:** Especificación OpenSpec en `sprint-a-categorias-ofertas-seleccion-conductor/`, modelos `CategoriaViaje` y `ConductorOfertaModel`, repositorio reactivo Firestore, vista `DriverOffersSheet` y cotizador interactivo en `PassengerHomeView`.
- **TDD:** Suite `categoria_oferta_test.dart` pasando 14/14 tests al 100%.

---

## 📝 Sesión: 2026-11-21 11:15:00 — Desarrollo e Implementación de Modelos Firestore, Vistas Conductor/Pasajero y TDD

### 1. Resumen Ejecutivo
- **Contexto:** Materialización técnica de las fases de desarrollo e implementación bajo OpenSpec sobre Flutter y Firebase.
- **Acción:** Creación de modelos NoSQL puros (`UserModel`, `ViajeModel`, `OrganizacionModel`, `TarifaSectorModel`, `RecaudoModel`), `FirestoreRepository`, `firestore.rules`, sincronización en `TurnoController`, vistas `DriverHomeView`, `PassengerHomeView`, `PassengerTripTrackingView` y widget `AdmobBannerWidget` con enclavamiento vial.
- **TDD:** Corrección de imports residuales `synergia_movil` hacia `package:taxi` y 46 pruebas unitarias/widgets pasando al 100% (cero fallos).

---

## 📝 Sesión: 2026-11-21 09:15:00 — Constitución Taxi y Repositorio de Referencia

### 1. Resumen Ejecutivo
- **Contexto:** Creación e independización de la versión `Taxi` a partir de `synergia_movil` para una cobertura ampliada y desacoplamiento de Odoo 11 hacia Firebase.
- **Acción:** Inspección y extracción en modo estricto de SOLO LECTURA del servidor en producción (`fundetaxcol.co`), respaldando módulos de Odoo, Node.js y configuraciones en `reference/`.
- **Implementación:** Adopción obligatoria de la Constitución Maestra `AGENTS.md` y `GEMINI.md`, inicialización de `docs/wiki/`, creación del Toolkit Unificado `Consolidados/` y custodia de scripts en `scripts/back/20261121/`.

### 2. Archivos e Hitos Clave
- Constitución: [`AGENTS.md`](file:///c:/Workspaces/taxi/AGENTS.md)
- Toolkit CLI: [`Consolidados/cli.py`](file:///c:/Workspaces/taxi/Consolidados/cli.py)
- Wiki Maestro: [`docs/wiki/index.md`](file:///c:/Workspaces/taxi/docs/wiki/index.md)
- Compendio Tests: [`tests/COMPENDIO_TESTS.md`](file:///c:/Workspaces/taxi/tests/COMPENDIO_TESTS.md)
- Snapshot Atómico: [`Bitacoras 20261121 091500.md`](file:///c:/Workspaces/taxi/Bitacoras/2026/11/21/Bitacoras%2020261121%20091500.md)


---

## 📝 Sesión: 2026-11-21 09:22:00 — Definición de Perfiles y Plataformas de Despliegue

### 1. Resumen Ejecutivo
- Se establecieron los 3 perfiles principales del sistema: Administradores (Desktop/Tablet), Conductores (Android Móvil) y Clientes (Android Móvil).
- Se definió la compatibilidad multiplataforma de Flutter para abarcar teléfonos, tablets de garita y consolas desktop Windows.
- Se documentaron las entidades y conceptos en la LLM Wiki y se guardó la memoria arquitectónica en Engram (ID `#644`).
