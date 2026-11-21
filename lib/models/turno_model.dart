import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import '../core/theme/app_colors.dart';

enum EstadoTurno { espera, actual, siguiente, despachado, cancelado }

class TurnoModel {
  final int id;
  final String name;             // Ej: T-0142 / TR-0042
  final String vehiculoPlaca;     // Ej: WBD-512
  final String conductorNombre;   // Ej: Carlos Ramírez
  final String bahiaNombre;       // Ej: Bahía Norte
  final int numeroTurno;          // Posición en fila / sequence
  final EstadoTurno estado;
  final DateTime fechaCreacion;
  final DateTime? fechaDespacho;
  final double valorTotal;
  final int tarifaId;             // 0 = Turno en espera, != 0 = Despacho
  final String tarifaNombre;       // Ej: Aeropuerto -> Centro
  final String nota;
  final bool esAnonimo;
  final String placaAnonima;
  final int bahiaSesionId;
  final int bahiaBaseId;
  final int vehiculoId;
  final int conductorId;

  TurnoModel({
    required this.id,
    required this.name,
    required this.vehiculoPlaca,
    required this.conductorNombre,
    required this.bahiaNombre,
    required this.numeroTurno,
    required this.estado,
    required this.fechaCreacion,
    this.fechaDespacho,
    this.valorTotal = 0.0,
    this.tarifaId = 0,
    this.tarifaNombre = '',
    this.nota = '',
    this.esAnonimo = false,
    this.placaAnonima = '',
    this.bahiaSesionId = 0,
    this.bahiaBaseId = 0,
    this.vehiculoId = 0,
    this.conductorId = 0,
  });

  /// Determina si un turno ya fue despachado (asignado a destino/tarifa o marcado como despachado)
  bool get esDespacho => tarifaId != 0 || estado == EstadoTurno.despachado;

  /// Determina si un vehículo está físicamente en espera activa en la cola de la bahía
  bool get enFila => !esDespacho && estado != EstadoTurno.cancelado;

  String get placaVisible => esAnonimo ? placaAnonima : vehiculoPlaca;

  Color get estadoColor {
    switch (estado) {
      case EstadoTurno.actual:
        return AppColors.turnActual;
      case EstadoTurno.siguiente:
        return AppColors.turnSiguiente;
      case EstadoTurno.espera:
        return AppColors.turnEspera;
      case EstadoTurno.despachado:
        return AppColors.turnDespachado;
      case EstadoTurno.cancelado:
        return AppColors.turnCancelado;
    }
  }

  Color get colorEstado => estadoColor;

  String get estadoLabel {
    switch (estado) {
      case EstadoTurno.actual:
        return 'ACTUAL EN BAHÍA';
      case EstadoTurno.siguiente:
        return 'SIGUIENTE';
      case EstadoTurno.espera:
        return 'EN ESPERA';
      case EstadoTurno.despachado:
        return 'DESPACHADO';
      case EstadoTurno.cancelado:
        return 'CANCELADO';
    }
  }

  String get etiquetaEstado => estadoLabel;

