# 🏛️ Registro de Errores, Falsas Impresiones y Fixes Obligatorios

Este archivo es de **lectura obligatoria** para cualquier agente o sesión antes de ejecutar compilaciones, despliegues, comandos de sistema o afirmar estados al usuario. Se rige por la **Regla Inviolable #5 de AGENTS.md y GEMINI.md**.

---

## 📋 Protocolo de Operación y Gates de Verificación

Queda terminantemente prohibido asumir que un proceso o compilación "terminó bien" o "está actualizado" sin contrastar la evidencia física en el sistema de archivos o en el dispositivo de destino.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       GATE DE VERIFICACIÓN OBLIGATORIO                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Ejecución del Comando ➔ NUNCA reportar éxito solo por código de salida. │
│  2. Inspección Empírica   ➔ Verificar mtime, versionName y package dumps.   │
│  3. Validación de Usuario ➔ Comprobar que lo que ve el usuario en pantalla  │
│                             coincide al 100% con lo reportado.              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📜 Índice de Gotchas y Fixes en Mármol

### FIX-001: Compilación Windows Release (Timestamp Visible de `synergia_movil.exe`)
* **Falsa Impresión / Error:** Asumir que `flutter build windows --release` siempre actualiza la fecha de `synergia_movil.exe`.
* **Causa Raíz:** En Flutter Desktop Windows, el ejecutable `.exe` (91 KB) es solo un *runner* C++ que aloja `flutter_windows.dll` y carga `data/app.so` (el código AOT de Dart). Si no se modifican archivos C++ en `windows/runner/`, CMake/MSBuild no recompila el `.exe` para ahorrar tiempo, actualizando únicamente `data/app.so`. El usuario abre el Explorador de Windows, ve la fecha del `.exe` de horas o días atrás y concluye que no se compiló nada.
* **Fix Obligatorio:**
  1. Eliminar previamente el ejecutable viejo con `os.remove(exe_path)` o tocar `windows/runner/main.cpp`.
  2. Ejecutar `flutter build windows --release`.
  3. **Gate de Validación:** Inspeccionar `os.path.getmtime(exe_path)` y verificar que la fecha y hora coincidan con el minuto actual.

---

### FIX-002: Despliegue de APK en Dispositivo Físico Android vía ADB
* **Falsa Impresión / Error:** Asumir que `adb install -r <apk>` actualiza la experiencia visual del usuario en el móvil.
* **Causa Raíz:**
  1. `adb install -r` instala silenciosamente en segundo plano; Android no reinicia ni trae la app al frente automáticamente.
  2. Si `version` en `pubspec.yaml` no se incrementa (ej: sigue en `2.0.0+1`), en los Ajustes del teléfono o en la pantalla de información de la app se sigue leyendo la versión antigua.
  3. En terminales donde conviven apps legacy (como `com.fundetaxcolapp` de 2025 y la nueva `com.synergia.synergia_movil`), el usuario puede estar mirando el icono de la app equivocada.
* **Fix Obligatorio:**
  1. Incrementar siempre el `version` en `pubspec.yaml` (ej: `version: 2.1.0+2`).
  2. Compilar con `flutter build apk --release`.
  3. Instalar con `adb install -r build/app/outputs/flutter-apk/app-release.apk`.
  4. **Lanzar en primer plano:** Ejecutar `adb shell am start -n com.synergia.synergia_movil/.MainActivity` para abrirla directamente ante los ojos del usuario.
  5. **Gate de Validación:** Ejecutar `adb shell dumpsys package com.synergia.synergia_movil` y verificar que `versionName` y `lastUpdateTime` correspondan a la compilación actual.

---

### FIX-003: Ejecución de Scripts Remotos en Odoo vía SSH (Paramiko / Bash)
* **Falsa Impresión / Error:** Enviar código Python largo en una sola línea mediante `ssh.exec_command('python3 -c "..."')`.
* **Causa Raíz:** Bash interpreta comillas dobles, comillas simples, saltos de línea y operadores como `(` o `&`, arrojando errores de sintaxis tipo `syntax error near unexpected token '('`.
* **Fix Obligatorio:**
  1. Redactar el código en un archivo local o subirlo directamente vía SFTP a `/tmp/script_name.py`.
  2. Ejecutar mediante comando limpio:
     `PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/script_name.py`
  3. Capturar y decodificar tanto `stdout` como `stderr`.
