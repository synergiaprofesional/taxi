import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/tarifa_sector_model.dart';
import '../../../models/viaje_model.dart';
import '../../../services/firestore_repository.dart';
import '../../widgets/admob_banner_widget.dart';
import 'driver_offers_sheet.dart';

class PassengerHomeView extends StatefulWidget {
  final String pasajeroId;
  final String pasajeroNombre;

  const PassengerHomeView({
    super.key,
    this.pasajeroId = 'pas_001',
    this.pasajeroNombre = 'Ana Martínez',
  });

  @override
  State<PassengerHomeView> createState() => _PassengerHomeViewState();
}

class _PassengerHomeViewState extends State<PassengerHomeView> {
  final firestoreRepo = Get.find<FirestoreRepository>();

  final origenController = TextEditingController(text: 'Calle 72 # 54 - 20 (Edificio Prado)');
  final destinoController = TextEditingController();

  CategoriaViaje _categoriaSeleccionada = CategoriaViaje.taxiEstandar;
  TarifaSectorModel? _sectorSeleccionado;
  bool _esNocturno = false;
  bool _esFestivo = false;
  bool _esAeropuerto = false;
  double _ajusteOferta = 0.0;
  bool _solicitando = false;

  double get _tarifaLegalCalculada {
    if (_sectorSeleccionado == null) return 10000.0;
    double base = firestoreRepo.calcularTarifaLegal(
      sector: _sectorSeleccionado!,
      esNocturno: _esNocturno,
      esFestivo: _esFestivo,
      esAeropuerto: _esAeropuerto,
    );
    // Categorías con recargo premium
    if (_categoriaSeleccionada == CategoriaViaje.ejecutivoVip) base += 5000.0;
    if (_categoriaSeleccionada == CategoriaViaje.bahiaPrioritaria) base += 2000.0;
    return base;
  }

  double get _ofertaFinalPasajero {
    final finalVal = _tarifaLegalCalculada + _ajusteOferta;
    return finalVal < 5000.0 ? 5000.0 : finalVal;
  }

