# Propuesta OpenSpec: Identidad Cromática Amarillo Taxi y Negro con Alto Contraste Dual

## Justificación
El gremio de taxistas se identifica a nivel global y nacional con el **Amarillo y Negro**. Si bien la aplicación contaba con un rediseño de listas continuas tipo WhatsApp, algunos elementos utilizaban el verde genérico de mensajería para los estados activos, diluyendo la personalidad corporativa del servicio de transporte y movilidad.

El desafío técnico de diseño radica en que el amarillo puro sobre fondo blanco carece de contraste (falla los estándares WCAG), mientras que el **negro puro sobre amarillo taxi** ofrece uno de los contrastes más altos del ojo humano (> 12:1). Esta propuesta establece la armonización cromática global de Synergia Móvil para que respire la identidad de taxi profesional con contraste estricto tanto en Modo Oscuro (noche/cabina) como en Modo Claro (luz solar en calle).

## Alcance
1. **Tokens Institucionales en `AppColors`:**
   - Adición de tokens dedicados: `taxiYellow` (`0xFFF59E0B`), `taxiYellowLight` (`0xFFFBBF24`), `taxiYellowDark` (`0xFFD97706`), `taxiBlack` (`0xFF0F172A`) y `taxiBlackPure` (`0xFF000000`).
   - Mapeo de `turnActual` a `taxiYellow` para que el vehículo en atención vista el color insignia del gremio.
2. **Tarjeta y Avatar de Turnos (`TurnoCardWidget`):**
   - El avatar del turno en atención viste fondo `taxiYellow` con el número en `taxiBlackPure` y peso tipográfico `FontWeight.w900`, emulando la placa y distintivo de taxi oficial.
   - Borde perimetral o badge distintivo "EN ATENCIÓN" en Amarillo Taxi.
3. **Consistencia en Tema Oscuro y Claro (`AppTheme`):**
   - Modo Oscuro: Fondos asfalto/carbón profundo, acentos en amarillo taxi vibrante, texto blanco nítido.
   - Modo Claro: Fondos blanco puro y asfalto suave, botones en amarillo taxi con tipografía e iconos en negro puro para contraste de 12.8:1.
4. **Barras Superiores y Botones Operativos:**
   - Botón FAB ("PAGAR Y ENTURNAR") consolidado en Amarillo Taxi con Negro.
   - Chips de estado y selector de bahía con sutiles acentos dorados/ámbar.

## Impacto
- Identidad de marca inmediata para los conductores, cajeros y directivos del gremio taxista.
- Cumplimiento de accesibilidad visual WCAG AAA / AA en ambos temas.
- Cero regresiones en la navegación ni en la lógica de negocio.
