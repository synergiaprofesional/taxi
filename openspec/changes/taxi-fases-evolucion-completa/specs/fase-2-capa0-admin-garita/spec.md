## ADDED Requirements

### Requirement: Consola de Garita en Tablet con Vista Dividida
El sistema SHALL proporcionar en tablets Android un layout horizontal *Split-View* con la cola de bahías a la izquierda y las acciones rápidas de despacho y cobro a la derecha.

#### Scenario: Despacho Rápido desde Tablet
- **WHEN** el operador pulsa el botón de despacho en la bahía activa
- **THEN** el primer vehículo en cola pasa a estado despachado y se emite la orden de impresión del ticket en menos de 300 ms

### Requirement: Impresión Térmica ESC/POS Nativa sin Latencia de Red
El sistema SHALL soportar impresión de tiquetes de turno y comprobantes de recaudo vía Bluetooth SPP en móviles/tablets y vía Spooler Win32 en Windows Desktop.

#### Scenario: Impresión de Ticket de Salida
- **WHEN** se confirma el despacho de un taxi
- **THEN** el formateador ESC/POS envía los bytes crudos a la impresora configurada sin bloquear el hilo principal de la interfaz
