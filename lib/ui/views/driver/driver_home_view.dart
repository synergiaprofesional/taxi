import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/turno_model.dart';
import '../../../models/viaje_model.dart';
import '../../../services/firestore_repository.dart';
import '../../widgets/admob_banner_widget.dart';

class DriverHomeView extends StatefulWidget {
  final String conductorNombre;
  final String conductorId;
  final String vehiculoPlaca;
  final String vehiculoModelo;

  const DriverHomeView({
    super.key,
    this.conductorNombre = 'Carlos Ramírez',
    this.conductorId = 'cond_001',
    this.vehiculoPlaca = 'WBD-512',
    this.vehiculoModelo = 'Kia Rio 2024',
  });

  @override
  State<DriverHomeView> createState() => _DriverHomeViewState();
}

class _DriverHomeViewState extends State<DriverHomeView> {
  final turnoController = Get.find<TurnoController>();
  final firestoreRepo = Get.find<FirestoreRepository>();

  bool _auxilioEnviado = false;
  final Set<String> _carrerasOfertadas = {};

  void _activarBotonPanico() async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.warning_amber_rounded, color: Colors.red, size: 28),
            SizedBox(width: 8),
            Text('Botón de Auxilio Vial', style: TextStyle(fontWeight: FontWeight.bold)),
          ],
        ),
        content: const Text(
          '¿Desea enviar una alerta de pánico y auxilio vial inmediato a la garita central y compañeros cercanos con su ubicación actual?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('EMITIR ALERTA', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );

    if (confirmar == true) {
      await firestoreRepo.registrarPanicoVial(
        conductorId: widget.conductorId,
        conductorNombre: widget.conductorNombre,
        vehiculoPlaca: widget.vehiculoPlaca,
        lat: 10.9685,
        lng: -74.7813,
        motivo: 'Auxilio vial activado desde la app del conductor',
      );
      setState(() => _auxilioEnviado = true);
      Get.snackbar(
        'Alerta Emitida',
        'Se ha notificado a la garita central y supervisión vial.',
        backgroundColor: Colors.red,
        colorText: Colors.white,
        snackPosition: SnackPosition.TOP,
        duration: const Duration(seconds: 5),
      );
    }
  }

  void _enviarOfertaConductor(ViajeModel viaje, double precio) async {
    final oferta = ConductorOfertaModel(
      conductorId: widget.conductorId,
      conductorNombre: widget.conductorNombre,
      conductorFotoUrl: '',
      conductorCalificacion: 4.9,
      vehiculoPlaca: widget.vehiculoPlaca,
      vehiculoModelo: widget.vehiculoModelo,
      distanciaMetros: 450,
      tiempoMinutos: 3,
      precioPropuesto: precio,
      fechaOferta: DateTime.now(),
    );

    await firestoreRepo.proponerOfertaConductor(viaje.id, oferta);
    setState(() => _carrerasOfertadas.add(viaje.id));

    Get.snackbar(
      'Oferta Enviada',
      'Has postulado tu taxi por \$ ${precio.toInt()}. El pasajero está decidiendo.',
      backgroundColor: AppColors.primary,
      colorText: Colors.white,
      duration: const Duration(seconds: 4),
    );
  }

  void _mostrarDialogoContraoferta(ViajeModel viaje) {
    final base = viaje.tarifaPropuestaPasajero > 0 ? viaje.tarifaPropuestaPasajero : viaje.tarifaTotal;
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.surface,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Contraofertar Carrera',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              'Oferta actual del pasajero: \$ ${base.toInt()}',
              style: const TextStyle(color: Colors.grey),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
                    onPressed: () {
                      Navigator.pop(ctx);
                      _enviarOfertaConductor(viaje, base + 2000.0);
                    },
                    child: Text('+ \$2.000 (\$ ${(base + 2000).toInt()})', style: const TextStyle(color: Colors.white)),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.orange.shade800),
                    onPressed: () {
                      Navigator.pop(ctx);
                      _enviarOfertaConductor(viaje, base + 4000.0);
                    },
                    child: Text('+ \$4.000 (\$ ${(base + 4000).toInt()})', style: const TextStyle(color: Colors.white)),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.conductorNombre, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text('Móvil: ${widget.vehiculoPlaca} • ${widget.vehiculoModelo}', style: const TextStyle(fontSize: 12, color: Colors.white70)),
          ],
        ),
        actions: [
          IconButton(
            icon: Icon(
              Icons.sos,
              color: _auxilioEnviado ? Colors.amber : Colors.redAccent,
              size: 32,
            ),
            tooltip: 'Botón de Auxilio / Pánico',
            onPressed: _activarBotonPanico,
          ),
        ],
      ),
      body: Obx(() {
        final misTurnos = turnoController.turnos
            .where((t) => t.vehiculoPlaca.toUpperCase() == widget.vehiculoPlaca.toUpperCase())
            .toList();

        final TurnoModel? turnoActivo = misTurnos.firstWhereOrNull((t) => t.enFila || t.estado == EstadoTurno.actual);

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Banner de estado en cola de bahía
              if (turnoActivo != null)
                _buildCardTurnoActivo(turnoActivo)
              else
                _buildCardSinTurno(),

              const SizedBox(height: 16),

              // Billetera y Ahorro Programado
              _buildCardBilleteraAhorro(),

              const SizedBox(height: 16),

              // Carreras Disponibles en Calle (Radar con Ofertas y Contraofertas inDrive)
              _buildSeccionCarrerasRadar(),

              const SizedBox(height: 16),

              // Banner publicitario AdMob (Cero intrusión en conducción)
              const AdmobBannerWidget(isInActiveRide: false),
            ],
          ),
        );
      }),
    );
  }

  Widget _buildCardTurnoActivo(TurnoModel turno) {
    final esActual = turno.estado == EstadoTurno.actual;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: esActual ? AppColors.turnActual.withValues(alpha: 0.15) : AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: esActual ? AppColors.turnActual : AppColors.primary.withValues(alpha: 0.3),
          width: 2,
        ),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: esActual ? AppColors.turnActual : AppColors.primary,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  esActual ? '¡ES TU TURNO EN BAHÍA!' : 'EN ESPERA',
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                ),
              ),
              Text(
                'Posición #${turno.numeroTurno}',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            turno.bahiaNombre,
            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(
            'Enturnado a las ${turno.fechaCreacion.hour.toString().padLeft(2, '0')}:${turno.fechaCreacion.minute.toString().padLeft(2, '0')}',
            style: const TextStyle(color: Colors.grey),
          ),
          if (esActual) ...[
            const SizedBox(height: 16),
            const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.touch_app, color: AppColors.turnActual),
                SizedBox(width: 8),
                Text(
                  'Acérquese a la cabecera para abordar pasajero',
                  style: TextStyle(fontWeight: FontWeight.w600, color: AppColors.turnActual),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildCardSinTurno() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.withValues(alpha: 0.3)),
      ),
      child: Column(
        children: [
          const Icon(Icons.local_taxi_outlined, size: 48, color: Colors.grey),
          const SizedBox(height: 12),
          const Text(
            'Sin turno activo en bahía',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 6),
          const Text(
            'Acérquese a una garita autorizada para registrar su turno o active el radar en calle.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Widget _buildCardBilleteraAhorro() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.primary, AppColors.primary.withBlue(160)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
      ),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Mi Ahorro Programado', style: TextStyle(color: Colors.white70, fontSize: 14)),
              Icon(Icons.savings_outlined, color: Colors.white, size: 24),
            ],
          ),
          SizedBox(height: 8),
          Text(
            '\$ 145.000',
            style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 8),
          Text(
            'Fondo de Repuestos y Bienestar Gremial',
            style: TextStyle(color: Colors.white70, fontSize: 12),
          ),
        ],
      ),
    );
  }

  Widget _buildSeccionCarrerasRadar() {
    return StreamBuilder<List<ViajeModel>>(
      stream: firestoreRepo.streamViajesDisponiblesCalle(),
      builder: (context, snapshot) {
        final viajes = snapshot.data ?? [];
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Radar de Carreras en Calle',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.green.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    '${viajes.length} disponibles',
                    style: const TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 12),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (viajes.isEmpty)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Center(
                  child: Text('No hay solicitudes de pasajeros en tu zona actualmente.', style: TextStyle(color: Colors.grey)),
                ),
              )
            else
              ...viajes.map((viaje) {
                final yaOfertado = _carrerasOfertadas.contains(viaje.id);
                final precioPasajero = viaje.tarifaPropuestaPasajero > 0 ? viaje.tarifaPropuestaPasajero : viaje.tarifaTotal;

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  child: Padding(
                    padding: const EdgeInsets.all(14),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Categoría Pill y Precio Pasajero
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: AppColors.primary.withValues(alpha: 0.15),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                viaje.categoria.label,
                                style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 11),
                              ),
                            ),
                            Text(
                              'Oferta: \$ ${precioPasajero.toInt()}',
                              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Row(
                          children: [
                            const Icon(Icons.trip_origin, color: Colors.green, size: 18),
                            const SizedBox(width: 8),
                            Expanded(child: Text(viaje.origenDireccion, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14))),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Row(
                          children: [
                            const Icon(Icons.location_on, color: Colors.redAccent, size: 18),
                            const SizedBox(width: 8),
                            Expanded(child: Text(viaje.destinoDireccion, style: const TextStyle(color: Colors.black87, fontSize: 13))),
                          ],
                        ),
                        const SizedBox(height: 12),

                        // Acciones: Aceptar o Contraofertar (inDrive Style)
                        if (yaOfertado)
                          Container(
                            padding: const EdgeInsets.symmetric(vertical: 8),
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              color: Colors.amber.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Text('⏳ Postulado — Esperando decisión del pasajero...', style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold, fontSize: 12)),
                          )
                        else
                          Row(
                            children: [
                              Expanded(
                                flex: 3,
                                child: ElevatedButton.icon(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.green,
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                                  ),
                                  icon: const Icon(Icons.check, color: Colors.white, size: 18),
                                  label: Text('ACEPTAR (\$ ${precioPasajero.toInt()})', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12)),
                                  onPressed: () => _enviarOfertaConductor(viaje, precioPasajero),
                                ),
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                flex: 2,
                                child: OutlinedButton(
                                  style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.orange.shade800,
                                    side: BorderSide(color: Colors.orange.shade800),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                                  ),
                                  onPressed: () => _mostrarDialogoContraoferta(viaje),
                                  child: const Text('CONTRAOFERTA', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
                                ),
                              ),
                            ],
                          ),
                      ],
                    ),
                  ),
                );
              }),
          ],
        );
      },
    );
  }
}
