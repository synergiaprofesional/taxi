import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_colors.dart';
import '../../../services/odoo_service.dart';
import '../home/home_view.dart';
import 'login_view.dart';

/// Control de Acceso Raíz (Gatekeeper):
/// Bloquea completamente el acceso a HomeView hasta que el usuario se haya autenticado
/// exitosamente contra fundetaxcol.co en Odoo.
/// Si se cierra la sesión o se sale del sistema, retorna inmediatamente a LoginView.
class AuthGatekeeper extends StatelessWidget {
  final bool autoConnectSockets;
  const AuthGatekeeper({super.key, this.autoConnectSockets = true});

  @override
  Widget build(BuildContext context) {
    final odooService = Get.find<OdooService>();

    return Obx(() {
      if (odooService.isAuthenticated.value) {
        return HomeView(autoConnectSockets: autoConnectSockets);
      }

      // Si está en proceso de auto-login al arrancar, muestra splash elegante
      if (odooService.isLoggingIn.value) {
        return const Scaffold(
          backgroundColor: AppColors.background,
          body: Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.local_taxi, color: AppColors.primary, size: 48),
                SizedBox(height: 16),
                Text(
                  'SYNERGIA MÓVIL',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                    color: Colors.white,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'Conectando a fundetaxcol.co...',
                  style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
                ),
                SizedBox(height: 24),
                SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.primary),
                ),
              ],
            ),
          ),
        );
      }

      // No autenticado: Bloqueo total de la interfaz operativa
      return const LoginView();
    });
  }
}
