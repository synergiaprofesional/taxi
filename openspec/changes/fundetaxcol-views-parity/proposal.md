# Proposal: Paridad Modular Vista a Vista (1 a 1) de fundetaxcol_flutter en Synergia Móvil

## Why

La aplicación actual `synergia_movil` presenta deficiencias de usabilidad y visualización (selectores de bahías contaminados con registros históricos antiguos, avatares deformados `B8816`, y falta de la arquitectura modular de pestañas y formularios especializados probada en producción).

Para resolver esta brecha de manera rigurosa, se establece la especificación formal OpenSpec individual para cada una de las 14 vistas y formularios operativos de `fundetaxcol_flutter`, garantizando una trazabilidad y paridad técnica absoluta sin ambigüedades.

## What Changes

- Creación de 14 especificaciones canónicas individuales en OpenSpec, mapeadas 1 a 1 contra las 14 vistas documentadas en `docs/especificaciones_vistas/`.
- Replicación exacta de los componentes visuales, layouts, contratos JSON-RPC con Odoo 11, controladores y reglas de negocio para cada pantalla.

## Capabilities

### New Capabilities

- `view-splash-root`: Inicialización de storage, validación de token y enrutador inicial (`01_splash_root_view.md`).
- `view-login`: Formulario de autenticación por credenciales contra Odoo 11 (`02_login_view.md`).
- `view-bahia-list`: Selección de bahías activas de la sesión de hoy usando `name_sec` (`03_bahia_list_view.md`).
- `view-bahia-selected-shell`: Contenedor maestro con 3 pestañas fijas, buscador universal y WebSocket (`04_bahia_selected_shell_view.md`).
- `view-turno-list`: Fila reactiva de taxis en espera de servicio en bahía (`05_turno_list_view.md`).
- `view-turno-form-enturnar`: Formulario de ingreso a cola, modo anónimo y exclusión de placas (`06_turno_form_enturnar_view.md`).
- `view-turno-form-despacho`: Asignación de ruta, cálculo de recargo nocturno, cancelación e impresión (`07_turno_form_despacho_view.md`).
- `view-despacho-list`: Historial cronológico de despachos con destino, tarifa y reimpresión (`08_despacho_list_view.md`).
- `view-pago-list`: Historial y consulta de cobros y recaudos contables diarios (`09_pago_list_view.md`).
- `view-pago-form`: Formulario maestro de cobro con sub-lista de conceptos y totalización (`10_pago_form_view.md`).
- `view-pago-concepto-form`: Modal de captura y edición de conceptos contables dinámicos (`11_pago_concepto_form_view.md`).
- `view-search-generic-modal`: Modal incremental con división en secciones para vehículos y conductores (`12_search_generic_modal.md`).
- `view-settings`: Configuración de MAC de impresora, switch autoPrint y concepto por defecto (`13_settings_view.md`).
- `view-setting-info-extra`: Panel de auditoría técnica y verificación de parámetros del servidor (`14_setting_info_extra_view.md`).

### Modified Capabilities

(Ninguna).

## Impact

- **Frontend**: Separación estricta de responsabilidades en 14 pantallas y componentes especializados.
- **Backend Odoo 11**: Consumo estricto y seguro de los modelos existentes sin modificaciones en el servidor `fundetaxcol.co`.
