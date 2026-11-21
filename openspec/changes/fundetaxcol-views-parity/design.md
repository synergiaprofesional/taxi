# Technical Design: Arquitectura y Paridad Modular de Vistas fundetaxcol_flutter

## Context

`fundetaxcol_flutter` es la aplicación nativa en producción utilizada por los despachadores en las bahías de taxis (Cartagena, Bolívar). Su arquitectura operativa está dividida en un flujo determinista:
1. `SplashWidget` (inicialización de storage, validación de token y consulta de vista activa).
2. `LoginWidget` (autenticación JSON-RPC contra Odoo 11).
3. `BahiaListView` (selección obligatoria de bahía activa de la sesión de hoy).
4. `BahiaSelectedView` (contenedor Shell con 3 pestañas: Pagos, Turnos, Despachos, AppBar con buscador en vivo y sincronización WebSocket).
5. Formularios y sub-flujos modulares: `TurnoFormView` (Enturnar y Despachar), `PaymentFormView` + `PaymentConceptForm` (cobro con desglose de conceptos) y buscadores incrementales `SearchGenericWidget`.

`synergia_movil` intentó unificar toda la operación en una sola pantalla (`HomeView`) con diálogos superpuestos. Esto provocó:
- Selección de bahías contaminada con registros históricos de sesiones pasadas (con fechas 2022-2026 y etiquetas visuales truncadas `B8816`).
- Falta de una lista dedicada para historial de despachos del día.
- Falta de un flujo formal de cobro de recaudos con múltiples conceptos contables y totalización.
- Falta de los buscadores modulares que dividen conductores habituales del padrón general y excluyen vehículos ya en cola.

## Goals / Non-Goals

**Goals:**
- Replicar con fidelidad 1 a 1 los modelos, controladores, vistas y reglas de negocio de `fundetaxcol_flutter`.
- Implementar la navegación Shell en `BahiaSelectedView` con `BottomNavigationBar` de 3 tabs: Pagos (`PagoListView`), Turnos (`TurnoListView`) y Despachos (`DespachoListView`).
- Corregir el selector de bahías para que use exclusivamente `fields: ['id', 'name_sec']` y filtre por `domain: [['sesion_id', '=', settings.currentSession]]`.
- Implementar el formulario de pago completo con agregación dinámica de conceptos y suma total reactiva.
- Implementar los buscadores genéricos con soporte para dos secciones (conductores habituales vs otros).
- Mantener la compatibilidad nativa con la impresora térmica Win32 (`TIQUETES` en `USB001`) y Bluetooth en Android.

**Non-Goals:**
- No modificar el backend Odoo 11 en `fundetaxcol.co` ni alterar el servidor `server_rt_odoo` en puerto 3000.
- No implementar pasarelas de pago externas o flujos que no existan en `fundetaxcol_flutter`.

## Decisions

### Decisión 1: Estructura de Navegación Basada en 3 Tabs Nativos
- **Opción elegida**: Usar un Shell `BahiaSelectedView` con `IndexedStack` o `PageView` gestionado por `BottomNavigationBar` con 3 pestañas (Pagos, Turnos, Despachos).
- **Razón**: Es el modelo ergonómico que los operadores de bahía conocen y utilizan a diario sin necesidad de reentrenamiento.
- **Alternativa descartada**: Mantener el panel monolítico con botones flotantes (rechazado por el usuario por ser deficiente).

### Decisión 2: Consulta de Bahías mediante `name_sec` y Filtro de Sesión
- **Opción elegida**:
  ```dart
  model: 'fundetaxcol.sesion.bahia',
  fields: ['id', 'name_sec'],
  domain: [['sesion_id', '=', currentSession]]
  ```
- **Razón**: El campo `name` en Odoo incluye la fecha de la sesión (`"Av. Lago Sesión [2022-05-03]"`), lo que saturaba la pantalla. `name_sec` contiene solo el nombre operativo (`"29D"`, `"Garita"`, `"Av. Lago"`). Filtrar por `currentSession` garantiza que solo aparezcan las bahías activas de hoy.
- **Alternativa descartada**: Consultar `domain: [['state', '=', 'progreso']]` sin filtro de sesión (traía sesiones antiguas nunca cerradas).

### Decisión 3: Arquitectura de Formularios y Modales de Conceptos
- **Opción elegida**: Desacoplar el formulario de pagos `PaymentFormView` del modal de concepto `PaymentConceptForm`. Al retornar del modal, se inserta el `PaymentConceptModel` en la lista en memoria `conceptoIds` y se recalcula el total `totalConcepts`.
- **Razón**: Permite agregar múltiples conceptos (ej. Rodamiento $15.000 + Ahorro $5.000) antes de enviar la transacción atómica a Odoo.

### Decisión 4: Buscador Incremental con Partición de Secciones
- **Opción elegida**: Componente `SearchGenericWidget` con `SearchPageWidget`. Si el objeto seleccionado es un taxi (`vehiculoId`), se extraen sus `conductorIds` y se inyectan como primera sección en el selector de conductor ("Conductores principales") antes del listado general ("Otros conductores").
- **Razón**: Acelera en más del 80% la selección de conductores en la ventanilla de la bahía.

## Risks / Trade-offs

- **Riesgo**: Pérdida de estado en tabs al cambiar de pestaña.
  - **Mitigación**: Usar `IndexedStack` o `AutomaticKeepAliveClientMixin` en los controladores de lista para conservar el scroll y los datos cargados.
- **Riesgo**: Disparo doble de impresión térmica en modo autoPrint.
  - **Mitigación**: Validar bandera booleana `isPrinting` y ejecutar de forma asíncrona no bloqueante después de recibir confirmación exitosa de Odoo.
