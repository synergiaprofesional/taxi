# Especificación: Persistencia Local por Usuario y Desplazamiento Lateral Responsive

## REQ-001: Persistencia Local de Impresora Térmica por Usuario
- **GIVEN** que el usuario "operador1@fundetaxcol.co" ingresa a `SettingsView`.
- **WHEN** selecciona impresora tipo Spooler / Windows USB, nombre "TIQUETES", ancho 80 mm y auto-corte activo, y presiona "Guardar Ajustes".
- **THEN** los valores deben persistir en `LocalStorage` bajo la clave `user_pref_operador1@fundetaxcol.co_printer_config`.
- **AND** al reiniciar la app o cambiar de sesión y volver a ingresar como "operador1@fundetaxcol.co", los campos deben cargarse automáticamente con dichos valores.

## REQ-002: Aislamiento entre Operadores
- **GIVEN** que el usuario A configuró impresora "TIQUETES" de 80 mm.
- **WHEN** el usuario B ingresa en el mismo dispositivo y configura impresora Bluetooth "PORTATIL-01" de 58 mm.
- **THEN** la configuración del usuario A no debe sobreescribirse ni alterarse.
- **AND** al iniciar sesión el usuario A, se restaura la configuración de 80 mm, y al iniciar sesión el usuario B, se restaura la de 58 mm.

## REQ-003: Desplazamiento Táctil en Panel Lateral Landscape
- **GIVEN** un dispositivo smartphone rotado horizontalmente con altura de viewport menor a 450px.
- **WHEN** el usuario interactúa con el panel lateral izquierdo en `_buildTabletLayout`.
- **THEN** el panel debe permitir desplazamiento vertical táctil suave (scroll).
- **AND** las métricas de recaudo y servicios clientes deben ser completamente visibles al deslizar hacia abajo, sin errores de render flex overflow.
