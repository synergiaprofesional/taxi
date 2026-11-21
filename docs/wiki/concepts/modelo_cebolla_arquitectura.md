# 🧅 Concepto: Modelo Cebolla de Arquitectura y Cobertura

El sistema **Taxi** evoluciona desde una aplicación cerrada de garita hacia un **Modelo Cebolla (Capas Concéntricas de Acceso y Servicio)**. Este modelo define cómo los datos, la seguridad y las operaciones fluyen desde el núcleo administrativo hacia los conductores y, finalmente, hacia los pasajeros en el perímetro.

---

## 1. Diagrama del Modelo Cebolla

```text
               ┌────────────────────────────────────────────────────────┐
               │              CAPA 2: CLIENTES FINALES                  │
               │                   (Pasajeros)                          │
               │   ┌────────────────────────────────────────────────┐   │
               │   │             CAPA 1: CONDUCTORES                │   │
               │   │                (Flota Móvil)                   │   │
               │   │   ┌────────────────────────────────────────┐   │   │
               │   │   │     CAPA 0: NÚCLEO ADMINISTRATIVO      │   │   │
               │   │   │         (Garitas y Despacho)           │   │   │
               │   │   │                                        │   │   │
               │   │   │ - Control de bahías y colas FIFO       │   │   │
               │   │   │ - Censo de vehículos y conductores     │   │   │
               │   │   │ - Tarifas maestras y sectores          │   │   │
               │   │   │ - Cajas, liquidación y auditoría       │   │   │
               │   │   └────────────────────────────────────────┘   │   │
               │   │                                                │   │
               │   │ - Enturne digital y posición en cola           │   │
               │   │ - Aceptación de despachos y carreras           │   │
               │   │ - Monitoreo de aportes y recaudos              │   │
               │   │ - Navegación y contacto con cliente            │   │
               │   └────────────────────────────────────────────────┘   │
               │                                                        │
               │ - Solicitud de taxi (origen / destino)                 │
               │ - Cotización anticipada de tarifa                      │
               │ - Seguimiento en tiempo real del vehículo asignado     │
               │ - Calificación, seguridad e historial de viajes        │
               └────────────────────────────────────────────────────────┘
```

---

## 2. Descripción de las Capas y Flujo Operativo

### 🏛️ Capa 0: Núcleo Administrativo (Garitas y Operación Central)
* **Origen Legacy:** Es el único nivel que existía en `synergia_movil` (operadores de garita registrando placas y despachando físicamente).
* **Rol en Taxi:** Actúa como el centro neurálgico de reglas y conciliación:
  * Regula las bahías físicas y virtuales.
  * Valida que los vehículos y conductores cumplan con requisitos legales (SOAT, tarjeta de control, tecnomecánica).
  * Audita los recaudos y fija las políticas tarifarias.

### 🚖 Capa 1: Capa Intermedia de Conductores (Extensión Operativa)
* **Objetivo:** Empoderar al conductor directamente desde su smartphone.
* **Interacción con Capa 0:** El conductor ya no depende exclusivamente de un operador humano en garita para conocer su turno; la aplicación le notifica su posición, tiempo estimado y asignación de bahía.
* **Interacción con Capa 2:** Recibe las solicitudes de servicio originadas por pasajeros cercanos o despachadas desde garita, con confirmación bidireccional inmediata.

### 🙋 Capa 2: Capa Externa de Clientes Finales (Pasajeros)
* **Objetivo:** Abrir el ecosistema al usuario final que toma el taxi en la calle, en terminales o desde su hogar.
* **Beneficio para el Pasajero:** Solicita el servicio con confianza, conoce la tarifa estimada de antemano y ve el recorrido del vehículo en tiempo real.
* **Cierre de Ciclo:** Al completar el servicio, el pago/recaudo y la calificación retroalimentan la Capa 1 (historial del conductor) y la Capa 0 (auditoría del servicio en garita/administración).

---

## 3. Principio de Seguridad y Privacidad entre Capas
* **Aislamiento de Datos:** Un cliente de Capa 2 **nunca** tiene acceso a la información administrativa de Capa 0 (recaudos de caja, balances contables o tarifas internas).
* **Información Just-in-Time:** El cliente solo visualiza los datos del conductor de Capa 1 asignado a su servicio específico (nombre, foto, placa, modelo del vehículo y ubicación durante el viaje activo).
* **Reglas de Seguridad Firestore:** Cada capa cuenta con políticas de lectura/escritura (`rules_version = '2'`) estrictamente delimitadas por el rol del token en Firebase Auth.