* **Gate de Validación:** Verificar que el script retorne código de salida `0` y salida estructurada sin trazas de Python.

---

### FIX-004: Many2one Autocomplete en Odoo 11 Bloqueado por Dominios Vacíos
* **Falsa Impresión / Error:** Pensar que la lentitud en un Many2one es contención de base de datos o fallo de red cuando el spinner no desaparece.
* **Causa Raíz:** Si un campo Many2one tiene `domain="[('id','in',campo_m2m)]"` y `options="{'no_create': True}"`, cuando `campo_m2m` se evalúa como `[]` (por ejemplo, si no hay sesiones abiertas o pagos), Odoo envía `name_search` con `[('id','in',[])]` devolviendo `[]`. El widget Many2one de Odoo 11 no muestra errores ni opciones; se queda pasivo esperando una selección que nunca puede ocurrir, dando la falsa impresión de un spinner colgado.
* **Fix Obligatorio:** Liberar el dominio en la vista a `[('active','=',True)]` o permitir fallback general si no se requiere validación contable previa.
* **Gate de Validación:** Probar `name_search(name='...', args=[], limit=7)` y validar que retorne resultados en `< 15 ms`.

---

### FIX-008: Scripts de Despliegue Batch (.bat), Subshell en Windows y Bloqueo de Pipe con ADB
* **Falsa Impresión / Error:** 
  1. Usar pipes encadenados `^|` con `for /f` dentro de archivos `.bat` en Windows provocando `The filename, directory name, or volume label syntax is incorrect`.
  2. Usar `for /f ... in ('powershell ... adb ...')` y que el script `.bat` quede congelado indefinidamente sin avanzar del paso 1.
* **Causa Raíz:**
  1. `cmd.exe` evalúa subshells con serias limitaciones cuando intervienen comillas o rutas con espacios. Además `timeout /t >nul` falla en entornos no interactivos con `Input redirection is not supported`.
  2. Si dentro del subshell de `for /f` se invoca `adb` y este arranca el daemon en segundo plano (`adb server tcp:5037`), el proceso daemon hereda los handles de salida anónimos del pipe del subshell. Como el daemon nunca termina, `for /f` espera eternamente a que se cierre el pipe, bloqueando el batch.
* **Fix Obligatorio:**
  1. NUNCA ejecutar llamadas a `adb` dentro de `for /f ('...')`.
  2. Diseñar los scripts `.bat` como *runners* ligeros que deleguen directamente la ejecución a scripts de PowerShell robustos:
     `powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\verify_and_deploy_tablet.ps1"`
  3. En pausas de lote, usar siempre `powershell -NoProfile -Command "Start-Sleep -Seconds N"`.
  4. Dejar los scripts principales (`.bat` y `.ps1`) en la raíz del proyecto para invocación directa desde cualquier terminal, conservando el repositorio central en `scripts/`.
* **Gate de Validación:** Ejecutar el `.bat` desde PowerShell (`.\deploy_phone.bat` o `.\deploy_tablet.bat`) y validar que detecte el serial del dispositivo, instale el APK y abra la app en pantalla en `< 15 segundos` sin ningún error de sintaxis ni cuelgues.

---

### FIX-005: Mapeo de Campos en Odoo 11 `fundetaxcol.pago` (`valor` vs `total`)
* **Falsa Impresión / Error:** Asumir que el backend de Odoo envía el importe de pago bajo la clave estándar `total`, reportando falsamente que el valor del pago es `$ 0` o que no tiene importe registrado.
* **Causa Raíz:** En el módulo de transporte de Fundetaxcol en Odoo 11, la tabla `fundetaxcol_pago` almacena el importe contable en la columna `valor` (`double precision`). No existe ninguna columna llamada `total`. Al ejecutar `searchRead` solicitando `total` o deserializar `json['total']`, el resultado es `null`, haciendo que la app asigne `0.0` y muestre en la tarjeta del pago: `Monto: $ 0`.
* **Fix Obligatorio:**
  1. En `payment_model.dart`: deserializar siempre con fallback: `total: (json['valor'] ?? json['total'] ?? 0.0).toDouble()`.
  2. En `turno_controller.dart`: incluir explícitamente `'valor'` en la lista de `fields` solicitados en el RPC `searchRead` a `fundetaxcol.pago`.
