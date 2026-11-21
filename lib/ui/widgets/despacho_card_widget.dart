import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_colors.dart';
import '../../models/turno_model.dart';

class DespachoCardWidget extends StatelessWidget {
  final TurnoModel turno;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;

  const DespachoCardWidget({
    super.key,
    required this.turno,
    this.onTap,
    this.onLongPress,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final currencyFormat = NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0);
    final timeFormat = DateFormat('hh:mm a');
    final fechaAMostrar = turno.fechaDespacho ?? turno.fechaCreacion;
    final horaTexto = timeFormat.format(fechaAMostrar);

    final textPrimary = isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary;
    final textSecondary = isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary;
    final avatarBg = isDark ? AppColors.waDarkSearchField : const Color(0xFFE2E8F0);
    final avatarTextColor = isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary;

    return InkWell(
      onTap: onTap,
      onLongPress: onLongPress,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Avatar circular con el Número de Turno / Consecutivo
            CircleAvatar(
              radius: 24,
              backgroundColor: avatarBg,
              child: Text(
                '${turno.numeroTurno}',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                  color: avatarTextColor,
                ),
              ),
            ),
            const SizedBox(width: 12),

            // Columna Central: 3 Filas completas
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // [Fila 1]: Placa + Hora + Valor Pagado al final
                  Row(
                    children: [
                      Text(
                        turno.placaVisible,
                        style: TextStyle(
                          fontSize: 15.5,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 0.3,
                          color: textPrimary,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        horaTexto,
                        style: TextStyle(
                          fontSize: 12.5,
                          color: textSecondary,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        currencyFormat.format(turno.valorTotal),
                        style: TextStyle(
                          fontSize: 14.5,
                          fontWeight: FontWeight.bold,
                          color: isDark ? AppColors.waDarkBadgeGreen : AppColors.waLightActiveGreen,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 3),

                  // [Fila 2]: Verificación + Nombre del Conductor
                  Row(
                    children: [
                      const Icon(
                        Icons.done_all,
                        size: 15,
                        color: AppColors.waCheckBlue,
                      ),
                      const SizedBox(width: 5),
                      Expanded(
                        child: Text(
                          turno.conductorNombre.isNotEmpty ? turno.conductorNombre : 'Conductor General',
                          style: TextStyle(
                            fontSize: 13.5,
                            color: textSecondary,
                            letterSpacing: 0.1,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 3),

                  // [Fila 3]: Destino Oficial + Dirección / Nota complementaria
                  Row(
                    children: [
                      Icon(
                        Icons.near_me_outlined,
                        size: 14,
                        color: isDark ? AppColors.waDarkActiveGreen : AppColors.waLightActiveGreen,
                      ),
                      const SizedBox(width: 5),
                      Expanded(
                        child: Builder(builder: (context) {
                          final destino = turno.tarifaNombre.isNotEmpty
                              ? turno.tarifaNombre.toUpperCase()
                              : (turno.nota.trim().isNotEmpty ? turno.nota.trim().toUpperCase() : 'DESPACHO');
                          final direccion = (turno.nota.trim().isNotEmpty && turno.nota.trim().toUpperCase() != destino)
                              ? ' • ${turno.nota.trim()}'
                              : '';
                          return Text(
                            '$destino$direccion',
                            style: TextStyle(
                              fontSize: 12.5,
                              fontWeight: FontWeight.w600,
                              color: isDark ? AppColors.waDarkActiveGreen : AppColors.waLightActiveGreen,
                              letterSpacing: 0.1,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          );
                        }),
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

