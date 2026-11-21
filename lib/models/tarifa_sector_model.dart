import 'package:cloud_firestore/cloud_firestore.dart';

class TarifaSectorModel {
  final int id;
  final String name;
  final double valor;
  final double valorRecargo;
  final String nota;
  final String sectorOrigen;
  final String sectorDestino;
  final String decretoReferencia;
  final double recargoNocturno;
  final double recargoFestivo;
  final double recargoAeropuerto;

  const TarifaSectorModel({
    required this.id,
    required this.name,
    required this.valor,
    this.valorRecargo = 0.0,
    this.nota = '',
    this.sectorOrigen = '',
    this.sectorDestino = '',
    this.decretoReferencia = 'Decreto Distrital Vigente',
    this.recargoNocturno = 1000.0,
    this.recargoFestivo = 1000.0,
    this.recargoAeropuerto = 5000.0,
  });

  factory TarifaSectorModel.fromJson(Map<String, dynamic> json) {
    double parseDouble(dynamic val, [double fallback = 0.0]) {
      if (val == null) return fallback;
      if (val is num) return val.toDouble();
      return double.tryParse(val.toString()) ?? fallback;
    }

    int parseInt(dynamic val) {
      if (val == null) return 0;
      if (val is int) return val;
      return int.tryParse(val.toString()) ?? 0;
    }

    String parseString(dynamic val) {
      if (val == null || val == false) return '';
      return val.toString().trim();
    }

    return TarifaSectorModel(
      id: parseInt(json['id']),
      name: parseString(json['name']),
      valor: parseDouble(json['valor']),
      valorRecargo: parseDouble(json['valor_recargo']),
      nota: parseString(json['nota']),
      sectorOrigen: parseString(json['sector_origen']),
      sectorDestino: parseString(json['sector_destino']),
      decretoReferencia: parseString(json['decreto_referencia']).isNotEmpty
          ? parseString(json['decreto_referencia'])
          : 'Decreto Distrital Vigente',
      recargoNocturno: parseDouble(json['recargo_nocturno'], 1000.0),
      recargoFestivo: parseDouble(json['recargo_festivo'], 1000.0),
      recargoAeropuerto: parseDouble(json['recargo_aeropuerto'], 5000.0),
    );
  }

  factory TarifaSectorModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    int docId = int.tryParse(doc.id) ?? 0;
    final merged = Map<String, dynamic>.from(data);
    if (merged['id'] == null || merged['id'] == 0) {
      merged['id'] = docId;
    }
    return TarifaSectorModel.fromJson(merged);
  }

  Map<String, dynamic> toFirestore() {
    return {
      'id': id,
      'name': name,
      'valor': valor,
      'valor_recargo': valorRecargo,
      'nota': nota,
      'sector_origen': sectorOrigen,
      'sector_destino': sectorDestino,
      'decreto_referencia': decretoReferencia,
      'recargo_nocturno': recargoNocturno,
      'recargo_festivo': recargoFestivo,
      'recargo_aeropuerto': recargoAeropuerto,
    };
  }

  Map<String, dynamic> toJson() => toFirestore();

  @override
  String toString() => '$name (\$ ${valor.toInt()})';
}