* **Gate de Validación:** Contrastar el valor del pago en base de datos PostgreSQL (`SELECT id, consecutivo, valor FROM fundetaxcol_pago WHERE consecutivo = '214159'`) contra la tarjeta renderizada en la app. Debe mostrar exactamente `$ 15.000` y no `$ 0`.

---

### FIX-006: Compilación de Flutter Windows - Falta de Fuentes en `cpp_client_wrapper`
* **Falsa Impresión / Error:** Asumir que `flutter clean` o `flutter pub get` siempre regenera todos los fuentes C++ efímeros de Windows.
* **Causa Raíz:** Si la carpeta `windows/flutter/ephemeral/cpp_client_wrapper` se crea vacía o solo con el subdirectorio `include`, MSBuild falla con error `fatal error C1083: Cannot open source file: '.../core_implementations.cc': No such file or directory` al compilar `flutter_wrapper_app.vcxproj`.
* **Fix Obligatorio:** Sincronizar directamente los archivos fuente `.cc` y encabezados `.h` desde el SDK de Flutter (`C:\flutter\bin\cache\artifacts\engine\windows-x64\cpp_client_wrapper`) hacia `windows/flutter/ephemeral/cpp_client_wrapper`.
* **Gate de Validación:** Verificar que `flutter build windows --release` termine con código 0 y genere `synergia_movil.exe` con tamaño ~91 KB y mtime del minuto en curso.

---

### FIX-007: Autenticación SSH y Esquema SQL en Producción (`fundetaxcol.co`)
* **Falsa Impresión / Error:** Intentar conectar por SSH con `key_filename=r'C:\Users\salis\.ssh\id_rsa'`, provocando `AuthenticationException: Authentication failed` y pérdida de tiempo en scripts de diagnóstico.
* **Causa Raíz:** El servidor `fundetaxcol.co` no tiene autorizada la llave RSA local para `root`; la autenticación se realiza estrictamente por contraseña.
* **Fix Obligatorio SSH:**
  ```python
  ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)
  ```
* **Gotchas de Columnas SQL en PostgreSQL (`fundetaxcol`):**
  * `fundetaxcol_turno`: El número de turno es la columna **`name`** (no existe `numero`). El importe recaudado es **`valor`** (no existe `valor_total`).
  * `fundetaxcol_pago`: El importe contable es **`valor`** (no existe `total`). No existe columna `state` (se usa `enturnar`, `sesion_en_progreso`, `ajuste_id`).
  * Ejecutar consultas con: `sudo -u postgres psql -d fundetaxcol -c "..."` para evitar errores de autenticación peer de PostgreSQL.

---

### FIX-009: Caddy Server Local y Error SSL (`ERR_SSL_PROTOCOL_ERROR`) en Windows
* **Falsa Impresión / Error:** Configurar `:80` en `C:\proxyServer\Caddyfile` esperando que Caddy atienda HTTPS automáticamente en `localhost` o en la IP local (`192.168.6.227`), provocando `ERR_SSL_PROTOCOL_ERROR` / conexión rechazada en puerto 443.
* **Causa Raíz:**
  1. Si en un bloque de `Caddyfile` se especifica `:80`, Caddy asume exclusivamente HTTP y desactiva el listener en puerto 443.
  2. Los navegadores que acceden por IP (`https://192.168.6.227/`) requieren que la IP esté explícitamente declarada con la directiva `tls internal` para que Caddy emita un certificado SAN IP válido. Si no existe, Caddy rechaza o aborta el handshake TLS arrojando `ERR_SSL_PROTOCOL_ERROR`.
