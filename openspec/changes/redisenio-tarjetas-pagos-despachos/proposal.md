# Propuesta: Rediseño Visual de Tarjetas de Pagos y Despachos (Estructura de 3 Filas)

## 1. Justificación y Contexto
A partir del análisis de novedades operativas y la solicitud directa del usuario, se identificó la necesidad de optimizar el espacio y la jerarquía visual de las tarjetas en la app móvil, tablet y desktop de Synergia Móvil:
1. **Zona Horaria Limpia:** No agregar el sufijo "COT" en pantalla para no sobresaturar la interfaz visual; mantener la hora limpia y calculada en hora local Colombia (`05:12 PM`).
2. **Tarjeta de Recaudos / Pagos (`PagoCardWidget`):** 
   - Fila 1: `Placa` + `[Tiquete/Consecutivo]` + `Hora` + `$Valor` (al extremo derecho).
   - Fila 2: Ícono de confirmación + `Nombre del Conductor`.
   - Fila 3: `Nombre de la Bahía` (ej: `🏢 Bahía Caribe Plaza`).
3. **Tarjeta de Despachos (`TurnoCardWidget` - modo despacho):**
   - Fila 1: `Placa` + `[Consecutivo Turno]` + `Hora` + `$Valor` (subido a la cabecera derecha).
   - Fila 2: Ícono de verificación + `Nombre del Conductor`.
   - Fila 3: `📍 Destino` (en color acento) + `Dirección / Nota complementaria` (si existe).

## 2. Alcance del Cambio
- **Archivos de UI a modificar:**
  - `lib/ui/widgets/pago_card_widget.dart`
  - `lib/ui/widgets/turno_card_widget.dart`
- **Componentes que se benefician:**
  - `PagoListView` (Pestaña 0 - Recaudos de Caja).
  - `TurnoListView` (Pestaña 1 - Turnos en espera).
  - `DespachoListView` (Pestaña 2 - Despachos del día).
  - `DespachoHistoryView` (Historial general de despachos).

## 3. Criterios de Aceptación
1. `PagoCardWidget` renderiza 3 filas con el valor monetario en la Fila 1 y la bahía en la Fila 3.
2. `TurnoCardWidget` en modo despacho renderiza 3 filas con el valor monetario en la Fila 1 y el destino + dirección/nota en la Fila 3.
3. Cero desbordamientos de píxeles (`RenderFlex overflow`) en pantallas angostas (360px) y amplias (tablets/PC).
4. La totalidad de los 21 tests de Flutter pasan con éxito.
5. Despliegue verificado en móvil Xiaomi, tablet Lenovo y ejecutable Windows.

