# Leyes y Metodología del Proyecto - Taxi

Este documento es la **Constitución Inviolable** del repositorio `Taxi`. Cualquier agente de IA, subagente o desarrollador humano **DEBE** obedecer estas reglas de forma estricta e incondicional.

---

## 1. Metodología de Entrega: "La Tripleta"

Todo cambio técnico no trivial sigue de manera obligatoria e indivisible el ciclo de la **Tripleta de Trabajo**:

1. **SDD + OpenSpec Híbrido (`artifact_store: hybrid`):**
   - Planificar antes de picar (`propose` → `spec` → `design` → `tasks`).
   - Persistencia dual: Engram MCP (`topic_key: sdd/{change-name}/*`) y archivos Markdown locales (`openspec/changes/{change-name}/`).
   - TDD Estricto con pruebas unitarias (cero fallos tolerados).
   - Archivado formal al terminar (`openspec archive`).
2. **Tríada de Bitácoras Obligatoria (3 Archivos en Disco):**
   - `Bitacoras/{YYYY}/{MM}/bitacora.md` (Monolito Mensual).
   - `Bitacoras/{YYYY}/{MM}/{DD}/Bitacoras YYYYMMDD.md` (Diario del Día).
   - `Bitacoras/{YYYY}/{MM}/{DD}/Bitacoras YYYYMMDD HHmmss.md` (Snapshot Atómico con Resumen, Cambios Técnicos, Tool Attribution, Decisiones, Memoria y Próximos Pasos).
3. **Curación y Gobernanza Obligatoria de LLM Wiki (`docs/wiki/`):**
   - Sincronizar entidades (`docs/wiki/entities/`) y conceptos (`docs/wiki/concepts/`).
   - Catalogar en `docs/wiki/index.md` y asentar el evento en `docs/wiki/log.md`.
4. **Persistencia en Engram:**
   - Registro de decisiones y aprendizajes con `mem_save` y cierre de sesión con `mem_session_summary`.

---

## 2. Desacoplamiento Absoluto de Configuración ("La Tripleta de Código")

Queda **ESTRICTAMENTE PROHIBIDO** quemar variables, rutas locales absolutas, IPs o credenciales en el código fuente.
- Capa 1: Infraestructura y Secretos (`.env` y `.env.example`).
- Capa 2: Matrices de Negocio Declarativas (`config_*.json`).
- Capa 3: Capa Tipada de Carga (`config.py` o equivalente tipado en Dart/Python).

---

## 3. Toolkit Unificado y Custodia Histórica (`Consolidados/`)

1. **Preservación Inmutable:** Prohibido purgar scripts históricos. Se custodian en `scripts/back/{YYYYMMDD}/`.
2. **Centralización Obligatoria:** Prohibido crear scripts sueltos en la raíz. Toda rutina debe implementarse como método de servicio en `Consolidados/services/` y exponerse en `Consolidados/cli.py`.
3. **Tool Attribution:** Todo script o comando utilizado debe ser documentado con enlaces `file://...` en bitácoras y artefactos SDD.

---

## 4. Inviolabilidad de Dominio y Bounded Context

1. Cada agente y subagente opera única y exclusivamente dentro de su frontera funcional.
2. Si una solicitud está fuera de dominio, el agente debe detenerse en seco, rechazarla cortésmente y derivar al subagente o área competente sin inventar datos ni ejecutar herramientas ajenas.
3. Prohibido lanzar falsas alarmas o notificaciones de fallos técnicos ante consultas fuera de alcance.

---

## 5. Compendio TDD y Estructura Modular de Pruebas (`tests/`)

1. Prohibido crear pruebas sueltas en la raíz de `tests/` o `test/`. Toda suite debe ubicarse bajo su subcarpeta modular isomórfica.
2. Todo test nuevo o modificado debe quedar catalogado en `tests/COMPENDIO_TESTS.md`.
3. Cero tolerancia a fallos en la ejecución de la suite de pruebas.

---

## 6. Servidor de Producción: Perímetro de Solo Consulta (Estricto Read-Only)

1. **PROHIBICIÓN TOTAL DE ESCRITURA EN EL SERVIDOR:** El servidor `fundetaxcol.co` es exclusivamente para consulta.
2. Queda prohibida cualquier mutación o modificación en el servidor remoto.
3. El código del servidor reside localmente como referencia en la carpeta `reference/`.

---

## 7. Misión Arquitectónica de Taxi: Desacoplamiento de Odoo hacia Firebase

1. **Sin Odoo 11:** La nueva aplicación Taxi opera con base de datos Firebase (Firestore, Auth, Functions).
2. **UX Familiar:** Interfaz y flujos que garanticen cero dificultad de transición a los operadores y conductores actuales.
3. **Mayor Cobertura:** Diseñada para una cobertura superior y escalabilidad de servicios de taxi.
