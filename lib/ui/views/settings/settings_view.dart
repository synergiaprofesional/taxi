import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:taxi/controllers/theme_controller.dart';
import 'package:taxi/core/config/app_version.dart';
import 'package:taxi/core/theme/app_colors.dart';
import 'package:taxi/core/utils/local_storage.dart';
import 'package:taxi/models/printer_config_model.dart';
import 'package:taxi/models/ticket_data_model.dart';
import 'package:taxi/services/odoo_service.dart';
import 'package:taxi/services/printer_service.dart';
import 'package:taxi/services/socket_service.dart';
import 'package:taxi/ui/views/settings/setting_info_extra_view.dart';
import 'package:taxi/ui/widgets/ticket_preview_dialog.dart';

class SettingsView extends StatefulWidget {
  const SettingsView({super.key});

  @override
  State<SettingsView> createState() => _SettingsViewState();
}

class _SettingsViewState extends State<SettingsView> {
  final odooService = Get.find<OdooService>();
  final socketService = Get.find<SocketService>();
  final printerService = Get.find<PrinterService>();
  final themeController = Get.find<ThemeController>();

  late TextEditingController _hostCtrl;
  late TextEditingController _dbCtrl;
  late TextEditingController _userCtrl;
  late TextEditingController _passCtrl;
  late TextEditingController _socketCtrl;
  late TextEditingController _printerAddressCtrl;

  TipoImpresora _tipoImpresora = TipoImpresora.emulador;
  int _anchoPapel = 58;
  bool _autoCorte = true;
  bool _useHttps = false;
  bool _isTesting = false;

  @override
  void initState() {
    super.initState();
    _hostCtrl = TextEditingController(text: odooService.networkConfig.rawHost);
    _dbCtrl = TextEditingController(text: odooService.dbName.value);
    _userCtrl = TextEditingController(text: LocalStorage.getString('odoo_login') ?? '29d@fundetaxcol.co');
    _passCtrl = TextEditingController(text: LocalStorage.getString('odoo_password') ?? '');
    _socketCtrl = TextEditingController(text: 'http://fundetaxcol.co:3000');
    _printerAddressCtrl = TextEditingController(text: printerService.config.nombreODireccion);
    _tipoImpresora = printerService.config.tipo;
    _anchoPapel = printerService.config.anchoPapel;
    _autoCorte = printerService.config.autoCorte;
    _useHttps = odooService.networkConfig.useHttps;
  }

  @override
  void dispose() {
    _hostCtrl.dispose();
    _dbCtrl.dispose();
    _userCtrl.dispose();
    _passCtrl.dispose();
    _socketCtrl.dispose();
    _printerAddressCtrl.dispose();
    super.dispose();
  }

