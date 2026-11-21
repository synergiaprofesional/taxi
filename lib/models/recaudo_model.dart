import 'package:cloud_firestore/cloud_firestore.dart';
import 'payment_model.dart';

class RecaudoModel {
  final String id;
  final String name; // ej. REC-20261121-001
  final String vehiculoPlaca;
  final String conductorNombre;
  final String conductorCedula;
  final int bahiaSesionId;
  final String bahiaNombre;
  final String cajeroNombre;
  final DateTime fecha;
  final double total;
  final double totalAhorro;
  final List<PaymentConceptLine> lineas;
  final String metodoPago;
  final String nota;

  const RecaudoModel({
    required this.id,
    required this.name,
    required this.vehiculoPlaca,
    required this.conductorNombre,
    this.conductorCedula = '',
    this.bahiaSesionId = 0,
    this.bahiaNombre = '',
    this.cajeroNombre = 'Cajero',
    required this.fecha,
    required this.total,
    this.totalAhorro = 0.0,
    this.lineas = const [],
    this.metodoPago = 'efectivo',
    this.nota = '',
  });

  factory RecaudoModel.fromJson(Map<String, dynamic> json, [String? docId]) {
    DateTime parseDate(dynamic val) {
      if (val is Timestamp) return val.toDate();
      if (val is DateTime) return val;
      if (val is String && val.isNotEmpty) {
        return DateTime.tryParse(val) ?? DateTime.now();
      }
      return DateTime.now();
    }

    double parseDouble(dynamic val, [double fallback = 0.0]) {
      if (val is double) return val;
      if (val is num) return val.toDouble();
      if (val is String) return double.tryParse(val) ?? fallback;
      return fallback;
    }

    int parseInt(dynamic val, [int fallback = 0]) {
      if (val is int) return val;
      if (val is num) return val.toInt();
      if (val is String) return int.tryParse(val) ?? fallback;
      return fallback;
    }

    List<PaymentConceptLine> parsedLines = [];
    final rawLines = json['lineas'] ?? json['lines'] ?? [];
    if (rawLines is List) {
      for (final item in rawLines) {
        if (item is Map<String, dynamic>) {
          parsedLines.add(PaymentConceptLine(
            concepto: ConceptoCobroModel.fromJson(item['concepto'] ?? item),
            cantidad: parseInt(item['cantidad'], 1),
            valorUnitario: parseDouble(item['valor_unitario'] ?? item['valor']),
          ));
        }
      }
    }

    return RecaudoModel(
      id: docId ?? json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? 'REC-000',
      vehiculoPlaca: (json['vehiculo_placa'] ?? json['placa'] ?? '').toString().toUpperCase(),
      conductorNombre: json['conductor_nombre']?.toString() ?? 'Conductor General',
      conductorCedula: json['conductor_cedula']?.toString() ?? '',
      bahiaSesionId: parseInt(json['bahia_sesion_id']),
      bahiaNombre: json['bahia_nombre']?.toString() ?? 'Bahía',
      cajeroNombre: json['cajero_nombre']?.toString() ?? 'Cajero',
      fecha: parseDate(json['fecha']),
      total: parseDouble(json['total']),
      totalAhorro: parseDouble(json['total_ahorro']),
      lineas: parsedLines,
      metodoPago: json['metodo_pago']?.toString() ?? 'efectivo',
      nota: json['nota']?.toString() ?? '',
    );
  }

  factory RecaudoModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    return RecaudoModel.fromJson(data, doc.id);
  }

  Map<String, dynamic> toFirestore() {
    return {
      'id': id,
      'name': name,
      'vehiculo_placa': vehiculoPlaca,
      'conductor_nombre': conductorNombre,
      'conductor_cedula': conductorCedula,
      'bahia_sesion_id': bahiaSesionId,
      'bahia_nombre': bahiaNombre,
      'cajero_nombre': cajeroNombre,
      'fecha': Timestamp.fromDate(fecha),
      'total': total,
      'total_ahorro': totalAhorro,
      'metodo_pago': metodoPago,
      'nota': nota,
      'lineas': lineas
          .map((l) => {
                'concepto_id': l.concepto.id,
                'concepto_nombre': l.concepto.nombre,
                'cantidad': l.cantidad,
                'valor_unitario': l.valorUnitario,
                'subtotal': l.subtotal,
              })
          .toList(),
    };
  }

  Map<String, dynamic> toJson() => toFirestore();
}
