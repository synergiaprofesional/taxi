# 📢 Concepto: Modelo de Monetización y Publicidad

Para garantizar la viabilidad financiera, el sustento de la infraestructura en la nube (Firebase Firestore, Cloud Functions, mapas e infraestructura de servidores) y el mantenimiento continuo, el sistema **Taxi** incorpora un subsistema de **monetización mediante publicidad integrada**.

---

## 1. Estrategia de Publicidad por Capas (Modelo Cebolla)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   MONETIZACIÓN Y PUBLICIDAD EN TAXI                    │
├─────────────────────────┬──────────────────────────────────────────────┤
│ 🙋 Capa 2: Clientes     │ - Banners inferiores discretos en cotización │
│   (Pasajeros)           │ - Intersticial suave al finalizar viaje      │
│                         │ - Cupones y promociones de comercios locales │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 🚖 Capa 1: Conductores  │ - Anuncios en pantalla de reposo/espera      │
│                         │ - Cero intrusión durante conducción activa   │
│                         │ - Publicidad del gremio (talleres, seguros)  │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 👑 Capa 0: Admin/Garita │ - Sin publicidad externa (foco operativo)    │
│                         │ - Gestor de convenios y anunciantes locales  │
└─────────────────────────┴──────────────────────────────────────────────┘
```

---

## 2. Invariantes de Seguridad y Experiencia de Usuario (UX)

### ⚠️ Regla de Oro: Seguridad Vial del Conductor
* **Cero distracciones en marcha:** Está terminantemente prohibido disparar anuncios intersticiales, videos o pop-ups interactivos mientras el vehículo esté en movimiento o en carrera activa.
* **Momentos permitidos para el Conductor:**
  * En reposo en bahía esperando turno.
  * En la pantalla de consulta de saldo o historial de recaudos.

### 🎯 Experiencia del Cliente / Pasajero
* **No obstaculizar la solicitud:** El flujo de pedir un taxi (seleccionar destino y cotizar) debe ser inmediato y sin fricciones.
* **Momentos permitidos para el Cliente:**
  * Banner nativo en la parte inferior durante la espera del vehículo.
  * Pantalla de confirmación y calificación posterior al viaje.

---

## 3. Arquitectura Técnica de Integración

1. **Red de Anuncios Principal (Google AdMob):**
   - Paquete Flutter: `google_mobile_ads`.
   - Soporte para: Banners adaptativos (`Adaptive Banner`), Anuncios Intersticiales (`InterstitialAd`) y Anuncios Nativos (`NativeAd`).
2. **Gobernanza Dinámica vía Firebase Remote Config:**
   - Control en caliente de activación/desactivación de anuncios sin requerir actualización de APK en Play Store.
   - Limitación de frecuencia (*Frequency Capping*) para evitar saturar al usuario (ejemplo: máximo 1 intersticial cada 3 viajes completados).
3. **Plataforma de Publicidad Local Propia (Direct Ad Server):**
   - Espacios reservados en Firestore (`colección /campanas_publicitarias`) para que la empresa de taxis o cooperativa pueda vender banners directamente a talleres mecánicos, restaurantes, centros comerciales, aseguradoras y repuesteros locales.
