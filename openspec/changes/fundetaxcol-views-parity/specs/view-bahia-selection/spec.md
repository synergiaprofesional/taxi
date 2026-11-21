# OpenSpec: View Bahía Selection (Selección de Bahías Operativas)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con el selector de bahías de `fundetaxcol_flutter`, integrando:
- **Vista Canónica**: `lib/ui/views/list/bahia_list_view.dart` (`BahiaListView`) y `bahia_view.dart`
- **Controlador**: `BayListController` (`lib/controllers/list/bay_list.controller.dart`)
- **Tarjeta Visual**: `BahiaCardWidget` (`lib/ui/widgets/bahia_card_widget.dart`)
- **Modelo DTO**: `BayModel` (`lib/classes/bahia.dart`)
- **Almacenamiento Local**: `Storage.getBays()` y `SettingsStorage.getSettings()`

---

## Modelado de Datos y Contratos Odoo 11

### Consulta Odoo JSON-RPC para Carga de Bahías:
```json
{
  "model": "fundetaxcol.sesion.bahia",
  "method": "search_read",
  "args": [],
  "kwargs": {
    "fields": ["id", "name_sec"],
    "domain": [
      ["sesion_id", "=", "<currentSessionId>"]
    ]
  }
}
```
- **Justificación de Campos**: `name_sec` contiene el nombre operativo conciso (`29D`, `Garita`, `Av. Lago`). Se PROHÍBE terminantemente usar el campo `name` sin parsear ya que concatena la fecha de la sesión (ej. `Av. Lago Sesión [2022-05-03]`).
- **Justificación de Dominio**: El dominio `['sesion_id', '=', currentSession]` restringe los resultados a la sesión abierta de la fecha actual, impidiendo la contaminación con sesiones inactivas de años anteriores.

### Invocación RPC de Activación de Estado:
```json
{
  "model": "fundetaxcol.settings.mobile",
  "method": "set_state",
  "args": [],
  "kwargs": {
    "uid": "<userId>",
    "current_bay": "<selectedBayId>"
  }
}
```

---

## Componentes UI y Layout
- **Contenedor Principal**: `SmartRefresher` con `WaterDropMaterialHeader(color: Colors.blue)` para pull-to-refresh.
- **Lista**: `ListView.separated` con espaciado vertical de `6.0 px` y `BouncingScrollPhysics`.
- **Tarjeta `BahiaCardWidget`**:
  - Contenedor con borde gris redondeado (`BorderRadius.circular(5.0)`).
  - Título a la izquierda: Nombre corto de la bahía en negrita (`29D`, `Garita`, `Av. Lago`).
  - Trailing a la derecha: Icono de acceso `Icon(Icons.login)` en color azul.
  - **Restricción de Diseño**: Queda terminantemente PROHIBIDO renderizar avatares circulares con identificadores alfanuméricos desbordados (como `B8816`) o fechas de años anteriores.

---

## Requirements

### Requirement: Filtrado Estricto de Bahías Operativas del Día
El sistema DEBE consultar a Odoo el modelo `fundetaxcol.sesion.bahia` solicitando únicamente los campos `id` y `name_sec`, aplicando un filtro estricto por la sesión activa de la fecha (`sesion_id = currentSession`), eliminando del listado cualquier registro histórico de fechas previas o sesiones cerradas.

#### Scenario: Carga de bahías de la sesión activa
- **WHEN** el despachador ingresa a `BahiaListView` tras autenticarse
- **THEN** el sistema DEBE invocar `search_read` sobre `fundetaxcol.sesion.bahia` con el dominio `[['sesion_id', '=', settings.currentSession]]` y campos `['id', 'name_sec']`.

#### Scenario: Renderizado limpio sin fechas antiguas ni avatares deformados
- **WHEN** las bahías se renderizan en pantalla
- **THEN** cada tarjeta `BahiaCardWidget` DEBE mostrar exclusivamente el nombre corto (`29D`, `Garita`, `Av. Lago`) y un icono de acceso, sin prefijos `B8816` ni fechas concatenadas.

#### Scenario: Refresco manual mediante Pull-to-Refresh
- **WHEN** el operador desliza la lista hacia abajo
- **THEN** el sistema DEBE disparar `loadBays(reload: true)` forzando la consulta fresca a Odoo y completando la animación de `WaterDropMaterialHeader`.

---

### Requirement: Activación y Persistencia de Bahía Operativa
El sistema DEBE actualizar el estado operativo del despachador en el backend mediante RPC `fundetaxcol.settings.mobile.set_state` al seleccionar una bahía y transicionar inmediatamente al centro de comando.

#### Scenario: Selección satisfactoria de bahía
- **WHEN** el operador pulsa sobre una de las tarjetas de bahía activa
- **THEN** el sistema DEBE enviar `fundetaxcol.settings.mobile.set_state(current_bay: selected.id)`, almacenar la bahía en `SettingsStorage` y abrir `BahiaSelectedView` mediante `Get.offAll`.

#### Scenario: Persistencia de selección ante reinicio de app
- **WHEN** la aplicación se cierra y se vuelve a abrir con una sesión vigente
- **THEN** el `RootController` DEBE leer `currentView == 'bay'` y abrir directamente `BahiaSelectedView` en la bahía previamente elegida sin pedir seleccionarla nuevamente.
