# 📱 Especificación de Vista 01: `SplashWidget` y `RootWidget`
## Control de Arranque, Gatekeeper de Token y Enrutador Inicial

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\widgets\root\splash_widget.dart` y `root_widget.dart`
- **Controlador:** `lib/controllers/root/root.controller.dart` (`RootController`)
- **Tipo de Componente:** `StatelessWidget` / `StatefulWidget` con `GetBuilder<RootController>`

---

### 1. Propósito y Responsabilidad
Controlar el ciclo de vida inicial de la aplicación. Muestra el logotipo corporativo de Fundetaxcol, inicializa el almacenamiento local (`LocalStorage`), verifica si existe una sesión válida en Odoo 11 mediante token (`checkSession`), y enruta al usuario según su estado operativo.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│                                              │
│                                              │
│               [ LOGO OFICIAL ]               │
│               (size: 250 px)                 │
│                                              │
│                                              │
│                                              │
└──────────────────────────────────────────────┘
```
- **Contenedor:** Fondo blanco puro (`Colors.white`).
- **Centro:** `LogoWidget(size: 250.0)` renderizando `assets/img/logo.jpg`.
- **Transición:** `Duration(milliseconds: 1500)` con animación suave `Transition.zoom`.

---

### 3. Controlador Asociado: `RootController`
- **Inyección:** `GetBuilder<RootController>(init: RootController(), ...)`
- **Variables de Estado:**
  - `bool logged = false`: Indica si el token es válido.
  - `bool loading = true`: Bloquea mientras verifica el estado.
  - `Duration duration = const Duration(seconds: 2)`
- **Métodos Principales:**
  - `onInit()`:
    ```dart
    authController.validateToken().then((value) async {
      logged = value;
      loading = false;
      if (!logged) {
        Timer(duration, splash.goToLogin);
      } else {
        await goToHome();
      }
      update();
    });
    ```
  - `goToHome()`:
    ```dart
    var settings = await SettingsStorage.getSettings();
    if (settings.currentView == 'bay') {
      Timer(duration, splash.goToBay);     // BahiaSelectedView
    } else if (settings.currentView == 'bays') {
      Timer(duration, splash.goToBays);    // BahiaListView
    } else {
      Timer(duration, splash.goToHome);    // HomeWidget
    }
    ```

---

### 4. Modelos y DTOs Acompañantes
- **`SettingModel`** (`lib/classes/setting.dart`):
  - `currentView`: `String` ('bay' | 'bays' | 'home').
  - `currentBay`: `int` (ID de la bahía seleccionada en la sesión).
  - `currentSession`: `int` (ID de la sesión de Odoo).

---

### 5. Invocaciones Odoo JSON-RPC
- `odoo.checkSession()`: Valida si la cookie/token en SharedPreferences sigue viva en el backend.
- `fundetaxcol.settings.mobile.get_data`:
  - `kwargs: {'uid': authController.getUserId()}`
  - Retorna la configuración completa del operador móvil.
