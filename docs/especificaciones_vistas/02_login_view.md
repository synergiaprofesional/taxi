# 🔐 Especificación de Vista 02: `LoginWidget`
## Autenticación de Operadores y Despachadores en Odoo 11

- **Archivo Canónico:** `C:\Workspaces\fundetaxcol_flutter\lib\ui\widgets\root\login_widget.dart`
- **Controlador:** `lib/controllers/root/login.controller.dart` (`LoginController`)
- **Tipo de Componente:** `StatelessWidget` con `GetBuilder<LoginController>`

---

### 1. Propósito y Responsabilidad
Permitir a los operadores de bahía y cajeros iniciar sesión de forma segura contra Odoo 11 utilizando credenciales de usuario del sistema. Bloquea el acceso a las funciones operativas hasta que la autenticación sea confirmada por el servidor.

---

### 2. Componentes UI y Layout
```
┌──────────────────────────────────────────────┐
│                                              │
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
│                                              │
│               ⚙️ Ajustes de Red               │
└──────────────────────────────────────────────┘
```
- **Campos del Formulario:**
  - `TextFormField` Usuario: `controller: _.usernameCtrl`, con validación obligatoria.
  - `TextFormField` Contraseña: `controller: _.passwordCtrl`, `obscureText: true`.
  - Botón Principal: `CupertinoButton` con fondo azul (`AppColors.primary`), texto blanco "Iniciar sesión".
  - Botón Secundario / Icono: Acceso a configuración de Host/Puerto si se requiere contingencia.
- **Overlay de Bloqueo:** Cuando `_.loading == true`, despliega [`BlurLoadingWidget`](file:///C:/Workspaces/fundetaxcol_flutter/lib/ui/widgets/blur_load_widget.dart) para impedir doble envío de peticiones.

---

### 3. Controlador Asociado: `LoginController`
- **Variables:**
  - `TextEditingController usernameCtrl`
  - `TextEditingController passwordCtrl`
  - `bool loading = false`
- **Método `signIn()`:**
  ```dart
  Future<void> signIn() async {
    final username = usernameCtrl.text.trim();
    final password = passwordCtrl.text.trim();
    loading = true;
    update();
    final ok = await authController.signIn(username, password);
    loading = false;
    update();
    if (ok) {
      // Limpia cachés obsoletas y navega a selección de bahía
      await Storage.loadData();
      Get.offAll(() => const BahiaView());
    } else {
      showSnackBar('Usuario o contraseña incorrectos', color: Colors.red);
    }
  }
  ```

---

### 4. Invocación Odoo JSON-RPC
- **Endpoint:** `/web/session/authenticate`
- **Params:**
  ```json
  {
    "db": "fundetaxcol",
    "login": "<username>",
    "password": "<password>"
  }
  ```
- **Respuesta Exitosa:**
  - `result.uid`: ID del usuario en `res.users`.
  - `result.name`: Nombre completo del operador.
  - Header `Set-Cookie`: Almacena la cookie de sesión (`session_id`).