  void _guardarConfiguracion() {
    odooService.networkConfig.updateHost(_hostCtrl.text.trim());
    odooService.networkConfig.setUseHttps(_useHttps);
    odooService.dbName.value = _dbCtrl.text.trim();

    final user = _userCtrl.text.trim();
    final pass = _passCtrl.text.trim();
    if (user.isNotEmpty) LocalStorage.setString('odoo_login', user);
    if (pass.isNotEmpty) LocalStorage.setString('odoo_password', pass);

    final activeUser = (odooService.usuarioActivo.value.isNotEmpty && odooService.usuarioActivo.value != 'Operador')
        ? odooService.usuarioActivo.value
        : user;

    final newPrinterConfig = PrinterConfigModel(
      tipo: _tipoImpresora,
      nombreODireccion: _printerAddressCtrl.text.trim(),
      anchoPapel: _anchoPapel,
      autoCorte: _autoCorte,
    );
    printerService.saveUserConfig(activeUser, newPrinterConfig);

    Get.snackbar(
      'Configuración Guardada',
      'Parámetros persistidos localmente para el usuario: $activeUser',
      backgroundColor: AppColors.success,
      colorText: Colors.white,
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  Future<void> _probarConexionOdoo() async {
    setState(() => _isTesting = true);
    final latency = await odooService.verificarLatencia();
    setState(() => _isTesting = false);

    Get.snackbar(
      latency >= 0 ? 'Conexión Exitosa' : 'Servidor Inaccesible',
      latency >= 0
          ? 'Servidor respondió en ${latency}ms (Modo Online)'
          : 'No se pudo contactar el servidor. Se operará en Modo Offline.',
      backgroundColor: latency >= 0 ? AppColors.success : AppColors.warning,
      colorText: Colors.white,
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _probarImpresion() {
    final ticketPrueba = TicketDataModel(
      bahiaNombre: 'Bahía Principal',
      turnoNumero: 'T-0001',
      placa: 'TEST-00',
      movilNumero: 'M-01',
      conductor: 'Prueba de Sistema',
      destino: 'Aeropuerto (\$ 18.000)',
      direccion: 'Terminal 1 - Puerta 2',
      fechaHora: DateTime.now(),
      valorTotal: 18000.0,
      cajero: 'Admin',
      pieMensaje: '¡Prueba de Tiquete Exitosa!',
    );

    Get.dialog(
      TicketPreviewDialog(
        ticket: ticketPrueba,
        printerService: printerService,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Configuración y Diagnóstico', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.save, color: AppColors.primary),
            tooltip: 'Guardar Ajustes',
            onPressed: _guardarConfiguracion,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // SECCIÓN 0: TEMA CLARO Y OSCURO MANDATORIO
                _buildCard(
                  title: 'APARIENCIA Y TEMA VISUAL',
                  icon: Icons.palette_outlined,
                  color: AppColors.primary,
                  children: [
                    const Text(
                      'Seleccione el modo visual según las condiciones de iluminación operativa:',
                      style: TextStyle(fontSize: 13),
                    ),
                    const SizedBox(height: 12),
                    Obx(() {
                      final currentMode = themeController.themeMode.value;
                      return SegmentedButton<ThemeMode>(
                        segments: const [
                          ButtonSegment<ThemeMode>(
                            value: ThemeMode.light,
                            label: Text('Claro (Sol)'),
                            icon: Icon(Icons.wb_sunny_outlined),
                          ),
                          ButtonSegment<ThemeMode>(
                            value: ThemeMode.dark,
                            label: Text('Oscuro (Noche)'),
                            icon: Icon(Icons.dark_mode_outlined),
                          ),
                          ButtonSegment<ThemeMode>(
                            value: ThemeMode.system,
                            label: Text('Sistema'),
                            icon: Icon(Icons.brightness_auto),
                          ),
                        ],
                        selected: {currentMode},
                        onSelectionChanged: (Set<ThemeMode> newSelection) {
                          themeController.setThemeMode(newSelection.first);
                        },
                      );
                    }),
                  ],
                ),
                const SizedBox(height: 20),

                // SECCIÓN 1: Servidor Odoo
                _buildCard(
                  title: 'SERVIDOR CENTRAL (ODOO 11)',
                  icon: Icons.dns_outlined,
                  color: AppColors.secondary,
                  children: [
                    TextFormField(
                      controller: _hostCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Host / Dominio del Servidor',
                        hintText: 'ej. fundetaxcol.co',
                        prefixIcon: Icon(Icons.language),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _dbCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Base de Datos',
                              prefixIcon: Icon(Icons.storage),
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Row(
                          children: [
                            const Text('HTTPS (SSL):', style: TextStyle(fontWeight: FontWeight.bold)),
                            Switch(
                              value: _useHttps,
                              activeTrackColor: AppColors.primary,
                              onChanged: (val) => setState(() => _useHttps = val),
                            ),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _userCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Usuario Odoo',
                              prefixIcon: Icon(Icons.person),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: TextFormField(
                            controller: _passCtrl,
                            obscureText: true,
                            decoration: const InputDecoration(
                              labelText: 'Contraseña',
                              prefixIcon: Icon(Icons.lock),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.surfaceElevated,
                        foregroundColor: AppColors.primary,
                      ),
                      onPressed: _isTesting ? null : _probarConexionOdoo,
                      icon: _isTesting
                          ? const SizedBox(
                              width: 16,
                              height: 16,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.network_check),
                      label: Text(_isTesting ? 'Verificando...' : 'Probar Conexión Odoo (Ping)'),
                    ),
                  ],
                ),

                const SizedBox(height: 20),

                // SECCIÓN 2: WebSockets en Tiempo Real
                _buildCard(
                  title: 'CANAL EN TIEMPO REAL (SOCKET.IO)',
                  icon: Icons.sync,
                  color: AppColors.accent,
                  children: [
                    TextFormField(
                      controller: _socketCtrl,
                      decoration: const InputDecoration(
                        labelText: 'URL de server_rt_odoo',
                        hintText: 'http://fundetaxcol.co:3000',
                        prefixIcon: Icon(Icons.bolt),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Obx(() => Wrap(
                          spacing: 12,
                          runSpacing: 10,
                          crossAxisAlignment: WrapCrossAlignment.center,
                          alignment: WrapAlignment.spaceBetween,
                          children: [
                            Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  socketService.isConnected.value ? Icons.circle : Icons.circle_outlined,
                                  color: socketService.isConnected.value ? AppColors.success : AppColors.error,
                                  size: 14,
                                ),
                                const SizedBox(width: 8),
                                Text(
                                  socketService.isConnected.value
                                      ? 'Estado: Conectado a Sockets'
                                      : 'Estado: Desconectado',
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                ),
                              ],
                            ),
                            ElevatedButton.icon(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.primary,
                                foregroundColor: Colors.black,
                                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                              ),
                              icon: const Icon(Icons.refresh, size: 16),
                              label: const Text('Reconectar', style: TextStyle(fontWeight: FontWeight.bold)),
                              onPressed: () => socketService.conectar(host: _socketCtrl.text.trim()),
                            ),
                          ],
                        )),
                  ],
                ),

                const SizedBox(height: 20),

                // SECCIÓN 3: Hardware de Impresión
                _buildCard(
                  title: 'IMPRESIÓN TÉRMICA DUAL (ESC/POS)',
                  icon: Icons.print,
                  color: AppColors.primary,
                  children: [
                    Obx(() {
                      final activeUser = odooService.usuarioActivo.value;
                      return Container(
                        margin: const EdgeInsets.only(bottom: 12),
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        decoration: BoxDecoration(
                          color: AppColors.surfaceElevated,
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(color: AppColors.primary.withValues(alpha: 0.3)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.person_pin, size: 16, color: AppColors.primary),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                'Preferencias de hardware para: $activeUser',
                                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textSecondary),
                              ),
                            ),
                          ],
                        ),
                      );
                    }),
                    DropdownButtonFormField<TipoImpresora>(
                      initialValue: _tipoImpresora,
                      decoration: const InputDecoration(
                        labelText: 'Tipo de Dispositivo',
                        prefixIcon: Icon(Icons.device_hub),
                      ),
                      items: const [
                        DropdownMenuItem(
                          value: TipoImpresora.emulador,
                          child: Text('Emulador Virtual en Pantalla'),
                        ),
                        DropdownMenuItem(
                          value: TipoImpresora.bluetooth,
                          child: Text('Bluetooth Portátil (Android / SPP)'),
                        ),
                        DropdownMenuItem(
                          value: TipoImpresora.tcp,
                          child: Text('Wi-Fi / Red LAN (TCP Port 9100)'),
                        ),
                        DropdownMenuItem(
                          value: TipoImpresora.spoolerWindows,
                          child: Text('Spooler / Cola de Windows USB'),
                        ),
                        DropdownMenuItem(
                          value: TipoImpresora.url,
                          child: Text('Servicio Web / URL de Impresión (HTTP)'),
                        ),
                      ],
                      onChanged: (val) {
                        if (val != null) setState(() => _tipoImpresora = val);
                      },
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _printerAddressCtrl,
                      decoration: InputDecoration(
                        labelText: _tipoImpresora == TipoImpresora.url
                            ? 'URL del Servicio de Impresión (PC o Servidor)'
                            : _tipoImpresora == TipoImpresora.tcp
                                ? 'Dirección IP de Impresora Wi-Fi (ej: 192.168.1.200)'
                                : _tipoImpresora == TipoImpresora.bluetooth
                                    ? 'Dirección MAC Bluetooth / Nombre de Dispositivo'
                                    : _tipoImpresora == TipoImpresora.spoolerWindows
                                        ? 'Nombre de la Impresora en Windows (ej: TIQUETES)'
                                        : 'Identificador / Nombre del Emulador',
                        hintText: _tipoImpresora == TipoImpresora.url
                            ? 'http://192.168.1.100:8080/imprimir'
                            : _tipoImpresora == TipoImpresora.tcp
                                ? '192.168.1.200'
                                : _tipoImpresora == TipoImpresora.bluetooth
                                    ? '00:11:22:33:44:55'
                                    : _tipoImpresora == TipoImpresora.spoolerWindows
                                        ? 'TIQUETES'
                                        : 'Emulador Virtual Synergia',
                        prefixIcon: Icon(
                          _tipoImpresora == TipoImpresora.url
                              ? Icons.link
                              : _tipoImpresora == TipoImpresora.tcp
                                  ? Icons.wifi
                                  : _tipoImpresora == TipoImpresora.bluetooth
                                      ? Icons.bluetooth
                                      : _tipoImpresora == TipoImpresora.spoolerWindows
                                          ? Icons.usb
                                          : Icons.desktop_windows,
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 16,
                      runSpacing: 12,
                      crossAxisAlignment: WrapCrossAlignment.center,
                      alignment: WrapAlignment.spaceBetween,
                      children: [
                        Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text('Ancho de Papel: ', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                            const SizedBox(width: 6),
                            ChoiceChip(
                              label: const Text('58 mm'),
                              selected: _anchoPapel == 58,
                              onSelected: (_) => setState(() => _anchoPapel = 58),
                            ),
                            const SizedBox(width: 6),
                            ChoiceChip(
                              label: const Text('80 mm'),
                              selected: _anchoPapel == 80,
                              onSelected: (_) => setState(() => _anchoPapel = 80),
                            ),
                          ],
                        ),
                        Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text('Auto-corte:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                            const SizedBox(width: 6),
                            Switch(
                              value: _autoCorte,
                              activeTrackColor: AppColors.primary,
                              onChanged: (val) => setState(() => _autoCorte = val),
                            ),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        foregroundColor: Colors.black,
                        textStyle: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      onPressed: _probarImpresion,
                      icon: const Icon(Icons.receipt),
                      label: const Text('Imprimir / Ver Tiquete de Prueba'),
                    ),
                    const SizedBox(height: 12),
                    OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: AppColors.secondary),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                      onPressed: () => Get.to(() => const SettingInfoExtraView()),
                      icon: const Icon(Icons.info_outline, color: AppColors.secondary),
                      label: const Text('Información Adicional y Diagnóstico', style: TextStyle(color: AppColors.secondary, fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 24),
                    Center(
                      child: Column(
                        children: [
                          Text(
                            'Synergia Móvil ${AppVersion.display}',
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textSecondary,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            '${AppVersion.environment} • Flutter 3',
                            style: TextStyle(
                              fontSize: 11,
                              color: AppColors.textSecondary.withValues(alpha: 0.6),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCard({
    required String title,
    required IconData icon,
    required Color color,
    required List<Widget> children,
  }) {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: color.withValues(alpha: 0.3)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 22),
                const SizedBox(width: 10),
                Text(
                  title,
                  style: TextStyle(
                    color: color,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.8,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
            const Divider(height: 24),
            ...children,
          ],
        ),
      ),
    );
  }
}
