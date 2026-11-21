import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/config/app_version.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/bay_model.dart';
import '../../../models/turno_model.dart';
import '../bahia/bahia_selector_dialog.dart';
import '../form/payment_form_view.dart';
import '../form/turno_form_view.dart';
import '../list/despacho_list_view.dart';
import '../list/pago_list_view.dart';
import '../list/turno_list_view.dart';
import '../settings/setting_info_extra_view.dart';
import '../settings/settings_view.dart';

class BahiaSelectedView extends StatefulWidget {
  final int initialTabIndex;

  const BahiaSelectedView({
    super.key,
    this.initialTabIndex = 1, // Por defecto en la pestaña de Turnos (Fila activa)
  });

  @override
  State<BahiaSelectedView> createState() => _BahiaSelectedViewState();
}

class _BahiaSelectedViewState extends State<BahiaSelectedView> {
  final controller = Get.find<TurnoController>();
  late int _currentIndex;
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialTabIndex;
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _abrirSelectorBahia() async {
    final bay = await showDialog<BahiaModel>(
      context: context,
      builder: (ctx) => BahiaSelectorDialog(bahiaActualId: controller.bahiaIdActual.value),
    );
    if (bay != null) {
      controller.cambiarBahia(bay);
    }
  }

  void _abrirDialogoEnturnar() {
    Get.to(() => const TurnoFormView());
  }

