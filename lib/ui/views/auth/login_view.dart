import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import '../../../core/config/app_version.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/utils/local_storage.dart';
import '../../../services/odoo_service.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _usuarioCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final odooService = Get.find<OdooService>();

  bool _obscurePassword = true;
  bool _recordar = true;
  String? _errorMessage;

  final List<Map<String, String>> _bahias = [
    {'label': 'Bahía 29D', 'login': '29d@pidemeaqui.com', 'icon': 'local_taxi'},
    {'label': 'Bahía Garita', 'login': 'garita@pidemeaqui.com', 'icon': 'shield'},
    {'label': 'Bahía Av. Lago', 'login': 'lago@pidemeaqui.com', 'icon': 'water'},
    {'label': 'Frank Operador', 'login': 'frank@pidemeaqui.com', 'icon': 'badge'},
    {'label': 'Admin Central', 'login': 'admin@pidemeaqui.com', 'icon': 'person'},
  ];

  @override
  void initState() {
    super.initState();
    final savedLogin = LocalStorage.getString('odoo_login') ?? '29d@pidemeaqui.com';
    _usuarioCtrl.text = savedLogin;
    _passwordCtrl.text = LocalStorage.getString('odoo_password') ?? '';
  }

  @override
  void dispose() {
    _usuarioCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  Future<void> _iniciarSesion() async {
    final usuario = _usuarioCtrl.text.trim();
    final password = _passwordCtrl.text.trim();

    if (usuario.isEmpty || password.isEmpty) {
      setState(() {
        _errorMessage = 'Por favor ingresa usuario y contraseña.';
      });
      return;
    }

    setState(() {
      _errorMessage = null;
    });

    final exito = await odooService.autenticar(
      usuario: usuario,
      password: password,
      recordar: _recordar,
    );

    if (!exito && mounted) {
      setState(() {
        _errorMessage = 'Credenciales no válidas. Verifica tu usuario y clave.';
      });
    }
  }

  Future<void> _confirmarSalida() async {
    final salir = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: AppColors.cardBorder),
        ),
        title: const Row(
          children: [
            Icon(Icons.power_settings_new, color: AppColors.error),
            SizedBox(width: 10),
            Text('Salir de la aplicación', style: TextStyle(color: Colors.white, fontSize: 18)),
          ],
        ),
        content: const Text(
          '¿Estás seguro de que deseas cerrar y salir de Synergia Móvil?',
          style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(false),
            child: const Text('Cancelar', style: TextStyle(color: AppColors.textSecondary)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.error,
              foregroundColor: Colors.white,
            ),
            onPressed: () => Navigator.of(ctx).pop(true),
            child: const Text('Salir'),
          ),
        ],
      ),
    );

    if (salir == true) {
      if (Platform.isAndroid) {
        await SystemNavigator.pop();
        Future.delayed(const Duration(milliseconds: 300), () => exit(0));
      } else if (Platform.isIOS) {
        await SystemNavigator.pop();
      } else {
        exit(0);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isCompact = screenWidth < 750;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            child: ConstrainedBox(
              constraints: BoxConstraints(maxWidth: isCompact ? 500 : 850),
              child: Card(
                elevation: 8,
                color: AppColors.surface,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                  side: const BorderSide(color: AppColors.cardBorder, width: 1),
                ),
                child: Padding(
                  padding: EdgeInsets.all(isCompact ? 24 : 36),
                  child: isCompact ? _buildVerticalLayout() : _buildTwoColumnLayout(),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildVerticalLayout() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _buildHeader(),
        const SizedBox(height: 24),
        _buildBahiasGrid(),
        const SizedBox(height: 24),
        _buildForm(),
      ],
    );
  }

  Widget _buildTwoColumnLayout() {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          flex: 5,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildHeader(),
              const SizedBox(height: 24),
              const Text(
                'SELECCIÓN RÁPIDA DE BAHÍA / TERMINAL:',
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.1,
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 12),
              _buildBahiasGrid(),
            ],
          ),
        ),
        const SizedBox(width: 32),
        const VerticalDivider(width: 1, color: AppColors.cardBorder),
        const SizedBox(width: 32),
        Expanded(
          flex: 5,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 12),
              const Text(
                'CREDENCIALES ODOO',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(height: 16),
              _buildForm(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.primary.withValues(alpha: 0.3)),
              ),
              child: const Icon(Icons.local_taxi, color: AppColors.primary, size: 28),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Wrap(
                    crossAxisAlignment: WrapCrossAlignment.center,
                    spacing: 6,
                    children: [
                      const Text(
                        'SYNERGIA MÓVIL',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 1.1,
                          color: Colors.white,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1.5),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(4),
                          border: Border.all(color: AppColors.primary.withValues(alpha: 0.4)),
                        ),
                        child: Text(
                          AppVersion.display,
                          style: const TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: AppColors.primary,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const Text(
                    'Terminal de Bahías y Turnos • PídemeAquí',
                    style: TextStyle(fontSize: 11, color: AppColors.textSecondary),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
            IconButton(
              onPressed: _confirmarSalida,
              tooltip: 'Salir de la aplicación',
              icon: const Icon(Icons.power_settings_new, color: AppColors.textSecondary),
              style: IconButton.styleFrom(
                hoverColor: AppColors.error.withValues(alpha: 0.15),
                highlightColor: AppColors.error.withValues(alpha: 0.2),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildBahiasGrid() {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: _bahias.map((b) {
        final isSelected = _usuarioCtrl.text == b['login'];
        return InkWell(
          onTap: () {
            setState(() {
              _usuarioCtrl.text = b['login']!;
              _errorMessage = null;
            });
          },
          borderRadius: BorderRadius.circular(10),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
              color: isSelected ? AppColors.primary.withValues(alpha: 0.2) : AppColors.surfaceElevated,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color: isSelected ? AppColors.primary : AppColors.cardBorder,
                width: isSelected ? 1.5 : 1,
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  isSelected ? Icons.check_circle : Icons.radio_button_unchecked,
                  size: 16,
                  color: isSelected ? AppColors.primary : AppColors.textSecondary,
                ),
                const SizedBox(width: 8),
                Text(
                  b['label']!,
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    color: isSelected ? Colors.white : AppColors.textPrimary,
                  ),
                ),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildForm() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (_errorMessage != null) ...[
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.error.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: AppColors.error.withValues(alpha: 0.3)),
            ),
            child: Row(
              children: [
                const Icon(Icons.error_outline, color: AppColors.error, size: 20),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    _errorMessage!,
                    style: const TextStyle(color: AppColors.error, fontSize: 12),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
        ],

        TextField(
          controller: _usuarioCtrl,
          decoration: const InputDecoration(
            labelText: 'Usuario / Correo Odoo',
            prefixIcon: Icon(Icons.person_outline),
            hintText: 'ej. 29d@pidemeaqui.com',
          ),
          keyboardType: TextInputType.emailAddress,
        ),
        const SizedBox(height: 14),

        TextField(
          controller: _passwordCtrl,
          obscureText: _obscurePassword,
          decoration: InputDecoration(
            labelText: 'Contraseña de Bahía',
            prefixIcon: const Icon(Icons.lock_outline),
            suffixIcon: IconButton(
              icon: Icon(_obscurePassword ? Icons.visibility_off : Icons.visibility),
              onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
            ),
          ),
          onSubmitted: (_) => _iniciarSesion(),
        ),
        const SizedBox(height: 12),

        Row(
          children: [
            Checkbox(
              value: _recordar,
              activeColor: AppColors.primary,
              onChanged: (val) => setState(() => _recordar = val ?? true),
            ),
            const Expanded(
              child: Text(
                'Recordar en esta terminal',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
        const SizedBox(height: 18),

        Obx(() {
          final loading = odooService.isLoggingIn.value;
          return ElevatedButton(
            onPressed: loading ? null : _iniciarSesion,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              elevation: 4,
            ),
            child: loading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                  )
                : const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.login, size: 20),
                      SizedBox(width: 10),
                      Text(
                        'INGRESAR A BAHÍA',
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, letterSpacing: 1.1),
                      ),
                    ],
                  ),
          );
        }),
        const SizedBox(height: 12),
        OutlinedButton.icon(
          onPressed: _confirmarSalida,
          icon: const Icon(Icons.power_settings_new, size: 18, color: AppColors.error),
          label: const Text(
            'SALIR DE LA APLICACIÓN',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 13,
              letterSpacing: 1.0,
              color: AppColors.textSecondary,
            ),
          ),
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.error,
            side: const BorderSide(color: AppColors.cardBorder),
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
      ],
    );
  }
}
