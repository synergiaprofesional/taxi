# Design: Solución Integral de Novedades Fundetaxcol

## 1. Arquitectura de Componentes y Flujo de Datos

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   ARQUITECTURA DEL CAMBIO                              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [1. ACCESO SILENCIOSO]                                                                │
│  callKw / searchRead ──(Fallo Sesión/401)──▶ _handleSessionRecovery()                  │
│                                                  │                                     │
│                                                  ├── LocalStorage(login, pwd)          │
│                                                  ├── autenticar() [silencioso]         │
│                                                  └── Reintento de la petición original │
│                                                                                        │
│  [2. PAGOS: CONCEPTO & CAPTURA MANUAL]                                                 │
│  Odoo _get_data['concepto_ids'] ──▶ PagoRecaudoModel.fromJson (parseo lineas)         │
│                                            │                                           │
│                                            ├── PagoCardWidget (Fila 2: Conductor • [Concepto])
│                                            └── PaymentFormView (Autocomplete / Manual) │
│                                                                                        │
│  [3. TURNOS: DESTINOS MANUALES, CATÁLOGO EXPANDIDO & RECARGO $1.100]                   │
│  getTarifasSector(limit: 1000) ──▶ Incluye Manga, Manzanillo, Pedro Salazar, etc.      │
│  TurnoFormView ──▶ Autocomplete<String/Tarifa> (Entrada Libre y Sugerida)              │
│  TurnoFormView ──▶ Recargo Nocturno = exactamente $1.100 (19:00 - 05:00)               │
│  BahiaSelectedView ──▶ Metrics Box visible SOLO en Pestaña 0 (Pagos), oculto en Turnos │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Decisiones de Diseño y Trade-offs

### A. Interceptor de Auto-Reconexión en OdooService
* **Problema:** En redes móviles (3G/4G/WiFi inestable) o tras suspensión de pantalla, Odoo invalida la sesión o la cookie se pierde.
* **Decisión:** Implementar una envoltura de reintento (`_withAutoRetry`) en `callKw`. Si la llamada retorna `null` o una excepción asociada a sesión y existen credenciales en `LocalStorage`, se ejecuta un `autoLogin()` transparente y se reintenta la llamada 1 vez antes de propagar el fallo.
* **Beneficio:** Elimina el síntoma donde la app de la nada expulsa al operador al `LoginView`.

### B. Deserialización de Conceptos en PagoRecaudoModel y Proyección Visual
* **Estructura en Odoo:** En `fundetaxcol.pago._get_data()`, el campo `concepto_ids` es una lista de mapas con `{'id': ..., 'concepto_id': {'id': ..., 'name': '...'}, 'cantidad': ..., 'valor': ...}`.
* **Modelo Dart:**
  - Extraer cada línea en `PaymentConceptLine`.
  - Exponer un getter conveniente `conceptoPrincipal`: si hay líneas, toma el nombre de la primera; si no, `'Recaudo General'`.
* **Visualización en `PagoCardWidget`:**
  - En la Fila 2, al lado del nombre del conductor, renderizar una etiqueta sutil o texto destacado con el concepto (`• Cuota Sostenimiento`, `• Rodamiento`, etc.).
  - El operador sabrá de inmediato qué pagó el taxista, no solo el valor monetario.

### C. Captura Manual de Tipos de Pago en PaymentFormView
* **Diseño:** Reemplazar el flujo de "abrir diálogo -> seleccionar de lista -> guardar" por un campo directo en el formulario principal con `Autocomplete<ConceptoCobroModel>`.
  - Permite escribir libremente si es un concepto nuevo o seleccionar de las opciones frecuentes.
  - La cantidad y valor se prellenan o ajustan en la misma pantalla.

### D. Destinos Manuales y Eliminación de Corte Alfabético en Tarifas
* **Corte Alfabético:** Aumentar `limit: 1000` en `OdooService.getTarifasSector()`. Se asegura la carga de Manga, Manzanillo del Mar, Pedro Salazar, San Pedro, San Francisco, etc.
* **Entrada Manual en `TurnoFormView`:**
  - Usar un widget `Autocomplete<String>` o `TextFormField` con sugerencias de las tarifas cargadas.
  - Si el operador escribe un destino que existe en el catálogo, se asocia su `tarifa_id` y su valor base. Si escribe un destino libre no tarifado, se asigna como texto en la nota/destino y se permite ingresar el valor acordado.

### E. Recargo Nocturno Inflexible de $1.100
* **Regla:** Desde las 19:00 hasta las 05:00 horas, el recargo nocturno es estrictamente **$1.100 COP**.
* **Ajuste:** Eliminar el fallback condicional `_tarifaSeleccionada!.valorRecargo > 0 ? _tarifaSeleccionada!.valorRecargo : _valorRecargo` que permitía a valores viejos de Odoo (2500) sobreescribir la tarifa oficial.

### F. Ocultamiento de Métricas en Pestañas de Turnos
* **Diseño:** En `BahiaSelectedView.build()`, envolver el contenedor de métricas (`Recaudo Empresa` y `Servicios Clientes`) con una condición:
  `if (_currentIndex == 0) ...[ // Solo en Pagos ]`.
* En la Pestaña 1 (Turnos en Cola) y Pestaña 2 (Despachados), el cuadro no se muestra, dando espacio vertical 100% libre para las tarjetas de turnos y despachos.

