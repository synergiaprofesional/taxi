# 🏢 Entidad: Gremios, Organizaciones y Jerarquías (Multi-Tenant)

El sistema **Taxi** incorpora una arquitectura de **Gremios y Agremiaciones de Transporte** (cooperativas, asociaciones, empresas de taxi y sindicatos), modelando sus organigramas internos, jerarquías de mando y tipología de flota.

---

## 1. Organigrama y Jerarquías Internas del Gremio

Cada Gremio (`/organizaciones/{orgId}`) opera con su propia estructura jerárquica y dependencias:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ORGANIGRAMA TÍPICO DE UN GREMIO                      │
├────────────────────────────────────────────────────────────────────────┤
│ 👑 Nivel 1: Gerencia / Presidencia / Junta Directiva                   │
│   - Parámetros globales, estatutos, alianzas comerciales y convenios.  │
├────────────────────────────────────────────────────────────────────────┤
│ 🎖️ Nivel 2: Coordinadores de Zona y Jefes de Bahía                    │
│   - Supervisión operativa de puestos de control, garitas y terminales. │
├────────────────────────────────────────────────────────────────────────┤
│ 🖥️ Nivel 3: Operadores de Garita, Despachadores y Cajeros              │
│   - Registro presencial, enturnamiento, emisión de tickets y recaudo.  │
├────────────────────────────────────────────────────────────────────────┤
│ 🤝 Nivel 4: Propietarios de Flota / Concesionarios                     │
│   - Dueños de uno o múltiples vehículos afiliados con liquidación.     │
├────────────────────────────────────────────────────────────────────────┤
│ 🚖 Nivel 5: Conductores (Públicos y Privados)                          │
│   - Operación en calle, bahías y atención de carreras.                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tipología de Conductores: Públicos vs Privados

Una innovación crítica del sistema es la clasificación operativa de los conductores dentro de la organización:

### 🚖 2.1. Conductor Público (Flota Abierta)
* **Perfil:** Taxista afiliado al gremio habilitado para la atención general de la ciudadanía.
* **Visibilidad:**
  * Aparece en el radar de todos los pasajeros públicos (Capa 2) que piden taxi en calle o por la app general.
  * Enturna en bahías públicas y rotativas.
  * Recibe despachos estándar por cola FIFO o proximidad.

### 🔒 2.2. Conductor Privado / Exclusivo (Flota Corporativa / Convenios)
* **Perfil:** Taxista asignado a operaciones exclusivas, circuitos cerrados o convenios corporativos de alto valor gestionados por su gremio.
* **Casos de Uso:**
  * **Hoteles 5 Estrellas y Turismo VIP:** Flota asignada con estándares de bilingüismo, modelo reciente y vestimenta formal.
  * **Convenios Empresariales / Industriales:** Transporte de personal corporativo (clínicas, puertos, empresas petroleras) con facturación centralizada a crédito.
  * **Rutas Privadas / Escolta:** Servicios concertados con clientes institucionales.
* **Regla de Despacho:**
  * **Restricción de visibilidad:** No son asignados automáticamente a carreras públicas de la calle.
  * Su cola y despacho responden exclusivamente a las solicitudes originadas por los clientes vinculados a su convenio corporativo específico.

---

## 3. Clientes Finales (Pasajeros) y Modelos de Vinculación

Los pasajeros son por naturaleza de **carácter público** (cualquier ciudadano o visitante puede descargar la app y solicitar servicio), pero el sistema permite **vincularlos** para segmentar su experiencia y tarifas:

### 🙋 3.1. Cliente Público General (Sin Vinculación Específica)
* **Registro:** Descarga la app, ingresa su número celular, valida con OTP por SMS (Firebase Auth) e ingresa su nombre.
* **Operación:** Solicita servicio en cualquier punto de la ciudad y el sistema le asigna un **Conductor Público** disponible cercano o despachado de bahía. Tarifa oficial estándar por sectores.

### 🏢 3.2. Cliente Corporativo / Institucional (Vinculado a Convenio)
* **Mecanismo de Vinculación:**
  1. **Registro con Dominio Corporativo:** Al registrarse con correo corporativo (ej: `@hilton.com`, `@refineria.com`), Firebase Auth le asocia automáticamente el claim de su empresa.
  2. **Código de Convenio / Token:** El pasajero ingresa un código alfanumérico suministrado por su empresa o por el hotel.
* **Beneficios:** 
  * Acceso a la flota de **Conductores Privados/Corporativos**.
  * Facturación a cuenta corporativa (voucher digital sin pago en efectivo).
  * Tarifas preferenciales pactadas entre el gremio y la empresa.

### 🏷️ 3.3. Cliente Vinculado por Conductor Referido (Fidelización)
* **Mecanismo:** El taxista entrega su tarjeta o código QR personal a sus clientes frecuentes.
* **Efecto:** Cuando el cliente solicita un viaje, el algoritmo le da **prioridad de notificación** al conductor vinculado si este se encuentra libre y a menos de 5 minutos de distancia. Si el conductor habitual no está disponible, el viaje se enruta al gremio, garantizando que el servicio nunca se pierda.
