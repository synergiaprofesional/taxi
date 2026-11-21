## 1. Corrección del Selector de Bahías y Modelado de Datos

- [x] 1.1 Actualizar la consulta RPC de bahías en `lib/services/odoo_service.dart` para solicitar `name_sec` en lugar de `name` y filtrar por la sesión activa de hoy (`sesion_id = currentSession`).
- [x] 1.2 Refactorizar `bahia_selector_dialog.dart` reemplazando los avatares deformados (`B8816`) por tarjetas limpias `BahiaCardWidget` mostrando únicamente el nombre corto (`29D`, `Garita`, `Av. Lago`).

## 2. Arquitectura Shell y Navegación de 3 Pestañas

- [x] 2.1 Implementar el shell `BahiaSelectedView` con `BottomNavigationBar` de 3 pestañas: Pagos, Turnos y Despachos usando `IndexedStack` para preservar el estado.
- [x] 2.2 Integrar el `TitleSearchWidget` en la AppBar del Shell para delegar búsquedas en tiempo real a la pestaña activa.
- [x] 2.3 Vincular la escucha de eventos WebSocket (`turn`, `dispatch`, `payment`, `session`) al Shell maestro.

## 3. Módulo de Turnos (Enturnar y Despachar)

- [x] 3.1 Implementar `TurnoListView` con tarjeta `TurnoCardWidget` mostrando círculo de secuencia numérica, placa, conductor y hora.
- [x] 3.2 Implementar `TurnoFormView` en modo Enturnar con switch anónimo, selector de placa con exclusión de vehículos en turno y selector de conductor prioritario.
- [x] 3.3 Implementar `TurnoFormView` en modo Despachar con selector de tarifa, cálculo de recargo nocturno automático y botón de cancelación.

## 4. Módulo de Historial de Despachos

- [x] 4.1 Implementar `DespachoListView` filtrando turnos con tarifa cobrada (`tarifaId.id != 0`).
- [x] 4.2 Habilitar diálogo de reimpresión rápida de tiquetes térmicos al pulsar una tarjeta de despacho.

## 5. Módulo de Recaudos y Pagos Contables

- [x] 5.1 Implementar `PagoListView` ordenado descendentemente por consecutivo contable oficial.
- [x] 5.2 Implementar `PaymentFormView` con formulario maestro, selectores de vehículo y conductor, y footer de total acumulado.
- [x] 5.3 Implementar el sub-componente `PaymentDetail` y la vista modal `PaymentConceptForm` para adición y eliminación dinámica de conceptos.

## 6. Buscadores Genéricos y Ajustes

- [x] 6.1 Implementar `SearchGenericWidget` y `SearchPageWidget` con filtrado incremental y división en dos secciones (conductores principales vs otros).
- [x] 6.2 Implementar `SettingsView` y `SettingInfoExtra` para configuración de impresora, autoPrint y auditoría técnica.

## 7. Pruebas y Verificación Integral

- [x] 7.1 Ejecutar suite de pruebas unitarias y verificar ausencia de errores de compilación (`flutter analyze`).
- [ ] 7.2 Probar flujo completo en tableta física y validar impresión en impresora de tiquetes.
