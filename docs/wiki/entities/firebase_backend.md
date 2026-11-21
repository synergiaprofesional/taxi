# ☁️ Entidad: Backend Firebase (Arquitectura Objetivo)

## 1. Misión
Reemplazar al 100% el backend legacy de Odoo 11 por una infraestructura reactiva, escalable y en tiempo real sobre Google Firebase.

## 2. Componentes Clave
- **Cloud Firestore:**
  - Base de datos NoSQL documental de baja latencia con sincronización offline nativa en Flutter.
  - Colecciones principales mapeadas:
    - `turnos`: Gestión de turnos, estados (`activo`, `despachado`, `cancelado`), marcas de tiempo.
    - `vehiculos`: Placa, móvil, marca, estado técnico-mecánico, asignación de conductor.
    - `conductores`: Datos personales, contacto, licencia, historial.
    - `bahias`: Bahías de despacho, capacidad y orden de salida.
    - `pagos_recaudo`: Consecutivo, montos, conceptos, sesiones de caja.
    - `tarifas`: Matriz de precios por sector/zona geográfica.
- **Firebase Authentication:**
  - Control de acceso por roles (Operador Garita, Administrador, Conductor).
  - Autenticación por correo/contraseña y tokens JWT auto-renovables (sin problemas de cookies de sesión expiradas).
- **Cloud Functions:**
  - Disparadores de negocio (asignación de turnos FIFO, validación de cupos, auditoría de pagos).
  - Webhooks de integración y notificaciones push vía FCM (Firebase Cloud Messaging).
