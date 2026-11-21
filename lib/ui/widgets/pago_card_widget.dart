import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_colors.dart';
import '../../models/payment_model.dart';

class PagoCardWidget extends StatelessWidget {
  final PagoRecaudoModel pago;
  final VoidCallback? onTap;

  const PagoCardWidget({
    super.key,
    required this.pago,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final currencyFormat = NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0);
    final timeFormat = DateFormat('hh:mm a');
    final horaTexto = timeFormat.format(pago.fecha);

    final textPrimary = isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary;
    final textSecondary = isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary;
    final avatarBg = isDark ? AppColors.waDarkSearchField : const Color(0xFFE2E8F0);

    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Avatar circular estilo WhatsApp con ícono de recibo / pago
            CircleAvatar(
              radius: 24,
              backgroundColor: avatarBg,
              child: Icon(
                Icons.receipt_long,
                color: isDark ? AppColors.taxiYellowLight : AppColors.taxiYellowDark,
                size: 24,
              ),
            ),
            const SizedBox(width: 12),

            // Columna Central Expandida (3 Filas)
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // [Fila 1]: Placa + Consecutivo/Tiquete + Hora + Valor del Pago al final
                  Row(
                    children: [
                      if (pago.placa.isNotEmpty) ...[
                        Text(
                          pago.placa,
                          style: TextStyle(
                            fontSize: 15.5,
                            fontWeight: FontWeight.w700,
                            letterSpacing: 0.3,
                            color: textPrimary,
                          ),
                        ),
                        const SizedBox(width: 6),
                      ],
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: isDark ? Colors.white10 : Colors.black12,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          pago.consecutivo,
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: textSecondary,
                          ),
                        ),
                      ),
                      const SizedBox(width: 6),
                      Text(
                        horaTexto,
                        style: TextStyle(
                          fontSize: 12,
                          color: textSecondary,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        currencyFormat.format(pago.total),
                        style: TextStyle(
                          fontSize: 14.5,
                          fontWeight: FontWeight.bold,
                          color: isDark ? AppColors.waDarkBadgeGreen : AppColors.waLightActiveGreen,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 3),

                  // [Fila 2]: Doble check + Conductor • Tipo de Pago / Concepto
                  Row(
                    children: [
                      const Icon(
                        Icons.done_all,
                        size: 15,
                        color: AppColors.waCheckBlue,
                      ),
                      const SizedBox(width: 5),
                      Expanded(
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Flexible(
                              child: Text(
                                pago.conductorNombre.isNotEmpty ? pago.conductorNombre : 'Conductor',
                                style: TextStyle(
                                  fontSize: 13.5,
                                  color: textSecondary,
                                  letterSpacing: 0.1,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            if (pago.conceptoNombre.isNotEmpty) ...[
                              Text(
                                ' • ',
                                style: TextStyle(
                                  fontSize: 13.5,
                                  fontWeight: FontWeight.bold,
                                  color: textSecondary,
                                ),
                              ),
                              Flexible(
                                child: Text(
                                  pago.conceptoNombre,
                                  style: TextStyle(
                                    fontSize: 13.5,
                                    fontWeight: FontWeight.w700,
                                    color: isDark ? AppColors.taxiYellowLight : const Color(0xFFD97706),
                                  ),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 3),

                  // [Fila 3]: Nombre de la Bahía
                  Row(
                    children: [
                      Icon(
                        Icons.storefront_outlined,
                        size: 14,
                        color: textSecondary.withValues(alpha: 0.7),
                      ),
                      const SizedBox(width: 5),
                      Expanded(
                        child: Text(
                          pago.bahiaNombre.isNotEmpty ? pago.bahiaNombre : 'Bahía Principal',
                          style: TextStyle(
                            fontSize: 12.5,
                            color: textSecondary.withValues(alpha: 0.8),
                            letterSpacing: 0.1,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
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
