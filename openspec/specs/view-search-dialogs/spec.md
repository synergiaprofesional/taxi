# OpenSpec: View Search Dialogs (Componentes de Búsqueda y Autocompletado)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con los componentes de búsqueda incremental de `fundetaxcol_flutter`, integrando:
- **Vista de Campo Integrado**: `SearchGenericWidget<T extends ISearchBaseController>` (`lib/ui/views/search/search_widget.dart`)
- **Vista Modal de Búsqueda**: `SearchPageWidget` (`lib/ui/views/search/search_widget.dart#L71`)
- **Controlador Base**: `ISearchBaseController` (`lib/controllers/search/search.base.controller.dart`)
- **Implementaciones Especializadas**:
  - `CarSearchController` (`lib/controllers/search/vehiculo.search.controller.dart` sobre `fundetaxcol.vehiculo`, con filtro de exclusión de placas en turno)
  - `DriverSearchController` (`lib/controllers/search/conductor.search.controller.dart` sobre `res.partner`, con partición conductores principales vs padrón)
  - `PathSearchController` (`lib/controllers/search/tarifa.search.controller.dart` sobre `fundetaxcol.tarifa.sector`)
  - `ConceptSearchController` (`lib/controllers/search/concepto.search.controller.dart` sobre `fundetaxcol.concepto`)
- **Estructura de Secciones**: `ListSection(title: String, elements: List)`

---

## Componentes UI y Layout

### 1. `SearchGenericWidget` (Campo Disparador)
- Renderiza un `TextFormField` de solo lectura (`readOnly: true`).
- Decoración:
  - Borde con `OutlineInputBorder()`.
  - Etiqueta (`labelText: title`).
  - Fondo morado tenue (`fillColor: Colors.purple.shade50`) si el campo es obligatorio (`required: true`).
- Al pulsar (`onTap`):
  - Abre la vista modal a pantalla completa `SearchPageWidget`.
  - Al retornar el elemento seleccionado, ejecuta el callback `onChange(element)` y actualiza el controlador local `controller.setValue(element)`.

### 2. `SearchPageWidget` (Pantalla de Búsqueda Incremental)
- **AppBar**:
  - Título con `TextFormField` integrado, `autofocus: true` y `hintText: 'Buscar [título]...'`.
  - Botón de acción con icono de cierre `Icons.close`:
    - Si el texto está lleno, lo limpia.
    - Si el texto está vacío, cierra la vista retornando `-1` (deselección).
- **Lista de Resultados**:
  - Si `elementsSection` tiene elementos, renderiza `firstSectionWidget`:
    - Encabezado de primera sección con fondo gris (`gray200`): `"Conductores principales"`.
    - Lista de elementos prioritarios con tap individual.
    - Encabezado de segunda sección con fondo gris: `"Otros conductores"`.
  - Renderizado mediante `ListView.builder` de los elementos filtrados.
  - Indicador de carga: `BlurLoadingWidget` si el controlador está cargando datos de Odoo.
  - Estado vacío: `Center(child: Text('No hay datos'))` si no hay coincidencias.

---

## Requirements

### Requirement: Buscador Incremental Genérico en SearchPageWidget
El sistema DEBE proveer un componente modal de búsqueda a pantalla completa (`SearchPageWidget`) accesible desde cualquier campo `SearchGenericWidget`, con filtrado en memoria ultrarrápido y foco automático en el teclado.

#### Scenario: Búsqueda reactiva por pulsación de tecla
- **WHEN** el usuario ingresa a `SearchPageWidget` y digita caracteres
- **THEN** el sistema DEBE actualizar instantáneamente el listado en memoria mostrando únicamente los registros cuyo campo designado contenga el texto buscado.

#### Scenario: Partición de resultados en dos secciones para conductores
- **WHEN** el controlador `DriverSearchController` recibe la lista `elementsToSection` con los conductores asignados al vehículo
- **THEN** el modal DEBE renderizar en la cabecera el encabezado `"Conductores principales"` con dichos registros, y abajo `"Otros conductores"` con el resto de la base de datos.

#### Scenario: Exclusión de vehículos activos en cola
- **WHEN** el operador pulsa el selector de placas en modo nuevo turno o nuevo pago
- **THEN** `CarSearchController` DEBE filtrar y omitir todos los vehículos cuyos IDs figuren en `excludeValue` (`carsToExclude`), impidiendo seleccionar un taxi duplicado.

#### Scenario: Retorno de selección al formulario padre
- **WHEN** el usuario pulsa sobre cualquiera de las filas de resultado
- **THEN** el sistema DEBE cerrar la vista de búsqueda con `Get.back(result: element)` y pasar el mapa JSON al callback `onChange`.
