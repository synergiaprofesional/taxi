import 'dart:async';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/payment_model.dart';
import '../../../models/ticket_data_model.dart';
import '../../../models/vehicle_model.dart';
import '../../../services/odoo_service.dart';
import '../../widgets/ticket_preview_dialog.dart';
import 'payment_concept_form.dart';

class PaymentFormView extends StatefulWidget {
  final PagoRecaudoModel? pago; // null => Nuevo pago; != null => Modo consulta

  const PaymentFormView({super.key, this.pago});

  @override
  State<PaymentFormView> createState() => _PaymentFormViewState();
}

class _PaymentFormViewState extends State<PaymentFormView> {
  final odooService = Get.find<OdooService>();
  final turnoController = Get.find<TurnoController>();
  final _formKey = GlobalKey<FormState>();

  bool get esModoConsulta => widget.pago != null;

  late TextEditingController _placaCtrl;
  late TextEditingController _conductorCtrl;
  late TextEditingController _conceptoManualCtrl;
  late TextEditingController _valorManualCtrl;

  VehiculoModel? _vehiculoSeleccionado;
  ConductorModel? _conductorSeleccionado;
  List<VehiculoModel> _vehiculosSugeridos = [];
  bool _isSearchingVehicle = false;
  Timer? _searchDebounce;

  List<ConceptoCobroModel> _catalogoConceptos = [];
  final List<String> _conceptosSugeridos = [
    'Cuota de Sostenimiento',
    'Rodamiento',
    'Planilla',
    'Tarjeta de Control',
    'Aporte Social',
    'BASICO',
  ];

  final List<PaymentConceptLine> _lineas = [];
  bool _isLoading = false;
  bool _isSaving = false;

