import 'dart:async';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import '../../../controllers/turno_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/tarifa_sector_model.dart';
import '../../../models/ticket_data_model.dart';
import '../../../models/turno_model.dart';
import '../../../models/vehicle_model.dart';
import '../../../services/odoo_service.dart';

class TurnoFormView extends StatefulWidget {
  final TurnoModel? turno; // Si es null => Modo Enturnar; si != null => Modo Despachar

  const TurnoFormView({super.key, this.turno});

  @override
  State<TurnoFormView> createState() => _TurnoFormViewState();
}

class _TurnoFormViewState extends State<TurnoFormView> {
  final turnoController = Get.find<TurnoController>();
  final odooService = Get.find<OdooService>();

  bool get esModoDespacho => widget.turno != null;

  // Variables para Enturnar
  bool _esAnonimo = false;
  final TextEditingController _placaCtrl = TextEditingController();
  final TextEditingController _conductorCtrl = TextEditingController();
  VehiculoModel? _vehiculoSeleccionado;
  ConductorModel? _conductorSeleccionado;
  bool _isSearchingVehicle = false;
  List<VehiculoModel> _vehiculosSugeridos = [];
  Timer? _searchDebounce;

  // Variables para Despachar
  TarifaSectorModel? _tarifaSeleccionada;
  final TextEditingController _destinoCtrl = TextEditingController();
  final TextEditingController _tarifaBaseCtrl = TextEditingController();
  final TextEditingController _direccionCtrl = TextEditingController();
  double _tarifaBase = 18000.0;
  bool _aplicaRecargoNocturno = false;
  final double _valorRecargo = 1100.0;
  List<TarifaSectorModel> _tarifasSugeridas = [];

  final List<String> _destinosFrecuentes = [
    'Caribe Plaza',
    'Manga',
    'Bocagrande',
    'Centro Histórico',
    'Pedro Salazar',
    'San Pedro',
    'San Francisco',
    'Manzanillo del Mar',
  ];

