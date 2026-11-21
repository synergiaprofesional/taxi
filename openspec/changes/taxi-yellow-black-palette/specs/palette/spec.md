# Especificación: Identidad Amarillo Taxi y Negro

## REQ-001: Tokens de Movilidad Oficial en `AppColors`
- **GIVEN** la clase `AppColors`.
- **WHEN** cualquier componente de la aplicación solicita colores corporativos.
- **THEN** deben estar disponibles los tokens `taxiYellow`, `taxiYellowLight`, `taxiYellowDark`, `taxiBlack` y `taxiBlackPure`.
- **AND** `AppColors.primary` y `AppColors.turnActual` deben utilizar el tono `taxiYellow` (`0xFFF59E0B`).

## REQ-002: Avatar y Distintivo de Turno en Atención
- **GIVEN** un turno con `estado == EstadoTurno.actual`.
- **WHEN** se renderiza dentro de `TurnoCardWidget`.
- **THEN** su avatar circular debe poseer fondo Amarillo Taxi (`taxiYellow`) y el número de turno en Negro Puro (`taxiBlackPure`, `FontWeight.w900`).
- **AND** el badge o indicador de estado debe mostrar "EN ATENCIÓN" con el acento Amarillo Taxi.

## REQ-003: Contraste de Botones de Acción Primaria
- **GIVEN** los botones elevados de acción principal (como "PAGAR Y ENTURNAR").
- **WHEN** se visualizan en Modo Claro o en Modo Oscuro.
- **THEN** el fondo debe ser Amarillo Taxi y la tipografía/icono en Negro Puro, garantizando un ratio de contraste mínimo de 12:1 (WCAG AAA).