  final currencyFormat = NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0);

  @override
  void initState() {
    super.initState();
    if (esModoConsulta) {
      _placaCtrl = TextEditingController(text: widget.pago!.placa);
      _conductorCtrl = TextEditingController(text: widget.pago!.conductorNombre);
      _conceptoManualCtrl = TextEditingController(text: widget.pago!.conceptoNombre);
      _valorManualCtrl = TextEditingController(text: widget.pago!.total.toStringAsFixed(0));
    } else {
      _placaCtrl = TextEditingController();
      _conductorCtrl = TextEditingController();
      _conceptoManualCtrl = TextEditingController(text: 'Cuota de Sostenimiento');
      _valorManualCtrl = TextEditingController(text: '15000');
      _cargarConceptosPorDefecto();
    }
  }

  @override
  void dispose() {
    _searchDebounce?.cancel();
    _placaCtrl.dispose();
    _conductorCtrl.dispose();
    _conceptoManualCtrl.dispose();
    _valorManualCtrl.dispose();
    super.dispose();
  }

  Future<void> _cargarConceptosPorDefecto() async {
    setState(() => _isLoading = true);
    final catalogo = await odooService.getConceptosCobro();
    if (mounted) {
      _catalogoConceptos = catalogo;
      final inicial = catalogo.isNotEmpty
          ? catalogo.first
          : ConceptoCobroModel(id: 1, nombre: 'Cuota de Sostenimiento', valorPorDefecto: 15000.0);
      _conceptoManualCtrl.text = inicial.nombre;
      _valorManualCtrl.text = inicial.valorPorDefecto.toStringAsFixed(0);
      _lineas.clear();
      _lineas.add(PaymentConceptLine(
        concepto: inicial,
        cantidad: 1,
        valorUnitario: inicial.valorPorDefecto,
      ));
      setState(() => _isLoading = false);
    }
  }

  void _sincronizarConceptoManual() {
    final nombre = _conceptoManualCtrl.text.trim();
    if (nombre.isEmpty) return;
    final valor = double.tryParse(_valorManualCtrl.text.trim()) ?? 0.0;
    final match = _catalogoConceptos.firstWhereOrNull((c) => c.nombre.toLowerCase() == nombre.toLowerCase());
    final concepto = match ?? ConceptoCobroModel(id: 0, nombre: nombre, valorPorDefecto: valor);

    setState(() {
      if (_lineas.isNotEmpty) {
        _lineas[0] = PaymentConceptLine(
          concepto: concepto,
          cantidad: _lineas[0].cantidad,
          valorUnitario: valor > 0 ? valor : concepto.valorPorDefecto,
        );
      } else {
        _lineas.add(PaymentConceptLine(
          concepto: concepto,
          cantidad: 1,
          valorUnitario: valor,
        ));
      }
    });
  }

  double get _totalRecaudo {
    if (esModoConsulta) return widget.pago!.total;
    if (_lineas.isEmpty) return 0.0;
    return _lineas.map((l) => l.subtotal).reduce((a, b) => a + b);
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

    // Si hay coincidencia exacta de placa (ej: WGM776), autoseleccionar inmediatamente
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

      // Autocompletado del primer conductor real
      if (vehiculo.conductores.isNotEmpty) {
        _conductorSeleccionado = vehiculo.conductores.first;
        _conductorCtrl.text = _conductorSeleccionado!.name;

        // Carga de conceptos asociados al conductor
        if (_conductorSeleccionado!.conceptos.isNotEmpty) {
          _lineas.clear();
          for (final c in _conductorSeleccionado!.conceptos) {
            _lineas.add(PaymentConceptLine(
              concepto: c,
              cantidad: 1,
              valorUnitario: c.valorPorDefecto,
            ));
          }
          final primerC = _conductorSeleccionado!.conceptos.first;
          _conceptoManualCtrl.text = primerC.nombre;
          _valorManualCtrl.text = primerC.valorPorDefecto.toStringAsFixed(0);
        }
      }
    });
  }

  void _abrirAgregarConcepto() async {
    final linea = await PaymentConceptForm.show(context);
    if (linea != null && mounted) {
      setState(() {
        _lineas.add(linea);
      });
    }
  }

  void _eliminarConcepto(int index) {
    setState(() {
      _lineas.removeAt(index);
    });
  }

  void _guardarPago() async {
    if (_formKey.currentState?.validate() != true) return;
    _sincronizarConceptoManual();

    if (_lineas.isEmpty) {
      Get.snackbar('Sin conceptos', 'Agregue al menos un concepto de cobro',
          backgroundColor: AppColors.error, colorText: Colors.white);
      return;
    }

    setState(() => _isSaving = true);
    final placa = _placaCtrl.text.trim().toUpperCase();
    final conductor = _conductorCtrl.text.trim();
    final total = _totalRecaudo;
    final conceptoDesc = _lineas.map((l) => l.concepto.nombre).join(', ');

    try {
      if (odooService.isAuthenticated.value) {
        await odooService.crearPago({
          'bahia_id': turnoController.bahiaIdActual.value,
          'vehiculo_id': _vehiculoSeleccionado?.id ?? false,
          'conductor_id': _conductorSeleccionado?.id ?? false,
          'placa': placa,
          'conductor': conductor,
          'total': total,
          'valor': total,
          'nota': conceptoDesc,
          'concepto_ids': _lineas.map((l) => [0, 0, l.toOdooRpc()]).toList(),
        });
        await turnoController.cargarPagosDesdeServidor();
      }

      final ticket = TicketDataModel(
        bahiaNombre: turnoController.bahiaSeleccionada.value,
        turnoNumero: 'REC-NUEVO',
        placa: placa,
        conductor: conductor,
        destino: conceptoDesc,
        fechaHora: DateTime.now(),
        valorTotal: total,
        cajero: odooService.usuarioActivo.value,
      );
      await turnoController.printerService.imprimirTicket(ticket);

      Get.back();
      Get.snackbar('Recaudo Guardado', 'Pago por ${currencyFormat.format(total)} ($conceptoDesc) registrado exitosamente',
          backgroundColor: AppColors.success, colorText: Colors.black);
    } catch (e) {
      Get.snackbar('Error', 'No se pudo guardar el pago: $e',
          backgroundColor: AppColors.error, colorText: Colors.white);
    } finally {
      if (mounted) setState(() => _isSaving = false);
    }
  }

  void _imprimirRecibo() {
    final p = widget.pago!;
    TicketPreviewDialog.show(
      context,
      consecutivo: p.consecutivo,
      placa: p.placa,
      conductor: p.conductorNombre,
      bahia: p.bahiaNombre,
      destino: 'Recaudo Oficial',
      total: p.total,
      fecha: p.fecha,
      printerService: turnoController.printerService,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(esModoConsulta ? widget.pago!.consecutivo : 'Nuevo Recaudo de Caja'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppColors.primary))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Campo Placa
                    TextFormField(
                      controller: _placaCtrl,
                      readOnly: esModoConsulta,
                      textCapitalization: TextCapitalization.characters,
                      decoration: InputDecoration(
                        labelText: 'Placa del Vehículo',
                        hintText: 'Ej: WBD512',
                        prefixIcon: const Icon(Icons.local_taxi, color: AppColors.primary),
                        suffixIcon: _isSearchingVehicle
                            ? const SizedBox(width: 20, height: 20, child: Padding(padding: EdgeInsets.all(12), child: CircularProgressIndicator(strokeWidth: 2)))
                            : null,
                        filled: true,
                        fillColor: AppColors.surface,
                      ),
                      validator: (val) => val == null || val.trim().isEmpty ? 'Ingrese la placa' : null,
                      onChanged: (val) {
                        if (!esModoConsulta) _onPlacaChanged(val);
                      },
                    ),

                    if (_vehiculosSugeridos.isNotEmpty)
                      Container(
                        margin: const EdgeInsets.symmetric(vertical: 8),
                        decoration: BoxDecoration(
                          color: AppColors.surfaceElevated,
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: Colors.white24),
                        ),
                        child: ListView.separated(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: _vehiculosSugeridos.length,
                          separatorBuilder: (_, _) => const Divider(height: 1),
                          itemBuilder: (ctx, idx) {
                            final v = _vehiculosSugeridos[idx];
                            return ListTile(
                              dense: true,
                              leading: const Icon(Icons.check_circle_outline, color: AppColors.primary),
                              title: Text(v.placa, style: const TextStyle(fontWeight: FontWeight.bold)),
                              subtitle: Text(v.conductores.isNotEmpty ? v.conductores.first.name : 'Sin conductor asignado'),
                              onTap: () => _seleccionarVehiculo(v),
                            );
                          },
                        ),
                      ),

                    const SizedBox(height: 12),

                    // Campo Conductor
                    TextFormField(
                      controller: _conductorCtrl,
                      readOnly: esModoConsulta,
                      textCapitalization: TextCapitalization.words,
                      decoration: const InputDecoration(
                        labelText: 'Conductor',
                        hintText: 'Ej: Carlos Ramírez',
                        prefixIcon: Icon(Icons.person, color: AppColors.primary),
                        filled: true,
                        fillColor: AppColors.surface,
                      ),
                      validator: (val) => val == null || val.trim().isEmpty ? 'Ingrese el conductor' : null,
                    ),

                    const SizedBox(height: 16),

                    // Sección de Tipo de Pago / Concepto (Escritura Manual + Autocomplete)
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.surface,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.white12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Row(
                            children: [
                              Icon(Icons.edit_note, color: AppColors.primary, size: 20),
                              SizedBox(width: 8),
                              Text(
                                'Tipo de Pago / Concepto',
                                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),

                          if (!esModoConsulta) ...[
                            TextFormField(
                              controller: _conceptoManualCtrl,
                              onChanged: (val) {
                                final match = _catalogoConceptos.firstWhereOrNull(
                                    (c) => c.nombre.toLowerCase().trim() == val.toLowerCase().trim());
                                if (match != null && match.valorPorDefecto > 0) {
                                  _valorManualCtrl.text = match.valorPorDefecto.toStringAsFixed(0);
                                }
                                _sincronizarConceptoManual();
                              },
                              decoration: const InputDecoration(
                                labelText: 'Escriba o Seleccione el Tipo de Pago',
                                hintText: 'Ej: Cuota de Sostenimiento, Rodamiento, Planilla...',
                                prefixIcon: Icon(Icons.category, color: AppColors.primary),
                                filled: true,
                                fillColor: AppColors.surfaceElevated,
                              ),
                              validator: (val) => val == null || val.trim().isEmpty ? 'Ingrese el tipo de pago' : null,
                            ),
                            const SizedBox(height: 8),
                            Wrap(
                              spacing: 6,
                              runSpacing: 4,
                              children: _conceptosSugeridos.map((s) {
                                return ActionChip(
                                  label: Text(s, style: const TextStyle(fontSize: 11)),
                                  backgroundColor: AppColors.surfaceElevated,
                                  onPressed: () {
                                    _conceptoManualCtrl.text = s;
                                    final match = _catalogoConceptos.firstWhereOrNull((c) => c.nombre.toLowerCase() == s.toLowerCase());
                                    if (match != null && match.valorPorDefecto > 0) {
                                      _valorManualCtrl.text = match.valorPorDefecto.toStringAsFixed(0);
                                    }
                                    _sincronizarConceptoManual();
                                  },
                                );
                              }).toList(),
                            ),
                            const SizedBox(height: 12),
                            TextFormField(
                              controller: _valorManualCtrl,
                              keyboardType: TextInputType.number,
                              decoration: const InputDecoration(
                                labelText: 'Valor a Recaudar (\$)',
                                hintText: 'Ej: 15000',
                                prefixIcon: Icon(Icons.attach_money, color: AppColors.primary),
                                filled: true,
                                fillColor: AppColors.surfaceElevated,
                              ),
                              onChanged: (_) => _sincronizarConceptoManual(),
                              validator: (val) {
                                final n = double.tryParse(val ?? '');
                                if (n == null || n <= 0) return 'Ingrese un valor mayor a 0';
                                return null;
                              },
                            ),
                          ] else ...[
                            TextFormField(
                              controller: _conceptoManualCtrl,
                              readOnly: true,
                              decoration: const InputDecoration(
                                labelText: 'Concepto Registrado',
                                prefixIcon: Icon(Icons.receipt, color: AppColors.primary),
                                filled: true,
                                fillColor: AppColors.surfaceElevated,
                              ),
                            ),
                            const SizedBox(height: 10),
                            TextFormField(
                              controller: _valorManualCtrl,
                              readOnly: true,
                              decoration: const InputDecoration(
                                labelText: 'Valor Registrado (\$)',
                                prefixIcon: Icon(Icons.attach_money, color: AppColors.primary),
                                filled: true,
                                fillColor: AppColors.surfaceElevated,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),

                    const SizedBox(height: 16),

                    // Sub-Lista de Conceptos Adicionales si hubiere más de 1
                    if (!esModoConsulta) ...[
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Otros Conceptos Adicionales', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          TextButton.icon(
                            onPressed: _abrirAgregarConcepto,
                            icon: const Icon(Icons.add, color: AppColors.primary, size: 18),
                            label: const Text('Agregar Otro', style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 13)),
                          ),
                        ],
                      ),
                      if (_lineas.length > 1)
                        ListView.separated(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: _lineas.length - 1,
                          separatorBuilder: (_, _) => const Divider(height: 1),
                          itemBuilder: (ctx, idx) {
                            final linea = _lineas[idx + 1];
                            return Container(
                              margin: const EdgeInsets.symmetric(vertical: 4),
                              decoration: BoxDecoration(
                                color: AppColors.surface,
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: ListTile(
                                dense: true,
                                title: Text(linea.concepto.nombre, style: const TextStyle(fontWeight: FontWeight.bold)),
                                subtitle: Text('${linea.cantidad} x ${currencyFormat.format(linea.valorUnitario)}'),
                                trailing: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Text(currencyFormat.format(linea.subtotal), style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.success)),
                                    IconButton(
                                      icon: const Icon(Icons.close, color: Colors.grey, size: 20),
                                      onPressed: () => _eliminarConcepto(idx + 1),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                    ],

                    const SizedBox(height: 24),

                    // Footer Total
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppColors.primary.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppColors.primary.withValues(alpha: 0.5)),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('TOTAL RECAUDO:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                          Text(
                            currencyFormat.format(_totalRecaudo),
                            style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 22, color: AppColors.success),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 24),

                    if (esModoConsulta)
                      ElevatedButton.icon(
                        onPressed: _imprimirRecibo,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green.shade600,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        icon: const Icon(Icons.print, color: Colors.white, size: 22),
                        label: const Text('REIMPRIMIR COMPROBANTE', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                      )
                    else
                      ElevatedButton.icon(
                        onPressed: _isSaving ? null : _guardarPago,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primary,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        icon: _isSaving
                            ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black))
                            : const Icon(Icons.save, color: Colors.black, size: 22),
                        label: const Text('GUARDAR E IMPRIMIR RECIBO', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
                      ),
                  ],
                ),
              ),
            ),
    );
  }
}
