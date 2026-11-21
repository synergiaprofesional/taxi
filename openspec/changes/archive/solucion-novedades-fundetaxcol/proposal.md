# Proposal: Solución Integral de Novedades Fundetaxcol

## 1. Contexto y Problema
El cliente Fundetaxcol remitió el documento oficial "INFORME DE NOVEDADES – SISTEMA FUNDETAXCOL" (02 de noviembre de 2026), señalando que los puntos reportados aún persisten en las terminales operativas. Tras la auditoría exhaustiva de la base de código en `v2.1.23+25`, se constató que las sesiones previas se concentraron en calibración horaria (-5h UTC/COT) y formato de filas en tarjetas, dejando pendientes los siguientes requerimientos fundamentales de negocio y ergonomía operativa:

1. **Acceso al sistema (Cierre de sesión automático):**
   * *Problema:* La sesión en Odoo 11 caduca por timeout de cookies web (`session_id`) o suspensión de la app en segundo plano en Android. Al expirar, las llamadas RPC fallan y `AuthGatekeeper` expulsa al operador directamente a la pantalla de `LoginView`.
   * *Solución:* Implementar un interceptor de auto-reconexión silenciosa en `OdooService` que, ante un fallo de sesión o 401/403, intente re-autenticar de forma transparente con las credenciales persistidas en `LocalStorage` y reintente la llamada antes de desconectar al usuario.

2. **Módulo de Pagos (Visualización y captura manual de tipo de pago):**
   * *Problema 2.1:* En `PagoRecaudoModel.fromJson`, el arreglo `lineas: []` está forzado en blanco, ignorando `concepto_ids` devuelto por Odoo en `_get_data()`. La tarjeta `PagoCardWidget` no muestra el concepto, dejando al operador únicamente con el texto ambiguo "Recaudo $15.000".
   * *Solución 2.1:* Deserializar `concepto_ids` en `PagoRecaudoModel`, extraer el concepto principal (`conceptoNombre`) y proyectarlo claramente en la Fila 2 de `PagoCardWidget`.
   * *Problema 2.2:* En `PaymentFormView` y `PaymentConceptForm`, el concepto está restringido a un `DropdownButtonFormField` y diálogo secundario, ralentizando el registro en caja.
   * *Solución 2.2:* Habilitar captura rápida con campo editable/Autocomplete en `PaymentFormView` permitiendo escribir manualmente el concepto o seleccionarlo de sugerencias.

3. **Módulo de Turnos (Destinos manuales, corte de catálogo, recargo y métricas):**
   * *Problema 3.1:* En `TurnoFormView`, el destino está confinado a un `DropdownButtonFormField<TarifaSectorModel>`.
   * *Solución 3.1:* Sustituir el dropdown rígido por un campo `Autocomplete` con entrada de texto libre (`TextFormField`), permitiendo al operador escribir cualquier destino al vuelo o seleccionarlo de las tarifas de Odoo.
   * *Problema 3.2:* Destinos que inician con M, P y S (Manga, Manzanillo del Mar, Pedro Salazar, San Pedro, San Francisco, etc.) no aparecen en la app.
   * *Solución 3.2:* La causa raíz en `OdooService.getTarifasSector()` era `limit: 200` con `order: 'name asc'`, que truncaba el catálogo antes de la letra M. Se eleva el límite a 1000 y se agregan sectores clave en el catálogo de respaldo para garantizar disponibilidad 100%.
   * *Problema 3.3:* El recargo nocturno debe aplicar desde las 19:00 (7:00 p.m.) con valor de $1.100. En `TurnoFormView`, si la tarifa en Odoo contenía `valor_recargo > 0` (ej: 2500 histórico), se sobreescribía el valor oficial.
   * *Solución 3.3:* Fijar estrictamente el recargo nocturno oficial en $1.100 COP sin sobreescrituras arbitrarias.
   * *Problema 3.4:* En `BahiaSelectedView`, el cuadro de métricas ("Recaudo Empresa" y "Servicios Clientes") ocupa espacio vertical innecesario en la vista de turnos.
   * *Solución 3.4:* Ocultar el cuadro de métricas cuando el operador esté en las pestañas de Turnos (Cola o Despachos), mostrándolo únicamente en la pestaña de Pagos o eliminándolo de los turnos para maximizar el área visible.

## 2. Alcance e Impacto
* **Capa de Red y Modelos:** `OdooService`, `PagoRecaudoModel`, `TarifaSectorModel`.
* **Capa de UI:** `PagoCardWidget`, `PaymentFormView`, `TurnoFormView`, `BahiaSelectedView`.
* **Versionamiento:** Bump a `v2.1.24+26`.
* **Despliegue Multi-Dispositivo:** Verificación física en Móvil Xiaomi, Tablet Lenovo y Windows Desktop.

