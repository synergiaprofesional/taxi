## 1. Interfaz de Autenticación y Gatekeeper

- [x] 1.1 Implementar `lib/ui/views/auth/login_view.dart` con branding Fundetaxcol, botones táctiles de acceso rápido por bahía y formulario seguro.
- [x] 1.2 Implementar `lib/ui/views/auth/auth_gatekeeper.dart` con widget reactivo `Obx` que bloquea la interfaz operativa hasta autenticar en Odoo.

## 2. Integración de Servicios y Cierre de Sesión

- [x] 2.1 Actualizar `lib/services/odoo_service.dart` con estado reactivo `isLoggingIn` y purga atómica de sesión en `cerrarSesion()`.
- [x] 2.2 Conectar `AuthGatekeeper` en `lib/main.dart` como punto de entrada raíz de la aplicación.
- [x] 2.3 Vincular los botones de cerrar sesión y salida en `lib/ui/views/home/home_view.dart` para retorno instantáneo al Login.

## 3. Verificación y Pruebas

- [x] 3.1 Crear prueba automatizada `test/login_gatekeeper_test.dart` verificando bloqueo sin sesión y desbloqueo con sesión activa.
- [x] 3.2 Ejecutar `flutter analyze` y `flutter test` verificando 0 advertencias y 100% pruebas aprobadas.
