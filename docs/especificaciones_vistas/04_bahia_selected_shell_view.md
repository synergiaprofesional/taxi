# 🎛️ Especificación de Vista 04: `BahiaSelectedView`
## Shell Central de Operación: Buscador Universal, Menú Contextual y 3 Tabs Nativas

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\views\main\bahia_selected_view.dart`
- **Controlador:** `lib/controllers/root/bahia_selected.controller.dart` (`BahiaSelectedController`)
- **Tipo de Componente:** `StatelessWidget` con `GetBuilder<BahiaSelectedController>`

---

### 1. Propósito y Responsabilidad
Es el marco operativo principal donde el despachador trabaja todo el día. Centraliza la búsqueda universal, el cambio de bahías, los ajustes y la navegación rápida entre las **3 operaciones fundamentales de Fundetaxcol**: Cobros (`Pagos`), Fila de espera (`Turnos`) y Salidas con pasajero (`Despachos`).

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│ [🔍 Buscar turno/pago...]             (⋮)    │
├──────────────────────────────────────────────┤
│                                              │
│                                              │
│                                              │
│             [ BODY DINÁMICO ]                │
│       (Renderiza la pestaña activa)          │
│                                              │
│                                              │
│                                              │
├──────────────────────────────────────────────┤
│    💳 Pagos   │   🚕 Turnos   │  🚪 Despachos │
└──────────────────────────────────────────────┘
```

#### 2.1 AppBar con Buscador Universal (`TitleSearchWidget`)
- Campo de búsqueda interactivo en el AppBar que filtra en tiempo real la pestaña seleccionada.
- Menú contextual `(⋮)` (`PopupMenuButton`):
  - `Bahías`: Invoca RPC `set_state(go_to_bays: true)` y regresa a `BahiaListView`.
  - `Ajustes`: Abre `SettingsView` (Impresora, MAC, autoPrint).
  - `Salir`: Destruye sesión y sale a `LoginWidget`.

#### 2.2 Barra de Navegación Inferior (`BottomNavigationBar`)
- **Pestaña 1:** `Pagos` (`Icons.payment`) $\rightarrow$ Renderiza `PagoListView`.
- **Pestaña 2:** `Turnos` (`Icons.login`) $\rightarrow$ Renderiza `TurnoListView`.
- **Pestaña 3:** `Despachos` (`Icons.logout`) $\rightarrow$ Renderiza `DespachoListView`.

---

### 3. Controlador Asociado: `BahiaSelectedController`
- **Suscripción a WebSocket en Vivo (Puerto 3000):**
  Escucha `server_rt_odoo` y actualiza automáticamente la pestaña correspondiente sin recargar la pantalla completa:
  ```dart
  SocketController().streamController.stream.listen((event) async {
    if (event == sessionId) {
      GlobalControllers.getPreferences().closeSession();
      await Get.offAll(() => MainApp.rootApp);
    } else if (event == turnId || event == dispatchId) {
      final turnWidget = childrenSelectedBay.firstWhere((e) => e.id == turnId).widget as TurnoListView;
      await turnWidget.controller.loadTurns();
      final dispatchWidget = childrenSelectedBay.firstWhere((e) => e.id == dispatchId).widget as DespachoListView;
      await dispatchWidget.controller.loadTurns();
    } else if (event == paymentId) {
      final paymentWidget = childrenSelectedBay.firstWhere((e) => e.id == paymentId).widget as PagoListView;
      await paymentWidget.controller.loadPayments();
    }
  });
  ```
- **Manejo del Botón Atrás (`WillPopScope`):** Si el usuario estaba buscando texto, pulsar atrás cierra la búsqueda en lugar de salirse de la aplicación.
