# Tareas: Sprint B — Despacho en Bahía con Enlace WhatsApp para Pasajeros sin App

- [x] 1. Extender `FirestoreRepository` con el método `despacharTurnoConViaje(...)` que actualiza el turno y genera el documento en `/viajes`.
- [x] 2. Crear el servicio helper `WhatsAppTrackingHelper` con métodos para formatear el mensaje y generar la URL de WhatsApp y la URL de tracking web.
- [x] 3. Actualizar `TurnoFormView` en `lib/ui/views/form/turno_form_view.dart` agregando el campo de celular del pasajero y la integración del envío por WhatsApp.
- [x] 4. Desarrollar la vista `WebTicketTrackingView` en `lib/ui/views/passenger/web_ticket_tracking_view.dart` adaptada para navegadores móviles y desktop.
- [x] 5. Implementar suite de pruebas unitarias en `test/services/despacho_whatsapp_test.dart` y catalogar en `tests/COMPENDIO_TESTS.md`.
- [x] 6. Ejecutar pruebas unitarias para validar 100% de aserciones.
- [x] 7. Documentar en la Tríada de Bitácoras (Diaria, Sesión, Monolito) y persistir en Engram.
