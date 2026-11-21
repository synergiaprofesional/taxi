# OpenSpec: View Search Generic Modal (Búsqueda Incremental y Autocompletado)

## Contexto y Arquitectura de Referencia
- **Componentes Canónicos**: `SearchGenericWidget` y `SearchPageWidget` (`lib/ui/views/search/search_widget.dart`)
- **Controlador Base**: `ISearchBaseController` (`lib/controllers/search/search.base.controller.dart`)
- **Controladores Especializados**:
  - `CarSearchController` (`fundetaxcol.vehiculo`, con exclusión de taxis en turno)
  - `DriverSearchController` (`res.partner`, partición conductores habituales vs padrón)
  - `PathSearchController` (`fundetaxcol.tarifa.sector`)
  - `ConceptSearchController` (`fundetaxcol.concepto`)
- **Referencia Técnica**: `docs/especificaciones_vistas/12_search_generic_modal.md`

---

## Componentes UI y Layout
- **Campo `SearchGenericWidget`**: `readOnly: true`, `onTap` abre `SearchPageWidget`, fondo morado tenue si `required: true`.
- **Pantalla Modal `SearchPageWidget`**:
  - AppBar con `TextFormField` integrado, `autofocus: true`, botón `Icons.close` para limpiar o cancelar con `-1`.
  - Soporte de dos secciones (`firstSectionWidget`): Encabezado superior `"Conductores principales"`, encabezado inferior `"Otros conductores"`.
  - Tap en ítem: Cierra con `Get.back(result: element)`.

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
