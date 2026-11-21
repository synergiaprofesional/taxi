import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/payment_model.dart';
import '../../widgets/pago_card_widget.dart';
import '../form/payment_form_view.dart';

class PagoListView extends StatelessWidget {
  final String searchQuery;
  final Function(PagoRecaudoModel)? onPagoTap;
  final VoidCallback? onNuevoRecaudoPressed;

  const PagoListView({
    super.key,
    this.searchQuery = '',
    this.onPagoTap,
    this.onNuevoRecaudoPressed,
  });

  @override
  Widget build(BuildContext context) {
    final controller = Get.find<TurnoController>();

    return Obx(() {
      if (controller.isLoading.value) {
        return const Center(child: CircularProgressIndicator(color: AppColors.primary));
      }

      if (controller.isSearchingRemotePagos.value) {
        return Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const CircularProgressIndicator(color: AppColors.primary),
              const SizedBox(height: 14),
              Text(
                'Buscando recaudos en el historial de Odoo...',
                style: TextStyle(fontSize: 15, color: Colors.grey.shade400, fontWeight: FontWeight.w500),
              ),
            ],
          ),
        );
      }

      final filteredList = controller.pagosFiltrados(searchQuery);

      if (filteredList.isEmpty) {
        final canSearchRemote = searchQuery.trim().length >= 3;
        final emptyMsg = searchQuery.trim().isEmpty
            ? 'No hay recaudos en ${controller.bahiaSeleccionada.value}'
            : 'No se encontraron recaudos en la sesión activa para "$searchQuery"';
        return Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.point_of_sale_outlined, size: 64, color: Colors.grey.shade600),
                const SizedBox(height: 12),
                Text(
                  emptyMsg,
                  style: TextStyle(fontSize: 16, color: Colors.grey.shade400, fontWeight: FontWeight.w600),
                  textAlign: TextAlign.center,
                ),
                if (canSearchRemote) ...[
                  const SizedBox(height: 16),
                  OutlinedButton.icon(
                    onPressed: () => controller.buscarPagosHistoricosRemotos(searchQuery),
                    icon: const Icon(Icons.cloud_sync_outlined, color: AppColors.primary),
                    label: const Text(
                      'Buscar en Historial General de Odoo',
                      style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold),
                    ),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: AppColors.primary, width: 1.5),
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ],
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  onPressed: onNuevoRecaudoPressed ?? () => Get.to(() => const PaymentFormView()),
                  icon: const Icon(Icons.add, color: Colors.black),
                  label: const Text('Nuevo Recaudo de Caja', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                ),
              ],
            ),
          ),
        );
      }

      final isDark = Theme.of(context).brightness == Brightness.dark;
      final dividerColor = isDark ? AppColors.waDarkDivider : AppColors.waLightDivider;

      return RefreshIndicator(
        color: isDark ? AppColors.waDarkActiveGreen : AppColors.waLightActiveGreen,
        onRefresh: () => controller.cargarPagosDesdeServidor(),
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
            final pago = filteredList[idx];
            return PagoCardWidget(
              pago: pago,
              onTap: () {
                if (onPagoTap != null) {
                  onPagoTap!(pago);
                } else {
                  Get.to(() => PaymentFormView(pago: pago));
                }
              },
            );
          },
        ),
      );
    });
  }
}
