# Especificación: Despacho en Bahía con Enlace WhatsApp para Pasajeros sin App

## 1. Requerimientos Funcionales

### RF-01: Captura Opcional de Celular en Despacho de Bahía
- En `TurnoFormView` (modo despacho), el sistema DEBE disponer de un campo de texto `Celular Pasajero (Opcional)` con teclado numérico e icono identificativo de WhatsApp.
- Si el campo está vacío, el despacho procede con el flujo tradicional de tiquete físico sin errores.
- Si se ingresa un número de 10 dígitos, el sistema DEBE autocompletar el prefijo de país `+57` para Colombia.

### RF-02: Generación Automática del Viaje en Firestore
- Al pulsar `Despachar`, si hay celular del pasajero, `FirestoreRepository` DEBE invocar `crearViajeDesdeBahia(...)` registrando:
  - `categoria`: `CategoriaViaje.bahiaPrioritaria`
  - `estado`: `EstadoViaje.asignado`
  - `origen`: Nombre de la Bahía
  - `destino`: Destino o sector seleccionado
  - `precioAcordado`: Tarifa total oficial calculada
  - `conductorId` / `conductorNombre`: Datos del taxi enturnado
  - `placa`: Placa del vehículo
  - `telefonoPasajero`: Celular formateado

### RF-03: Generador de Enlace y Disparo de WhatsApp
- El sistema DEBE exponer el helper `WhatsAppService.generarUrlTracking(viajeId, telefono, datos)` que construya la URL `https://api.whatsapp.com/send?phone=57...&text=...`.
- En la interfaz de despacho, tras confirmar, DEBE mostrarse un botón o snackbar de acción directa para abrir el chat de WhatsApp con el mensaje preformateado.

### RF-04: Visor Web Responsive del Pasajero (`WebTicketTrackingView`)
- La vista DEBE escuchar de forma reactiva el stream de `/viajes/{viajeId}`.
- Debe presentar de forma nítida la placa, conductor, tarifa oficial decretada y el botón para compartir la ubicación en tiempo real.
