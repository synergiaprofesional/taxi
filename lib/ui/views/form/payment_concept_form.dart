import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/payment_model.dart';
import '../../../services/odoo_service.dart';

class PaymentConceptForm extends StatefulWidget {
  const PaymentConceptForm({super.key});

  static Future<PaymentConceptLine?> show(BuildContext context) {
    return Navigator.push<PaymentConceptLine>(
      context,
      MaterialPageRoute(builder: (ctx) => const PaymentConceptForm()),
    );
  }

  @override
  State<PaymentConceptForm> createState() => _PaymentConceptFormState();
}

class _PaymentConceptFormState extends State<PaymentConceptForm> {
  final odooService = Get.find<OdooService>();
  final _formKey = GlobalKey<FormState>();

  List<ConceptoCobroModel> _conceptos = [];
  ConceptoCobroModel? _conceptoSeleccionado;
  bool _isLoading = true;

  late TextEditingController _conceptoNombreCtrl;
  late TextEditingController _cantidadCtrl;
  late TextEditingController _valorCtrl;

  final List<String> _conceptosSugeridos = [
    'Cuota de Sostenimiento',
    'Rodamiento',
    'Planilla',
    'Tarjeta de Control',
    'Aporte Social',
    'BASICO',
  ];

  @override
  void initState() {
    super.initState();
    _conceptoNombreCtrl = TextEditingController();
    _cantidadCtrl = TextEditingController(text: '1');
    _valorCtrl = TextEditingController(text: '0');
    _cargarCatalogo();
  }

  @override
  void dispose() {
    _conceptoNombreCtrl.dispose();
    _cantidadCtrl.dispose();
    _valorCtrl.dispose();
    super.dispose();
  }

  Future<void> _cargarCatalogo() async {
    setState(() => _isLoading = true);
    final lista = await odooService.getConceptosCobro();
    setState(() {
      _conceptos = lista;
      _isLoading = false;
      if (lista.isNotEmpty) {
        _seleccionarConcepto(lista.first);
      } else {
        _conceptoNombreCtrl.text = 'Cuota de Sostenimiento';
        _valorCtrl.text = '15000';
      }
    });
  }

  void _seleccionarConcepto(ConceptoCobroModel c) {
    setState(() {
      _conceptoSeleccionado = c;
      _conceptoNombreCtrl.text = c.nombre;
      _valorCtrl.text = c.valorPorDefecto.toStringAsFixed(0);
    });
  }

  void _seleccionarNombreConcepto(String nombre) {
    final match = _conceptos.firstWhereOrNull((c) => c.nombre.toLowerCase() == nombre.toLowerCase());
    setState(() {
      _conceptoNombreCtrl.text = nombre;
      if (match != null) {
        _conceptoSeleccionado = match;
        _valorCtrl.text = match.valorPorDefecto.toStringAsFixed(0);
      }
    });
  }

  void _guardar() {
    if (_formKey.currentState?.validate() != true) return;
    final nombre = _conceptoNombreCtrl.text.trim();
    if (nombre.isEmpty) return;

    final cantidad = int.tryParse(_cantidadCtrl.text.trim()) ?? 1;
    final valor = double.tryParse(_valorCtrl.text.trim()) ?? (_conceptoSeleccionado?.valorPorDefecto ?? 0.0);

    final match = _conceptos.firstWhereOrNull((c) => c.nombre.toLowerCase() == nombre.toLowerCase());
    final concepto = match ?? (_conceptoSeleccionado != null && _conceptoSeleccionado!.nombre.toLowerCase() == nombre.toLowerCase()
        ? _conceptoSeleccionado!
        : ConceptoCobroModel(
            id: 0,
            nombre: nombre,
            valorPorDefecto: valor,
          ));

    final linea = PaymentConceptLine(
      concepto: concepto,
      cantidad: cantidad,
      valorUnitario: valor,
    );

    Navigator.pop(context, linea);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Agregar Concepto'),
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
                    // Selector / Entrada Manual de Concepto
                    const Text('Tipo de Pago / Concepto (Escriba o Seleccione):', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 8),
                    Autocomplete<String>(
                      initialValue: TextEditingValue(text: _conceptoNombreCtrl.text),
                      optionsBuilder: (TextEditingValue textEditingValue) {
                        final allNames = {
                          ..._conceptos.map((c) => c.nombre),
                          ..._conceptosSugeridos,
                        }.toList();
                        if (textEditingValue.text.isEmpty) {
                          return allNames;
                        }
                        return allNames.where((String option) {
                          return option.toLowerCase().contains(textEditingValue.text.toLowerCase());
                        });
                      },
                      onSelected: (String selection) {
                        _seleccionarNombreConcepto(selection);
                      },
                      fieldViewBuilder: (context, controller, focusNode, onEditingComplete) {
                        if (_conceptoNombreCtrl.text.isNotEmpty && controller.text.isEmpty) {
                          controller.text = _conceptoNombreCtrl.text;
                        }
                        return TextFormField(
                          controller: controller,
                          focusNode: focusNode,
                          onEditingComplete: onEditingComplete,
                          onChanged: (val) {
                            _conceptoNombreCtrl.text = val;
                            final match = _conceptos.firstWhereOrNull((c) => c.nombre.toLowerCase() == val.toLowerCase());
                            if (match != null) {
                              _conceptoSeleccionado = match;
                              _valorCtrl.text = match.valorPorDefecto.toStringAsFixed(0);
                            }
                          },
                          decoration: const InputDecoration(
                            labelText: 'Tipo de Pago / Concepto',
                            hintText: 'Ej: Cuota de Sostenimiento, Rodamiento, Planilla...',
                            prefixIcon: Icon(Icons.edit_note, color: AppColors.primary),
                            filled: true,
                            fillColor: AppColors.surface,
                          ),
                          validator: (val) => val == null || val.trim().isEmpty ? 'Ingrese o elija el tipo de pago' : null,
                        );
                      },
                    ),

                    const SizedBox(height: 8),
                    // Chips de sugerencia rápida
                    Wrap(
                      spacing: 6,
                      runSpacing: 4,
                      children: _conceptosSugeridos.map((s) {
                        return ActionChip(
                          label: Text(s, style: const TextStyle(fontSize: 11)),
                          backgroundColor: AppColors.surface,
                          onPressed: () {
                            _seleccionarNombreConcepto(s);
                          },
                        );
                      }).toList(),
                    ),

                    const SizedBox(height: 16),

                    // Cantidad
                    TextFormField(
                      controller: _cantidadCtrl,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Cantidad',
                        prefixIcon: Icon(Icons.numbers, color: AppColors.primary),
                        filled: true,
                        fillColor: AppColors.surface,
                      ),
                      validator: (val) {
                        final n = int.tryParse(val ?? '');
                        if (n == null || n <= 0) return 'Ingrese una cantidad mayor a 0';
                        return null;
                      },
                    ),

                    const SizedBox(height: 16),

                    // Valor Unitario
                    TextFormField(
                      controller: _valorCtrl,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Valor Unitario (\$)',
                        prefixIcon: Icon(Icons.attach_money, color: AppColors.primary),
                        filled: true,
                        fillColor: AppColors.surface,
                      ),
                      validator: (val) {
                        final n = double.tryParse(val ?? '');
                        if (n == null || n < 0) return 'Ingrese un valor válido';
                        return null;
                      },
                    ),

                    const SizedBox(height: 30),

                    ElevatedButton.icon(
                      onPressed: _guardar,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.check, color: Colors.black, size: 22),
                      label: const Text('AGREGAR AL RECIBO', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
