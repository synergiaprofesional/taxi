# 🚕 Concepto: Arquitectura Taxi (Alta Cobertura y Multi-Perfil)

## 1. Visión General
El proyecto **Taxi** es una plataforma integral de movilidad y despacho de transporte público que amplía sustancialmente el alcance de la aplicación anterior, soportando tres perfiles de usuario diferenciados y tres formatos de dispositivo:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        ARQUITECTURA SISTEMA TAXI                       │
│                                                                        │
│   [ Administradores ]        [ Conductores ]          [ Clientes ]     │
│       (Desktop/Tablet)        (Android Móvil)       (Android Móvil)    │
│              │                       │                     │           │
│              └───────────────────────┼─────────────────────┘           │
│                                      ▼                                 │
│                      [ FLUTTER CLIENT SUITE ]                          │
│               (Módulos segregados por Perfil/RBAC)                     │
│                                      │                                 │
│                                      ▼                                 │
│                     [ GOOGLE FIREBASE BACKEND ]                        │
│             Firestore │ Auth │ Functions │ Messaging │ Storage         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Segregación de Perfiles y Experiencia
1. **Perfil Administrador:**
   - Supervisión integral de la operación: tarifas por sector, bahías, censo de flota (vehículos/conductores), liquidación de recaudo y auditoría.
   - Disponible en **Windows Desktop** y **Tablets de Garita**.
2. **Perfil Conductor:**
   - Ciclo de vida del taxi: enturnado, visualización de posición en cola, alerta de despacho a bahía, aceptación de carreras y control de recaudos/ahorros.
   - Disponible en **Android Móvil** (teléfonos).
3. **Perfil Cliente (Pasajero):**
   - Solicitud de servicio de taxi, cotización previa estimada, seguimiento en vivo del vehículo asignado y calificación del servicio.
   - Disponible en **Android Móvil** (teléfonos).

---

## 3. Principio de Desacoplamiento de Odoo 11 hacia Firebase
- Odoo 11 queda formalmente excluido de la arquitectura operativa en tiempo real.
- Firebase asume la persistencia y sincronización reactiva sub-segundo con soporte offline nativo en Flutter.
- Se garantiza una transición ergonómica fluida para los usuarios veteranos de garita y conductores mediante interfaces que respetan sus hábitos operativos consolidados.


---

## 4. Visión de Futuro y Destino Estratégico del Sistema
1. **SuperApp Gremial:** Competir y superar a las apps transnacionales (Uber, InDrive) basándose en legalidad, tarifas justas y acceso a bahías exclusivas protegidas.
2. **Despacho Híbrido:** Combinación de colas físicas en bahías con radar digital en calle para eliminar el rodamiento en vacío.
3. **Fidelización del Conductor:** Billetera digital de ahorros decembrinos, autoliquidación de recaudos por PSE/Nequi, botón de pánico y club de descuentos automotrices.
4. **Distribución en Tiendas Oficiales:** Google Play Store con actualizaciones continuas.
5. **Autonomía y Escalabilidad:** Modelo SaaS multi-empresa con autosostenibilidad financiera mediante publicidad no invasiva.