  void _abrirFormularioDespacho(TurnoModel turno) {
    Get.to(() => TurnoFormView(turno: turno));
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final scaffoldBg = isDark ? AppColors.waDarkBackground : AppColors.waLightBackground;
    final appbarBg = isDark ? AppColors.waDarkSurface : AppColors.waLightSurface;
    final taxiAccent = isDark ? AppColors.taxiYellowLight : AppColors.taxiYellowDark;
    final textPrimary = isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary;
    final textSecondary = isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary;
    final searchBg = isDark ? AppColors.waDarkSearchField : AppColors.waLightSearchField;

    return Scaffold(
      backgroundColor: scaffoldBg,
      appBar: AppBar(
        backgroundColor: appbarBg,
        elevation: isDark ? 0 : 0.5,
        title: FittedBox(
          fit: BoxFit.scaleDown,
          alignment: Alignment.centerLeft,
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              InkWell(
                borderRadius: BorderRadius.circular(8),
                onTap: _abrirSelectorBahia,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: taxiAccent.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: taxiAccent.withValues(alpha: 0.4)),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.swap_horiz, color: taxiAccent, size: 16),
                      const SizedBox(width: 4),
                      Obx(() => Text(
                            controller.bahiaSeleccionada.value,
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.bold,
                              color: taxiAccent,
                            ),
                          )),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Text(
                'Synergia Móvil',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: textPrimary,
                ),
              ),
              const SizedBox(width: 6),
              InkWell(
                borderRadius: BorderRadius.circular(6),
                onTap: () => Get.to(() => const SettingInfoExtraView()),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: taxiAccent.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: taxiAccent.withValues(alpha: 0.3)),
                  ),
                  child: Text(
                    AppVersion.display,
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 0.3,
                      color: taxiAccent,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        actions: [
          Obx(() {
            final isOnline = controller.socketService.isConnected.value;
            return Tooltip(
              message: isOnline ? 'Tiempo real activo (server_rt_odoo)' : 'Sin tiempo real (Tap para reconectar)',
              child: InkWell(
                borderRadius: BorderRadius.circular(8),
                onTap: isOnline ? null : () => controller.socketService.reconnect(),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 4),
                  margin: const EdgeInsets.symmetric(vertical: 13, horizontal: 2),
                  decoration: BoxDecoration(
                    color: isOnline
                        ? AppColors.success.withValues(alpha: 0.15)
                        : AppColors.error.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: isOnline
                          ? AppColors.success.withValues(alpha: 0.5)
                          : AppColors.error.withValues(alpha: 0.5),
                    ),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.circle,
                        size: 8,
                        color: isOnline ? AppColors.success : AppColors.error,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        isOnline ? 'RT' : 'Sin RT',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                          color: isOnline ? AppColors.success : AppColors.error,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            );
          }),
          IconButton(
            icon: Icon(Icons.refresh, color: taxiAccent),
            tooltip: 'Refrescar datos',
            onPressed: () {
              controller.cargarTurnosDesdeServidor();
              controller.cargarPagosDesdeServidor();
            },
          ),
          PopupMenuButton<String>(
            icon: Icon(Icons.more_vert, color: textPrimary),
            onSelected: (val) {
              if (val == 'bahia') _abrirSelectorBahia();
              if (val == 'settings') Get.to(() => const SettingsView());
              if (val == 'logout') controller.odooService.cerrarSesion();
            },
            itemBuilder: (ctx) => [
              const PopupMenuItem(
                value: 'bahia',
                child: Row(
                  children: [
                    Icon(Icons.swap_horiz, color: AppColors.primary, size: 20),
                    SizedBox(width: 10),
                    Text('Cambiar Bahía'),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'settings',
                child: Row(
                  children: [
                    Icon(Icons.settings_outlined, color: AppColors.textPrimary, size: 20),
                    SizedBox(width: 10),
                    Text('Ajustes'),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout, color: AppColors.error, size: 20),
                    SizedBox(width: 10),
                    Text('Cerrar Sesión', style: TextStyle(color: AppColors.error)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          // Barra de métricas duales compactas adaptativa (Exclusiva de Pestaña de Pagos)
          if (_currentIndex == 0)
            Obx(() {
              final recaudoEmpresa = controller.totalRecaudoEmpresa;
              final serviciosClientes = controller.totalServiciosClientes;
              final formatRecaudo = NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0).format(recaudoEmpresa);
              final formatServicios = NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0).format(serviciosClientes);

            return Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              color: appbarBg,
              child: Row(
                children: [
                  Expanded(
                    child: _buildCompactMetric(
                      'Recaudo Empresa',
                      formatRecaudo,
                      Icons.point_of_sale,
                      taxiAccent,
                      isDark,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: _buildCompactMetric(
                      'Servicios Clientes',
                      formatServicios,
                      Icons.local_taxi,
                      AppColors.secondary,
                      isDark,
                    ),
                  ),
                ],
              ),
            );
          }),

          // Buscador integrado fiel estilo WhatsApp (Cápsula/Píldora)
          Container(
            color: appbarBg,
            padding: const EdgeInsets.fromLTRB(14, 4, 14, 10),
            child: Container(
              height: 42,
              decoration: BoxDecoration(
                color: searchBg,
                borderRadius: BorderRadius.circular(24),
              ),
              child: TextField(
                controller: _searchController,
                style: TextStyle(
                  color: textPrimary,
                  fontSize: 14.5,
                ),
                decoration: InputDecoration(
                  hintText: _currentIndex == 0
                      ? 'Buscar recaudo por placa o conductor...'
                      : (_currentIndex == 1
                          ? 'Buscar turno por placa o conductor...'
                          : 'Buscar despacho por placa o destino...'),
                  hintStyle: TextStyle(
                    color: textSecondary,
                    fontSize: 13.5,
                  ),
                  prefixIcon: Icon(
                    Icons.search,
                    color: textSecondary,
                    size: 20,
                  ),
                  suffixIcon: _searchController.text.isNotEmpty
                      ? IconButton(
                          icon: Icon(Icons.close, color: textSecondary, size: 18),
                          onPressed: () {
                            _searchController.clear();
                            setState(() {});
                          },
                        )
                      : null,
                  border: InputBorder.none,
                  enabledBorder: InputBorder.none,
                  focusedBorder: InputBorder.none,
                  contentPadding: const EdgeInsets.symmetric(vertical: 10),
                ),
                onChanged: (_) => setState(() {}),
              ),
            ),
          ),

          // INMEDIATAMENTE LA LISTA FLUIDA EDGE-TO-EDGE (Sin botones ni filtros debajo)
          Expanded(
            child: IndexedStack(
              index: _currentIndex,
              children: [
                // Pestaña 0: Recaudos y Pagos
                PagoListView(
                  searchQuery: _searchController.text,
                  onNuevoRecaudoPressed: () => Get.to(() => const PaymentFormView()),
                ),
                // Pestaña 1: Fila reactiva de Turnos en espera
                TurnoListView(
                  searchQuery: _searchController.text,
                  onTurnoTap: _abrirFormularioDespacho,
                  onEnturnarPressed: _abrirDialogoEnturnar,
                ),
                // Pestaña 2: Historial de Despachos del día
                DespachoListView(
                  searchQuery: _searchController.text,
                ),
              ],
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        selectedItemColor: taxiAccent,
        unselectedItemColor: textSecondary,
        backgroundColor: appbarBg,
        elevation: 4,
        type: BottomNavigationBarType.fixed,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.point_of_sale),
            activeIcon: Icon(Icons.point_of_sale),
            label: 'Pagos',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.local_taxi),
            activeIcon: Icon(Icons.local_taxi),
            label: 'Turnos',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.departure_board),
            activeIcon: Icon(Icons.departure_board),
            label: 'Despachos',
          ),
        ],
      ),
      // FAB estilo Movilidad Taxi: Amarillo Taxi con Negro Puro (12.8:1 contraste)
      floatingActionButton: _currentIndex != 2
          ? FloatingActionButton.extended(
              backgroundColor: AppColors.taxiYellow,
              foregroundColor: AppColors.taxiBlackPure,
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              tooltip: _currentIndex == 0 ? 'Nuevo Recaudo' : 'Enturnar Vehículo',
              onPressed: _currentIndex == 0
                  ? () => Get.to(() => const PaymentFormView())
                  : _abrirDialogoEnturnar,
              icon: Icon(
                _currentIndex == 0 ? Icons.add_card : Icons.local_taxi,
                size: 22,
                color: AppColors.taxiBlackPure,
              ),
              label: Text(
                _currentIndex == 0 ? 'NUEVO PAGO' : 'PAGAR Y ENTURNAR',
                style: const TextStyle(fontWeight: FontWeight.w900, letterSpacing: 0.5, color: AppColors.taxiBlackPure),
              ),
            )
          : null,
    );
  }

  Widget _buildCompactMetric(
    String label,
    String value,
    IconData icon,
    Color color,
    bool isDark,
  ) {
    final cardBg = isDark ? AppColors.waDarkSearchField : AppColors.waLightSearchField;
    final textSecondary = isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary;
    final textPrimary = isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withValues(alpha: 0.25)),
      ),
      child: Row(
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(width: 6),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  label,
                  style: TextStyle(
                    color: textSecondary,
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 1),
                FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    value,
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w900,
                      color: textPrimary,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
