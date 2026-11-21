import 'dart:async';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/payment_model.dart';
import '../../../models/vehicle_model.dart';
import '../../../services/odoo_service.dart';
import '../../../services/printer_service.dart';

class PagoDialog extends StatefulWidget {
  final String? placaInicial;
  final String? conductorInicial;
  final int bahiaId;
  final String bahiaNombre;

  const PagoDialog({
    super.key,
    this.placaInicial,
    this.conductorInicial,
    required this.bahiaId,
    required this.bahiaNombre,
  });

  @override
  State<PagoDialog> createState() => _PagoDialogState();
}

class _PagoDialogState extends State<PagoDialog> {
  final odooService = Get.find<OdooService>();
  final printerService = Get.find<PrinterService>();

  final _formKey = GlobalKey<FormState>();
  late TextEditingController _placaCtrl;
  late TextEditingController _conductorCtrl;

  List<VehiculoModel> _vehiculosSugeridos = [];
  bool _isSearchingVehicle = false;
  VehiculoModel? _vehiculoSeleccionado;
  Timer? _searchDebounce;

  List<ConceptoCobroModel> _catalogoConceptos = [];
  final List<PaymentConceptLine> _lineasCobro = [];
  bool _isLoading = true;
  bool _isSaving = false;

  @override
  void initState() {
    super.initState();
    _placaCtrl = TextEditingController(text: widget.placaInicial ?? '');
    _conductorCtrl = TextEditingController(text: widget.conductorInicial ?? '');
    _cargarConceptos();
  }

  @override
  void dispose() {
    _searchDebounce?.cancel();
    _placaCtrl.dispose();
    _conductorCtrl.dispose();
    super.dispose();
  }

  Future<void> _cargarConceptos() async {
    setState(() => _isLoading = true);
    final conceptos = await odooService.getConceptosCobro();
    _catalogoConceptos = conceptos;

    // Agregar el primer concepto obligatorio por defecto (ej. Rodamiento)
    if (_catalogoConceptos.isNotEmpty) {
      _lineasCobro.add(
        PaymentConceptLine(
          concepto: _catalogoConceptos.first,
          cantidad: 1,
          valorUnitario: _catalogoConceptos.first.valorPorDefecto,
        ),
      );
    }
    setState(() => _isLoading = false);
  }

  double get _totalPagar {
    if (_lineasCobro.isEmpty) return 0.0;
    return _lineasCobro.map((l) => l.subtotal).reduce((a, b) => a + b);
  }

  void _onPlacaChanged(String query) {
    _searchDebounce?.cancel();
    final clean = query.trim().toUpperCase();
    if (clean.length < 2) {
      setState(() {
        _vehiculosSugeridos = [];
        _isSearchingVehicle = false;
      });
      return;
    }
    setState(() => _isSearchingVehicle = true);
    _searchDebounce = Timer(const Duration(milliseconds: 250), () async {
      await _buscarVehiculo(clean);
    });
  }

  Future<void> _buscarVehiculo(String query) async {
    final clean = query.trim().toUpperCase();
    final resultados = await odooService.buscarVehiculos(clean);
    if (!mounted) return;

    // Descartar si el texto cambió mientras respondía el servidor (anti-race condition)
    if (_placaCtrl.text.trim().toUpperCase() != clean) return;

    // Filtrado estricto por la subcadena digitada
    final filtrados = resultados.where((v) => v.placa.contains(clean)).toList();

    // Priorizar coincidencias al final (ej: WGN842 con 842)
    filtrados.sort((a, b) {
      final aEnds = a.placa.endsWith(clean) ? 0 : 1;
      final bEnds = b.placa.endsWith(clean) ? 0 : 1;
      if (aEnds != bEnds) return aEnds.compareTo(bEnds);
      return a.placa.compareTo(b.placa);
    });

    setState(() {
      _vehiculosSugeridos = filtrados;
      _isSearchingVehicle = false;
    });

    if (clean.length >= 6) {
      final exacto = filtrados.firstWhereOrNull((v) => v.placa == clean);
      if (exacto != null) {
        _seleccionarVehiculo(exacto);
      }
    }
  }

  void _seleccionarVehiculo(VehiculoModel vehiculo) {
    setState(() {
      _vehiculoSeleccionado = vehiculo;
      _placaCtrl.text = vehiculo.placa;
      _vehiculosSugeridos = [];

      if (vehiculo.conductores.isNotEmpty) {
        _conductorCtrl.text = vehiculo.conductores.first.name;
      }
    });
  }

