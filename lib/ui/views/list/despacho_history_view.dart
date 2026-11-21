import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/turno_model.dart';
import 'despacho_list_view.dart';

class DespachoHistoryView extends StatefulWidget {
  const DespachoHistoryView({super.key});

  @override
  State<DespachoHistoryView> createState() => _DespachoHistoryViewState();
}

class _DespachoHistoryViewState extends State<DespachoHistoryView> {
  final controller = Get.find<TurnoController>();
  final TextEditingController _searchController = TextEditingController();
  String _searchQuery = '';

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor = isDark ? AppColors.waDarkBackground : AppColors.waLightBackground;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Historial de Despachos del Día',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            Obx(() {
              final count = controller.turnos
                  .where((t) => t.esDespacho || t.estado == EstadoTurno.despachado)
                  .length;
              return Text(
                '$count despachos registrados hoy',
                style: TextStyle(
                  fontSize: 12,
                  color: isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                  fontWeight: FontWeight.normal,
                ),
              );
            }),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refrescar (F5)',
            onPressed: () => controller.cargarTurnosDesdeServidor(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Cápsula integrada de búsqueda estilo WhatsApp / Telegram
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Container(
              height: 42,
              decoration: BoxDecoration(
                color: isDark ? AppColors.waDarkSearchField : AppColors.waLightSearchField,
                borderRadius: BorderRadius.circular(24.0),
              ),
              child: TextField(
                controller: _searchController,
                onChanged: (val) => setState(() => _searchQuery = val),
                style: TextStyle(
                  color: isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary,
                  fontSize: 14.0,
                ),
                decoration: InputDecoration(
                  hintText: 'Buscar por placa, conductor, destino o turno...',
                  hintStyle: TextStyle(
                    color: isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                    fontSize: 13.5,
                  ),
                  prefixIcon: Icon(
                    Icons.search,
                    size: 20,
                    color: isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                  ),
                  suffixIcon: _searchQuery.isNotEmpty
                      ? IconButton(
                          icon: const Icon(Icons.clear, size: 18),
                          color: isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary,
                          onPressed: () {
                            _searchController.clear();
                            setState(() => _searchQuery = '');
                          },
                        )
                      : null,
                  border: InputBorder.none,
                  contentPadding: const EdgeInsets.symmetric(vertical: 10.0),
                ),
              ),
            ),
          ),
          // Lista de despachos continua Edge-to-Edge
          Expanded(
            child: DespachoListView(
              searchQuery: _searchQuery,
            ),
          ),
        ],
      ),
    );
  }
}
