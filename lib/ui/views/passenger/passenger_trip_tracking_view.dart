import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/viaje_model.dart';
import '../../../services/firestore_repository.dart';
import '../../widgets/admob_banner_widget.dart';

class PassengerTripTrackingView extends StatefulWidget {
  final ViajeModel viajeInicial;

  const PassengerTripTrackingView({
    super.key,
    required this.viajeInicial,
  });

  @override
  State<PassengerTripTrackingView> createState() => _PassengerTripTrackingViewState();
}

class _PassengerTripTrackingViewState extends State<PassengerTripTrackingView> {
  final firestoreRepo = Get.find<FirestoreRepository>();
  double _calificacion = 5.0;
  final _comentarioController = TextEditingController();

  void _mostrarDialogoCalificacion(String viajeId) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => StatefulBuilder(
        builder: (context, setDlgState) => AlertDialog(
          title: const Text('¡Viaje Finalizado!', textAlign: TextAlign.center),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('¿Cómo estuvo tu experiencia con el conductor?'),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(5, (index) {
                  return IconButton(
                    icon: Icon(
                      index < _calificacion ? Icons.star : Icons.star_border,
                      color: Colors.amber,
                      size: 32,
                    ),
                    onPressed: () => setDlgState(() => _calificacion = (index + 1).toDouble()),
                  );
                }),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _comentarioController,
                decoration: const InputDecoration(
                  hintText: 'Comentario opcional...',
                  border: OutlineInputBorder(),
                ),
                maxLines: 2,
              ),
            ],
          ),
          actions: [
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
              onPressed: () async {
                await firestoreRepo.calificarViaje(
                  viajeId,
                  calificacion: _calificacion,
                  comentario: _comentarioController.text.trim(),
                  esPasajero: true,
                );
                Navigator.pop(ctx);
                Get.back();
              },
              child: const Text('ENVIAR CALIFICACIÓN', style: TextStyle(color: Colors.white)),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<List<ViajeModel>>(
      stream: firestoreRepo.streamViajesPasajero(widget.viajeInicial.pasajeroId),
      builder: (context, snapshot) {
        final viajes = snapshot.data ?? [];
        final viaje = viajes.firstWhereOrNull((v) => v.id == widget.viajeInicial.id) ?? widget.viajeInicial;

        final enCarrera = viaje.estado == EstadoViaje.aBordo;

        return Scaffold(
          appBar: AppBar(
            title: const Text('Tu Viaje en Vivo'),
            leading: IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: () => Get.back(),
            ),
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Estado del Viaje
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: _getColorEstado(viaje.estado).withOpacity(0.12),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: _getColorEstado(viaje.estado), width: 2),
                  ),
                  child: Row(
                    children: [
                      CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(_getColorEstado(viaje.estado)),
                        strokeWidth: 3,
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              viaje.estado.label,
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: _getColorEstado(viaje.estado),
                              ),
                            ),
                            Text(
                              _getDescripcionEstado(viaje.estado),
                              style: const TextStyle(fontSize: 13, color: Colors.grey),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                // Datos del Taxi y Conductor (Si está asignado)
                if (viaje.conductorNombre.isNotEmpty)
                  Card(
                    elevation: 3,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              const CircleAvatar(
                                radius: 28,
                                backgroundColor: AppColors.primary,
                                child: Icon(Icons.person, color: Colors.white, size: 32),
                              ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      viaje.conductorNombre,
                                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                                    ),
                                    Text(
                                      'Móvil: ${viaje.vehiculoPlaca} ${viaje.vehiculoModelo.isNotEmpty ? '• ' + viaje.vehiculoModelo : ''}',
                                      style: const TextStyle(fontSize: 14, color: Colors.grey),
                                    ),
                                  ],
                                ),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                decoration: BoxDecoration(
                                  color: Colors.amber,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  viaje.vehiculoPlaca,
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),

                const SizedBox(height: 20),

                // Resumen de Ruta y Pantalla Espejo
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.withOpacity(0.3)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Detalle de Ruta Oficial', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                      const Divider(),
                      ListTile(
                        leading: const Icon(Icons.trip_origin, color: Colors.green),
                        title: const Text('Recogida'),
                        subtitle: Text(viaje.origenDireccion),
                        dense: true,
                      ),
                      ListTile(
                        leading: const Icon(Icons.location_on, color: Colors.redAccent),
                        title: const Text('Destino'),
                        subtitle: Text(viaje.destinoDireccion),
                        dense: true,
                      ),
                      const Divider(),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Tarifa Oficial Estandarizada:', style: TextStyle(fontWeight: FontWeight.bold)),
                          Text(
                            '\$ ${viaje.tarifaTotal.toInt()}',
                            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppColors.primary),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                // Acciones
                if (viaje.estado == EstadoViaje.solicitado)
                  OutlinedButton.icon(
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.red,
                      side: const BorderSide(color: Colors.red),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    icon: const Icon(Icons.cancel),
                    label: const Text('CANCELAR SOLICITUD'),
                    onPressed: () async {
                      await firestoreRepo.actualizarEstadoViaje(viaje.id, EstadoViaje.cancelado);
                      Get.back();
                    },
                  )
                else if (viaje.estado == EstadoViaje.finalizado)
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    icon: const Icon(Icons.star, color: Colors.white),
                    label: const Text('CALIFICAR SERVICIO', style: TextStyle(color: Colors.white)),
                    onPressed: () => _mostrarDialogoCalificacion(viaje.id),
                  ),

                const SizedBox(height: 16),

                // Enclavamiento de Seguridad Vial: Anuncio inhibido si está en carrera activa
                AdmobBannerWidget(isInActiveRide: enCarrera),
              ],
            ),
          ),
        );
      },
    );
  }

  Color _getColorEstado(EstadoViaje estado) {
    switch (estado) {
      case EstadoViaje.solicitado:
        return Colors.orange;
      case EstadoViaje.asignado:
      case EstadoViaje.enCamino:
        return Colors.blue;
      case EstadoViaje.aBordo:
        return Colors.purple;
      case EstadoViaje.finalizado:
        return Colors.green;
      case EstadoViaje.cancelado:
        return Colors.red;
    }
  }

  String _getDescripcionEstado(EstadoViaje estado) {
    switch (estado) {
      case EstadoViaje.solicitado:
        return 'Notificando a la flota de taxis más cercana...';
      case EstadoViaje.asignado:
        return 'Un taxista oficial ha tomado tu carrera.';
      case EstadoViaje.enCamino:
        return 'El conductor se está desplazando hacia tu punto de recogida.';
      case EstadoViaje.aBordo:
        return '¡Viaje en curso! Disfrute su trayecto.';
      case EstadoViaje.finalizado:
        return 'Has llegado a tu destino con tarifa legal.';
      case EstadoViaje.cancelado:
        return 'El servicio fue cancelado.';
    }
  }
}