  void _agregarConcepto() {
    if (_catalogoConceptos.isEmpty) return;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) => Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Seleccionar Concepto de Recaudo',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            ..._catalogoConceptos.map((concepto) => ListTile(
              title: Text(concepto.nombre, style: const TextStyle(fontWeight: FontWeight.w600)),
              trailing: Text(
                NumberFormat.currency(symbol: '\$', decimalDigits: 0).format(concepto.valorPorDefecto),
                style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold),
              ),
              onTap: () {
                setState(() {
                  _lineasCobro.add(
                    PaymentConceptLine(
                      concepto: concepto,
                      cantidad: 1,
                      valorUnitario: concepto.valorPorDefecto,
                    ),
                  );
                });
                Navigator.pop(ctx);
              },
            )),
          ],
        ),
      ),
    );
  }

  Future<void> _guardarEImprimirRecaudo() async {
    if (!_formKey.currentState!.validate()) return;
    if (_lineasCobro.isEmpty) {
      Get.snackbar('Error', 'Debe incluir al menos un concepto de cobro.', backgroundColor: AppColors.error, colorText: Colors.white);
      return;
    }

    setState(() => _isSaving = true);
    final placa = _placaCtrl.text.trim().toUpperCase();
    final conductor = _conductorCtrl.text.trim();
    final consecutivo = 'REC-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}';

    final nuevoPago = PagoRecaudoModel(
      id: DateTime.now().millisecondsSinceEpoch,
      consecutivo: consecutivo,
      bahiaId: widget.bahiaId,
      bahiaNombre: widget.bahiaNombre,
      vehiculoId: _vehiculoSeleccionado?.id ?? 0,
      placa: placa,
      conductorId: _vehiculoSeleccionado?.conductores.isNotEmpty == true ? _vehiculoSeleccionado!.conductores.first.id : 0,
      conductorNombre: conductor,
      fecha: DateTime.now(),
      total: _totalPagar,
      lineas: List.from(_lineasCobro),
    );

    // Enviar a Odoo en segundo plano si está online
    if (odooService.isAuthenticated.value) {
      await odooService.crearPago(nuevoPago.toOdooJson());
    }

    setState(() => _isSaving = false);
    Get.back(result: nuevoPago);

    Get.snackbar(
      'Recaudo Exitoso',
      'Pago registrado con consecutivo $consecutivo por valor de ${NumberFormat.currency(symbol: '\$', decimalDigits: 0).format(_totalPagar)}',
      backgroundColor: AppColors.success,
      colorText: Colors.white,
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  @override
  Widget build(BuildContext context) {
    final currency = NumberFormat.currency(symbol: '\$', decimalDigits: 0);

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 580, maxHeight: 720),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Encabezado
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Nuevo Recaudo de Caja',
                                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                              ),
                              Text(
                                widget.bahiaNombre,
                                style: TextStyle(color: Theme.of(context).textTheme.bodySmall?.color, fontSize: 13),
                              ),
                            ],
                          ),
                          IconButton(
                            icon: const Icon(Icons.close),
                            onPressed: () => Navigator.pop(context),
                          ),
                        ],
                      ),
                      const Divider(height: 24),

                      // Campos de Placa y Conductor
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Expanded(
                            flex: 2,
                            child: TextFormField(
                              controller: _placaCtrl,
                              textCapitalization: TextCapitalization.characters,
                              decoration: InputDecoration(
                                labelText: 'Placa del Taxi',
                                hintText: 'WBD512',
                                prefixIcon: const Icon(Icons.local_taxi),
                                suffixIcon: _isSearchingVehicle
                                    ? const SizedBox(
                                        width: 18,
                                        height: 18,
                                        child: Padding(
                                          padding: EdgeInsets.all(12),
                                          child: CircularProgressIndicator(strokeWidth: 2),
                                        ),
                                      )
                                    : (_placaCtrl.text.isNotEmpty
                                        ? IconButton(
                                            icon: const Icon(Icons.clear, size: 18),
                                            onPressed: () {
                                              _placaCtrl.clear();
                                              setState(() {
                                                _vehiculoSeleccionado = null;
                                                _vehiculosSugeridos = [];
                                              });
                                            },
                                          )
                                        : null),
                              ),
                              validator: (val) => val == null || val.trim().isEmpty ? 'Requerido' : null,
                              onChanged: _onPlacaChanged,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            flex: 3,
                            child: TextFormField(
                              controller: _conductorCtrl,
                              decoration: const InputDecoration(
                                labelText: 'Nombre Conductor',
                                prefixIcon: Icon(Icons.person),
                              ),
                              validator: (val) => val == null || val.trim().isEmpty ? 'Requerido' : null,
                            ),
                          ),
                        ],
                      ),

                      // Lista desplegable de sugerencias de vehículos
                      if (_vehiculosSugeridos.isNotEmpty)
                        Container(
                          margin: const EdgeInsets.only(top: 8, bottom: 4),
                          constraints: const BoxConstraints(maxHeight: 180),
                          decoration: BoxDecoration(
                            color: Theme.of(context).cardColor,
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: AppColors.primary.withValues(alpha: 0.5), width: 1.2),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withValues(alpha: 0.3),
                                blurRadius: 6,
                                offset: const Offset(0, 3),
                              ),
                            ],
                          ),
                          child: ListView.separated(
                            shrinkWrap: true,
                            itemCount: _vehiculosSugeridos.length,
                            separatorBuilder: (_, _) => const Divider(height: 1),
                            itemBuilder: (ctx, idx) {
                              final v = _vehiculosSugeridos[idx];
                              return ListTile(
                                dense: true,
                                leading: const Icon(Icons.local_taxi, color: AppColors.primary, size: 20),
                                title: Text(v.placa, style: const TextStyle(fontWeight: FontWeight.bold)),
                                subtitle: Text(v.conductores.isNotEmpty ? v.conductores.first.name : 'Conductor General'),
                                trailing: v.numeroInterno.isNotEmpty
                                    ? Chip(
                                        label: Text('Móvil ${v.numeroInterno}', style: const TextStyle(fontSize: 11)),
                                        visualDensity: VisualDensity.compact,
                                        padding: EdgeInsets.zero,
                                      )
                                    : null,
                                onTap: () => _seleccionarVehiculo(v),
                              );
                            },
                          ),
                        ),
                      const SizedBox(height: 16),

                      // Detalle de Conceptos
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'CONCEPTOS COBRADOS',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, letterSpacing: 0.5),
                          ),
                          TextButton.icon(
                            icon: const Icon(Icons.add_circle_outline, size: 18),
                            label: const Text('Agregar Rubro'),
                            onPressed: _agregarConcepto,
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),

                      Expanded(
                        child: Container(
                          decoration: BoxDecoration(
                            border: Border.all(color: Theme.of(context).dividerColor),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: _lineasCobro.isEmpty
                              ? const Center(child: Text('Sin conceptos agregados.'))
                              : ListView.separated(
                                  itemCount: _lineasCobro.length,
                                  separatorBuilder: (_, _) => const Divider(height: 1),
                                  itemBuilder: (ctx, idx) {
                                    final linea = _lineasCobro[idx];
                                    return ListTile(
                                      title: Text(linea.concepto.nombre, style: const TextStyle(fontWeight: FontWeight.w600)),
                                      subtitle: Text('${linea.cantidad}x ${currency.format(linea.valorUnitario)}'),
                                      trailing: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Text(
                                            currency.format(linea.subtotal),
                                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                                          ),
                                          IconButton(
                                            icon: const Icon(Icons.delete_outline, color: AppColors.error, size: 20),
                                            onPressed: () => setState(() => _lineasCobro.removeAt(idx)),
                                          ),
                                        ],
                                      ),
                                    );
                                  },
                                ),
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Total y Botón de Pago
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Theme.of(context).cardColor,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: AppColors.primary, width: 1.2),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text('TOTAL A RECAUDAR:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                            Text(
                              currency.format(_totalPagar),
                              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.primary),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),

                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          backgroundColor: AppColors.primary,
                        ),
                        icon: _isSaving
                            ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2))
                            : const Icon(Icons.print, color: Colors.black),
                        label: Text(
                          _isSaving ? 'REGISTRANDO...' : 'PAGAR E IMPRIMIR RECIBO',
                          style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16),
                        ),
                        onPressed: _isSaving ? null : _guardarEImprimirRecaudo,
                      ),
                    ],
                  ),
                ),
        ),
      ),
    );
  }
}
