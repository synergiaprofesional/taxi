# Proposal: Paridad Funcional Absoluta con fundetaxcol_flutter

## Resumen Ejecutivo
Alineación militar y paridad funcional estricta de la aplicación `synergia_movil` con el sistema base de producción `C:\Workspaces\fundetaxcol_flutter`. Se conservará al 100% el diseño visual moderno actual (Dark Theme estilo WhatsApp / Movilidad Taxi), corrigiendo las limitaciones operativas reportadas por los coordinadores de terminal:
1. **Búsqueda Transversal de Pagos**: Búsqueda global a través de todas las bahías del sistema cuando hay texto en el buscador (no solo Garita).
2. **Búsqueda Global de Turnos**: Búsqueda en el pool general de turnos de la jornada.
3. **Servicios Despachados del Conductor**: Visualización y búsqueda de todos los despachos que realiza el conductor en el día a nivel general de la sesión (sin limitarse a una bahía).
4. **Resolución Automática de Conductor**: Erradicar el estado "Conductor Desconocido" al ingresar placa (ej. WGM776) y asociar automáticamente los conceptos de cobro del conductor/vehículo.
5. **Estabilidad de Sesión y Ciclo de Vida Android**: Erradicar el cierre automático de la aplicación por inactividad o cambio de app, eliminando `taskAffinity=""` y garantizando tolerancia a latencia de red.

## Alcance
- **Capacidades Modificadas**:
  - `view-pago-list`: Búsqueda reactiva global multi-bahía.
  - `view-turno-list`: Búsqueda transversal en cola operativa.
  - `view-despacho-list`: Historial transversal de despachos del conductor.
  - `view-pago-form`: Auto-resolución de conductor y carga de conceptos.
  - `view-root-auth`: Preservación de proceso en Android y tolerancia de timeout.

## Impacto
Cero impacto en el diseño visual de la interfaz. Corrección del 100% de los defectos operativos reportados en pruebas de campo.