  void _publicarOfertaViaje() async {
    if (_sectorSeleccionado == null) {
      Get.snackbar('Seleccionar Destino', 'Por favor selecciona el sector o destino de tu viaje.');
      return;
    }

    setState(() => _solicitando = true);

    final viaje = ViajeModel(
      id: '',
      pasajeroId: widget.pasajeroId,
      pasajeroNombre: widget.pasajeroNombre,
      pasajeroTelefono: '3109876543',
      origenDireccion: origenController.text.trim(),
      destinoDireccion: destinoController.text.trim().isNotEmpty
          ? destinoController.text.trim()
          : _sectorSeleccionado!.name,
      sectorDestinoId: _sectorSeleccionado!.id,
      sectorNombre: _sectorSeleccionado!.name,
      tarifaBase: _sectorSeleccionado!.valor,
      recargoNocturno: _esNocturno ? _sectorSeleccionado!.recargoNocturno : 0.0,
      recargoFestivo: _esFestivo ? _sectorSeleccionado!.recargoFestivo : 0.0,
      recargoAeropuerto: _esAeropuerto ? _sectorSeleccionado!.recargoAeropuerto : 0.0,
      tarifaPropuestaPasajero: _ofertaFinalPasajero,
      tarifaTotal: _ofertaFinalPasajero,
      estado: EstadoViaje.solicitado,
      tipoServicio: TipoServicioViaje.calle,
      categoria: _categoriaSeleccionada,
      fechaSolicitud: DateTime.now(),
    );

    final nuevoViaje = await firestoreRepo.solicitarViaje(viaje);
    setState(() => _solicitando = false);

    // Desplegar de inmediato la hoja interactiva "Elige tu Conductor"
    DriverOffersSheet.show(context, nuevoViaje);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            const Icon(Icons.local_taxi, color: AppColors.primary, size: 28),
            const SizedBox(width: 8),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Taxi Oficial', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                Text('Hola, ${widget.pasajeroNombre}', style: const TextStyle(fontSize: 12, color: Colors.white70)),
              ],
            ),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. Selector de Categorías en 1 Toque (Estilo Uber)
            _buildSelectorCategorias(),

            const SizedBox(height: 16),

            // 2. Banner de Garantía Legal Oficial
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.amber.withOpacity(0.12),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.amber.shade700),
              ),
              child: const Row(
                children: [
                  Icon(Icons.gavel, color: Colors.amber, size: 22),
                  SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Tarifas legales ancladas por decreto distrital. Tú decides el precio final y eliges a tu conductor.',
                      style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // 3. Origen y Destino
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Ruta de Viaje', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 12),
                    TextField(
                      controller: origenController,
                      decoration: const InputDecoration(
                        labelText: 'Punto de Recogida',
                        prefixIcon: Icon(Icons.my_location, color: Colors.green),
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),
                    StreamBuilder<List<TarifaSectorModel>>(
                      stream: firestoreRepo.streamTarifas(),
                      builder: (context, snapshot) {
                        final tarifas = snapshot.data ?? [];
                        return DropdownButtonFormField<TarifaSectorModel>(
                          value: _sectorSeleccionado,
                          decoration: const InputDecoration(
                            labelText: 'Sector / Destino Oficial',
                            prefixIcon: Icon(Icons.location_on, color: Colors.redAccent),
                            border: OutlineInputBorder(),
                          ),
                          hint: const Text('Seleccionar sector oficial'),
                          items: tarifas
                              .map((t) => DropdownMenuItem(
                                    value: t,
                                    child: Text('${t.name} (\$ ${t.valor.toInt()})', overflow: TextOverflow.ellipsis),
                                  ))
                              .toList(),
                          onChanged: (val) {
                            setState(() {
                              _sectorSeleccionado = val;
                              _ajusteOferta = 0.0; // reset ajuste
                              if (val != null) {
                                destinoController.text = val.name;
                                if (val.name.toLowerCase().contains('aeropuerto')) {
                                  _esAeropuerto = true;
                                }
                              }
                            });
                          },
                        );
                      },
                    ),
                    const SizedBox(height: 12),
                    const Text('Recargos Legales Vigentes:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                    Wrap(
                      spacing: 8,
                      children: [
                        FilterChip(
                          label: const Text('Nocturno (+\$1.000)'),
                          selected: _esNocturno,
                          onSelected: (v) => setState(() => _esNocturno = v),
                        ),
                        FilterChip(
                          label: const Text('Festivo (+\$1.000)'),
                          selected: _esFestivo,
                          onSelected: (v) => setState(() => _esFestivo = v),
                        ),
                        FilterChip(
                          label: const Text('Aeropuerto (+\$5.000)'),
                          selected: _esAeropuerto,
                          onSelected: (v) => setState(() => _esAeropuerto = v),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 16),

            // 4. Componente "Ofrece tu Precio" con Ancla Legal (Estilo inDrive + Taxi)
            _buildComponenteOfertaPasajero(),

            const SizedBox(height: 20),

            // 5. Botón Publicar Oferta
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
              ),
              onPressed: _solicitando ? null : _publicarOfertaViaje,
              child: _solicitando
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text(
                      'PUBLICAR OFERTA DE VIAJE',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                    ),
            ),

            const SizedBox(height: 16),

            // Banner AdMob (Inhibido en viaje)
            const AdmobBannerWidget(isInActiveRide: false),
          ],
        ),
      ),
    );
  }

  Widget _buildSelectorCategorias() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: [
          _buildCategoryCard(
            categoria: CategoriaViaje.taxiEstandar,
            icon: Icons.local_taxi,
            titulo: 'Taxi Clásico',
            subtitulo: 'Flota oficial en calle',
          ),
          const SizedBox(width: 8),
          _buildCategoryCard(
            categoria: CategoriaViaje.bahiaPrioritaria,
            icon: Icons.storefront,
            titulo: 'Bahía Prioritaria',
            subtitulo: 'Asignación inmediata',
          ),
          const SizedBox(width: 8),
          _buildCategoryCard(
            categoria: CategoriaViaje.ejecutivoVip,
            icon: Icons.star_border,
            titulo: 'Ejecutivo VIP',
            subtitulo: 'Aire acondicionado',
          ),
          const SizedBox(width: 8),
          _buildCategoryCard(
            categoria: CategoriaViaje.envioExpress,
            icon: Icons.local_shipping_outlined,
            titulo: 'Envíos / Carga',
            subtitulo: 'Paquetes en baúl',
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryCard({
    required CategoriaViaje categoria,
    required IconData icon,
    required String titulo,
    required String subtitulo,
  }) {
    final seleccionada = _categoriaSeleccionada == categoria;
    return GestureDetector(
      onTap: () => setState(() => _categoriaSeleccionada = categoria),
      child: Container(
        width: 140,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        decoration: BoxDecoration(
          color: seleccionada ? AppColors.primary.withOpacity(0.15) : AppColors.surface,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: seleccionada ? AppColors.primary : Colors.grey.withOpacity(0.3),
            width: seleccionada ? 2 : 1,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: seleccionada ? AppColors.primary : Colors.grey, size: 26),
            const SizedBox(height: 6),
            Text(
              titulo,
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: seleccionada ? AppColors.primary : Colors.black87),
            ),
            Text(
              subtitulo,
              style: const TextStyle(fontSize: 10, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildComponenteOfertaPasajero() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.primary.withOpacity(0.4), width: 2),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Tarifa Legal por Decreto:', style: TextStyle(color: Colors.grey, fontSize: 13)),
              Text(
                '\$ ${_tarifaLegalCalculada.toInt()}',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
              ),
            ],
          ),
          const Divider(height: 20),
          const Text('Tu Oferta al Conductor', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton.filledTonal(
                icon: const Text('-\$2k', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                onPressed: () => setState(() => _ajusteOferta -= 2000.0),
              ),
              const SizedBox(width: 12),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '\$ ${_ofertaFinalPasajero.toInt()}',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.primary),
                ),
              ),
              const SizedBox(width: 12),
              IconButton.filledTonal(
                icon: const Text('+\$2k', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                onPressed: () => setState(() => _ajusteOferta += 2000.0),
              ),
            ],
          ),
          const SizedBox(height: 6),
          Text(
            _ajusteOferta == 0
                ? 'Oferta equivalente a la tarifa oficial'
                : (_ajusteOferta > 0 ? 'Oferta con propina (+ \$${_ajusteOferta.toInt()})' : 'Oferta con descuento (- \$${(-_ajusteOferta).toInt()})'),
            style: TextStyle(
              fontSize: 11,
              color: _ajusteOferta > 0 ? Colors.green : (_ajusteOferta < 0 ? Colors.orange : Colors.grey),
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
