# Propuesta: Sprint B — Despacho en Bahía con Enlace WhatsApp para Pasajeros sin App

## 1. Justificación y Contexto
La ventaja competitiva más poderosa del taxi formal frente a Uber e inDrive es la **bahía física / garita** (centros comerciales, terminales, aeropuertos y hoteles). En estos puntos, miles de pasajeros abordan un taxi directamente a pie sin haber descargado previamente ninguna aplicación móvil.

Mientras que Uber e inDrive son incapaces de atender a este usuario a menos que descargue su app y cree una cuenta, **Taxi** introduce el **Despacho con Enlace WhatsApp**:
1. El despachador en garita puede ingresar opcionalmente el número celular del pasajero al momento de subir al taxi.
2. El sistema genera un viaje en Firestore (`categoria: bahiaPrioritaria`) y produce un enlace web de tracking seguro (`https://taxi.fundetaxcol.co/t/{viajeId}`).
3. Se despacha al instante un mensaje formal de WhatsApp al pasajero con los datos del taxi, conductor, placa, tarifa decretada y el enlace de rastreo en vivo.
4. El pasajero abre el enlace en cualquier navegador móvil (Chrome, Safari) y visualiza su ticket digital en vivo, con botón de pánico SOS y opción de compartir el viaje con familiares, **sin necesidad de instalar ninguna app**.

## 2. Alcance Técnico
- **Interfaz Garita (`TurnoFormView`):** Campo opcional para ingresar el celular del pasajero, validación de formato Colombia (+57) y botón de disparo rápido de WhatsApp.
- **Servicios (`FirestoreRepository` & `TurnoController`):** Transacción de creación de viaje vinculado al turno y generador de URL / payload de WhatsApp.
- **Frontend Web / Responsive (`WebTicketTrackingView`):** Pantalla de ticket y tracking web adaptativa con sello de verificación, placa destacada, tarifa legal desglosada y centro de seguridad.
- **TDD:** Pruebas unitarias de generación de links, formateo y persistencia en Firestore en `test/services/despacho_whatsapp_test.dart`.
