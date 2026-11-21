# Propuesta OpenSpec: Persistencia de Preferencias por Usuario y Scroll Lateral en Landscape

## Justificación
1. **Pérdida de Configuración de Hardware en el Dispositivo:**
   Actualmente, cuando el operador configura la impresora térmica dual ESC/POS (tipo de conexión Spooler/Bluetooth/Red, nombre de cola/IP/MAC, ancho de papel 58mm/80mm y auto-corte) en `SettingsView`, los ajustes solo se guardan en la memoria RAM de `PrinterService`. Al cerrar la aplicación, reiniciar o cambiar de usuario, la configuración se pierde. Dado que Odoo 11 no maneja configuración de hardware térmico local de cada terminal, estas preferencias deben persistir 100% de forma local en el dispositivo (`LocalStorage`), pero segmentadas por el usuario autenticado (`usuarioActivo`), para que cada cajero mantenga su propio hardware sin sobreescribir el de otros operadores.
2. **Bloqueo de Interfaz en Smartphone Horizontal (Landscape):**
   Al rotar el teléfono a posición horizontal, el ancho salta al breakpoint de tablet (650px - 1050px) activando `_buildTabletLayout`. En este modo, el panel lateral izquierdo (`Column` con altura fija y `Spacer()`) excede la altura útil de la pantalla horizontal (~380px), impidiendo el desplazamiento táctil. Como resultado, las métricas y controles inferiores quedan inaccesibles para el usuario.

## Alcance
- **Persistencia Local por Usuario (Key Scoping):**
  - Serialización y deserialización de `PrinterConfigModel` en `LocalStorage`.
  - Mecanismo de claves con namespace: `user_pref_${usuario}_printer_config`.
  - Carga automática de la configuración del usuario al autenticar en `OdooService` o al iniciar `SettingsView`.
- **Desplazamiento Suave en Panel Lateral Responsive:**
  - Envolver el panel de control izquierdo en `SingleChildScrollView` en `_buildTabletLayout` y `_buildDesktopLayout`.
  - Reemplazo de `const Spacer()` por separadores proporcionales (`SizedBox(height: 16)`) para evitar conflictos de layout no acotado.

## Impacto
- Cero pérdida de configuración de impresoras térmicas al cerrar la app o reiniciar el dispositivo.
- Aislamiento total de preferencias entre múltiples operadores que comparten el mismo móvil o terminal POS.
- Experiencia táctil fluida y completa en teléfonos operados horizontalmente y tablets POS.
