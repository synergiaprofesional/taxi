## ADDED Requirements

### Requirement: Modelado de Gremios y Estructura Jerárquica
El sistema SHALL soportar múltiples agremiaciones u organizaciones de transporte (`/organizaciones/{id}`), permitiendo la asignación de roles jerárquicos estructurados en 5 niveles: Gerencia/Presidencia, Coordinadores de Zona, Operadores de Garita, Propietarios de Flota y Conductores.

#### Scenario: Asignación de Rol Jerárquico en Gremio
- **WHEN** un administrador de gremio crea o edita la ficha de un miembro operativo
- **THEN** el sistema asigna el nivel jerárquico correspondiente y restringe sus permisos de acceso y liquidación al ámbito estricto de su organización

### Requirement: Dualidad Operativa de Flota (Conductor Público vs Privado)
El sistema SHALL clasificar a los conductores afiliados en dos modalidades operativas: `publica` (visible en el radar general para cualquier pasajero en calle o bahía pública) y `privada_corporativa` (reservada exclusivamente para convenios institucionales, hoteles o empresas aliadas).

#### Scenario: Restricción de Visibilidad para Conductor Privado
- **WHEN** un pasajero público general solicita un taxi en la calle
- **THEN** los conductores clasificados como `privada_corporativa` permanecen ocultos del algoritmo de emparejamiento público y no reciben la solicitud

#### Scenario: Despacho Prioritario para Convenio Corporativo
- **WHEN** un huésped o empleado corporativo vinculado a un convenio solicita un servicio
- **THEN** el sistema prioriza y enruta la carrera exclusivamente a la flota de conductores privados asignados a ese convenio específico

### Requirement: Modalidades de Vinculación de Pasajeros Públicos
El sistema SHALL permitir el registro de pasajeros como usuarios de carácter público, admitiendo tres modalidades de vinculación: `publico_general`, `corporativo` (mediante código de convenio o correo empresarial) y `vinculado_referido` (mediante código QR o identificador de taxista).

#### Scenario: Despacho Preferente por Código de Referido
- **WHEN** un pasajero vinculado a un conductor frecuente solicita un viaje y dicho conductor se encuentra libre a menos de 5 minutos de distancia
- **THEN** el sistema notifica en primera instancia al conductor preferido antes de abrir la carrera a la flota general del gremio
