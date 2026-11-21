# 🏢 Especificación de Vista 03: `BahiaListView` / `BahiaView`
## Selector de Bahía de Operación (Solo Bahías de la Sesión de Hoy)

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\views\list\bahia_list_view.dart` y `bahia_view.dart`
- **Controlador:** `lib/controllers/list/bay_list.controller.dart` (`BayListController`)
- **Widget de Tarjeta:** `lib/ui/widgets/bahia_card_widget.dart` (`BahiaCardWidget`)
- **Tipo de Componente:** `StatefulWidget` con `GetBuilder<BayListController>`

---

### 1. Propósito y Responsabilidad
Permitir que el operador seleccione en cuál de las bahías asignadas a la sesión activa va a despachar o recaudar. **Debe mostrar única y exclusivamente las bahías activas de la sesión de hoy**, excluyendo sesiones pasadas archivadas.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│  Bahías de Operación                         │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  29D                              🚪 > │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Garita                           🚪 > │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Av. Lago                         🚪 > │  │
│  └────────────────────────────────────────┘  │
│                                              │
└──────────────────────────────────────────────┘
```
- **Contenedor:** `SmartRefresher` con `WaterDropMaterialHeader(color: Colors.blue)` para refresco manual hacia abajo.
- **Lista:** `ListView.separated` con espaciado vertical de `6.0 px`.
- **Tarjeta [`BahiaCardWidget`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/bahia_card_widget.dart):**
  - Borde gris redondeado (`BorderRadius.circular(5.0)`).
  - Título: **Nombre corto de la bahía** en negrita (ej. `29D`, `Garita`, `Av. Lago`).
  - Trailing: Icono de entrada `Icon(Icons.login)` en azul.
  - **PROHIBIDO:** No muestra avatares circulares con IDs desbordados (`B8816`) ni fechas de años pasados (`[2022-05-03]`).

---

### 3. Controlador Asociado: `BayListController`
- **Herencia:** `ListBaseController<BayModel>`
- **Carga de Datos (`loadBays`):**
  ```dart
  Future<void> loadBays({bool reload = false}) async {
    await loadPage(() async {
      entitiesFound = entities = await Storage.getBays(reload: reload);
    }, isLoading: !reload);
  }
  ```
- **Selección de Entidad (`selectEntity`):**
  ```dart
  void selectEntity(BayModel selected) async {
    final authController = GlobalControllers.getAuth();
    await authController.authCommon.client.odoo.callKw({
      'model': 'fundetaxcol.settings.mobile',
      'method': 'set_state',
      'args': [],
      'kwargs': {
        'uid': authController.getUserId(),
        'current_bay': selected.id,
      },
    });
    await SettingsStorage.getSettings();
    await Get.offAll(
      () => BahiaSelectedView(controller: BahiaSelectedController()),
    );
  }
  ```

---

### 4. Invocación Odoo JSON-RPC Exacta
```dart
model: 'fundetaxcol.sesion.bahia',
method: 'search_read',
fields: ['id', 'name_sec'], // <-- name_sec entrega el nombre corto sin fecha
domain: [
  ['sesion_id', '=', settings.currentSession] // <-- Limita a la sesión de hoy
]
```

---

### 5. Modelos Acompañantes
- **`BayModel`** (`lib/classes/bahia.dart`):
  ```dart
  class BayModel {
    int id = 0;
    String name = '';
    factory BayModel.fromJson(Map<String, dynamic> json) {
      final bay = BayModel();
      bay.id = json['id'];
      bay.name = json['name_sec'] ?? json['name'];
      return bay;
    }
  }
  ```
