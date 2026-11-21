# Diseño Técnico: Desacoplamiento Estricto de Tarjetas (Turnos en Cola vs Despachos vs Pagos)

## 1. Principio de Aislamiento de Widgets

Para prevenir cualquier contaminación cruzada o alteración no deseada sobre los turnos en espera, se desacoplan formalmente los tres componentes de tarjeta en archivos dedicados:

1. **`lib/ui/widgets/turno_card_widget.dart` (EXCLUSIVO PARA TURNOS EN COLA):**
   - Restaurado 100% a su diseño original intacto.
   - Columna central con Placa en línea 1 y Conductor • Espera en línea 2.
   - Columna trailing derecha con Hora arriba y Badge (ACTUAL / Bahía) abajo.
   - Cero tercera fila, cero valor monetario, cero repetición de datos.

2. **`lib/ui/widgets/despacho_card_widget.dart` (EXCLUSIVO PARA DESPACHOS):**
   - Nuevo widget autónomo para la Pestaña 2 (`DespachoListView`) y el Historial (`DespachoHistoryView`).
   - Anatomía de 3 filas a todo el ancho:
     - Fila 1: `Placa` + `[Consecutivo Turno]` + `Hora Despacho` + `$Valor Pagado` (al extremo derecho).
     - Fila 2: Ícono de verificación + `Nombre del Conductor`.
     - Fila 3: `📍 Destino Oficial` + Dirección / Nota (si existe).

3. **`lib/ui/widgets/pago_card_widget.dart` (EXCLUSIVO PARA RECAUDOS / PAGOS):**
   - Anatomía de 3 filas a todo el ancho:
     - Fila 1: `Placa` + `[REC-0012]` + `Hora` + `$Valor Recaudado` (al extremo derecho).
     - Fila 2: Doble check + `Nombre del Conductor`.
     - Fila 3: `🏢 Nombre de la Bahía`.

## 2. Diagrama de Asignación por Vista

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DESACOPLAMIENTO DE TARJETAS                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Pestaña 0: Recaudos]   ──▶ PagoCardWidget                                 │
│                              (3 Filas: Placa/Hora/$Valor, Conductor, Bahía) │
│                                                                             │
│  [Pestaña 1: Turnos]     ──▶ TurnoCardWidget (100% ORIGINAL INTACTO)        │
│                              (2 Filas + Trailing: Placa, Conductor, Espera) │
│                                                                             │
│  [Pestaña 2: Despachos]  ──▶ DespachoCardWidget (NUEVO DEDICADO)            │
│                              (3 Filas: Placa/Hora/$Valor, Conductor, Destino)│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