* **Fix Obligatorio:**
  1. Configurar en `C:\proxyServer\Caddyfile`:
     ```caddyfile
     https://192.168.6.227, https://localhost, https://127.0.0.1 {
         tls internal
         reverse_proxy 127.0.0.1:4000
     }

     http://192.168.6.227, http://localhost, http://127.0.0.1 {
         reverse_proxy 127.0.0.1:4000
     }
     ```
  2. Recargar Caddy sin interrumpir la tarea de Windows con:
     `c:\windows\caddy_windows_amd64.exe reload --config C:\proxyServer\Caddyfile`
* **Gate de Validación:**
  Verificar que `curl.exe -s --ssl-no-revoke https://192.168.6.227/hw_proxy/hello` y `https://localhost/hw_proxy/hello` respondan `{"result":"pong"}` con código HTTP 200 y encabezado `Via: 1.1 Caddy`.


---

### FIX-010: Disparidad de IDs entre Sesión de Bahía (`bahia_sesion_id`) y Bahía Base (`bahia_id`) en Turnos Móviles
* **Falsa Impresión / Error:** Los tableros web de Odoo (`/tablero_turnos`) muestran turnos en espera y despachos con normalidad, pero la app móvil y tablet muestran la cola y los despachos 100% vacíos ("No hay despachos en...").
* **Causa Raíz:**
  1. En Odoo 11 `fundetaxcol_movil`, el método `TurnoMovil._get_data()` retorna dos identificadores diferentes:
     * `'bahia_sesion_id'`: ID del registro operativo de la sesión diaria (`fundetaxcol.sesion.bahia`, ej. 8843 para Garita, 8842 para 29D).
     * `'bahia_id'`: Diccionario con la bahía física estática base `{'id': 4, 'name': 'Garita'}` (`fundetaxcol.bahia`).
  2. En Flutter, `TurnoModel.fromJson` al procesar `json['bahia_id']` como Map extraía `rawBahia['id'] = 4` y lo asignaba a `bahiaSesionId`, ignorando el `json['bahia_sesion_id'] = 8843`.
  3. `TurnoController.bahiaIdActual` contiene `8843` (el ID de la sesión seleccionada por el usuario). Al filtrar con `t.bahiaSesionId == bahiaIdActual.value`, comparaba `4 == 8843`, resultando `false` y descartando todos los turnos en espera y despachados.
* **Fix Obligatorio:**
  1. En `TurnoModel`: Declarar `bahiaSesionId` y `bahiaBaseId`.
  2. En `TurnoModel.fromJson`: Extraer prioritariamente `json['bahia_sesion_id']` (8843) para `bahiaSesionId` y `rawBahia['id']` (4) para `bahiaBaseId`, con fallback cruzado si alguno es 0.
  3. En `TurnoController`: Filtrar siempre con correspondencia dual:
     `(t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value)`
     en `turnosEnCola`, `turnosDespachados`, `turnosEnColaFiltrados`, `turnosDespachadosFiltrados`, `totalServiciosClientes`, `turnoEnAtencion` y `enturnarVehiculo`.


---

### FIX-011: Instanciación de TurnoModel en Tests de Widgets con TurnoController
* **Falsa Impresión / Error:** Los tests de widgets esperan encontrar texto de tarjeta de turno o despacho (ej. `'WBD512'`, `'FXS830'`) en `BahiaSelectedView` o `TurnoListView`, pero la prueba falla con `Expected: exactly one matching candidate. Actual: Found 0 widgets`.
* **Causa Raíz:** Si `turnoController.bahiaIdActual.value > 0`, los getters `turnosEnCola` y `turnosDespachados` aplican filtro de aislamiento por bahía:
  `t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value`
  Si los `TurnoModel` simulados en el test se instancian omitiendo `bahiaSesionId` o `bahiaBaseId`, ambos campos toman por defecto `0`, por lo que la comparación `0 == bahiaIdActual.value` resulta en `false`. La lista queda vacía y la interfaz renderiza el widget de cola vacía (*"No hay turnos en..."*).
* **Fix Obligatorio:** En cualquier suite de pruebas (`test/*.dart`), asignar siempre explícitamente `bahiaSesionId` y `bahiaBaseId` coincidiendo con `turnoController.bahiaIdActual.value`:
  ```dart
  TurnoModel(
    id: 101,
    name: 'T-0001',
    vehiculoPlaca: 'WBD512',
    conductorNombre: 'Carlos Ramírez',
    bahiaNombre: '29D',
    bahiaSesionId: 8815,
    bahiaBaseId: 8815,
    ...
  )
  ```
