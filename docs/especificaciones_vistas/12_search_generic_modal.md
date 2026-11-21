# Especificación Técnica de Vista: SearchGenericWidget y SearchPageWidget

## 1. Identificación y Ubicación
- **Archivo en fundetaxcol_flutter**: `lib/ui/views/search/search_widget.dart`
- **Controlador Base**: `ISearchBaseController` (`lib/controllers/search/search.base.controller.dart`)
- **Controladores Especializados**:
  - `CarSearchController` (`lib/controllers/search/vehiculo.search.controller.dart` sobre `fundetaxcol.vehiculo`)
  - `DriverSearchController` (`lib/controllers/search/conductor.search.controller.dart` sobre `res.partner`)
  - `PathSearchController` (`lib/controllers/search/tarifa.search.controller.dart` sobre `fundetaxcol.tarifa.sector`)
  - `ConceptSearchController` (`lib/controllers/search/concepto.search.controller.dart` sobre `fundetaxcol.concepto`)

---

## 2. Propósito y Flujo Operativo
`SearchGenericWidget` encapsula un campo de texto interactivo de solo lectura que al ser pulsado abre a pantalla completa la vista `SearchPageWidget`. Esta pantalla provee una barra de búsqueda con foco automático (`autofocus: true`), filtrado en memoria ultrarrápido y partición visual por secciones (ej. conductores principales vs otros conductores).

---

## 3. Comportamiento y Características Clave
1. **Filtrado Incremental en Vivo**:
   - `_textEditingController.addListener` ejecuta `controller.search(text)` con cada pulsación de tecla.
   - Permite limpiar la búsqueda pulsando la `X` o cerrarla retornando `-1`.
2. **Soporte de Dos Secciones (`firstSectionWidget`)**:
   - Si `elementsSection` contiene elementos (ej. los conductores habituales del vehículo seleccionado), se renderizan en la parte superior con un encabezado distintivo (`titleFirstSection`), seguidos de los elementos generales (`titleSecondSection`).
3. **Exclusión de Ítems Activos**:
   - `CarSearchController` recibe `excludeValue` para excluir automáticamente vehículos que ya se encuentren en la cola de turnos de la bahía.
4. **Retorno de Selección**:
   - Tap en cualquier elemento ejecuta `Get.back(result: element)` entregando el JSON del modelo seleccionado al formulario que invocó la búsqueda.
