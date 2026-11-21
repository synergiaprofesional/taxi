# OpenSpec: View Splash & Root (Arranque, Gatekeeper y Enrutamiento)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/widgets/root/splash_widget.dart` y `root_widget.dart`
- **Controlador**: `RootController` (`lib/controllers/root/root.controller.dart`)
- **Tipo de Componente**: `StatelessWidget` / `StatefulWidget` con `GetBuilder<RootController>`
- **Referencia Técnica**: `docs/especificaciones_vistas/01_splash_root_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│                                              │
│               [ LOGO OFICIAL ]               │
│               (size: 250 px)                 │
│                                              │
└──────────────────────────────────────────────┘
```
- **Fondo**: Blanco puro (`Colors.white`).
- **Logo**: `LogoWidget(size: 250.0)` renderizando `assets/img/logo.jpg`.
- **Transición**: `Duration(milliseconds: 1500)` con animación `Transition.zoom`.

---

## Controlador y Contratos Odoo 11
- `authController.validateToken()`: Valida vigencia de sesión en backend.
- RPC `fundetaxcol.settings.mobile.get_data` (`kwargs: {'uid': authController.getUserId()}`):
  - Retorna `currentView` (`'bay'` | `'bays'` | `'home'`), `currentBay` y `currentSession`.

---

## Requirements

### Requirement: Arranque y Ciclo de Vida en SplashWidget
El sistema DEBE iniciar la aplicación verificando el almacenamiento local, validando la vigencia del token de sesión en Odoo 11 y enrutando al operador automáticamente según `currentView`.

#### Scenario: Sesión ausente o token inválido
- **WHEN** la aplicación inicia en frío y no existe token o la validación RPC falla
- **THEN** el sistema DEBE redirigir inmediatamente a `LoginWidget` mediante una animación de transición suave (`Transition.zoom`).

#### Scenario: Sesión válida con bahía operativa activa
- **WHEN** el token es válido y la consulta RPC `fundetaxcol.settings.mobile.get_data` retorna `currentView == 'bay'`
- **THEN** el sistema DEBE abrir de inmediato el centro de mando `BahiaSelectedView` de dicha bahía.

#### Scenario: Sesión válida sin bahía asignada
- **WHEN** el token es válido pero `currentView == 'bays'`
- **THEN** el sistema DEBE abrir el selector de bahías activas `BahiaListView`.
