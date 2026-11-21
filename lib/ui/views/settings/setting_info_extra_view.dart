import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/config/app_version.dart';
import '../../../core/theme/app_colors.dart';
import '../../../services/odoo_service.dart';
import '../../../services/socket_service.dart';

class SettingInfoExtraView extends StatelessWidget {
  const SettingInfoExtraView({super.key});

  @override
  Widget build(BuildContext context) {
    final odooService = Get.find<OdooService>();
    final socketService = Get.find<SocketService>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Auditoría y Diagnóstico Técnico'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Conexión al Backend
          _buildSectionHeader('Conexión al Backend de Odoo'),
          _buildInfoCard([
            _buildTile('Host Servidor', odooService.networkConfig.rawHost, Icons.dns),
            _buildTile('Puerto RPC', '80 (JSON-RPC)', Icons.router),
            _buildTile('Base de Datos', odooService.dbName.value, Icons.storage),
            _buildTile('Estado Conexión', odooService.isOnline.value ? 'Online (Activo)' : 'Desconectado', Icons.wifi,
                color: odooService.isOnline.value ? AppColors.success : AppColors.error),
          ]),

          const SizedBox(height: 20),

          // WebSocket y Tiempo Real
          _buildSectionHeader('Servicio en Tiempo Real (Sockets)'),
          _buildInfoCard([
            _buildTile('Endpoint Sockets', socketService.serverUrl, Icons.sync_alt),
            _buildTile('Estado WebSockets', socketService.isConnected.value ? 'Conectado (Puerto 3000)' : 'Reconectando', Icons.flash_on,
                color: socketService.isConnected.value ? AppColors.success : AppColors.warning),
            _buildTile('Último Evento', socketService.lastEventName.value.isNotEmpty ? socketService.lastEventName.value : 'Ninguno recibido', Icons.notifications_active),
          ]),

          const SizedBox(height: 20),

          // Identidad del Operador
          _buildSectionHeader('Identidad del Operador'),
          _buildInfoCard([
            _buildTile('Usuario Activo', odooService.usuarioActivo.value, Icons.person),
            _buildTile('Estado Sesión', odooService.isAuthenticated.value ? 'Sesión Autenticada' : 'No Autenticado', Icons.verified_user,
                color: odooService.isAuthenticated.value ? AppColors.success : AppColors.error),
          ]),

          const SizedBox(height: 20),

          // Versión de la Aplicación
          _buildSectionHeader('Información de la Aplicación'),
          _buildInfoCard([
            _buildTile('Nombre', 'Synergia Móvil (Fundetaxcol Parity)', Icons.apps),
            _buildTile('Versión de Compilación', AppVersion.display, Icons.tag),
            _buildTile('Canal de Despliegue', AppVersion.environment, Icons.location_on),
          ]),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 8),
      child: Text(
        title.toUpperCase(),
        style: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.0,
          color: AppColors.primary,
        ),
      ),
    );
  }

  Widget _buildInfoCard(List<Widget> children) {
    return Card(
      elevation: 1.5,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: Colors.white10),
      ),
      color: AppColors.surface,
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Column(
          children: children,
        ),
      ),
    );
  }

  Widget _buildTile(String label, String value, IconData icon, {Color? color}) {
    return ListTile(
      dense: true,
      leading: Icon(icon, color: color ?? AppColors.textSecondary, size: 22),
      title: Text(label, style: const TextStyle(fontSize: 13, color: Colors.grey)),
      trailing: Text(
        value,
        style: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.bold,
          color: color ?? Colors.white,
        ),
      ),
    );
  }
}
