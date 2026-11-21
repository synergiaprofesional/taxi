import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/utils/whatsapp_tracking_helper.dart';
import '../../../models/viaje_model.dart';

/// Vista web y móvil responsive de ticket digital y tracking para pasajeros que abordan en bahía
class WebTicketTrackingView extends StatelessWidget {
  final ViajeModel viaje;

  const WebTicketTrackingView({super.key, required this.viaje});

  Color _obtenerColorEstado(EstadoViaje estado) {
    switch (estado) {
      case EstadoViaje.solicitado:
      case EstadoViaje.asignado:
        return AppColors.warning;
      case EstadoViaje.enCamino:
      case EstadoViaje.aBordo:
        return AppColors.primary;
      case EstadoViaje.finalizado:
        return AppColors.success;
      case EstadoViaje.cancelado:
        return AppColors.error;
    }
  }

  String _obtenerTextoEstado(EstadoViaje estado) {
    switch (estado) {
      case EstadoViaje.solicitado:
      case EstadoViaje.asignado:
        return 'VEHÍCULO ASIGNADO EN BAHÍA';
      case EstadoViaje.enCamino:
        return 'EN CAMINO';
      case EstadoViaje.aBordo:
        return 'VIAJE EN CURSO';
      case EstadoViaje.finalizado:
        return 'VIAJE FINALIZADO';
      case EstadoViaje.cancelado:
        return 'VIAJE CANCELADO';
    }
  }

  @override
  Widget build(BuildContext context) {
    final urlTracking = WhatsAppTrackingHelper.generarUrlWebTracking(viaje.id);
    final colorEstado = _obtenerColorEstado(viaje.estado);
    final textoEstado = _obtenerTextoEstado(viaje.estado);

    return Scaffold(
      backgroundColor: const Color(0xFF121212),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E1E1E),
        elevation: 0,
        centerTitle: true,
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.verified_user_rounded, color: AppColors.primary, size: 22),
            const SizedBox(width: 8),
            const Text(
              'TAXI FORMAL VERIFICADO',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 15,
                letterSpacing: 1.1,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Banner de estado
                Container(
                  padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
                  decoration: BoxDecoration(
                    color: colorEstado.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: colorEstado, width: 1.5),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.radio_button_checked, color: colorEstado, size: 16),
                      const SizedBox(width: 8),
                      Text(
                        textoEstado,
                        style: TextStyle(
                          color: colorEstado,
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                          letterSpacing: 1.0,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),

                // Tarjeta Principal del Ticket Digital
                Card(
                  color: const Color(0xFF1E1E1E),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  elevation: 6,
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        // Placa estilo colombiano
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFFD100),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.black, width: 2),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.4),
                                blurRadius: 4,
                                offset: const Offset(0, 2),
                              )
                            ],
                          ),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(
                                viaje.placa.toUpperCase(),
                                style: const TextStyle(
                                  color: Colors.black,
                                  fontSize: 28,
                                  fontWeight: FontWeight.w900,
                                  letterSpacing: 3,
                                  fontFamily: 'monospace',
                                ),
                              ),
                              const Text(
                                'COLOMBIA',
                                style: TextStyle(
                                  color: Colors.black87,
                                  fontSize: 9,
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 2,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 20),

                        // Datos del Conductor
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 28,
                              backgroundColor: AppColors.primary.withOpacity(0.2),
                              child: const Icon(Icons.person, color: AppColors.primary, size: 32),
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    viaje.conductorNombre.isNotEmpty
                                        ? viaje.conductorNombre
                                        : 'Conductor Registrado',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 17,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Row(
                                    children: const [
                                      Icon(Icons.star, color: Colors.amber, size: 16),
                                      SizedBox(width: 4),
                                      Text(
                                        '4.9 (Conductor Certificado)',
                                        style: TextStyle(color: Colors.grey, fontSize: 13),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const Divider(color: Colors.white12, height: 32),

                        // Ruta
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Column(
                              children: [
                                const Icon(Icons.circle, color: AppColors.primary, size: 12),
                                Container(width: 2, height: 28, color: Colors.white24),
                                const Icon(Icons.location_on, color: AppColors.error, size: 16),
                              ],
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    viaje.origen.isNotEmpty ? viaje.origen : 'Bahía de Salida',
                                    style: const TextStyle(color: Colors.white70, fontSize: 13),
                                  ),
                                  const SizedBox(height: 18),
                                  Text(
                                    viaje.destino.isNotEmpty ? viaje.destino : 'Destino acordado',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 15,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const Divider(color: Colors.white12, height: 32),

                        // Tarifa Oficial Decretada
                        Container(
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: Colors.black26,
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: Colors.white10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: const [
                                  Text(
                                    'TARIFA OFICIAL DECRETADA',
                                    style: TextStyle(
                                      color: Colors.white54,
                                      fontSize: 11,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  SizedBox(height: 2),
                                  Text(
                                    'Sin tarifa dinámica ni cobros ocultos',
                                    style: TextStyle(color: Colors.white38, fontSize: 10),
                                  ),
                                ],
                              ),
                              Text(
                                '\$${viaje.precioAcordado.toStringAsFixed(0)} COP',
                                style: const TextStyle(
                                  color: AppColors.primary,
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),

                // Centro de Seguridad y Compartir
                Card(
                  color: const Color(0xFF1E1E1E),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const Text(
                          'Centro de Seguridad y Confianza',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                        const SizedBox(height: 12),
                        ElevatedButton.icon(
                          onPressed: () {
                            // En Flutter Web o móvil abre el diálogo nativo de compartir
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('Enlace copiado: $urlTracking'),
                                backgroundColor: AppColors.primary,
                                behavior: SnackBarBehavior.floating,
                              ),
                            );
                          },
                          icon: const Icon(Icons.share, color: Colors.black),
                          label: const Text(
                            'COMPARTIR VIAJE POR WHATSAPP',
                            style: TextStyle(
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                              fontSize: 13,
                            ),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF25D366), // Color WhatsApp
                            padding: const EdgeInsets.symmetric(vertical: 13),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                        ),
                        const SizedBox(height: 8),
                        OutlinedButton.icon(
                          onPressed: () {
                            // Botón de auxilio
                            showDialog(
                              context: context,
                              builder: (ctx) => AlertDialog(
                                backgroundColor: const Color(0xFF252525),
                                title: const Text('Asistencia Vial 24/7', style: TextStyle(color: Colors.white)),
                                content: const Text(
                                  'Si tienes alguna novedad o emergencia durante el recorrido, comunícate con la central de garita o autoridades al 123.',
                                  style: TextStyle(color: Colors.white70),
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(ctx),
                                    child: const Text('CERRAR', style: TextStyle(color: AppColors.primary)),
                                  ),
                                ],
                              ),
                            );
                          },
                          icon: const Icon(Icons.shield_outlined, color: AppColors.error),
                          label: const Text(
                            'BOTÓN DE AUXILIO / SOS',
                            style: TextStyle(color: AppColors.error, fontWeight: FontWeight.bold, fontSize: 13),
                          ),
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(color: AppColors.error),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
