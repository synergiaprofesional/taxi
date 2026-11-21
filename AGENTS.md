# Leyes y Metodología del Proyecto - Taxi

Este documento es la **Constitución Inviolable** del repositorio `Taxi`. Cualquier agente de IA, subagente o desarrollador humano **DEBE** obedecer estas reglas de forma estricta e incondicional.

---

## 1. Metodología de Entrega: "La Tripleta"

Todo cambio técnico no trivial sigue de manera obligatoria e indivisible el ciclo de la **Tripleta de Trabajo**:

```text
┌────────────────────────┐      ┌─────────────────────────────────┐      ┌────────────────────────┐
│   1. Pipeline SDD      │ ───► │ 2. Tríada Bitácoras + LLM Wiki  │ ───► │  3. Memoria Persistente│
│ (Spec-Driven Develop.) │      │   (Cronológico + Ontológico)    │      │   (Engram MCP Saves)   │
└────────────────────────┘      └─────────────────────────────────┘      └────────────────────────┘
```

1. **SDD + OpenSpec Híbrido (`artifact_store: hybrid`):**
   - **Planificar antes de picar:** Todo desarrollo arranca con `propose` → `spec` → `design` → `tasks`.
   - **Persistencia Dual Obligatoria:** 
     - Memoria persistente MCP en **Engram** (`topic_key: sdd/{change-name}/*`).
     - Archivos locales en el repositorio dentro de **`openspec/changes/{change-name}/`**.
   - **TDD Estricto:** Obligatorio escribir y ejecutar pruebas unitarias en la fase `apply` y validar con `verify` (cero fallos tolerados).
   - **Cierre formal:** Todo cambio se archiva formalmente con `openspec archive <change-name>`.

2. **Generación Obligatoria de la Tríada de Bitácoras (3 Archivos en Disco):**
   - Al finalizar cualquier entrega o sesión, es **ESTRICTAMENTE OBLIGATORIO** sincronizar los tres niveles de bitácora bajo el árbol jerárquico por fecha:
     - **a) Monolito Mensual (`Bitacoras/{YYYY}/{MM}/bitacora.md`):** Reside dentro de la carpeta del mes correspondiente. Consolida y apendea todas las sesiones del mes en curso. Al iniciar un nuevo mes calendario, el monolito del mes anterior queda cerrado como histórico inmutable en su carpeta (`Bitacoras/{YYYY}/{MM_anterior}/bitacora.md`) y se inicia un nuevo `bitacora.md` limpio para el mes actual. Prohibido mantener monolitos globales en la raíz de `Bitacoras/`.
     - **b) Diario del Día (`Bitacoras/{YYYY}/{MM}/{DD}/Bitacoras YYYYMMDD.md`):** Consolida y agrupa todas las ejecuciones y cambios ocurridos durante la fecha.
     - **c) Snapshot Atómico (`Bitacoras/{YYYY}/{MM}/{DD}/Bitacoras YYYYMMDD HHmmss.md`):** Fotografía puntual e inmutable con 5 secciones:
       1. Resumen Ejecutivo (Contexto, Causa Raíz, Solución).
       2. Cambios Técnicos y Herramientas (Tool Attribution con enlaces `file://...`).
       3. Decisiones Arquitectónicas y Trade-offs.
       4. Estado de Memoria (Engram MCP Save ID).
       5. Próximos Pasos.
   - **Regla de Estructura Jerárquica:** Las carpetas de Año (`{YYYY}`), Mes (`{MM}`) y Día (`{DD}`) se crean bajo demanda única y exclusivamente cuando existan archivos para esa fecha. Prohibido crear carpetas vacías.

3. **Curación y Gobernanza Obligatoria de LLM Wiki (`docs/wiki/` - Memoria Ontológica):**
   - La LLM Wiki es la memoria ontológica viva de reglas de negocio, esquemas e invariantes (a diferencia de las bitácoras, que son cronológicas).
   - **Entidades (`docs/wiki/entities/`):** Crear o actualizar la página canónica del proveedor, sistema, motor de BD o actor con contratos, endpoints y modelos.
   - **Conceptos (`docs/wiki/concepts/`):** Registrar políticas de negocio, arquitecturas, fuentes e invariantes.
   - **Índice Central (`docs/wiki/index.md`):** Catalogar las entidades y conceptos en la tabla maestra.
   - **Log de Mutaciones (`docs/wiki/log.md`):** Registrar obligatoriamente el evento append-only (`## [YYYY-MM-DD] ingest|update | Título`).
   - **Prohibición Expresa:** Queda terminantemente prohibido cerrar una entrega si se descubrieron o alteraron invariantes de negocio sin haber actualizado la Wiki.

4. **Persistencia en Engram:**
   - Registro de decisiones y lecciones con `mem_save` y cierre de sesión formal con `mem_session_summary`.

---

## 2. Desacoplamiento Absoluto de Configuración ("La Tripleta de Código")

