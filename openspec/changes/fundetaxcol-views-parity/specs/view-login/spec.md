# OpenSpec: View Login (Autenticación de Operadores)

## Contexto y Arquitectura de Referencia
- **Archivo Canónico**: `lib/ui/widgets/root/login_widget.dart`
- **Controlador**: `LoginController` (`lib/controllers/root/login.controller.dart`)
- **Tipo de Componente**: `StatelessWidget` con `GetBuilder<LoginController>`
- **Referencia Técnica**: `docs/especificaciones_vistas/02_login_view.md`

---

## Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│               [ LOGO OFICIAL ]               │
│               (size: 200 px)                 │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ Usuario: [ jose@fundetaxcol.co       ] │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ Contraseña: [ ••••••••••             ] │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │         [ INICIAR SESIÓN ]             │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```
- **Campos**:
  - `TextFormField` Usuario (`usernameCtrl`), no vacío.
  - `TextFormField` Contraseña (`passwordCtrl`), `obscureText: true`.
  - `CupertinoButton` color primario azul, texto blanco "Iniciar sesión".
- **Overlay de Bloqueo**: `BlurLoadingWidget` cuando `loading == true`.

---

## Contratos Odoo 11
- Endpoint `/web/session/authenticate`:
  ```json
  {
    "db": "fundetaxcol",
    "login": "<username>",
    "password": "<password>"
  }
  ```
- Almacena cookie de sesión `session_id`, `uid` y llama a `Storage.loadData()`.

---

## Requirements

### Requirement: Autenticación de Operador en LoginWidget
El sistema DEBE proveer un formulario de autenticación por credenciales contra el endpoint `/web/session/authenticate` de Odoo 11 sobre la base de datos `fundetaxcol`.

#### Scenario: Autenticación exitosa
- **WHEN** el operador ingresa credenciales válidas y pulsa "Iniciar Sesión"
- **THEN** el sistema DEBE autenticar por JSON-RPC, almacenar el `session_id`, `uid` y contexto de usuario, invocar `Storage.loadData()` y transicionar a `BahiaListView`.

#### Scenario: Bloqueo de UI durante la autenticación
- **WHEN** el usuario pulsa "Iniciar Sesión"
- **THEN** el sistema DEBE desplegar un `BlurLoadingWidget` y desactivar los campos del formulario para impedir peticiones concurrentes.

#### Scenario: Credenciales inválidas
- **WHEN** el operador ingresa credenciales incorrectas en `fundetaxcol.co`
- **THEN** el sistema DEBE ocultar el overlay de carga, desplegar un `SnackBar` rojo indicando `"Usuario o contraseña incorrectos"` y permanecer en `LoginWidget`.
