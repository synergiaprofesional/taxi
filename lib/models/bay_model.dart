import 'package:cloud_firestore/cloud_firestore.dart';

class BahiaModel {
  final int id;
  final String name;
  final String codigo;
  final bool activa;
  final double lat;
  final double lng;
  final int capacidad;

  BahiaModel({
    required this.id,
    required this.name,
    this.codigo = '',
    this.activa = true,
    this.lat = 0.0,
    this.lng = 0.0,
    this.capacidad = 20,
  });

  factory BahiaModel.fromJson(Map<String, dynamic> json) {
    // 1. Extraer nombre limpio priorizando name_sec o bahia_id
    String cleanName = '';
    if (json['name_sec'] != null && json['name_sec'].toString().trim().isNotEmpty) {
      cleanName = json['name_sec'].toString().trim();
    } else if (json['bahia_id'] is List && (json['bahia_id'] as List).length >= 2) {
      cleanName = (json['bahia_id'] as List)[1].toString().trim();
    } else if (json['bahia_id'] is Map && json['bahia_id']['name'] != null) {
      cleanName = json['bahia_id']['name'].toString().trim();
    } else if (json['name'] != null) {
      cleanName = json['name'].toString().split('Sesión')[0].trim();
    } else {
      cleanName = 'Bahía';
    }

    // 2. Extraer código corto limpio (29D, GAR, LAG)
    String cleanCode = (json['code'] ?? json['codigo'] ?? '').toString().trim();
    if (cleanCode.isEmpty) {
      if (cleanName.contains('29D')) {
        cleanCode = '29D';
      } else if (cleanName.toLowerCase().contains('garita')) {
        cleanCode = 'GAR';
      } else if (cleanName.toLowerCase().contains('lago')) {
        cleanCode = 'LAG';
      } else {
        cleanCode = cleanName.length > 3 ? cleanName.substring(0, 3).toUpperCase() : cleanName.toUpperCase();
      }
    }

    double parseDouble(dynamic val) {
      if (val is double) return val;
      if (val is num) return val.toDouble();
      if (val is String) return double.tryParse(val) ?? 0.0;
      return 0.0;
    }

    int parseInt(dynamic val) {
      if (val is int) return val;
      if (val is num) return val.toInt();
      if (val is String) return int.tryParse(val) ?? 0;
      return 0;
    }

    return BahiaModel(
      id: json['id'] is int ? json['id'] : int.tryParse(json['id'].toString()) ?? 0,
      name: cleanName,
      codigo: cleanCode,
      activa: json['active'] ?? (json['state'] == 'progreso' || json['state'] == 'open'),
      lat: parseDouble(json['lat']),
      lng: parseDouble(json['lng']),
      capacidad: parseInt(json['capacidad'] ?? 20),
    );
  }

  factory BahiaModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    int docId = int.tryParse(doc.id) ?? 0;
    final merged = Map<String, dynamic>.from(data);
    if (merged['id'] == null || merged['id'] == 0) {
      merged['id'] = docId;
    }
    return BahiaModel.fromJson(merged);
  }

  Map<String, dynamic> toFirestore() => {
    'id': id,
    'name': name,
    'codigo': codigo,
    'activa': activa,
    'lat': lat,
    'lng': lng,
    'capacidad': capacidad,
  };

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'code': codigo,
    'active': activa,
    'lat': lat,
    'lng': lng,
    'capacidad': capacidad,
  };
}

class BahiaSesionModel {
  final int id;
  final int bahiaId;
  final String bahiaNombre;
  final String usuario;
  final DateTime fechaInicio;
  final String estado; // 'open', 'closed'
  final double totalRecaudado;
  final int totalTurnos;

  BahiaSesionModel({
    required this.id,
    required this.bahiaId,
    required this.bahiaNombre,
    required this.usuario,
    required this.fechaInicio,
    this.estado = 'open',
    this.totalRecaudado = 0.0,
    this.totalTurnos = 0,
  });

  factory BahiaSesionModel.fromJson(Map<String, dynamic> json) {
    final rawBahia = json['bahia_id'];
    int bId = 0;
    String bNom = 'Bahía';
    if (rawBahia is List && rawBahia.length >= 2) {
      bId = rawBahia[0];
      bNom = rawBahia[1].toString();
    } else if (rawBahia is Map) {
      bId = rawBahia['id'] ?? 0;
      bNom = rawBahia['name'] ?? 'Bahía';
    }

    DateTime parseDate(dynamic val) {
      if (val is Timestamp) return val.toDate();
      if (val is DateTime) return val;
      if (val is String && val.isNotEmpty) {
        return DateTime.tryParse(val) ?? DateTime.now();
      }
      return DateTime.now();
    }

    return BahiaSesionModel(
      id: json['id'] is int ? json['id'] : int.tryParse(json['id'].toString()) ?? 0,
      bahiaId: bId,
      bahiaNombre: bNom,
      usuario: json['user_id'] is List ? json['user_id'][1] : (json['user'] ?? 'Despachador').toString(),
      fechaInicio: parseDate(json['date_start'] ?? json['fecha']),
      estado: json['state'] ?? 'open',
      totalRecaudado: (json['total_recaudo'] ?? json['total'] ?? 0.0).toDouble(),
      totalTurnos: (json['total_turnos'] ?? json['turnos_count'] ?? 0).toInt(),
    );
  }

  factory BahiaSesionModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    int docId = int.tryParse(doc.id) ?? 0;
    final merged = Map<String, dynamic>.from(data);
    if (merged['id'] == null || merged['id'] == 0) {
      merged['id'] = docId;
    }
    return BahiaSesionModel.fromJson(merged);
  }

  Map<String, dynamic> toFirestore() => {
    'id': id,
    'bahia_id': bahiaId,
    'bahia_nombre': bahiaNombre,
    'user': usuario,
    'fecha': Timestamp.fromDate(fechaInicio),
    'state': estado,
    'total_recaudo': totalRecaudado,
    'total_turnos': totalTurnos,
  };

  Map<String, dynamic> toJson() => {
    'id': id,
    'bahia_id': bahiaId,
    'bahia_nombre': bahiaNombre,
    'user': usuario,
    'date_start': fechaInicio.toIso8601String(),
    'state': estado,
    'total_recaudo': totalRecaudado,
    'total_turnos': totalTurnos,
  };
}
