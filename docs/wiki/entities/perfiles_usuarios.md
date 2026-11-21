# 👥 Entidad: Perfiles y Roles de Usuario (RBAC)

El sistema **Taxi** implementa un modelo de control de acceso basado en roles (Role-Based Access Control - RBAC) gobernado por Firebase Authentication y Firestore Security Rules.

---

## 1. Matriz de Perfiles

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PERFILES DE USUARIO EN TAXI                          │
├──────────────────┬─────────────────────────┬───────────────────────────┤
│ 👑 Administrador │ 🚖 Conductor            │ 🙋 Cliente (Pasajero)     │
├──────────────────┼─────────────────────────┼───────────────────────────┤
│ - Gestión Flota  │ - Turno y Enturne       │ - Solicitud de Viaje      │
│ - Bahías/Tarifas │ - Bahía Asignada        │ - Cotización de Tarifa    │
│ - Liquidación    │ - Alertas de Despacho   │ - Rastreo de Móvil        │
│ - Monitoreo Vivo │ - Pagos y Recaudos      │ - Historial y Calificación│
│ - Soporte/Cuentas│ - Estado del Vehículo   │ - Soporte al Pasajero     │
└──────────────────┴─────────────────────────┴───────────────────────────┘
```

---

## 2. Detalle de Perfiles y Capacidades

### 👑 1. Administrador (Desktop / Tablet)
* **Público Objetivo:** Dueños de flota, supervisores de garita, cajeros y personal de soporte.
* **Dispositivo Típico:** Desktop (Windows) y Tablets de Garita.
* **Capacidades Operativas:**
  * Control total de la matriz de tarifas, sectores geográficos y recargos.
  * Gestión de bahías de despacho y cupos máximos por bahía.
  * Administración del censo de vehículos (placas, móviles, SOAT, técnico-mecánica) y conductores afiliados.
  * Cierre y liquidación de turnos de caja, reportes contables y recaudos.
  * Capacidad de anulación, reordenamiento o intervención de turnos por contingencia operativa.

### 🚖 2. Conductor (Android Móvil)
* **Público Objetivo:** Operadores y taxistas afiliados al sistema.
* **Dispositivo Típico:** Teléfonos móviles Android (versiones ligeras, bajo consumo de batería y datos).
* **Capacidades Operativas:**
  * **Enturne Digital:** Registro en cola/bahía mediante geolocalización o validación de garita.
  * **Monitoreo de Turno:** Visualización clara de su posición en la fila y tiempo estimado de salida.
  * **Aceptación de Despacho:** Notificación sonora y visual de asignación de carrera con datos del destino.
  * **Control Financiero:** Historial de pagos de recaudo, conceptos y estado de cuenta.
  * **Seguridad:** Botón de auxilio/emergencia y reporte de anomalías.

### 🙋 3. Cliente / Pasajero (Android Móvil)
* **Público Objetivo:** Usuarios particulares y corporativos que solicitan servicio de taxi.
* **Dispositivo Típico:** Teléfonos inteligentes Android.
* **Capacidades Operativas:**
  * **Solicitud de Taxi:** Geolocalización de punto de recogida y selección de destino.
  * **Cotización Transparente:** Cálculo automático de tarifa estimada según la matriz de sectores aprobada.
  * **Seguimiento en Vivo:** Visualización del móvil aproximándose en mapa.
  * **Seguridad e Identidad:** Consulta de placa, número móvil y datos del conductor verificado.
  * **Historial y Calificación:** Registro de viajes anteriores y evaluación del servicio.
