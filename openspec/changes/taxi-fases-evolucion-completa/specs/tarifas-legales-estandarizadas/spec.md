## ADDED Requirements

### Requirement: Tarifas Legales Estandarizadas por Matriz Oficial
El sistema SHALL calcular el valor de los servicios de transporte utilizando estrictamente la matriz oficial de sectores y barrios autorizada por decreto distrital de transporte, prohibiendo cualquier cálculo discrecional o tarifa dinámica especulativa.

#### Scenario: Cotización Basada en Matriz Oficial
- **WHEN** un pasajero ingresa el origen y destino del viaje
- **THEN** el sistema consulta la colección `/tarifas_sector/{id}` y obtiene el valor base fijado por la autoridad distrital para dicho par de zonas

### Requirement: Evaluación Centralizada de Recargos Legales en Servidor
El sistema SHALL calcular los recargos legales (nocturno, festivo/dominical y aeropuerto/terminal) exclusivamente del lado del servidor (Firebase Cloud Functions), validando marcas de tiempo UTC y calendarios oficiales para impedir manipulaciones desde el reloj del dispositivo cliente.

#### Scenario: Aplicación Automática de Recargo Nocturno
- **WHEN** se cotiza un viaje dentro de la franja horaria oficial de 20:00 a 05:00
- **THEN** el sistema suma automáticamente el valor del recargo nocturno legalmente reglamentado y lo desglosa en la tarifa total

### Requirement: Pantalla Espejo de Transparencia Tarifaria Bidireccional
El sistema SHALL presentar exactamente el mismo desglose tarifario (valor base + recargos aplicados = total a pagar) en la pantalla del pasajero y en la pantalla del conductor, tanto al momento de cotizar como al momento de cobrar.

#### Scenario: Coincidencia Exacta de Montos
- **WHEN** el conductor finaliza la carrera en destino
- **THEN** el valor exhibido en el terminal del taxista coincide al 100% con el valor exhibido en el smartphone del pasajero y en el comprobante digital

### Requirement: Prohibición y Auditoría de Cobros Arbitrarios
El sistema SHALL bloquear cualquier intento de cobrar un valor superior al emitido por la plataforma oficial y proporcionar un canal de reporte inmediato para los pasajeros.

#### Scenario: Reporte por Discrepancia Tarifaria
- **WHEN** un pasajero califica negativamente un viaje reportando sobrecosto arbitrario
- **THEN** el sistema genera una alerta automática de auditoría en la Capa 0 de la agremiación para investigación y posible bloqueo preventivo del conductor
