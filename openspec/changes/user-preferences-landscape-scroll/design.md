# Diseño Arquitectónico: Persistencia Local por Usuario y Scroll Lateral en Landscape

## 1. Arquitectura de Persistencia Local Segmentada (Key Scoping)

Dado que Odoo 11 no contiene modelos para los dispositivos térmicos locales (impresoras Bluetooth portátiles, colas Spooler de Windows o impresoras de red locales), la información debe almacenarse en el almacenamiento local del cliente (`SharedPreferences` a través de `LocalStorage`), pero con aislamiento estricto por usuario:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FLUJO DE PERSISTENCIA Y CARGA                   │
└────────────────────────────────────────────────────────────────────────┘

  [ Usuario Autenticado: "29d@fundetaxcol.co" ]
                      │
                      ▼
  Clave de Almacenamiento: "user_pref_29d@fundetaxcol.co_printer_config"
                      │
                      ▼
  Valor Almacenado (JSON):
  {
    "tipo": "spooler",
    "nombreODireccion": "TIQUETES",
    "anchoPapel": 80,
    "autoCorte": true
  }
```

### Métodos del Contrato en `PrinterService`:
1. `Future<void> saveUserConfig(String user, PrinterConfigModel newConfig)`:
   - Serializa a JSON y guarda en `LocalStorage.setString('user_pref_${user}_printer_config', jsonStr)`.
   - Muta `this.config = newConfig`.
2. `Future<PrinterConfigModel> loadUserConfig(String user)`:
   - Lee de `LocalStorage.getString('user_pref_${user}_printer_config')`.
   - Si existe, decodifica el JSON y actualiza `this.config`.
   - Si no existe, mantiene la configuración actual o los valores por defecto del sistema.

### Integración en `SettingsView`:
- En `initState`: Inicializa campos leyendo la configuración actual de `printerService.config` o cargando para `odooService.usuarioActivo.value`.
- En `_guardarConfiguracion`: Llama a `printerService.saveUserConfig(usuario, newPrinterConfig)`.

### Integración en `OdooService`:
- En `autenticar` exitoso y en `autoLogin`: invoca la carga de preferencias de impresión para el usuario recién logueado.

---

## 2. Arquitectura de Scroll Lateral en Landscape / Tablet

```
┌────────────────────────────────────────────────────────────────────────┐
│                  REESTRUCTURACIÓN DEL PANEL LATERAL                    │
└────────────────────────────────────────────────────────────────────────┘

  ANTES:
  Container(
    width: 300,
    child: Column(   <-- ❌ Desborda en pantallas de altura < 450px
      children: [
        ...,
        const Spacer(),  <-- ❌ Incompatible con scroll
        _buildMetricTile(...),
      ]
    )
  )

  DESPUÉS:
  Container(
    width: 300,
    child: SingleChildScrollView(  <-- ✅ Desplazamiento táctil fluido
      physics: const BouncingScrollPhysics(),
      child: Column(
        children: [
          ...,
          const SizedBox(height: 16), <-- ✅ Espaciado proporcional seguro
          _buildMetricTile(...),
        ]
      )
    )
  )
```
