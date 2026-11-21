import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:taxi/core/theme/app_colors.dart';
import 'package:taxi/controllers/turno_controller.dart';
import 'package:taxi/models/bay_model.dart';
import 'package:taxi/models/turno_model.dart';
import 'package:taxi/ui/views/auth/login_dialog.dart';
import 'package:taxi/ui/views/bahia/bahia_selector_dialog.dart';
import 'package:taxi/ui/views/main/bahia_selected_view.dart';
import 'package:taxi/ui/views/pago/pago_dialog.dart';
import 'package:taxi/ui/views/settings/settings_view.dart';
import 'package:taxi/ui/views/list/despacho_history_view.dart';
import 'package:taxi/ui/widgets/ticket_preview_dialog.dart';
import 'package:taxi/ui/widgets/turno_card_widget.dart';

enum DeviceType { mobile, tablet, desktop }

class HomeView extends StatefulWidget {
  final bool autoConnectSockets;
  const HomeView({super.key, this.autoConnectSockets = true});

  @override
  State<HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  final TextEditingController _searchController = TextEditingController();
  final RxString _searchQuery = ''.obs;

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  DeviceType _getDeviceType(double width) {
    if (width < 650) return DeviceType.mobile;
    if (width < 1050) return DeviceType.tablet;
    return DeviceType.desktop;
  }