* **Gate de Validación:** Ejecutar `flutter test` y certificar que todas las pruebas pasen con `All tests passed!`.

---

### FIX-012: Doble Conversión de Zona Horaria en Odoo 11 y Deserialización de `fecha_despacho`
* **Falsa Impresión / Error:** La app móvil y tablet muestran turnos y despachos con 5 horas de retraso (ej: `05:11 AM` en lugar de `10:11 AM` cuando la hora real del dispositivo en Colombia es `10:25 AM`), y los despachos muestran la hora de llegada a la fila en vez de la hora en que fueron efectivamente despachados.
* **Causa Raíz:**
  1. En el backend de Odoo 11 (`fundetaxcol.turno` y `fundetaxcol.pago`), el método `_get_data()` invoca `get_fecha_actual(fecha)`, el cual ya aplica el offset UTC-5 de `America/Bogota` y retorna una cadena formateada en hora colombiana local (ej. `'2026-11-02 10:11:58'`).
  2. En Flutter, los deserializadores `parseDate` (`turno_model.dart`) y `parseOdooDateTime` (`payment_model.dart`) agregaban de forma forzada un sufijo `'Z'` (`'${str}Z'`) y ejecutaban `.toLocal()`. Al añadir `'Z'`, Dart interpretaba erróneamente que la cadena de las 10:11 AM era hora UTC pura, por lo que le restaba otras 5 horas al convertir a local, resultando en `05:11 AM`.
  3. `TurnoModel` no deserializaba `fecha_despacho`, por lo que las tarjetas de despachos hacían fallback a `fechaCreacion` (hora en que el taxi llegó a la cola, no cuando salió hacia el destino).
* **Fix Obligatorio:**
  1. En `parseDate` y `parseOdooDateTime`: parsear directo con `DateTime.tryParse(str)`. Si el timestamp incluye indicador UTC (`dt.isUtc`), llamar a `.toLocal()`; si viene como fecha estándar sin zona (como lo entrega Odoo), preservarla como hora local intacta sin añadir `'Z'`.
  2. En `TurnoModel`: agregar y deserializar el campo `DateTime? fechaDespacho` desde `json['fecha_despacho']`.
  3. En `DespachoCardWidget`: formatear la hora a partir de `turno.fechaDespacho ?? turno.fechaCreacion`.
* **Gate de Validación:** Ejecutar test unitario con `'fecha': '2026-11-02 10:11:58'` y verificar que `turno.fechaCreacion.hour == 10`. En pantalla física, comprobar que la tarjeta muestre `10:11 AM` en perfecta coincidencia con el reloj de la barra de estado de Android.

---

### FIX-013: Preservación Absoluta e Inviolable de Scripts en `scripts/`
* **Falsa Impresión / Error:** Intentar eliminar, limpiar o purgar scripts auxiliares de diagnóstico, prueba o despliegue bajo el supuesto de "ordenar el espacio de trabajo".
* **Causa Raíz:** En proyectos de ingeniería de software con despliegues multi-dispositivo y diagnósticos de backend (Odoo 11 / PostgreSQL / WebSockets), cada script representa una herramienta de verificación forense, una prueba automatizada o un runner de despliegue. Borrarlos destruye la trazabilidad histórica, obliga a reinventar la rueda en sesiones futuras y vulnera la auditoría del proyecto.
* **Fix Obligatorio:**
  1. **PROHIBICIÓN TOTAL DE BORRADO:** Queda terminantemente prohibido borrar, purgar o ejecutar operaciones destructivas (`rm`, `del`, `Remove-Item`, `os.remove`, etc.) sobre archivos en la carpeta `scripts/`.
  2. Todos los scripts generados (`.py`, `.ps1`, `.bat`, `.sh`) deben almacenarse exclusivamente en `scripts/` y conservarse de forma permanente.
* **Gate de Validación:** Verificar en todo momento que el inventario de scripts en `scripts/` crezca o se conserve intacto, sin pérdida de archivos de sesiones anteriores.