  final currencyFormat = NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0);

  @override
  void initState() {
    super.initState();
    if (esModoDespacho) {
      _placaCtrl.text = widget.turno!.placaVisible;
      _conductorCtrl.text = widget.turno!.conductorNombre;
      _direccionCtrl.text = widget.turno!.nota;
      _tarifaBaseCtrl.text = _tarifaBase.toStringAsFixed(0);
      _calcularRecargoNocturnoAutomatico();
      _inicializarTarifa();
    }
  }

  void _inicializarTarifa() async {
    if (turnoController.tarifasDisponibles.isEmpty) {
      await turnoController.cargarTarifasDesdeServidor();
    }
    if (mounted && turnoController.tarifasDisponibles.isNotEmpty) {
      setState(() {
        if (widget.turno!.tarifaId > 0) {
          _tarifaSeleccionada = turnoController.tarifasDisponibles
              .firstWhereOrNull((t) => t.id == widget.turno!.tarifaId);
        }
        // Novedad Fundetaxcol: Preseleccionar prioritariamente "Caribe Plaza" como destino de salida
        _tarifaSeleccionada ??= turnoController.tarifasDisponibles
                .firstWhereOrNull((t) => t.name.toUpperCase().contains('CARIBE PLAZA')) ??
            turnoController.tarifasDisponibles.first;
        _tarifaBase = _tarifaSeleccionada!.valor;
        _destinoCtrl.text = _tarifaSeleccionada!.name;
        _tarifaBaseCtrl.text = _tarifaBase.toStringAsFixed(0);
      });
    }
  }

  void _seleccionarDestinoTexto(String destino) {
    final cleanDestino = destino.trim();
    if (cleanDestino.isEmpty) {
      setState(() {
        _destinoCtrl.text = '';
        _tarifaSeleccionada = null;
        _tarifaBase = 0.0;
        _tarifaBaseCtrl.clear();
        _tarifasSugeridas = [];
      });
      return;
    }

    final match = turnoController.tarifasDisponibles.firstWhereOrNull(
      (t) => t.name.toLowerCase().trim() == cleanDestino.toLowerCase(),
    );
    setState(() {
      _destinoCtrl.text = destino;
      if (match != null) {
        _tarifaSeleccionada = match;
        _tarifaBase = match.valor;
        _tarifaBaseCtrl.text = match.valor.toStringAsFixed(0);
      } else {
        _tarifaSeleccionada = null;
      }
      _tarifasSugeridas = [];
    });
  }

  void _buscarDestinosSugeridos(String query) {
    final q = query.trim().toLowerCase();
    if (q.isEmpty) {
      setState(() {
        _tarifaSeleccionada = null;
        _tarifaBase = 0.0;
        _tarifaBaseCtrl.clear();
        _tarifasSugeridas = [];
      });
      return;
    }
    _seleccionarDestinoTexto(query);
    final matches = turnoController.tarifasDisponibles.where((t) {
      return t.name.toLowerCase().contains(q);
    }).take(8).toList();
    setState(() => _tarifasSugeridas = matches);
  }

  @override
  void dispose() {
    _searchDebounce?.cancel();
    _placaCtrl.dispose();
    _conductorCtrl.dispose();
    _destinoCtrl.dispose();
    _tarifaBaseCtrl.dispose();
    _direccionCtrl.dispose();
    super.dispose();
  }

  void _calcularRecargoNocturnoAutomatico() {
    final now = DateTime.now();
    // Novedad Fundetaxcol: Recargo nocturno aplica a partir de las 19:00 (7:00 p.m.) hasta las 05:00 a.m.
    if (now.hour >= 19 || now.hour < 5) {
      _aplicaRecargoNocturno = true;
    }
  }

  double get _totalDespacho {
    if (_destinoCtrl.text.trim().isEmpty) return 0.0;
    final base = double.tryParse(_tarifaBaseCtrl.text.trim()) ?? (_tarifaSeleccionada?.valor ?? _tarifaBase);
    final recargo = _aplicaRecargoNocturno ? _valorRecargo : 0.0;
    return base + recargo;
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

    // Regla de Exclusión: No sugerir taxis que ya están en la cola de turnos en espera
    final placasEnTurno = turnoController.turnos
        .where((t) => !t.esDespacho && t.estado != EstadoTurno.cancelado)
        .map((t) => t.placaVisible.toUpperCase())
        .toSet();

    // Filtrado estricto por subcadena
    final filtrados = resultados
        .where((v) => v.placa.contains(clean) && !placasEnTurno.contains(v.placa.toUpperCase()))
        .toList();

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

      // Autocompleta inmediatamente el primer conductor registrado
      if (vehiculo.conductores.isNotEmpty) {
        _conductorSeleccionado = vehiculo.conductores.first;
        _conductorCtrl.text = _conductorSeleccionado!.name;
      }
    });
  }

  void _guardarEnturnar() async {
    final placa = _placaCtrl.text.trim().toUpperCase();
    final conductor = _conductorCtrl.text.trim();

    if (placa.isEmpty) {
      Get.snackbar('Campo Requerido', 'Por favor ingrese la placa del vehículo',
          backgroundColor: AppColors.error, colorText: Colors.white);
      return;
    }

    await turnoController.enturnarVehiculo(
      placa: placa,
      conductor: conductor.isNotEmpty ? conductor : 'Conductor General',
      vehiculoId: _vehiculoSeleccionado?.id,
      conductorId: _conductorSeleccionado?.id,
    );
    if (_vehiculoSeleccionado != null) {
      debugPrint('[TurnoFormView] Vehículo formal registrado: ${_vehiculoSeleccionado!.placa} (ID: ${_vehiculoSeleccionado!.id})');
    }

    Get.back();
    Get.snackbar('Turno Asignado', 'Vehículo $placa enturnado exitosamente',
        backgroundColor: AppColors.success, colorText: Colors.black);
  }

  void _ejecutarDespacho() async {
    final turno = widget.turno!;
    final total = _totalDespacho;
    final destinoNombre = _destinoCtrl.text.trim().isNotEmpty
        ? _destinoCtrl.text.trim()
        : (_tarifaSeleccionada?.name ?? 'Despacho Salida');

    // Actualiza el turno en el servidor con tarifaId oficial o nota personalizada
    await turnoController.despacharTurno(
      turno.id,
      tarifaId: _tarifaSeleccionada?.id,
      valor: total,
      nota: _direccionCtrl.text.trim().isNotEmpty
          ? '${_direccionCtrl.text.trim()} ($destinoNombre)'
          : destinoNombre,
    );

    final ticket = TicketDataModel(
      bahiaNombre: turno.bahiaNombre,
      turnoNumero: turno.name,
      placa: turno.placaVisible,
      conductor: turno.conductorNombre,
      destino: destinoNombre,
      direccion: _direccionCtrl.text.trim(),
      turnoId: turno.id,
      fechaHora: DateTime.now(),
      valorTotal: total,
      cajero: odooService.usuarioActivo.value,
    );
    await turnoController.printerService.imprimirTicket(ticket);

    Get.back();
    Get.snackbar('Turno Despachado', 'Despacho a $destinoNombre registrado e impreso exitosamente',
        backgroundColor: AppColors.success, colorText: Colors.black);
  }

  void _cancelarTurno() async {
    final turno = widget.turno!;
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Cancelar Turno'),
        content: Text('¿Está seguro de cancelar el turno de ${turno.placaVisible}?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('No')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppColors.error),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Sí, Cancelar', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );

    if (confirmar == true) {
      await turnoController.cancelarTurno(turno.id);
      Get.back();
      Get.snackbar('Turno Cancelado', 'El turno ha sido cancelado',
          backgroundColor: AppColors.warning, colorText: Colors.black);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(esModoDespacho
            ? 'Despachar: ${widget.turno!.placaVisible}'
            : 'Nuevo Turno (Enturnar)'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: esModoDespacho ? _buildFormDespachar() : _buildFormEnturnar(),
      ),
    );
  }

  Widget _buildFormEnturnar() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Switch de Turno Anónimo
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Row(
                children: [
                  Icon(Icons.visibility_off_outlined, color: AppColors.primary),
                  SizedBox(width: 10),
                  Text('Turno Anónimo / Foráneo', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                ],
              ),
              Switch(
                value: _esAnonimo,
                activeThumbColor: AppColors.primary,
                onChanged: (val) {
                  setState(() {
                    _esAnonimo = val;
                    if (val) {
                      _vehiculoSeleccionado = null;
                      _conductorSeleccionado = null;
                      _conductorCtrl.text = 'Conductor Externo';
                    } else {
                      _conductorCtrl.clear();
                    }
                  });
                },
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // Campo de Placa
        TextField(
          controller: _placaCtrl,
          textCapitalization: TextCapitalization.characters,
          maxLength: 6,
          decoration: InputDecoration(
            labelText: 'Placa del Taxi',
            hintText: 'Ej: WBD512',
            prefixIcon: const Icon(Icons.local_taxi, color: AppColors.primary),
            suffixIcon: _isSearchingVehicle
                ? const SizedBox(width: 20, height: 20, child: Padding(padding: EdgeInsets.all(12), child: CircularProgressIndicator(strokeWidth: 2)))
                : null,
            filled: true,
            fillColor: _esAnonimo ? Colors.deepPurple.shade900.withValues(alpha: 0.3) : AppColors.surface,
          ),
          onChanged: (val) {
            if (!_esAnonimo) _onPlacaChanged(val);
          },
        ),

        // Sugerencias de vehículos registrados
        if (_vehiculosSugeridos.isNotEmpty)
          Container(
            margin: const EdgeInsets.only(bottom: 12),
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

        // Campo de Conductor
        TextField(
          controller: _conductorCtrl,
          textCapitalization: TextCapitalization.words,
          decoration: const InputDecoration(
            labelText: 'Conductor',
            hintText: 'Ej: Carlos Ramírez',
            prefixIcon: Icon(Icons.person, color: AppColors.primary),
            filled: true,
            fillColor: AppColors.surface,
          ),
        ),

        const SizedBox(height: 24),

        ElevatedButton.icon(
          onPressed: _guardarEnturnar,
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          icon: const Icon(Icons.check, color: Colors.black, size: 22),
          label: const Text('ENTURNAR VEHÍCULO', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
        ),
      ],
    );
  }

  Widget _buildFormDespachar() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Datos fijos de solo lectura
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white12),
          ),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Placa:', style: TextStyle(color: Colors.grey)),
                  Text(widget.turno!.placaVisible, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: AppColors.primary)),
                ],
              ),
              const Divider(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Conductor:', style: TextStyle(color: Colors.grey)),
                  Text(widget.turno!.conductorNombre, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                ],
              ),
              const Divider(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Bahía:', style: TextStyle(color: Colors.grey)),
                  Text(widget.turno!.bahiaNombre, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.lightBlueAccent)),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // Selector / Entrada Manual de Destino (Odoo 11 + Escritura Libre)
        const Text('Destino / Tarifa (Escriba o Seleccione):', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 8),

        TextFormField(
          controller: _destinoCtrl,
          onChanged: _buscarDestinosSugeridos,
          decoration: InputDecoration(
            labelText: 'Destino',
            hintText: 'Ej: Manga, Manzanillo, Pedro Salazar, San Pedro...',
            prefixIcon: const Icon(Icons.location_on, color: AppColors.primary),
            suffixIcon: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (_tarifaSeleccionada != null)
                  Container(
                    margin: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.primary.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      currencyFormat.format(_tarifaSeleccionada!.valor),
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: AppColors.taxiYellowLight),
                    ),
                  ),
                if (_destinoCtrl.text.isNotEmpty)
                  IconButton(
                    icon: const Icon(Icons.clear, size: 18),
                    onPressed: () {
                      _destinoCtrl.clear();
                      setState(() {
                        _tarifaSeleccionada = null;
                        _tarifaBase = 0.0;
                        _tarifaBaseCtrl.clear();
                        _tarifasSugeridas = [];
                      });
                    },
                  ),
              ],
            ),
            filled: true,
            fillColor: AppColors.surface,
          ),
        ),

        // Lista de sugerencias al escribir destino
        if (_tarifasSugeridas.isNotEmpty)
          Container(
            margin: const EdgeInsets.only(top: 4, bottom: 8),
            decoration: BoxDecoration(
              color: AppColors.surfaceElevated,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: AppColors.primary.withValues(alpha: 0.3)),
            ),
            child: ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _tarifasSugeridas.length,
              separatorBuilder: (_, _) => const Divider(height: 1),
              itemBuilder: (ctx, idx) {
                final t = _tarifasSugeridas[idx];
                return ListTile(
                  dense: true,
                  leading: const Icon(Icons.place_outlined, color: AppColors.primary, size: 18),
                  title: Text(t.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                  trailing: Text(
                    currencyFormat.format(t.valor),
                    style: const TextStyle(color: AppColors.success, fontWeight: FontWeight.bold, fontSize: 13),
                  ),
                  onTap: () => _seleccionarDestinoTexto(t.name),
                );
              },
            ),
          ),

        const SizedBox(height: 8),

        // Chips de Destinos Frecuentes para selección rápida con un toque
        Wrap(
          spacing: 6,
          runSpacing: 4,
          children: _destinosFrecuentes.map((d) {
            final isSelected = _destinoCtrl.text.toLowerCase().trim() == d.toLowerCase().trim();
            return ActionChip(
              label: Text(d, style: TextStyle(fontSize: 11, fontWeight: isSelected ? FontWeight.bold : FontWeight.normal)),
              backgroundColor: isSelected ? AppColors.primary.withValues(alpha: 0.3) : AppColors.surface,
              onPressed: () {
                if (isSelected) {
                  _seleccionarDestinoTexto('');
                } else {
                  _seleccionarDestinoTexto(d);
                }
              },
            );
          }).toList(),
        ),

        const SizedBox(height: 12),

        // Tarifa Base Editable
        TextFormField(
          controller: _tarifaBaseCtrl,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(
            labelText: 'Tarifa Base (\$)',
            hintText: 'Ej: 18000',
            prefixIcon: Icon(Icons.attach_money, color: AppColors.primary),
            filled: true,
            fillColor: AppColors.surface,
          ),
          onChanged: (val) {
            final parsed = double.tryParse(val.trim());
            if (parsed != null && parsed >= 0) {
              setState(() => _tarifaBase = parsed);
            }
          },
        ),

        const SizedBox(height: 16),

        // Campo de Dirección / Referencia Específica
        const Text('Dirección / Referencia de Destino:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 8),
        TextFormField(
          controller: _direccionCtrl,
          decoration: const InputDecoration(
            labelText: 'Dirección o Punto de Llegada',
            hintText: 'Ej: Hotel Hilton Cra 1 # 1-1, Calle 30 # 20-15',
            prefixIcon: Icon(Icons.location_on_outlined, color: AppColors.primary),
            filled: true,
            fillColor: AppColors.surface,
          ),
        ),

        const SizedBox(height: 16),

        // Recargo Nocturno
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Recargo Nocturno / Festivo', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text('+ \$ 1.100 (Automático 7:00 PM - 5:00 AM)', style: TextStyle(fontSize: 11, color: Colors.grey)),
                ],
              ),
              Switch(
                value: _aplicaRecargoNocturno,
                activeThumbColor: AppColors.primary,
                onChanged: (val) => setState(() => _aplicaRecargoNocturno = val),
              ),
            ],
          ),
        ),

        const SizedBox(height: 20),

        // Total
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
              const Text('TOTAL A COBRAR:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text(
                currencyFormat.format(_totalDespacho),
                style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 22, color: AppColors.success),
              ),
            ],
          ),
        ),

        const SizedBox(height: 24),

        // Botón de Despacho
        ElevatedButton.icon(
          onPressed: _ejecutarDespacho,
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          icon: const Icon(Icons.print, color: Colors.black, size: 22),
          label: const Text('DESPACHAR E IMPRIMIR', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
        ),

        const SizedBox(height: 12),

        // Botón de Cancelar Turno
        OutlinedButton.icon(
          onPressed: _cancelarTurno,
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.error,
            side: const BorderSide(color: AppColors.error),
            padding: const EdgeInsets.symmetric(vertical: 12),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          icon: const Icon(Icons.cancel_outlined, size: 20),
          label: const Text('CANCELAR ESTE TURNO'),
        ),
      ],
    );
  }
}
