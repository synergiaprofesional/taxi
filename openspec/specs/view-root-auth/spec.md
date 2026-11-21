# OpenSpec: View Root & Auth (Inicialización y Autenticación)

## Contexto y Arquitectura de Referencia
Esta especificación define la paridad absoluta con los módulos de inicio, control de sesión y autenticación de `fundetaxcol_flutter`, integrando:
- **Vistas Canónicas**:
  - `lib/ui/widgets/root/splash_widget.dart` (`SplashWidget`)
  - `lib/ui/widgets/root/root_widget.dart` (`RootWidget`)
  - `lib/ui/widgets/root/login_widget.dart` (`LoginWidget`)
- **Controladores**:
  - `RootController` (`lib/controllers/root/root.controller.dart`)
  - `LoginController` (`lib/controllers/root/login.controller.dart`)
  - `AuthController` (`lib/controllers/global/auth.controller.dart`)
- **Componentes Visuales**: `LogoWidget(size: 250.0)`, `BlurLoadingWidget` (`lib/ui/widgets/blur_load_widget.dart`)
- **Modelos DTO**: `SettingModel` (`lib/classes/setting.dart`)
- **Almacenamiento Local**: `LocalStorage` / `SharedPreferences`

---

## Modelado de Datos y Contratos Odoo 11

### 1. Endpoint de Autenticación Odoo:
- **Ruta**: `/web/session/authenticate`
- **Payload**:
  ```json
  {
    "db": "fundetaxcol",
    "login": "<username>",
    "password": "<password>"
  }
  ```
- **Respuesta Esperada**: Objeto de sesión con `uid`, `name`, `partner_id`, y persistencia de cookie de sesión (`session_id`).

### 2. Consulta de Estado de Dispositivo Móvil:
- **Modelo**: `fundetaxcol.settings.mobile`
- **Método**: `get_data`
- **Argumentos**: `kwargs: {"uid": "<userId>"}`
- **Retorno**:
  - `currentView`: `'bay'` | `'bays'` | `'home'`
  - `currentBay`: ID de la bahía seleccionada en la sesión
  - `currentSession`: ID de la sesión abierta de hoy
  - `concept`: Concepto de recaudo por defecto
  - `driver`: Conductor genérico de apoyo

---

## Componentes UI y Layout

### 1. `SplashWidget`
- Fondo blanco puro (`Colors.white`).
- Centro: Logotipo oficial de Fundetaxcol mediante `LogoWidget(size: 250.0)`.
- Temporizador y animación de transición `Transition.zoom` con duración de 1.5 a 2 segundos mientras se valida el token.

### 2. `LoginWidget`
- Logotipo oficial centrado (`LogoWidget(size: 200.0)`).
- Formulario con campos:
  - `TextFormField` Usuario: `controller: usernameCtrl`, validación de texto no vacío.
  - `TextFormField` Contraseña: `controller: passwordCtrl`, `obscureText: true`.
- Botón principal `Iniciar sesión`: `CupertinoButton` con fondo azul primario y texto blanco.
- Indicador de carga: `BlurLoadingWidget` superpuesto para bloquear interacciones mientras se valida con el servidor.

---

## Requirements

### Requirement: Arranque y Ciclo de Vida en SplashWidget
El sistema DEBE iniciar la aplicación verificando el almacenamiento local, validando la vigencia del token de sesión en Odoo 11 mediante `validateToken()` y enrutando al operador automáticamente según `currentView`.

#### Scenario: Sesión ausente o token inválido
- **WHEN** la aplicación inicia en frío y no existe token o la validación RPC falla
- **THEN** el sistema DEBE redirigir inmediatamente a `LoginWidget` mediante una animación de transición suave (`Transition.zoom`).

#### Scenario: Sesión válida con bahía operativa activa
- **WHEN** el token es válido y la consulta RPC `fundetaxcol.settings.mobile.get_data` retorna `currentView == 'bay'`
- **THEN** el sistema DEBE abrir de inmediato el centro de mando `BahiaSelectedView` de dicha bahía.

#### Scenario: Sesión válida sin bahía asignada
- **WHEN** el token es válido pero `currentView == 'bays'`
- **THEN** el sistema DEBE abrir el selector de bahías activas `BahiaListView`.

---

### Requirement: Autenticación de Operador en LoginWidget
El sistema DEBE proveer un formulario de autenticación por credenciales contra el endpoint `/web/session/authenticate` de Odoo 11 sobre la base de datos `fundetaxcol`.

#### Scenario: Autenticación exitosa
- **WHEN** el operador ingresa credenciales válidas y pulsa "Iniciar Sesión"
- **THEN** el sistema DEBE autenticar por JSON-RPC, almacenar el `session_id`, `uid` y contexto de usuario en almacenamiento local, invocar `Storage.loadData()` y transicionar a `BahiaListView`.

#### Scenario: Bloqueo de UI durante la autenticación
- **WHEN** el usuario pulsa "Iniciar Sesión"
- **THEN** el sistema DEBE desplegar un `BlurLoadingWidget` y desactivar los campos del formulario para impedir peticiones concurrentes.

#### Scenario: Credenciales inválidas
- **WHEN** el operador ingresa credenciales incorrectas en `fundetaxcol.co`
- **THEN** el sistema DEBE ocultar el overlay de carga, desplegar un `SnackBar` rojo indicando `"Usuario o contraseña incorrectos"` y permanecer en `LoginWidget`.
