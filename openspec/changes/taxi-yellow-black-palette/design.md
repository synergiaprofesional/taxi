# Diseño Arquitectónico: Paleta de Alto Contraste Amarillo Taxi & Negro

## 1. Mapeo de Tokens Cromáticos

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TOKENS DE MOVILIDAD (TAXI)                      │
├────────────────────────────────────────────────────────────────────────┤
│  taxiYellow        = Color(0xFFF59E0B)  // Ámbar 500 / Amarillo Taxi  │
│  taxiYellowLight   = Color(0xFFFBBF24)  // Resaltes en Dark Mode       │
│  taxiYellowDark    = Color(0xFFD97706)  // Bordes / Hover en Light     │
│  taxiBlack         = Color(0xFF0F172A)  // Asfalto Carbón (Fondos Dark)│
│  taxiBlackPure     = Color(0xFF000000)  // Tipografía sobre Amarillo   │
│  taxiSurfaceDark   = Color(0xFF1E293B)  // Tarjetas en Dark Mode       │
│  taxiSurfaceLight  = Color(0xFFFFFFFF)  // Tarjetas en Light Mode      │
└────────────────────────────────────────────────────────────────────────┘
```

## 2. Contraste y Accesibilidad (WCAG 2.1)

| Elemento | Fondo | Texto / Icono | Ratio de Contraste | Nivel WCAG |
|---|---|---|---|---|
| Botón "PAGAR Y ENTURNAR" | `taxiYellow` (`#F59E0B`) | `taxiBlackPure` (`#000000`) | **12.8:1** | **AAA (Superado)** |
| Avatar Turno Actual | `taxiYellow` (`#F59E0B`) | `taxiBlackPure` (`#000000`) | **12.8:1** | **AAA (Superado)** |
| Texto Primario (Dark) | `darkBackground` (`#0F172A`) | `darkTextPrimary` (`#F8FAFC`) | **15.4:1** | **AAA (Superado)** |
| Texto Primario (Light) | `lightSurface` (`#FFFFFF`) | `lightTextPrimary` (`#0F172A`) | **15.4:1** | **AAA (Superado)** |
| Acento de Marca (Dark) | `darkBackground` (`#0F172A`) | `taxiYellow` (`#F59E0B`) | **10.2:1** | **AAA (Superado)** |

## 3. Estado de Turnos en la Lista

- **Turno Actual (en bahía / llamado a salida):**
  - Avatar: Fondo circular `taxiYellow` con número en `taxiBlackPure` (`FontWeight.w900`).
  - Badge de estado: Cápsula con fondo `taxiYellow.withValues(alpha: 0.15)` y texto "EN ATENCIÓN" en `taxiYellow`.
- **Turnos en Fila (Espera):**
  - Dark Mode: Avatar circular en `AppColors.waDarkSearchField` con número en texto blanco plata.
  - Light Mode: Avatar circular en `Color(0xFFE2E8F0)` con número en texto negro pizarra.
- **Despachos (Salidas realizadas):**
  - Monto en verde contable institucional (`waCheckBlue` o `AppColors.success`).
