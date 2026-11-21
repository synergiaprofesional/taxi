import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_colors.dart';
import '../../../models/bay_model.dart';
import '../../../services/odoo_service.dart';

class BahiaSelectorDialog extends StatefulWidget {
  final int bahiaActualId;

  const BahiaSelectorDialog({super.key, required this.bahiaActualId});

  @override
  State<BahiaSelectorDialog> createState() => _BahiaSelectorDialogState();
}

class _BahiaSelectorDialogState extends State<BahiaSelectorDialog> {
  final odooService = Get.find<OdooService>();
  List<BahiaModel> _bahias = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _cargarBahias();
  }

  Future<void> _cargarBahias() async {
    setState(() => _isLoading = true);
    final lista = await odooService.getBahias();
    setState(() {
      _bahias = lista;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 480, maxHeight: 520),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Seleccionar Bahía de Operación',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const Divider(height: 20),
              _isLoading
                  ? const Center(child: Padding(padding: EdgeInsets.all(30), child: CircularProgressIndicator()))
                  : Expanded(
                      child: ListView.separated(
                        itemCount: _bahias.length,
                        separatorBuilder: (_, _) => const Divider(height: 1),
                        itemBuilder: (ctx, idx) {
                          final bay = _bahias[idx];
                          final isSelected = bay.id == widget.bahiaActualId;

                          return Container(
                            margin: const EdgeInsets.symmetric(vertical: 4),
                            decoration: BoxDecoration(
                              color: isSelected ? AppColors.primary.withValues(alpha: 0.12) : AppColors.surfaceElevated,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(
                                color: isSelected ? AppColors.primary : Colors.white12,
                                width: isSelected ? 1.5 : 1.0,
                              ),
                            ),
                            child: ListTile(
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                              leading: Container(
                                width: 44,
                                height: 44,
                                alignment: Alignment.center,
                                decoration: BoxDecoration(
                                  color: isSelected ? AppColors.primary : Colors.grey.shade800,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  bay.codigo.isNotEmpty ? bay.codigo : bay.name.substring(0, bay.name.length > 3 ? 3 : bay.name.length).toUpperCase(),
                                  style: TextStyle(
                                    color: isSelected ? Colors.black : Colors.white,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 14,
                                  ),
                                ),
                              ),
                              title: Text(
                                bay.name,
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16,
                                ),
                              ),
                              subtitle: Text(
                                isSelected ? 'Bahía actualmente seleccionada' : 'Sesión activa de hoy',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: isSelected ? AppColors.primary : Colors.grey,
                                ),
                              ),
                              trailing: isSelected
                                  ? const Icon(Icons.check_circle, color: AppColors.primary, size: 24)
                                  : const Icon(Icons.login, color: Colors.blueAccent, size: 22),
                              onTap: () => Navigator.pop(context, bay),
                            ),
                          );
                        },
                      ),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}
