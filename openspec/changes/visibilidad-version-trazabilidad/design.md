# Design: Arquitectura de Visibilidad de Versión y Trazabilidad

## 1. Arquitectura de Datos (SSOT)
Se define `AppVersion` como una clase utilitaria de constantes estáticas en tiempo de compilación:

```
┌─────────────────────────────────────────────────────────────┐
│                      AppVersion (SSOT)                      │
├─────────────────────────────────────────────────────────────┤
│ • versionName = '2.1.16'                                    │
│ • versionCode = 18                                          │
│ • environment = 'Producción (Cartagena)'                    │
│ • display => 'v2.1.16+18'                                   │
│ • shortDisplay => 'v2.1.16'                                 │
│ • ticketFooter => 'Synergia Movil v2.1.16+18'               │
└─────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ BahiaSelected │       │   LoginView   │       │ PrinterService│
│  (AppBar UI)  │       │   (Splash)    │       │ (Ticket ESC)  │
└───────────────┘       └───────────────┘       └───────────────┘
```

## 2. Componentes de Interfaz Afectados

### A. AppBar de `BahiaSelectedView`
* Se incorpora un contenedor estilizado tipo *chip* junto al texto del título "Synergia Móvil".
* Tipografía en alto contraste con esquinas redondeadas (`BorderRadius.circular(6)`).
* Efecto táctil (`InkWell` / `GestureDetector`) que navega a `SettingInfoExtraView` para consultar latencia RPC, WebSockets y sesión.

### B. `LoginView`
* Debajo del encabezado institucional se añade un subtítulo con `AppVersion.display` y el entorno `fundetaxcol.co`.

### C. `SettingsView` y `SettingInfoExtraView`
* Sustitución de valores hardcodeados por `AppVersion.display`.
* Footer de soporte en `SettingsView`.

### D. `PrinterService`
* En el método `generarTextoTiquete`, se añade la línea de trazabilidad:
  `buffer.writeln(_centrar(AppVersion.ticketFooter, ancho));`
  garantizando que cada recibo contable o tiquete de despacho impreso en papel térmico de 58mm u 80mm contenga la versión de la app.

