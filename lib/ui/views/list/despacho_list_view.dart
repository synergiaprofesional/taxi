import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/turno_model.dart';
import '../../widgets/ticket_preview_dialog.dart';
import '../../widgets/despacho_card_widget.dart';

class DespachoListView extends StatelessWidget {
  final String searchQuery;
  final Function(TurnoModel)? onDespachoTap;

  const DespachoListView({
    super.key,
    this.searchQuery = '',
    this.onDespachoTap,
  });

  @override
  Widget build(BuildContext context) {
    final controller = Get.find<TurnoController>();

    return Obx(() {
      if (controller.isLoading.value) {
        return const Center(child: CircularProgressIndicator(color: AppColors.primary));
      }

      final filteredList = controller.turnosDespachadosFiltrados(searchQuery);

      if (filteredList.isEmpty) {
        final emptyMsg = searchQuery.trim().isEmpty
            ? 'No hay despachos en ${controller.bahiaSeleccionada.value}'
            : 'No se encontraron despachos para "$searchQuery"';
        return Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.departure_board_outlined, size: 64, color: Colors.grey.shade600),
              const SizedBox(height: 12),
              Text(
                emptyMsg,
                style: TextStyle(fontSize: 16, color: Colors.grey.shade400, fontWeight: FontWeight.w600),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 6),
              Text(
                'Los turnos despachados con tarifa aparecerán aquí.',
                style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
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
            return DespachoCardWidget(
              turno: turno,
              onTap: () {
                if (onDespachoTap != null) {
                  onDespachoTap!(turno);
                } else {
                  // Acción por defecto: diálogo de reimpresión de tiquete térmico
                  TicketPreviewDialog.show(
                    context,
                    consecutivo: turno.name,
                    placa: turno.placaVisible,
                    conductor: turno.conductorNombre,
                    bahia: turno.bahiaNombre,
                    destino: turno.tarifaNombre,
                    direccion: turno.nota,
                    turnoId: turno.id,
                    total: turno.valorTotal,
                    fecha: turno.fechaCreacion,
                    printerService: controller.printerService,
                  );
                }
              },
            );
          },
        ),
      );
    });
  }
}
