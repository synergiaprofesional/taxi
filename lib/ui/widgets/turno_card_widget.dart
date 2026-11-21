import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_colors.dart';
import '../../models/turno_model.dart';

class TurnoCardWidget extends StatelessWidget {
  final TurnoModel turno;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;

  const TurnoCardWidget({
    super.key,
    required this.turno,
    this.onTap,
    this.onLongPress,
  });

  String _calcularTiempoEspera(DateTime fecha) {
    final ahora = DateTime.now();
    final diff = ahora.difference(fecha);
    if (diff.isNegative) return '0 min';
    if (diff.inMinutes < 1) return '< 1 min';
    if (diff.inMinutes < 60) return '${diff.inMinutes} min';
    final horas = diff.inHours;
    final minutos = diff.inMinutes % 60;
    return '${horas}h ${minutos}m';
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final timeFormat = DateFormat('hh:mm a');
    final horaTexto = timeFormat.format(turno.fechaCreacion);

    final isActual = turno.estado == EstadoTurno.actual;
    final isAnonymous = turno.esAnonimo;

    // Colores dinámicos fieles al estilo WhatsApp con identidad Taxi (Amarillo y Negro)
    final textPrimary = isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary;
    final textSecondary = isDark ? AppColors.waDarkTextSecondary : AppColors.waLightTextSecondary;
    final avatarBg = isActual
        ? AppColors.taxiYellow
        : (isDark ? AppColors.waDarkSearchField : const Color(0xFFE2E8F0));
    final avatarTextColor = isActual
        ? AppColors.taxiBlackPure
        : (isDark ? AppColors.waDarkTextPrimary : AppColors.waLightTextPrimary);

    return InkWell(
      onTap: onTap,
      onLongPress: onLongPress,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Avatar circular con el Número de Turno como protagonista
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
            const SizedBox(width: 14),

            // Columna Central: Placa (Línea 1) y Conductor • Espera (Línea 2)
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Fila Superior: Placa en negrita nítida + indicador anónimo si aplica
                  Row(
                    children: [
                      Flexible(
                        child: Text(
                          turno.placaVisible,
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                            letterSpacing: 0.3,
                            color: textPrimary,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      if (isAnonymous) ...[
                        const SizedBox(width: 6),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1.5),
                          decoration: BoxDecoration(
                            color: Colors.amber.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Text(
                            'ANÓNIMO',
                            style: TextStyle(
                              fontSize: 9.5,
                              fontWeight: FontWeight.bold,
                              color: Colors.amber,
                            ),
                          ),
                        ),
                      ],
                      if (turno.bahiaNombre.isNotEmpty) ...[
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: isDark ? Colors.white10 : Colors.black12,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            turno.bahiaNombre,
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: textSecondary,
                            ),
                          ),
                        ),
                      ],
                    ],
                  ),
                  const SizedBox(height: 3),

                  // [Fila 2]: Ícono de estado + Nombre del Conductor
                  Row(
                    children: [
                      Icon(
                        isActual ? Icons.done_all : Icons.done,
                        size: 16,
                        color: isActual
                            ? AppColors.waCheckBlue
                            : textSecondary.withValues(alpha: 0.7),
                      ),
                      const SizedBox(width: 5),
                      Expanded(
                        child: Text(
                          turno.conductorNombre.isNotEmpty ? turno.conductorNombre : 'Sin conductor',
                          style: TextStyle(
                            fontSize: 13.5,
                            fontWeight: FontWeight.w500,
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

                  // [Fila 3]: Tiempo de Espera en fila dedicada
                  Row(
                    children: [
                      Icon(
                        Icons.access_time_rounded,
                        size: 14,
                        color: textSecondary.withValues(alpha: 0.7),
                      ),
                      const SizedBox(width: 5),
                      Text(
                        'Espera: ${_calcularTiempoEspera(turno.fechaCreacion)}',
                        style: TextStyle(
                          fontSize: 12.5,
                          color: textSecondary.withValues(alpha: 0.8),
                          letterSpacing: 0.1,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(width: 10),

            // Columna Lateral Derecha (Trailing): Hora y Badge / Bahía
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              mainAxisSize: MainAxisSize.min,
              children: [
                // Hora en tipografía fina y discreta estilo WhatsApp
                Text(
                  horaTexto,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: isActual ? FontWeight.bold : FontWeight.normal,
                    color: isActual
                        ? (isDark ? AppColors.taxiYellowLight : AppColors.taxiYellowDark)
                        : textSecondary,
                  ),
                ),
                const SizedBox(height: 4),

                // Badge de estado solo para el turno ACTUAL
                if (isActual) ...[
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2.5),
                    decoration: BoxDecoration(
                      color: AppColors.taxiYellow,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Text(
                      'ACTUAL',
                      style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w900,
                        color: AppColors.taxiBlackPure,
                        letterSpacing: 0.5,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ],
        ),
      ),
    );
  }
}
