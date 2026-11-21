import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/viaje_model.dart';
import '../../../services/firestore_repository.dart';
import 'passenger_trip_tracking_view.dart';

class DriverOffersSheet extends StatefulWidget {
  final ViajeModel viaje;

  const DriverOffersSheet({
    super.key,
    required this.viaje,
  });

  static Future<void> show(BuildContext context, ViajeModel viaje) {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => DriverOffersSheet(viaje: viaje),
    );
  }

  @override
  State<DriverOffersSheet> createState() => _DriverOffersSheetState();
}

class _DriverOffersSheetState extends State<DriverOffersSheet> {
  final firestoreRepo = Get.find<FirestoreRepository>();

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.65,
      decoration: const BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Drag handle
          Center(
            child: Container(
              width: 48,
              height: 5,
              decoration: BoxDecoration(
                color: Colors.grey.shade400,
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Header
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Conductores Disponibles',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    'Tu oferta: \$ ${widget.viaje.tarifaTotal.toInt()}',
                    style: const TextStyle(fontSize: 13, color: Colors.grey),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Row(
                  children: [
                    SizedBox(
                      width: 12,
                      height: 12,
                      child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.primary),
                    ),
                    SizedBox(width: 6),
                    Text(
                      'Buscando...',
                      style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ],
          ),

          const SizedBox(height: 16),

          // Stream de ofertas recibidas
          Expanded(
            child: StreamBuilder<List<ConductorOfertaModel>>(
              stream: firestoreRepo.streamOfertasViaje(widget.viaje.id),
              builder: (context, snapshot) {
                final ofertas = snapshot.data ?? [];

                if (ofertas.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.radar, size: 56, color: AppColors.primary),
                        const SizedBox(height: 16),
                        const Text(
                          'Notificando a la flota cercana...',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          'Mostraremos aquí los taxistas que acepten tus \$ ${widget.viaje.tarifaTotal.toInt()} o envíen contraofertas.',
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.grey, fontSize: 13),
                        ),
                      ],
                    ),
                  );
                }

                return ListView.separated(
                  itemCount: ofertas.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 10),
                  itemBuilder: (context, index) {
                    final oferta = ofertas[index];
                    final esMismoPrecio = oferta.precioPropuesto <= widget.viaje.tarifaTotal;

                    return Card(
                      elevation: 2,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      child: Padding(
                        padding: const EdgeInsets.all(14),
                        child: Row(
                          children: [
                            // Avatar conductor
                            CircleAvatar(
                              radius: 26,
                              backgroundColor: AppColors.primary.withOpacity(0.15),
                              child: const Icon(Icons.person, color: AppColors.primary, size: 30),
                            ),
                            const SizedBox(width: 14),

                            // Info conductor y móvil
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Text(
                                        oferta.conductorNombre,
                                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                      ),
                                      const SizedBox(width: 6),
                                      const Icon(Icons.star, color: Colors.amber, size: 16),
                                      Text(
                                        ' ${oferta.conductorCalificacion.toStringAsFixed(1)}',
                                        style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    '${oferta.vehiculoPlaca} • ${oferta.vehiculoModelo.isNotEmpty ? oferta.vehiculoModelo : 'Taxi Oficial'}',
                                    style: const TextStyle(color: Colors.grey, fontSize: 13),
                                  ),
                                  const SizedBox(height: 2),
                                  Text(
                                    '⏱️ A ${oferta.tiempoMinutos} min  (${oferta.distanciaMetros} m)',
                                    style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.w500, fontSize: 12),
                                  ),
                                ],
                              ),
                            ),

                            // Precio y botón de elegir
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.end,
                              children: [
                                Text(
                                  '\$ ${oferta.precioPropuesto.toInt()}',
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: esMismoPrecio ? Colors.green : Colors.deepOrange,
                                  ),
                                ),
                                if (!esMismoPrecio)
                                  const Text('Contraoferta', style: TextStyle(color: Colors.deepOrange, fontSize: 11)),
                                const SizedBox(height: 8),
                                ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppColors.primary,
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                                  ),
                                  onPressed: () async {
                                    await firestoreRepo.seleccionarConductorViaje(widget.viaje.id, oferta);
                                    Navigator.pop(context);
                                    Get.to(() => PassengerTripTrackingView(
                                          viajeInicial: widget.viaje.copyWith(
                                            conductorId: oferta.conductorId,
                                            conductorNombre: oferta.conductorNombre,
                                            vehiculoPlaca: oferta.vehiculoPlaca,
                                            vehiculoModelo: oferta.vehiculoModelo,
                                            tarifaTotal: oferta.precioPropuesto,
                                            estado: EstadoViaje.asignado,
                                          ),
                                        ));
                                  },
                                  child: const Text('ELEGIR', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
