import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../core/theme/app_colors.dart';
import '../../models/ticket_data_model.dart';
import '../../services/printer_service.dart';

class TicketPreviewDialog extends StatelessWidget {
  final TicketDataModel ticket;
  final PrinterService printerService;

  const TicketPreviewDialog({
    super.key,
    required this.ticket,
    required this.printerService,
  });

  static Future<void> show(
    BuildContext context, {
    required String consecutivo,
    required String placa,
    required String conductor,
    required String bahia,
    String destino = '',
    String direccion = '',
    int turnoId = 0,
    required double total,
    required DateTime fecha,
    required PrinterService printerService,
    String cajero = 'Operador',
  }) {
    final ticket = TicketDataModel(
      bahiaNombre: bahia,
      turnoNumero: consecutivo,
      placa: placa,
      conductor: conductor,
      destino: destino,
      direccion: direccion,
      turnoId: turnoId,
      fechaHora: fecha,
      valorTotal: total,
      cajero: cajero,
    );
    return showDialog(
      context: context,
      builder: (ctx) => TicketPreviewDialog(
        ticket: ticket,
        printerService: printerService,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final ticketText = printerService.generarTextoTiquete(ticket);

    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
      child: Container(
        width: 360,
        decoration: BoxDecoration(
          color: const Color(0xFF1E2124),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.primary.withValues(alpha: 0.5), width: 1.5),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.8),
              blurRadius: 20,
              offset: const Offset(0, 10),
            ),
          ],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Cabecera del diálogo
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: const BoxDecoration(
                color: Color(0xFF14171A),
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(11),
                  topRight: Radius.circular(11),
                ),
              ),
              child: Row(
                children: [
                  const Icon(Icons.receipt_long, color: AppColors.primary, size: 20),
                  const SizedBox(width: 8),
                  const Text(
                    'VISOR DE TIQUETE TÉRMICO',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 0.5,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white70, size: 18),
                    onPressed: () => Get.back(),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
                ],
              ),
            ),

            // Papel Térmico Virtual (Monoespaciado blanco sobre fondo crema/recibo)
            Container(
              margin: const EdgeInsets.all(16),
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFFF9F9F4),
                borderRadius: BorderRadius.circular(6),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black26,
                    blurRadius: 6,
                    offset: Offset(0, 3),
                  ),
                ],
              ),
              child: SingleChildScrollView(
                child: Text(
                  ticketText,
                  style: const TextStyle(
                    fontFamily: 'Courier',
                    fontSize: 11,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF111111),
                    height: 1.35,
                  ),
                ),
              ),
            ),

            // Botones de acción
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: Colors.white70,
                        side: const BorderSide(color: Colors.white24),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                      onPressed: () => Get.back(),
                      child: const Text('Cerrar'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        textStyle: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      icon: const Icon(Icons.print, size: 18),
                      label: const Text('Imprimir'),
                      onPressed: () async {
                        final ok = await printerService.imprimirTicket(ticket);
                        Get.back();
                        Get.snackbar(
                          ok ? 'Impresión Enviada' : 'Error de Impresión',
                          ok
                              ? 'Tiquete enviado a ${printerService.config.nombreODireccion}'
                              : 'No fue posible conectar con el dispositivo de impresión.',
                          backgroundColor:
                              ok ? AppColors.success : AppColors.error,
                          colorText: Colors.white,
                          snackPosition: SnackPosition.BOTTOM,
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
