# Propuesta de Cambio OpenSpec: Búsqueda Híbrida y Deserialización Polimórfica de Pagos

## 1. Justificación y Causa Raíz
1. **Fallo de Deserialización Silencioso en Pagos:** 
   Al consultar `fundetaxcol.pago.get_all` en Odoo 11, el método backend `_get_data()` retorna campos relacionales (`bahia_id`, `vehiculo_id`, `conductor_id`) como diccionarios (`Map<String, dynamic>`) en lugar de listas o enteros. El modelo `PagoRecaudoModel.fromJson` intentaba asignar directamente estos `Map` a variables de tipo `int`, provocando una excepción de casteo de tipos en tiempo de ejecución (`type '_InternalLinkedHashMap' is not a subtype of 'int'`). Como resultado, el método `cargarPagosDesdeServidor()` capturaba la excepción y la lista `pagos` permanecía vacía, impidiendo que el operador viera los 58 pagos de la sesión activa del 24 de Octubre.
2. **Limitación de Alcance en Búsqueda de Recaudos (Hallazgo de Jairo Acosta):**
   La app original restringía la consulta de pagos a la sesión activa (`bahia_ids` de la jornada). Si un conductor requería verificar un pago realizado en jornadas anteriores o en una sesión ya cerrada, el coordinador debía acudir a un computador de escritorio con la interfaz web de Odoo.

## 2. Alcance del Cambio
1. **Polimorfismo en DTO de Pago (`PagoRecaudoModel`):** Soportar transparentemente deserialización desde `Map`, `List`, `int` o `String` para `bahia_id`, `vehiculo_id`, `conductor_id`, y fallback en `total` (`valor` vs `total`).
2. **Carga Inmediata de la Sesión Activa:** Garantizar que los pagos de todas las bahías de la sesión en progreso se carguen y se muestren en reposo por bahía activa, y con filtrado transversal en memoria.
3. **Búsqueda Histórica Remota en Servidor:** Cuando el operador ingrese una consulta de búsqueda (placa, conductor o consecutivo) con $\ge 3$ caracteres y no existan resultados en la sesión actual, o como complemento opcional, consultar al backend Odoo mediante `searchRead` o `get_pago_ids` sin restricción de sesión para recuperar recaudos de fechas anteriores.
4. **Verificación Estática y Despliegue Físico:** Validación con `flutter analyze` (0 issues), incremento de versión en `pubspec.yaml` a `2.1.12+14` y despliegue automatizado en teléfono y tablet.

## 3. Impacto y Riesgos
* **Cero Impacto Visual:** No se alteran los estilos visuales, colores ni componentes de tarjeta existentes.
* **Rendimiento:** La búsqueda local sigue siendo instantánea ($< 5\text{ ms}$). La búsqueda remota se ejecuta con debouncing y spinner no bloqueante.
