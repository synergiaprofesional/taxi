import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/turno_model.dart';
import '../../widgets/turno_card_widget.dart';

class TurnoListView extends StatelessWidget {
  final String searchQuery;
  final Function(TurnoModel)? onTurnoTap;
  final VoidCallback? onEnturnarPressed;

  const TurnoListView({
    super.key,
    this.searchQuery = '',
    this.onTurnoTap,
    this.onEnturnarPressed,
  });

  @override
  Widget build(BuildContext context) {
    final controller = Get.find<TurnoController>();

    return Obx(() {
      if (controller.isLoading.value) {
        return const Center(child: CircularProgressIndicator(color: AppColors.primary));
      }

      final filteredList = controller.turnosEnColaFiltrados(searchQuery);

      if (filteredList.isEmpty) {
        final emptyMsg = searchQuery.trim().isEmpty
            ? 'No hay turnos en ${controller.bahiaSeleccionada.value}'
            : 'No se encontraron turnos para "$searchQuery"';
        return Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.local_taxi_outlined, size: 64, color: Colors.grey.shade600),
              const SizedBox(height: 12),
              Text(
                emptyMsg,
                style: TextStyle(fontSize: 16, color: Colors.grey.shade400, fontWeight: FontWeight.w600),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              if (onEnturnarPressed != null)
                ElevatedButton.icon(
                  onPressed: onEnturnarPressed,
                  icon: const Icon(Icons.add, color: Colors.black),
                  label: const Text('Enturnar Vehículo', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                ),
            ],
          ),
        );
      }

      final isDark = Theme.of(context).brightness == Brightness.dark;
      final dividerColor = isDark ? AppColors.waDarkDivider : AppColors.waLightDivider;

      return RefreshIndicator(
        color: isDark ? AppColors.waDarkActiveGreen : AppColors.waLightActiveGreen,
        onRefresh: () => controller.cargarTurnosDesdeServidor(),
        child: ListView.separated(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: EdgeInsets.zero,
          itemCount: filteredList.length,
          separatorBuilder: (ctx, idx) => Divider(
            height: 1,
            thickness: 0.8,
            indent: 74,
            endIndent: 0,
            color: dividerColor,
          ),
          itemBuilder: (ctx, idx) {
            final turno = filteredList[idx];
            return TurnoCardWidget(
              turno: turno,
              onTap: () {
                if (onTurnoTap != null) {
                  onTurnoTap!(turno);
                }
              },
            );
          },
        ),
      );
    });
  }
}
