# Proposal: Rediseño de Listas con Estética Fiel a WhatsApp / Telegram

## Why

Las listas operativas anteriores (`TurnoListView`, `DespachoListView`, `PagoListView`) utilizaban tarjetas flotantes (`Card`) con bordes rectangulares gruesos, elevaciones artificiales y márgenes laterales que reducían el área visible en pantalla a sólo 3.5 filas por vista móvil. Adicionalmente, el buscador superior se encontraba oculto o requería interacción adicional en AppBar.

Siguiendo el requerimiento directo del usuario, se adopta el estándar de diseño de listas de mensajería (WhatsApp / Telegram) con una lista continua edge-to-edge plana, avatar circular con número de turno en cola (Opción 2), indicador dinámico de tiempo de espera transcurrido en minutos (Opción 1: Opción B), y un buscador superior integrado en formato cápsula/píldora **sin botones o filtros debajo**, optimizando el espacio vertical y soportando con fidelidad cromática el Modo Oscuro y Modo Claro.

## What Changes

- **Componente Fila Continua (`TurnoCardWidget` y `PagoCardWidget`)**:
  - Reemplazo del widget `Card` por `InkWell` plano edge-to-edge con separador sangrado a 74px (`ListView.separated`).
  - Avatar circular (radio 24px) mostrando el número de turno secuencial en fila, con color verde esmeralda WhatsApp (`#00A884`) para el turno actual y fondos neutros para la cola.
  - Subtítulo de dos líneas estrictas: placa en negrita 16px arriba; ícono de check + `Conductor • Espera: X min` abajo.
  - Columna derecha con hora en tipografía fina 12px arriba y badge de estado / valor monetario en verde WhatsApp abajo.
- **Buscador Tipo Píldora Superior (`BahiaSelectedView`)**:
  - Cápsula redondeada (`borderRadius: 24`) de 42px de altura fija sobre la lista.
  - Eliminación absoluta de botones intermediarios bajo el buscador, dejando que la lista comience inmediatamente.
- **Paleta Cromática Dual Fiel (Dark & Light Mode)**:
  - Tokens oficiales en `AppColors`: Dark (`#0B141A`, `#111B21`, `#20272B`, `#E9EDEF`, `#8696A0`) y Light (`#FFFFFF`, `#F0F2F5`, `#111B21`, `#667781`, `#008069`).

## Capabilities

### New Capabilities

- `whatsapp-edge-to-edge-list`: Listas continuas con divisor sangrado tras el avatar, sin marcos de tarjeta, adaptables a modo claro y oscuro.
- `capsule-search-bar`: Barra de búsqueda fija tipo píldora sin botones intermediarios.
- `turn-wait-time-tracker`: Cálculo en tiempo real del tiempo de espera transcurrido (`Espera: X min`) desde la asignación del turno.

### Modified Capabilities

- `view-bahia-selected-shell`: Se integra la barra fija tipo píldora y se expande el viewport para las listas continuas.
- `view-turno-list`: Renderizado mediante `ListView.separated` con divisores sangrados a 74px.
- `view-despacho-list`: Renderizado con la nueva apariencia de fila continua.
- `view-pago-list`: Renderizado con el nuevo formato plano de recaudo.

## Impact

- **Experiencia de Usuario (UX)**: Aumento de un 40% en turnos visibles en pantalla móvil simultáneamente (de 3.5 a 5 turnos).
- **Consistencia de Tema**: Cero textos invisibles o fondos rígidos; adaptación fluida entre exterior bajo el sol y oficina nocturna.
- **Pruebas y Compatibilidad**: Total paridad con las pruebas unitarias y responsivas del sistema.
