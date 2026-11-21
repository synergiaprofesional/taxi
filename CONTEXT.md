# 🏛️ CONTEXT.md — Contexto Central de Arquitectura y Reglas

**Proyecto:** Taxi — PídemeAquí  
**Versión Actual:** `v3.0.0+1`  
**Framework:** Flutter SDK `^3.12.2` / Dart  
**Gestor de Estado:** GetX (`^4.7.3`)  
**Backend:** Google Cloud Firestore + Firebase Auth + Firebase Functions  
**Plataforma Web y Servidor VPS:** `https://pidemeaqui.com` (`80.190.75.49` con Caddy v2 y Docker)

---

## 📦 Paquetes y Versiones Clave (`pubspec.yaml`)
- `firebase_core`, `cloud_firestore`, `firebase_auth`, `firebase_messaging` (Backend reactivo en la nube)
- `google_mobile_ads: ^5.1.0` (Monetización con enclavamiento de seguridad vial)
- `get: ^4.7.3` (Gestión de estado reactivo, inyección de dependencias `Get.put`/`Get.find`, enrutamiento)
- `shared_preferences: ^2.5.6` (Persistencia local en disco)
- `intl: ^0.20.3` (Formateo de moneda `es_CO` y fechas)

---

## 🧱 Estructura Canónica de Directorios
- `lib/core/` -> Configuración, red (`NetworkConfig`), tema (`AppColors`, `AppTheme`), utilidades (`LocalStorage`, `WhatsAppTrackingHelper`).
- `lib/models/` -> Modelos puros e inmutables (`UserModel`, `ViajeModel`, `TurnoModel`, `OrganizacionModel`, `TarifaSectorModel`, `RecaudoModel`).
- `lib/services/` -> Servicios de datos y hardware (`FirestoreRepository`, `FirebaseService`, `PrinterService`).
- `lib/controllers/` -> Lógica de negocio reactiva (`TurnoController`, `ThemeController`).
- `lib/ui/views/` -> Pantallas multi-rol (`auth/`, `bahia/`, `driver/`, `passenger/`, `form/`, `home/`, `list/`, `settings/`).
- `lib/ui/widgets/` -> Componentes visuales (`admob_banner_widget.dart`, `despacho_card_widget.dart`, etc.).
- `scripts/` -> Scripts de despliegue y validación del VPS `pidemeaqui.com`.
- `Bitacoras/` -> Tríada obligatoria de documentación.
- `docs/` -> Memoria ontológica viva (LLM Wiki en `docs/wiki/`).

---

## 🛡️ Reglas Inviolables de Arquitectura y Código
1. **Independencia Total de Marca:** Prohibido referenciar a dominios o sistemas legacy externos. La plataforma oficial es `pidemeaqui.com`.
2. **Seguridad Vial:** Prohibición estricta de anuncios o popups mientras el conductor esté en movimiento (`en_camino`, `a_bordo`).
3. **Ancla Legal Oficial:** Las tarifas están ancladas al decreto distrital oficial por sectores; cero cobros arbitrarios o tarifas dinámicas sin piso.
4. **La Tripleta Obligatoria:** Todo cambio sigue OpenSpec $\to$ Bitácoras (Diaria + Sesión + Monolito) $\to$ Engram.
