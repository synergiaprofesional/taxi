## 1. Configuración de Red y Autenticación en Odoo 11

- [x] 1.1 Configurar `NetworkConfig` con fallback automático a HTTP (puerto 80) y Socket.IO (puerto 3000)
- [x] 1.2 Implementar método de auto-login y persistencia de credenciales en `OdooService`
- [x] 1.3 Crear componente UI `LoginDialog` con formulario y selector ágil de usuarios de bahía

## 2. Erradicación de Mock Data y Sincronización de Bahías

- [x] 2.1 Eliminar de forma definitiva `cargarTurnosSimulados()` en `TurnoController`
- [x] 2.2 Implementar `cargarBahiasDesdeServidor()` consumiendo `fundetaxcol.sesion.bahia` activas de la fecha
- [x] 2.3 Conectar selector de bahías en el AppBar con el listado dinámico de Odoo

## 3. Carga y Tiempo Real de Turnos de Producción

- [x] 3.1 Actualizar `cargarTurnosDesdeServidor()` para extraer turnos reales por `bahia_id`
- [x] 3.2 Configurar `SocketService` para escuchar eventos `turn`, `dispatch`, `session`, `payment`
- [x] 3.3 Integrar refresco reactivo automático en la vista principal `HomeView`

## 4. Verificación y Empaquetado Release

- [x] 4.1 Ejecutar `flutter analyze` y asegurar 0 errores de estática
- [x] 4.2 Ejecutar suite `flutter test` y verificar 100% pruebas aprobadas
- [x] 4.3 Compilar binarios Release nativos Windows (`synergia_movil.exe`) y Android (`app-release.apk`)