  factory TurnoModel.fromJson(Map<String, dynamic> json) {
    EstadoTurno parseEstado(String? state) {
      switch (state?.toLowerCase()) {
        case 'actual':
          return EstadoTurno.actual;
        case 'siguiente':
          return EstadoTurno.siguiente;
        case 'despachado':
        case 'done':
          return EstadoTurno.despachado;
        case 'cancelado':
        case 'cancel':
          return EstadoTurno.cancelado;
        default:
          return EstadoTurno.espera;
      }
    }

    int parseInt(dynamic val, [int fallback = 0]) {
      if (val is int) return val;
      if (val is num) return val.toInt();
      if (val is String) return int.tryParse(val) ?? fallback;
      return fallback;
    }

    double parseDouble(dynamic val, [double fallback = 0.0]) {
      if (val is double) return val;
      if (val is num) return val.toDouble();
      if (val is String) return double.tryParse(val) ?? fallback;
      return fallback;
    }

    DateTime parseDate(dynamic val) {
      if (val == null || val == false) return DateTime.now();
      if (val is Timestamp) return val.toDate();
      if (val is DateTime) return val;
      var str = val.toString().trim();
      if (str.isEmpty) return DateTime.now();
      str = str.replaceFirst(' ', 'T');
      final dt = DateTime.tryParse(str);
      if (dt != null) {
        return dt.isUtc ? dt.toLocal() : dt;
      }
      return DateTime.now();
    }

    final rawTarifa = json['tarifa_id'];
    int tId = 0;
    String tNom = '';
    if (rawTarifa is List && rawTarifa.length >= 2) {
      tId = parseInt(rawTarifa[0]);
      tNom = rawTarifa[1]?.toString() ?? '';
    } else if (rawTarifa is Map) {
      tId = parseInt(rawTarifa['id']);
      tNom = rawTarifa['name']?.toString() ?? '';
    } else if (rawTarifa is int) {
      tId = rawTarifa;
    }

    // Si la tarifa oficial viene vacía pero se registró un destino manual en 'nota':
    if (tNom.isEmpty && json['nota'] != null && json['nota'] != false) {
      final notaLimpia = json['nota'].toString().trim();
      if (notaLimpia.isNotEmpty && notaLimpia.toLowerCase() != 'false') {
        tNom = notaLimpia;
      }
    }

    // Nombre base del turno en Odoo (ej: 'Turno #125 [FXU168 - VEHICULO DE APOYO]')
    final rawName = (json['name'] != null && json['name'] != false) ? json['name'].toString() : 'T-000';

    // 1. Extraer placa e ID de vehículo: soporte polimórfico para Map (get_all), List (search_read), String y fallback en name
    int vehiculoIdParsed = 0;
    String placaParsed = '';
    final rawVehiculo = json['vehiculo_id'];
    if (rawVehiculo is Map) {
      placaParsed = rawVehiculo['name']?.toString() ?? '';
      vehiculoIdParsed = parseInt(rawVehiculo['id']);
    } else if (rawVehiculo is List && rawVehiculo.isNotEmpty) {
      if (rawVehiculo.length >= 2) {
        placaParsed = rawVehiculo[1]?.toString() ?? '';
      }
      vehiculoIdParsed = parseInt(rawVehiculo[0]);
    } else if (rawVehiculo is int) {
      vehiculoIdParsed = rawVehiculo;
    } else if (rawVehiculo is String && rawVehiculo.isNotEmpty) {
      placaParsed = rawVehiculo;
    }

    if (placaParsed.isEmpty || placaParsed == 'false') {
      if (json['vehiculo_placa'] != null && json['vehiculo_placa'] != false) {
        placaParsed = json['vehiculo_placa'].toString();
      } else if (json['placa'] != null && json['placa'] != false) {
        placaParsed = json['placa'].toString();
      } else if (json['placa_anonima'] != null && json['placa_anonima'] != false && json['placa_anonima'].toString().isNotEmpty) {
        placaParsed = json['placa_anonima'].toString();
      }
    }

    if (placaParsed.isEmpty || placaParsed == 'SIN-PLACA' || placaParsed == 'false') {
      final match = RegExp(r'\[\s*([A-Za-z0-9]+)\s*(?:-|\b)').firstMatch(rawName);
      if (match != null) {
        placaParsed = match.group(1)!;
      } else {
        placaParsed = 'SIN-PLACA';
      }
    }

    // 2. Extraer conductor e ID de conductor: soporte para Map, List, String y fallback en name
    int conductorIdParsed = 0;
    String conductorParsed = '';
    final rawConductor = json['conductor_id'];
    if (rawConductor is Map) {
      conductorParsed = rawConductor['name']?.toString() ?? '';
      conductorIdParsed = parseInt(rawConductor['id']);
    } else if (rawConductor is List && rawConductor.isNotEmpty) {
      if (rawConductor.length >= 2) {
        conductorParsed = rawConductor[1]?.toString() ?? '';
      }
      conductorIdParsed = parseInt(rawConductor[0]);
    } else if (rawConductor is int) {
      conductorIdParsed = rawConductor;
    } else if (rawConductor is String && rawConductor.isNotEmpty) {
      conductorParsed = rawConductor;
    }

    if (conductorParsed.isEmpty || conductorParsed == 'false') {
      if (json['conductor_nombre'] != null && json['conductor_nombre'] != false) {
        conductorParsed = json['conductor_nombre'].toString();
      } else if (json['conductor'] != null && json['conductor'] != false) {
        conductorParsed = json['conductor'].toString();
      }
    }

    if (conductorParsed.isEmpty || conductorParsed == 'false') {
      final matchConductor = RegExp(r'\[\s*[A-Za-z0-9]+\s*-\s*([^\]]+)\]').firstMatch(rawName);
      if (matchConductor != null) {
        conductorParsed = matchConductor.group(1)!.trim();
      } else {
        conductorParsed = 'Conductor General';
      }
    }

    // 3. Extraer bahía e ID de sesión de bahía: soporte polimórfico robusto para Map, List, int y String
    int sesionBahiaId = 0;
    int baseBahiaId = 0;
    String bahiaParsed = '';

    // Si viene explícito bahia_sesion_id (formato retornado por _get_data de fundetaxcol.turno)
    if (json['bahia_sesion_id'] != null) {
      sesionBahiaId = parseInt(json['bahia_sesion_id']);
    }

    final rawBahia = json['bahia_id'];
    if (rawBahia is Map) {
      bahiaParsed = rawBahia['name']?.toString() ?? '';
      baseBahiaId = parseInt(rawBahia['id']);
    } else if (rawBahia is List && rawBahia.isNotEmpty) {
      if (rawBahia.length >= 2) {
        bahiaParsed = rawBahia[1]?.toString() ?? '';
      }
      final parsedId = parseInt(rawBahia[0]);
      if (sesionBahiaId == 0) {
        sesionBahiaId = parsedId;
      } else if (baseBahiaId == 0) {
        baseBahiaId = parsedId;
      }
    } else if (rawBahia is int) {
      if (sesionBahiaId == 0) sesionBahiaId = rawBahia;
      baseBahiaId = rawBahia;
    } else if (rawBahia is String) {
      bahiaParsed = rawBahia;
    }

    if (sesionBahiaId == 0 && baseBahiaId != 0) {
      sesionBahiaId = baseBahiaId;
    }
    if (baseBahiaId == 0 && sesionBahiaId != 0) {
      baseBahiaId = sesionBahiaId;
    }

    if (bahiaParsed.isEmpty || bahiaParsed == 'false') {
      bahiaParsed = json['bahia_nombre']?.toString() ?? (json['bahia']?.toString() ?? 'Bahía Principal');
    }

    final esAnon = json['anonimo'] == true;
    final placaAnon = (json['placa_anonima'] != null && json['placa_anonima'] != false) ? json['placa_anonima'].toString() : '';

    return TurnoModel(
      id: parseInt(json['id']),
      name: rawName,
      vehiculoPlaca: placaParsed,
      conductorNombre: conductorParsed,
      bahiaNombre: bahiaParsed,
      numeroTurno: parseInt(json['sequence'] ?? json['numero_turno'], 1),
      estado: parseEstado(json['state'] ?? json['estado']),
      fechaCreacion: (json['fecha'] != null && json['fecha'] != false)
          ? parseDate(json['fecha'])
          : ((json['create_date'] != null && json['create_date'] != false)
              ? parseDate(json['create_date'])
              : DateTime.now()),
      fechaDespacho: (json['fecha_despacho'] != null && json['fecha_despacho'] != false)
          ? parseDate(json['fecha_despacho'])
          : null,
      valorTotal: parseDouble(json['total'] ?? json['valor_total']),
      tarifaId: tId,
      tarifaNombre: tNom,
      nota: (json['nota'] != null && json['nota'] != false) ? json['nota'].toString() : '',
      esAnonimo: esAnon,
      placaAnonima: placaAnon,
      bahiaSesionId: sesionBahiaId,
      bahiaBaseId: baseBahiaId,
      vehiculoId: vehiculoIdParsed,
      conductorId: conductorIdParsed,
    );
  }

