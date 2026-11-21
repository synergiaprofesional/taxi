import 'package:cloud_firestore/cloud_firestore.dart';
import 'payment_model.dart';

class ConductorModel {
  final int id;
  final String name;
  final String cedula;
  final String telefono;
  final String estado; // 'activo', 'inactivo', 'suspendido'
  final bool esPrivado;
  final String gremioId;
  final double calificacionPromedio;
  final List<ConceptoCobroModel> conceptos;

  ConductorModel({
    required this.id,
    required this.name,
    this.cedula = '',
    this.telefono = '',
    this.estado = 'activo',
    this.esPrivado = false,
    this.gremioId = '',
    this.calificacionPromedio = 5.0,
    this.conceptos = const [],
  });

  factory ConductorModel.fromJson(dynamic json) {
    if (json is Map<String, dynamic>) {
      final rawConcepts = json['concepto_ids'] ?? [];
      List<ConceptoCobroModel> concepts = [];
      if (rawConcepts is List) {
        concepts = rawConcepts
            .whereType<Map>()
            .map((c) => ConceptoCobroModel.fromJson(Map<String, dynamic>.from(c)))
            .toList();
      }
      return ConductorModel(
        id: json['id'] is int ? json['id'] : int.tryParse(json['id'].toString()) ?? 0,
        name: json['name']?.toString() ?? 'Sin Nombre',
        cedula: json['vat']?.toString() ?? json['cedula']?.toString() ?? '',
        telefono: json['phone']?.toString() ?? json['mobile']?.toString() ?? '',
        estado: json['estado']?.toString() ?? 'activo',
        esPrivado: json['es_privado'] == true,
        gremioId: json['gremio_id']?.toString() ?? '',
        calificacionPromedio: (json['calificacion_promedio'] ?? 5.0).toDouble(),
        conceptos: concepts,
      );
    } else if (json is int) {
      return ConductorModel(id: json, name: 'Conductor #$json');
    }
    return ConductorModel(id: 0, name: 'Conductor General');
  }

  factory ConductorModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    int docId = int.tryParse(doc.id) ?? 0;
    final merged = Map<String, dynamic>.from(data);
    if (merged['id'] == null || merged['id'] == 0) {
      merged['id'] = docId;
    }
    return ConductorModel.fromJson(merged);
  }

  Map<String, dynamic> toFirestore() => {
    'id': id,
    'name': name,
    'cedula': cedula,
    'telefono': telefono,
    'estado': estado,
    'es_privado': esPrivado,
    'gremio_id': gremioId,
    'calificacion_promedio': calificacionPromedio,
    'concepto_ids': conceptos.map((c) => c.toJson()).toList(),
  };

  Map<String, dynamic> toJson() => toFirestore();
}

class VehiculoModel {
  final int id;
  final String placa;
  final String numeroInterno;
  final String modelo;
  final String estado; // 'disponible', 'en_turno', 'en_carrera', 'fuera_servicio'
  final bool esPrivado;
  final String gremioId;
  final List<ConductorModel> conductores;

  VehiculoModel({
    required this.id,
    required this.placa,
    this.numeroInterno = '',
    this.modelo = '',
    this.estado = 'disponible',
    this.esPrivado = false,
    this.gremioId = '',
    this.conductores = const [],
  });

  factory VehiculoModel.fromJson(Map<String, dynamic> json) {
    final rawDrivers = json['conductor_ids'] ?? [];
    List<ConductorModel> drivers = [];
    if (rawDrivers is List) {
      drivers = rawDrivers.map((e) => ConductorModel.fromJson(e)).toList();
    }

    return VehiculoModel(
      id: json['id'] is int ? json['id'] : int.tryParse(json['id'].toString()) ?? 0,
      placa: (json['name'] ?? json['placa'] ?? '').toString().toUpperCase(),
      numeroInterno: (json['numero_interno'] ?? json['codigo'] ?? '').toString(),
      modelo: json['modelo']?.toString() ?? '',
      estado: json['estado']?.toString() ?? 'disponible',
      esPrivado: json['es_privado'] == true,
      gremioId: json['gremio_id']?.toString() ?? '',
      conductores: drivers,
    );
  }

  factory VehiculoModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    int docId = int.tryParse(doc.id) ?? 0;
    final merged = Map<String, dynamic>.from(data);
    if (merged['id'] == null || merged['id'] == 0) {
      merged['id'] = docId;
    }
    return VehiculoModel.fromJson(merged);
  }

  Map<String, dynamic> toFirestore() => {
    'id': id,
    'name': placa,
    'numero_interno': numeroInterno,
    'modelo': modelo,
    'estado': estado,
    'es_privado': esPrivado,
    'gremio_id': gremioId,
    'conductor_ids': conductores.map((c) => c.toJson()).toList(),
  };

  Map<String, dynamic> toJson() => toFirestore();
}