Queda **ESTRICTAMENTE PROHIBIDO** quemar variables, rutas locales absolutas, IPs o credenciales en el código fuente. La configuración se desacopla en tres capas:

1. **Infraestructura y Secretos (`.env` y `.env.example`):** Servidores, credenciales, usuarios, puertos y rutas raíz.
2. **Matriz de Negocio Declarativa (`config_*.json`):** Mapeos de negocio, tablas, fuentes y reglas declarativas.
3. **Capa Tipada de Carga (`config.py` o equivalente Dart/Python):** Dataclasses o clases tipadas que leen y validan las dos capas anteriores en tiempo de ejecución.

---

## 3. Toolkit Unificado y Custodia Histórica (`Consolidados/`)

1. **Preservación Inmutable (Cero Pérdida de Código):** Prohibido desechar o purgar código de scripts históricos. Todos los scripts heredados de minería, diagnóstico y soporte se custodian permanentemente en `scripts/back/{YYYYMMDD}/`.
2. **Centralización Obligatoria:** Queda **TERMINANTEMENTE PROHIBIDO** crear scripts sueltos o monouso en la raíz del workspace o en la raíz de `scripts/`. Toda rutina reutilizable debe residir en `Consolidados/services/` y exponerse en `Consolidados/cli.py`.
3. **Arquitectura Canónica:**
   - `Consolidados/core/`: Configuración tipada (`config.py`) y clientes de datos protegidos (`db.py`).
   - `Consolidados/services/`: Clases de servicio por dominio (`{modulo}_ops.py`) con métodos tipados y reutilizables.
   - `Consolidados/cli.py`: CLI maestro unificado con doble interfaz: menú interactivo por terminal (sin argumentos) y subcomandos automatizados por flags (`argparse`).
4. **Tool Attribution Obligatorio:** Todo script o comando utilizado o refactorizado debe documentarse obligatoriamente con enlace markdown explícito (`file://...`) en las bitácoras y artefactos SDD, detallando servicio invocado, comando exacto y resultado.

---

## 4. Inviolabilidad de Dominio y Bounded Context

1. **Aislamiento Estricto (Single Responsibility):** Cada agente, subagente o módulo opera única y exclusivamente dentro de su frontera funcional.
2. **Rechazo Inmediato:** Si se formula una solicitud fuera del dominio activo, el agente tiene **ESTRICTAMENTE PROHIBIDO** inventar datos o ejecutar herramientas ajenas. Debe detenerse en seco, rechazar cortésmente la operación y derivar al subagente o módulo competente.
3. **Prohibición de Falsas Alarmas:** Prohibido emitir falsas alarmas o notificaciones de error alegando problemas técnicos ficticios ante peticiones fuera de alcance.

---

## 5. Compendio TDD y Estructura Modular de Pruebas (`tests/`)

1. **Prohibición de Suites Sueltas:** Prohibido crear archivos de prueba sueltos en la raíz de `tests/` o `test/`. Toda suite debe ubicarse dentro de su subcarpeta modular isomórfica a la arquitectura del proyecto.
2. **Catálogo Obligatorio (`tests/COMPENDIO_TESTS.md`):** Todo archivo de prueba creado o modificado debe quedar catalogado detallando ruta del archivo, propósito técnico, componentes evaluados y comando CLI exacto de ejecución.
3. **Cero Tolerancia a Fallos:** Ninguna entrega se considera válida si el arnés de pruebas arroja un solo fallo o error.

---

## 6. Independencia Total y Dominio Oficial: PídemeAquí (pidemeaqui.com)

1. **Sin relación con fundetaxcol.co:** El proyecto `Taxi` es 100% independiente. Queda terminantemente prohibido incluir referencias a `fundetaxcol.co` en el código fuente, configuraciones activas o variables de entorno.
2. **Infraestructura VPS Propia:** El servidor de despliegue y backend web oficial es el VPS `80.190.75.49` bajo el dominio canónico `https://pidemeaqui.com` gestionado con Caddy y Docker.
3. **Custodia en Carpeta Local `reference/`:** El código heredado se conserva únicamente en local para análisis de compatibilidad operativa.

---

## 7. Misión Arquitectónica de Taxi: Desacoplamiento de Odoo hacia Firebase

1. **Sin Odoo 11:** La nueva aplicación `Taxi` NO se conecta a Odoo 11. Su infraestructura de persistencia y backend reactivo será Firebase (Firestore, Authentication, Cloud Functions).
2. **Transición sin Fricción (Ergonomía y UX Familiar):** La experiencia de usuario, interfaz visual, flujos de trabajo (turnos, despacho, cobros, bahías) deben mantenerse intuitivos y familiares para que los usuarios actuales operen sin curva de aprendizaje o rechazo operativo.
3. **Mayor Cobertura y Escalabilidad:** El nuevo propósito abarca mayores servicios, despacho dinámico y soporte multi-entorno sin las restricciones de latencia del legacy Odoo 11.