  factory TurnoModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    int docId = int.tryParse(doc.id) ?? 0;
    if (docId == 0 && data['id'] != null) {
      docId = (data['id'] is int) ? data['id'] : (int.tryParse(data['id'].toString()) ?? 0);
    }
    final merged = Map<String, dynamic>.from(data);
    merged['id'] = docId;
    return TurnoModel.fromJson(merged);
  }

  Map<String, dynamic> toFirestore() {
    return {
      'id': id,
      'name': name,
      'vehiculo_placa': vehiculoPlaca,
      'conductor_nombre': conductorNombre,
      'bahia_nombre': bahiaNombre,
      'numero_turno': numeroTurno,
      'state': estado.name,
      'fecha_creacion': Timestamp.fromDate(fechaCreacion),
      if (fechaDespacho != null) 'fecha_despacho': Timestamp.fromDate(fechaDespacho!),
      'valor_total': valorTotal,
      'tarifa_id': tarifaId,
      'tarifa_nombre': tarifaNombre,
      'nota': nota,
      'anonimo': esAnonimo,
      'placa_anonima': placaAnonima,
      'bahia_sesion_id': bahiaSesionId,
      'bahia_base_id': bahiaBaseId,
      'vehiculo_id': vehiculoId,
      'conductor_id': conductorId,
    };
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'vehiculo_placa': vehiculoPlaca,
    'conductor_nombre': conductorNombre,
    'bahia_nombre': bahiaNombre,
    'numero_turno': numeroTurno,
    'state': estado.name,
    'fecha_creacion': fechaCreacion.toIso8601String(),
    'fecha_despacho': fechaDespacho?.toIso8601String(),
    'valor_total': valorTotal,
    'tarifa_id': tarifaId,
    'tarifa_nombre': tarifaNombre,
    'nota': nota,
    'anonimo': esAnonimo,
    'placa_anonima': placaAnonima,
  };
}
