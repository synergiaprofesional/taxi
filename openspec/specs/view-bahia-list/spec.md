# OpenSpec: View Bahía List (Selector de Bahía Operativa)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/views/list/bahia_list_view.dart` (`BahiaListView`) y `bahia_view.dart`
- **Controlador**: `BayListController` (`lib/controllers/list/bay_list.controller.dart`)
- **Tarjeta Visual**: `BahiaCardWidget` (`lib/ui/widgets/bahia_card_widget.dart`)
- **Modelo DTO**: `BayModel` (`lib/classes/bahia.dart`)
- **Referencia Técnica**: `docs/especificaciones_vistas/03_bahia_list_view.md`

---

## Modelado Odoo 11 y Contratos RPC
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
- **Campos**: `name_sec` (nombre corto sin fecha de sesión: `29D`, `Garita`, `Av. Lago`).
- **Filtro**: Estricto a la sesión abierta de hoy (`sesion_id = currentSession`).

---

## Componentes UI y Layout
- `SmartRefresher` con `WaterDropMaterialHeader(color: Colors.blue)`.
- `ListView.separated` espaciado de `6.0 px`.
- `BahiaCardWidget`: Borde redondeado, nombre corto en negrita e icono de entrada `Icon(Icons.login)` en azul.
- Prohibición estricta de avatares `B8816` y fechas pasadas.

---

## Requirements

### Requirement: Filtrado Estricto de Bahías Operativas del Día
El sistema DEBE consultar a Odoo el modelo `fundetaxcol.sesion.bahia` solicitando únicamente los campos `id` y `name_sec`, aplicando un filtro estricto por la sesión activa de la fecha (`sesion_id = currentSession`), eliminando del listado cualquier registro histórico de fechas previas o sesiones cerradas.

#### Scenario: Carga de bahías de la sesión activa
- **WHEN** el despachador ingresa a `BahiaListView` tras autenticarse
- **THEN** el sistema DEBE invocar `search_read` sobre `fundetaxcol.sesion.bahia` con el dominio `[['sesion_id', '=', settings.currentSession]]` y campos `['id', 'name_sec']`.

#### Scenario: Visualización limpia de nombres de bahía
- **WHEN** las bahías se renderizan en pantalla
- **THEN** cada tarjeta `BahiaCardWidget` DEBE mostrar exclusivamente el nombre corto (`29D`, `Garita`, `Av. Lago`) sin concatenar fechas ni mostrar avatares numéricos desbordados.

### Requirement: Activación y Persistencia de Bahía Operativa
El sistema DEBE actualizar el estado operativo del despachador en el backend mediante RPC `fundetaxcol.settings.mobile.set_state` al seleccionar una bahía y transicionar inmediatamente al centro de comando.

#### Scenario: Selección satisfactoria de bahía
- **WHEN** el operador pulsa sobre una de las tarjetas de bahía activa
- **THEN** el sistema DEBE enviar `set_state(current_bay: selected.id)`, almacenar la bahía en `SettingsStorage` y abrir `BahiaSelectedView`.
