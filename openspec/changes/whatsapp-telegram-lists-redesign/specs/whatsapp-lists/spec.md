# Spec: Especificación Normativa de Listas Fieles Estilo WhatsApp / Telegram

## REQ-001: Fila Continua Edge-to-Edge con Separador Sangrado
- El componente de turno y pago DEBE abarcar el 100% del ancho de pantalla sin bordes de tarjeta ni márgenes perimetrales.
- El separador visual entre filas DEBE iniciar con una sangría de 74px desde el borde izquierdo y extenderse hasta el borde derecho.

#### Escenario: Renderizado de fila de turno en espera
- **GIVEN** un turno en cola con ID 5 y placa `TLZ-892`
- **WHEN** se visualiza en `TurnoListView`
- **THEN** se renderiza un avatar circular con texto `5`
- **AND** debajo de la placa se visualiza el nombre del conductor y el tiempo de espera transcurrido (`Espera: X min`)
- **AND** un divisor con sangría de 74px separa el ítem del siguiente elemento.

## REQ-002: Buscador en Cápsula Fija sin Botones Inferiores
- La pantalla `BahiaSelectedView` DEBE incluir una barra de búsqueda en formato píldora (`borderRadius: 24`).
- NO DEBE existir ningún botón de filtro, chip ni control intermedio entre el buscador y la lista fluida.

#### Escenario: Búsqueda en tiempo real sin obstrucción
- **GIVEN** que el usuario escribe texto en el buscador
- **WHEN** se ingresa una cadena de búsqueda
- **THEN** la lista filtra instantáneamente por placa o conductor
- **AND** el primer resultado aparece inmediatamente bajo la cápsula sin botones intermedios.

## REQ-003: Soporte Fiel Dual de Modo Oscuro y Modo Claro
- Todos los colores de texto, fondo, avatares y badges DEBEN alternar dinámicamente según el `Brightness` activo de la aplicación.
- En Modo Oscuro, el fondo DEBE ser grafito WhatsApp (`#0B141A`), los textos principales blanco suave (`#E9EDEF`) y los acentos verde esmeralda (`#00A884`).
- En Modo Claro, el fondo DEBE ser blanco (`#FFFFFF`), el campo de búsqueda gris claro (`#F0F2F5`) y los textos principales negro suave (`#111B21`).
