# Diseño: Sprint B — Despacho en Bahía con Enlace WhatsApp para Pasajeros sin App

## 1. Arquitectura del Flujo

```
┌─────────────────────────────────┐
│     Operador de Garita          │
│  (TurnoFormView - Despacho)     │
└───────────────┬─────────────────┘
                │ Ingresa Celular Pasajero (ej: 3001234567)
                ▼
┌─────────────────────────────────┐
│       FirestoreRepository       │
│  • Actualiza Turno a Despachado │
│  • Crea Documento en /viajes    │
│  • Genera UUID de Tracking      │
└───────────────┬─────────────────┘
                │
                ├──────────────────────────────────────────────┐
                ▼                                              ▼
┌─────────────────────────────────┐          ┌───────────────────────────────────┐
│    Impresión Ticket Térmico     │          │  Disparo Mensaje WhatsApp         │
│   (Físico para el Conductor)    │          │  https://wa.me/573001234567?text= │
└─────────────────────────────────┘          └─────────────────┬─────────────────┘
                                                               │ Enlace Web
                                                               ▼
                                             ┌───────────────────────────────────┐
                                             │     WebTicketTrackingView         │
                                             │  (Navegador del Pasajero sin App) │
                                             │  • Placa, Conductor, Destino      │
                                             │  • Tarifa Legal Oficial           │
                                             │  • Botón Compartir / SOS          │
                                             └───────────────────────────────────┘
```

## 2. Componentes y Contratos

### A. Estructura del Enlace y Mensaje WhatsApp
- **URL Base:** `https://taxi.fundetaxcol.co/t/{viajeId}`
- **Formato del Mensaje:**
```text
🚕 ¡Tu Taxi Formal en Bahía Caribe Plaza está en camino!

📋 Datos del Servicio:
• Vehículo: {PLACA}
• Conductor: {NOMBRE_CONDUCTOR}
• Destino: {DESTINO}
• Tarifa Oficial Decretada: ${VALOR_TOTAL} COP

🔒 Monitorea tu viaje y accede al Centro de Seguridad aquí:
https://taxi.fundetaxcol.co/t/{viajeId}
```

### B. Vista Web / Responsive (`WebTicketTrackingView`)
- Renderiza tanto en Flutter Web como embebida en móvil.
- Tarjeta de Seguridad Vial:
  - Header amarillo taxi con estado en vivo (`EN CAMINO` / `A BORDO` / `FINALIZADO`).
  - Ficha del Conductor: Foto/Avatar, Nombre formal, Calificación 4.9★, Empresa afiliada.
  - Ficha del Vehículo: Placa en tipografía de placa colombiana, Marca/Modelo.
  - Tarifa Oficial: Valor exacto decretado, desglose de recargos (sin sorpresas).
  - Acciones: Botón flotante "Compartir viaje por WhatsApp", Botón "Llamar al 123 / Garita".