  @override
  Widget build(BuildContext context) {
    final controller = Get.put(TurnoController(autoConnectSockets: widget.autoConnectSockets));
    final screenWidth = MediaQuery.of(context).size.width;
    final deviceType = _getDeviceType(screenWidth);

    if (deviceType == DeviceType.mobile) {
      return const BahiaSelectedView(initialTabIndex: 1);
    }

    return CallbackShortcuts(
      bindings: {
        const SingleActivator(LogicalKeyboardKey.f1): () => controller.despacharTurnoActual(),
        const SingleActivator(LogicalKeyboardKey.f2): () => _mostrarDialogoPagarYEnturnar(context, controller),
        const SingleActivator(LogicalKeyboardKey.f5): () => controller.cargarTurnosDesdeServidor(),
        const SingleActivator(LogicalKeyboardKey.f12): () => Get.to(() => const SettingsView()),
      },
      child: Focus(
        autofocus: true,
        child: Scaffold(
          appBar: AppBar(
            title: FittedBox(
              fit: BoxFit.scaleDown,
              alignment: Alignment.centerLeft,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(6),
                    child: Image.asset(
                      'assets/img/logo.jpg',
                      width: 28,
                      height: 28,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) =>
                          const Icon(Icons.local_taxi, color: AppColors.primary, size: 24),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: const Text(
                      'SYNERGIA MÓVIL',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.w900,
                        fontSize: 13,
                        letterSpacing: 0.8,
                      ),
                    ),
                  ),
                  if (deviceType == DeviceType.desktop) ...[
                    const SizedBox(width: 12),
                    Obx(() => Text(
                          controller.bahiaSeleccionada.value,
                          style: const TextStyle(fontSize: 13, color: AppColors.textSecondary),
                        )),
                  ],
                ],
              ),
            ),
            actions: [
              if (deviceType == DeviceType.desktop) ...[
                Obx(() => _buildStatusChip(
                      label: 'Odoo 11',
                      isOk: controller.odooService.isOnline.value,
                      okText: 'Online',
                      failText: 'Offline',
                    )),
                const SizedBox(width: 6),
                Obx(() => _buildStatusChip(
                      label: 'Sockets',
                      isOk: controller.socketService.isConnected.value,
                      okText: 'En Vivo',
                      failText: 'Reconectando',
                    )),
                const SizedBox(width: 6),
              ],
              Obx(() {
                final isAuth = controller.odooService.isAuthenticated.value;
                final user = controller.odooService.usuarioActivo.value;
                if (isAuth) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 4),
                    child: ActionChip(
                      avatar: const CircleAvatar(
                        radius: 6,
                        backgroundColor: AppColors.success,
                      ),
                      label: Text(
                        deviceType == DeviceType.mobile ? user.split('@').first : user,
                        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                      ),
                      onPressed: () => _mostrarMenuUsuario(context, controller),
                    ),
                  );
                } else {
                  return IconButton(
                    icon: const Icon(Icons.login, color: AppColors.accent),
                    tooltip: 'Iniciar Sesión',
                    onPressed: () => LoginDialog.show(context),
                  );
                }
              }),
              IconButton(
                icon: const Icon(Icons.swap_horiz, color: AppColors.secondary),
                tooltip: 'Cambiar Bahía',
                onPressed: () => _mostrarDialogoCambiarBahia(context, controller),
              ),
              if (deviceType == DeviceType.mobile)
                PopupMenuButton<String>(
                  icon: const Icon(Icons.more_vert),
                  onSelected: (val) {
                    if (val == 'tabs') Get.to(() => const BahiaSelectedView());
                    if (val == 'despachos') Get.to(() => const DespachoHistoryView());
                    if (val == 'recaudo') _mostrarDialogoRecaudo(context, controller);
                    if (val == 'reimprimir') _reimprimirTicket(context, controller);
                    if (val == 'settings') Get.to(() => const SettingsView());
                    if (val == 'refresh') controller.cargarTurnosDesdeServidor();
                    if (val == 'logout') _mostrarConfirmacionCerrarSesion(context, controller);
                  },
                  itemBuilder: (ctx) => [
                    const PopupMenuItem(
                      value: 'tabs',
                      child: Row(
                        children: [
                          Icon(Icons.tab, color: AppColors.primary, size: 20),
                          SizedBox(width: 10),
                          Text('Vista 3 Pestañas (Fundetaxcol)'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'despachos',
                      child: Row(
                        children: [
                          Icon(Icons.departure_board, color: AppColors.secondary, size: 20),
                          SizedBox(width: 10),
                          Text('Historial de Despachos'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'recaudo',
                      child: Row(
                        children: [
                          Icon(Icons.point_of_sale, color: AppColors.primary, size: 20),
                          SizedBox(width: 10),
                          Text('Nuevo Recaudo'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'reimprimir',
                      child: Row(
                        children: [
                          Icon(Icons.receipt_long, color: AppColors.textPrimary, size: 20),
                          SizedBox(width: 10),
                          Text('Reimprimir Tiquete'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'refresh',
                      child: Row(
                        children: [
                          Icon(Icons.refresh, color: AppColors.secondary, size: 20),
                          SizedBox(width: 10),
                          Text('Refrescar'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'settings',
                      child: Row(
                        children: [
                          Icon(Icons.settings_outlined, color: AppColors.textPrimary, size: 20),
                          SizedBox(width: 10),
                          Text('Configuración'),
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
                )
              else ...[
                IconButton(
                  icon: const Icon(Icons.tab, color: AppColors.primary),
                  tooltip: 'Vista 3 Pestañas (Fundetaxcol)',
                  onPressed: () => Get.to(() => const BahiaSelectedView()),
                ),
                IconButton(
                  icon: const Icon(Icons.departure_board, color: AppColors.secondary),
                  tooltip: 'Historial de Despachos del Día',
                  onPressed: () => Get.to(() => const DespachoHistoryView()),
                ),
                IconButton(
                  icon: const Icon(Icons.point_of_sale, color: AppColors.primary),
                  tooltip: 'Nuevo Recaudo de Caja',
                  onPressed: () => _mostrarDialogoRecaudo(context, controller),
                ),
                IconButton(
                  icon: const Icon(Icons.receipt_long, color: AppColors.textPrimary),
                  tooltip: 'Reimprimir Último Tiquete',
                  onPressed: () => _reimprimirTicket(context, controller),
                ),
                IconButton(
                  icon: const Icon(Icons.settings_outlined, color: AppColors.textPrimary),
                  tooltip: 'Configuración (F12)',
                  onPressed: () => Get.to(() => const SettingsView()),
                ),
                IconButton(
                  icon: const Icon(Icons.refresh, color: AppColors.secondary),
                  tooltip: 'Refrescar (F5)',
                  onPressed: () => controller.cargarTurnosDesdeServidor(),
                ),
                IconButton(
                  icon: const Icon(Icons.logout, color: AppColors.error),
                  tooltip: 'Cerrar Sesión / Salir',
                  onPressed: () => _mostrarConfirmacionCerrarSesion(context, controller),
                ),
              ],
              const SizedBox(width: 6),
            ],
          ),
          body: LayoutBuilder(
            builder: (context, constraints) {
              final currentType = _getDeviceType(constraints.maxWidth);
              switch (currentType) {
                case DeviceType.desktop:
                  return _buildDesktopLayout(context, controller);
                case DeviceType.tablet:
                  return _buildTabletLayout(context, controller);
                case DeviceType.mobile:
                  return _buildMobileLayout(context, controller);
              }
            },
          ),
          floatingActionButton: deviceType == DeviceType.mobile
              ? FloatingActionButton.extended(
                  onPressed: () => _mostrarDialogoPagarYEnturnar(context, controller),
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.black,
                  icon: const Icon(Icons.flash_on),
                  label: const Text('PAGAR Y ENTURNAR', style: TextStyle(fontWeight: FontWeight.bold)),
                )
              : null,
        ),
      ),
    );
  }

  Widget _buildStatusChip({
    required String label,
    required bool isOk,
    required String okText,
    required String failText,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: AppColors.surfaceElevated,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: isOk ? AppColors.success.withValues(alpha: 0.5) : AppColors.error.withValues(alpha: 0.5),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.circle, size: 8, color: isOk ? AppColors.success : AppColors.error),
          const SizedBox(width: 5),
          Text(
            '$label: ${isOk ? okText : failText}',
            style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }

  // =========================================================================
  // 1. DISPOSITIVO: PC DE ESCRITORIO / CABINA WINDOWS (> 1050px)
  // Layout de 3 columnas: Control Izquierdo, Cola Central, Métricas Derecha
  // =========================================================================
  Widget _buildDesktopLayout(BuildContext context, TurnoController controller) {
    return Row(
      children: [
        // Panel Izquierdo: Operación y Atajos (280px)
        Container(
          width: 280,
          color: AppColors.surface,
          padding: const EdgeInsets.all(16),
          child: SingleChildScrollView(
            physics: const BouncingScrollPhysics(),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'CONTROL DE BAHÍA',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.2, color: AppColors.primary),
                ),
                const SizedBox(height: 12),
                Obx(() => Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: AppColors.surfaceElevated,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: AppColors.primary.withValues(alpha: 0.3)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('Bahía Activa:', style: TextStyle(color: AppColors.textSecondary, fontSize: 11)),
                          const SizedBox(height: 4),
                          Text(controller.bahiaSeleccionada.value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
                        ],
                      ),
                    )),
                const SizedBox(height: 20),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.black,
                    minimumSize: const Size.fromHeight(48),
                    textStyle: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  icon: const Icon(Icons.add_shopping_cart),
                  label: const Text('PAGAR Y ENTURNAR (F2)'),
                  onPressed: () => _mostrarDialogoPagarYEnturnar(context, controller),
                ),
                const SizedBox(height: 10),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.turnActual,
                    foregroundColor: Colors.black,
                    minimumSize: const Size.fromHeight(48),
                    textStyle: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  icon: const Icon(Icons.send_rounded),
                  label: const Text('DESPACHAR ACTUAL (F1)'),
                  onPressed: () => controller.despacharTurnoActual(),
                ),
                const SizedBox(height: 20),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(color: AppColors.surfaceElevated, borderRadius: BorderRadius.circular(8)),
                  child: const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Atajos de Teclado:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
                      SizedBox(height: 6),
                      Text('• F1: Despachar Actual', style: TextStyle(fontSize: 11, color: AppColors.textSecondary)),
                      Text('• F2: Cobrar y Enturnar', style: TextStyle(fontSize: 11, color: AppColors.textSecondary)),
                      Text('• F5: Refrescar Cola', style: TextStyle(fontSize: 11, color: AppColors.textSecondary)),
                      Text('• F12: Configuración', style: TextStyle(fontSize: 11, color: AppColors.textSecondary)),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        // Panel Central: Cola de Turnos en Vivo (WhatsApp Edge-to-Edge Style)
        Expanded(
          flex: 5,
          child: Container(
            color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkBackground : AppColors.waLightBackground,
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        'COLA DE TURNOS EN BAHÍA',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Obx(() => Text(
                          '${controller.turnosEnCola.length} Vehículos en cola',
                          style: TextStyle(
                            color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                            fontWeight: FontWeight.w600,
                          ),
                        )),
                  ],
                ),
                const SizedBox(height: 12),

                // Buscador en Cápsula WhatsApp fija (Sin botones debajo)
                Container(
                  height: 42,
                  decoration: BoxDecoration(
                    color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkSearchField : AppColors.waLightSearchField,
                    borderRadius: BorderRadius.circular(24),
                  ),
                  child: TextField(
                    controller: _searchController,
                    style: TextStyle(
                      color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary,
                      fontSize: 14.5,
                    ),
                    decoration: InputDecoration(
                      hintText: 'Buscar en cola por placa o conductor...',
                      hintStyle: TextStyle(
                        color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                        fontSize: 13.5,
                      ),
                      prefixIcon: Icon(
                        Icons.search,
                        color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                        size: 20,
                      ),
                      suffixIcon: Obx(() => _searchQuery.value.isNotEmpty
                          ? IconButton(
                              icon: Icon(
                                Icons.close,
                                color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                                size: 18,
                              ),
                              onPressed: () {
                                _searchController.clear();
                                _searchQuery.value = '';
                              },
                            )
                          : const SizedBox.shrink()),
                      border: InputBorder.none,
                      contentPadding: const EdgeInsets.symmetric(vertical: 10),
                    ),
                    onChanged: (val) => _searchQuery.value = val.trim(),
                  ),
                ),
                const SizedBox(height: 12),

                // Lista Continua WhatsApp Edge-to-Edge
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkSurface : AppColors.waLightSurface,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkDivider : AppColors.waLightDivider,
                        width: 0.8,
                      ),
                    ),
                    clipBehavior: Clip.antiAlias,
                    child: Obx(() {
                      if (controller.isLoading.value) return const Center(child: CircularProgressIndicator());

                      final q = _searchQuery.value.toUpperCase();
                      final filteredTurnos = q.isEmpty
                          ? controller.turnosEnCola
                          : controller.turnosEnCola.where((t) =>
                              t.placaVisible.toUpperCase().contains(q) ||
                              t.conductorNombre.toUpperCase().contains(q)).toList();

                      if (filteredTurnos.isEmpty) {
                        return Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.local_taxi_outlined, size: 48, color: Colors.grey.shade600),
                              const SizedBox(height: 12),
                              Text(
                                controller.turnosEnCola.isEmpty
                                    ? 'No hay vehículos en espera en ${controller.bahiaSeleccionada.value}'
                                    : 'No se encontraron resultados para "$q"',
                                style: TextStyle(
                                  color: Theme.of(context).brightness == Brightness.dark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ],
                          ),
                        );
                      }

                      final isDark = Theme.of(context).brightness == Brightness.dark;
                      return ListView.separated(
                        itemCount: filteredTurnos.length,
                        separatorBuilder: (context, index) => Divider(
                          height: 1,
                          thickness: 0.8,
                          indent: 74,
                          endIndent: 0,
                          color: isDark ? AppColors.waDarkDivider : AppColors.waLightDivider,
                        ),
                        itemBuilder: (context, index) => TurnoCardWidget(
                          turno: filteredTurnos[index],
                          onTap: () {},
                        ),
                      );
                    }),
                  ),
                ),
              ],
            ),
          ),
        ),

        // Panel Derecho: Turno en Atención & Métricas (310px)
        Container(
          width: 310,
          color: AppColors.surface,
          padding: const EdgeInsets.all(16),
          child: SingleChildScrollView(
            physics: const BouncingScrollPhysics(),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('TURNO EN ATENCIÓN', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.2, color: AppColors.turnActual)),
                const SizedBox(height: 12),
                _buildTurnoAtencionWidget(controller),
                const SizedBox(height: 24),
                const Text('OPERACIÓN DE BAHÍA', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.2, color: AppColors.textSecondary)),
                const SizedBox(height: 12),
                Obx(() {
                  final despachados = controller.turnosDespachados.length;
                  final enEspera = controller.turnosEnCola.length;

                  return Column(
                    children: [
                      _buildMetricTile('En Fila', '$enEspera veh.', Icons.timer_outlined, AppColors.primary),
                      const SizedBox(height: 8),
                      _buildMetricTile('Despachados Hoy', '$despachados veh.', Icons.check_circle_outline, AppColors.success),
                    ],
                  );
                }),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // =========================================================================
  // 2. DISPOSITIVO: TABLET / POS TÁCTIL (650px - 1050px)
  // Layout de 2 columnas táctil: Columna de Despacho Rápido y Cola Central
  // =========================================================================
  Widget _buildTabletLayout(BuildContext context, TurnoController controller) {
    return Row(
      children: [
        // Panel Táctil Izquierdo (300px)
        Container(
          width: 300,
          color: AppColors.surface,
          padding: const EdgeInsets.all(16),
          child: SingleChildScrollView(
            physics: const BouncingScrollPhysics(),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'TERMINAL TÁCTIL POS',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.1, color: AppColors.primary),
                ),
                const SizedBox(height: 12),
                _buildTurnoAtencionWidget(controller),
                const SizedBox(height: 16),
                // Botón táctil grande de Cobro
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.black,
                    minimumSize: const Size.fromHeight(56),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    textStyle: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15),
                  ),
                  icon: const Icon(Icons.flash_on, size: 24),
                  label: const Text('PAGAR Y ENTURNAR'),
                  onPressed: () => _mostrarDialogoPagarYEnturnar(context, controller),
                ),
                const SizedBox(height: 12),
                // Botón táctil grande de Despacho
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.turnActual,
                    foregroundColor: Colors.black,
                    minimumSize: const Size.fromHeight(56),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    textStyle: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15),
                  ),
                  icon: const Icon(Icons.send_rounded, size: 24),
                  label: const Text('DESPACHAR SALIDA'),
                  onPressed: () => controller.despacharTurnoActual(),
                ),
                const SizedBox(height: 16),
                Obx(() {
                  final enEspera = controller.turnosEnCola.length;
                  final despachados = controller.turnosDespachados.length;
                  return Column(
                    children: [
                      _buildMetricTile('Vehículos en Fila', '$enEspera', Icons.timer_outlined, AppColors.primary),
                      const SizedBox(height: 8),
                      _buildMetricTile('Despachados', '$despachados', Icons.check_circle_outline, AppColors.success),
                    ],
                  );
                }),
              ],
            ),
          ),
        ),

        // Panel Derecho: Cola de Turnos Táctil
        Expanded(
          child: Container(
            color: AppColors.background,
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('COLA DE SALIDA', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                Expanded(
                  child: Obx(() {
                    if (controller.isLoading.value) return const Center(child: CircularProgressIndicator());
                    if (controller.turnosEnCola.isEmpty) {
                      return Center(
                        child: Text(
                          'No hay vehículos en espera en ${controller.bahiaSeleccionada.value}',
                          style: TextStyle(color: Colors.grey.shade400, fontSize: 14),
                        ),
                      );
                    }
                    return ListView.separated(
                      itemCount: controller.turnosEnCola.length,
                      separatorBuilder: (context, index) => const SizedBox(height: 8),
                      itemBuilder: (context, index) => _buildTurnoCard(controller.turnosEnCola[index]),
                    );
                  }),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // =========================================================================
  // 3. DISPOSITIVO: MÓVIL SMARTPHONE (< 650px)
  // Layout Vertical Ágil con navegación táctil compacta
  // =========================================================================
  Widget _buildMobileLayout(BuildContext context, TurnoController controller) {
    return Obx(() {
      if (controller.isLoading.value) return const Center(child: CircularProgressIndicator());
      return RefreshIndicator(
        onRefresh: () async => controller.cargarTurnosDesdeServidor(),
        child: ListView(
          padding: const EdgeInsets.all(12),
          children: [
            // Resumen Móvil Superior
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(color: AppColors.surfaceElevated, borderRadius: BorderRadius.circular(8)),
                    child: Text(
                      controller.bahiaSeleccionada.value,
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.turnActual,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  ),
                  icon: const Icon(Icons.send, size: 16),
                  label: const Text('Despachar', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                  onPressed: () => controller.despacharTurnoActual(),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: _buildMetricTile(
                    'En Fila',
                    '${controller.turnosEnCola.length} veh.',
                    Icons.timer_outlined,
                    AppColors.primary,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _buildMetricTile(
                    'Despachos Realizados',
                    '${controller.turnosDespachados.length}',
                    Icons.check_circle_outline,
                    AppColors.success,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (controller.turnosEnCola.isEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 40),
                child: Center(
                  child: Column(
                    children: [
                      Icon(Icons.local_taxi_outlined, size: 48, color: Colors.grey.shade600),
                      const SizedBox(height: 12),
                      Text(
                        'No hay vehículos en espera en ${controller.bahiaSeleccionada.value}',
                        style: TextStyle(color: Colors.grey.shade400, fontSize: 14),
                      ),
                    ],
                  ),
                ),
              )
            else
              ...controller.turnosEnCola.map((turno) => Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: _buildTurnoCard(turno),
                  )),
            const SizedBox(height: 80), // Espacio para el FAB
          ],
        ),
      );
    });
  }

  Widget _buildTurnoAtencionWidget(TurnoController controller) {
    return Obx(() {
      final actual = controller.turnoEnAtencion;
      if (actual == null) {
        return Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.surfaceElevated,
            borderRadius: BorderRadius.circular(10),
          ),
          child: const Center(
            child: Text('Sin vehículo en atención activa', style: TextStyle(color: AppColors.textSecondary, fontSize: 12)),
          ),
        );
      }
      return Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: AppColors.surfaceElevated,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: AppColors.turnActual, width: 2),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Flexible(
                  child: Text(
                    actual.name,
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: AppColors.turnActual),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(color: AppColors.primary, borderRadius: BorderRadius.circular(4)),
                  child: Text(actual.vehiculoPlaca, style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Text('Conductor: ${actual.conductorNombre}', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13), overflow: TextOverflow.ellipsis),
            Text('Hora Ingreso: ${DateFormat('HH:mm:ss').format(actual.fechaCreacion)}', style: const TextStyle(color: AppColors.textSecondary, fontSize: 11)),
            const Divider(height: 18),
            Text(
              'Recaudo: ${NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0).format(actual.valorTotal)}',
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      );
    });
  }

  Widget _buildTurnoCard(TurnoModel turno) {
    return TurnoCardWidget(
      turno: turno,
      onTap: () {},
    );
  }


  Widget _buildMetricTile(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.surfaceElevated,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: AppColors.textSecondary, fontSize: 11), overflow: TextOverflow.ellipsis),
                const SizedBox(height: 4),
                Text(value, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ],
            ),
          ),
          Icon(icon, color: color, size: 22),
        ],
      ),
    );
  }

  void _mostrarDialogoPagarYEnturnar(BuildContext context, TurnoController controller) {
    final placaCtrl = TextEditingController();
    final conductorCtrl = TextEditingController();
    final valorCtrl = TextEditingController(text: '15000');

    Get.defaultDialog(
      title: 'Pagar y Enturnar',
      titleStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
      backgroundColor: AppColors.surface,
      contentPadding: const EdgeInsets.all(16),
      content: Column(
        children: [
          TextField(controller: placaCtrl, decoration: const InputDecoration(labelText: 'Placa del Vehículo', hintText: 'Ej: WBD-512')),
          const SizedBox(height: 10),
          TextField(controller: conductorCtrl, decoration: const InputDecoration(labelText: 'Nombre del Conductor', hintText: 'Ej: Carlos Ramírez')),
          const SizedBox(height: 10),
          TextField(controller: valorCtrl, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Valor Recaudo (\$)', prefixText: '\$ ')),
        ],
      ),
      textConfirm: 'COBRAR, ENTURNAR E IMPRIMIR',
      confirmTextColor: Colors.black,
      buttonColor: AppColors.primary,
      onConfirm: () async {
        if (placaCtrl.text.isNotEmpty) {
          final valor = double.tryParse(valorCtrl.text) ?? 0.0;
          final ticket = await controller.pagarYEnturnar(
            placaCtrl.text,
            conductorCtrl.text.isEmpty ? 'Conductor General' : conductorCtrl.text,
            valor,
          );
          Get.back();
          // Muestra el preview del tiquete térmico inmediatamente
          Get.dialog(
            TicketPreviewDialog(
              ticket: ticket,
              printerService: controller.printerService,
            ),
          );
        }
      },
    );
  }

  void _mostrarDialogoRecaudo(BuildContext context, TurnoController controller) async {
    final nuevoPago = await showDialog(
      context: context,
      builder: (ctx) => PagoDialog(
        bahiaId: controller.bahiaIdActual.value,
        bahiaNombre: controller.bahiaSeleccionada.value,
      ),
    );
    if (nuevoPago != null) {
      controller.cargarTurnosDesdeServidor();
    }
  }

  void _mostrarDialogoCambiarBahia(BuildContext context, TurnoController controller) async {
    final nuevaBahia = await showDialog<BahiaModel>(
      context: context,
      builder: (ctx) => BahiaSelectorDialog(bahiaActualId: controller.bahiaIdActual.value),
    );
    if (nuevaBahia != null) {
      controller.cambiarBahia(nuevaBahia);
    }
  }

  void _reimprimirTicket(BuildContext context, TurnoController controller) {
    if (controller.ultimoTicketImpreso.value != null) {
      Get.dialog(
        TicketPreviewDialog(
          ticket: controller.ultimoTicketImpreso.value!,
          printerService: controller.printerService,
        ),
      );
    } else {
      Get.snackbar(
        'Sin Tiquetes',
        'No hay tiquetes registrados en la sesión actual.',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: AppColors.surfaceElevated,
        colorText: Colors.white,
      );
    }
  }

  void _mostrarMenuUsuario(BuildContext context, TurnoController controller) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              ListTile(
                leading: const CircleAvatar(
                  backgroundColor: AppColors.primary,
                  child: Icon(Icons.person, color: Colors.black),
                ),
                title: Text(
                  controller.odooService.usuarioActivo.value,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: const Text('Operador autenticado en Central PídemeAquí'),
              ),
              const Divider(),
              ListTile(
                leading: const Icon(Icons.switch_account, color: AppColors.secondary),
                title: const Text('Cambiar de Usuario / Bahía'),
                onTap: () {
                  Navigator.pop(ctx);
                  LoginDialog.show(context);
                },
              ),
              ListTile(
                leading: const Icon(Icons.logout, color: AppColors.error),
                title: const Text('Cerrar Sesión'),
                onTap: () async {
                  Navigator.pop(ctx);
                  _mostrarConfirmacionCerrarSesion(context, controller);
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _mostrarConfirmacionCerrarSesion(BuildContext context, TurnoController controller) {
    Get.defaultDialog(
      title: 'Cerrar Sesión',
      titleStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
      backgroundColor: AppColors.surface,
      contentPadding: const EdgeInsets.all(20),
      middleText: '¿Estás seguro de que deseas cerrar sesión y bloquear esta terminal de bahía?',
      middleTextStyle: const TextStyle(color: AppColors.textPrimary, fontSize: 14),
      textConfirm: 'SALIR',
      textCancel: 'CANCELAR',
      confirmTextColor: Colors.white,
      buttonColor: AppColors.error,
      onConfirm: () async {
        Get.back();
        await controller.odooService.cerrarSesion();
      },
    );
  }
}

