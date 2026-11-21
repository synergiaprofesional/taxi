import 'package:cloud_firestore/cloud_firestore.dart';

enum EstadoViaje {
  solicitado,
  asignado,
  enCamino,
  aBordo,
  finalizado,
  cancelado,
}

extension EstadoViajeExtension on EstadoViaje {
  String get key {
    switch (this) {
      case EstadoViaje.solicitado:
        return 'solicitado';
      case EstadoViaje.asignado:
        return 'asignado';
      case EstadoViaje.enCamino:
        return 'en_camino';
      case EstadoViaje.aBordo:
        return 'a_bordo';
      case EstadoViaje.finalizado:
        return 'finalizado';
      case EstadoViaje.cancelado:
        return 'cancelado';
    }
  }

  String get label {
    switch (this) {
      case EstadoViaje.solicitado:
        return 'Buscando Taxi...';
      case EstadoViaje.asignado:
        return 'Taxi Asignado';
      case EstadoViaje.enCamino:
        return 'Conductor en Camino';
      case EstadoViaje.aBordo:
        return 'En Carrera';
      case EstadoViaje.finalizado:
        return 'Completado';
      case EstadoViaje.cancelado:
        return 'Cancelado';
    }
  }

  static EstadoViaje fromString(String? estado) {
    switch (estado?.toLowerCase()) {
      case 'solicitado':
      case 'draft':
      case 'pending':
        return EstadoViaje.solicitado;
      case 'asignado':
      case 'assigned':
        return EstadoViaje.asignado;
      case 'en_camino':
      case 'on_way':
        return EstadoViaje.enCamino;
      case 'a_bordo':
      case 'on_board':
        return EstadoViaje.aBordo;
      case 'finalizado':
      case 'done':
      case 'completed':
        return EstadoViaje.finalizado;
      case 'cancelado':
      case 'cancel':
        return EstadoViaje.cancelado;
      default:
        return EstadoViaje.solicitado;
    }
  }
}

enum TipoServicioViaje {
  calle,
  bahia,
  corporativo,
}

extension TipoServicioViajeExtension on TipoServicioViaje {
  String get key {
    switch (this) {
      case TipoServicioViaje.calle:
        return 'calle';
      case TipoServicioViaje.bahia:
        return 'bahia';
      case TipoServicioViaje.corporativo:
        return 'corporativo';
    }
  }

  static TipoServicioViaje fromString(String? val) {
    switch (val?.toLowerCase()) {
      case 'bahia':
        return TipoServicioViaje.bahia;
      case 'corporativo':
      case 'convenio':
        return TipoServicioViaje.corporativo;
      case 'calle':
      default:
        return TipoServicioViaje.calle;
    }
  }
}

enum CategoriaViaje {
  taxiEstandar,
  bahiaPrioritaria,
  ejecutivoVip,
  envioExpress,
  intermunicipal,
}

extension CategoriaViajeExtension on CategoriaViaje {
  String get key {
    switch (this) {
      case CategoriaViaje.taxiEstandar:
        return 'taxi_estandar';
      case CategoriaViaje.bahiaPrioritaria:
        return 'bahia_prioritaria';
      case CategoriaViaje.ejecutivoVip:
        return 'ejecutivo_vip';
      case CategoriaViaje.envioExpress:
        return 'envio_express';
      case CategoriaViaje.intermunicipal:
        return 'intermunicipal';
    }
  }

  String get label {
    switch (this) {
      case CategoriaViaje.taxiEstandar:
        return 'Taxi Estándar';
      case CategoriaViaje.bahiaPrioritaria:
        return 'Bahía Prioritaria';
      case CategoriaViaje.ejecutivoVip:
        return 'Ejecutivo VIP';
      case CategoriaViaje.envioExpress:
        return 'Envío / Encomienda';
      case CategoriaViaje.intermunicipal:
        return 'Ciudad a Ciudad';
    }
  }

  static CategoriaViaje fromString(String? val) {
    switch (val?.toLowerCase()) {
      case 'bahia_prioritaria':
      case 'bahia':
        return CategoriaViaje.bahiaPrioritaria;
      case 'ejecutivo_vip':
      case 'vip':
        return CategoriaViaje.ejecutivoVip;
      case 'envio_express':
      case 'envio':
      case 'paquete':
        return CategoriaViaje.envioExpress;
      case 'intermunicipal':
      case 'ciudad':
        return CategoriaViaje.intermunicipal;
      case 'taxi_estandar':
      default:
        return CategoriaViaje.taxiEstandar;
    }
  }
}

class ConductorOfertaModel {
  final String conductorId;
  final String conductorNombre;
  final String conductorFotoUrl;
  final double conductorCalificacion;
  final String vehiculoPlaca;
  final String vehiculoModelo;
  final int distanciaMetros;
  final int tiempoMinutos;
  final double precioPropuesto;
  final DateTime fechaOferta;

  const ConductorOfertaModel({
    required this.conductorId,
    required this.conductorNombre,
    this.conductorFotoUrl = '',
    this.conductorCalificacion = 5.0,
    required this.vehiculoPlaca,
    this.vehiculoModelo = '',
    this.distanciaMetros = 500,
    this.tiempoMinutos = 3,
    required this.precioPropuesto,
    required this.fechaOferta,
  });

  factory ConductorOfertaModel.fromJson(Map<String, dynamic> json) {
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

    return ConductorOfertaModel(
      conductorId: json['conductor_id']?.toString() ?? '',
      conductorNombre: json['conductor_nombre']?.toString() ?? 'Conductor',
      conductorFotoUrl: json['conductor_foto_url']?.toString() ?? '',
      conductorCalificacion: parseDouble(json['conductor_calificacion'], 5.0),
      vehiculoPlaca: (json['vehiculo_placa'] ?? '').toString().toUpperCase(),
      vehiculoModelo: json['vehiculo_modelo']?.toString() ?? '',
      distanciaMetros: parseInt(json['distancia_metros'], 500),
      tiempoMinutos: parseInt(json['tiempo_minutos'], 3),
      precioPropuesto: parseDouble(json['precio_propuesto']),
      fechaOferta: parseDate(json['fecha_oferta']),
    );
  }

  Map<String, dynamic> toJson() => {
    'conductor_id': conductorId,
    'conductor_nombre': conductorNombre,
    'conductor_foto_url': conductorFotoUrl,
    'conductor_calificacion': conductorCalificacion,
    'vehiculo_placa': vehiculoPlaca,
    'vehiculo_modelo': vehiculoModelo,
    'distancia_metros': distanciaMetros,
    'tiempo_minutos': tiempoMinutos,
    'precio_propuesto': precioPropuesto,
    'fecha_oferta': Timestamp.fromDate(fechaOferta),
  };
}

class ViajeModel {
  final String id;
  final String pasajeroId;
  final String pasajeroNombre;
  final String pasajeroTelefono;
  final String conductorId;
  final String conductorNombre;
  final String conductorTelefono;
  final String vehiculoPlaca;
  final String vehiculoModelo;
  final String origenDireccion;
  final double origenLat;
  final double origenLng;
  final String destinoDireccion;
  final double destinoLat;
  final double destinoLng;
  final int sectorOrigenId;
  final int sectorDestinoId;
  final String sectorNombre;
  final double tarifaBase;
  final double recargoNocturno;
  final double recargoFestivo;
  final double recargoAeropuerto;
  final double tarifaPropuestaPasajero;
  final double tarifaTotal;
  final String metodoPago;
  final String codigoConvenio;
  final EstadoViaje estado;
  final TipoServicioViaje tipoServicio;
  final CategoriaViaje categoria;
  final DateTime fechaSolicitud;
  final DateTime? fechaAsignacion;
  final DateTime? fechaInicio;
  final DateTime? fechaFinalizacion;
  final double calificacionPasajero;
  final String comentarioPasajero;
  final double calificacionConductor;
  final String nota;

  const ViajeModel({
    required this.id,
    required this.pasajeroId,
    required this.pasajeroNombre,
    this.pasajeroTelefono = '',
    this.conductorId = '',
    this.conductorNombre = '',
    this.conductorTelefono = '',
    this.vehiculoPlaca = '',
    this.vehiculoModelo = '',
    required this.origenDireccion,
    this.origenLat = 0.0,
    this.origenLng = 0.0,
    required this.destinoDireccion,
    this.destinoLat = 0.0,
    this.destinoLng = 0.0,
    this.sectorOrigenId = 0,
    this.sectorDestinoId = 0,
    this.sectorNombre = '',
    this.tarifaBase = 0.0,
    this.recargoNocturno = 0.0,
    this.recargoFestivo = 0.0,
    this.recargoAeropuerto = 0.0,
    this.tarifaPropuestaPasajero = 0.0,
    this.tarifaTotal = 0.0,
    this.metodoPago = 'efectivo',
    this.codigoConvenio = '',
    this.estado = EstadoViaje.solicitado,
    this.tipoServicio = TipoServicioViaje.calle,
    this.categoria = CategoriaViaje.taxiEstandar,
    required this.fechaSolicitud,
    this.fechaAsignacion,
    this.fechaInicio,
    this.fechaFinalizacion,
    this.calificacionPasajero = 0.0,
    this.comentarioPasajero = '',
    this.calificacionConductor = 0.0,
    this.nota = '',
  });

  bool get estaActivo =>
      estado == EstadoViaje.solicitado ||
      estado == EstadoViaje.asignado ||
      estado == EstadoViaje.enCamino ||
      estado == EstadoViaje.aBordo;

  factory ViajeModel.fromJson(Map<String, dynamic> json, [String? docId]) {
    DateTime parseDate(dynamic val, [DateTime? fallback]) {
      if (val is Timestamp) return val.toDate();
      if (val is DateTime) return val;
      if (val is String && val.isNotEmpty) {
        return DateTime.tryParse(val) ?? fallback ?? DateTime.now();
      }
      return fallback ?? DateTime.now();
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

    return ViajeModel(
      id: docId ?? json['id']?.toString() ?? '',
      pasajeroId: json['pasajero_id']?.toString() ?? '',
      pasajeroNombre: json['pasajero_nombre']?.toString() ?? 'Pasajero',
      pasajeroTelefono: json['pasajero_telefono']?.toString() ?? '',
      conductorId: json['conductor_id']?.toString() ?? '',
      conductorNombre: json['conductor_nombre']?.toString() ?? '',
      conductorTelefono: json['conductor_telefono']?.toString() ?? '',
      vehiculoPlaca: json['vehiculo_placa']?.toString() ?? '',
      vehiculoModelo: json['vehiculo_modelo']?.toString() ?? '',
      origenDireccion: json['origen_direccion']?.toString() ?? '',
      origenLat: parseDouble(json['origen_lat']),
      origenLng: parseDouble(json['origen_lng']),
      destinoDireccion: json['destino_direccion']?.toString() ?? '',
      destinoLat: parseDouble(json['destino_lat']),
      destinoLng: parseDouble(json['destino_lng']),
      sectorOrigenId: parseInt(json['sector_origen_id']),
      sectorDestinoId: parseInt(json['sector_destino_id']),
      sectorNombre: json['sector_nombre']?.toString() ?? '',
      tarifaBase: parseDouble(json['tarifa_base']),
      recargoNocturno: parseDouble(json['recargo_nocturno']),
      recargoFestivo: parseDouble(json['recargo_festivo']),
      recargoAeropuerto: parseDouble(json['recargo_aeropuerto']),
      tarifaPropuestaPasajero: parseDouble(json['tarifa_propuesta_pasajero'] ?? json['tarifa_total']),
      tarifaTotal: parseDouble(json['tarifa_total']),
      metodoPago: json['metodo_pago']?.toString() ?? 'efectivo',
      codigoConvenio: json['codigo_convenio']?.toString() ?? '',
      estado: EstadoViajeExtension.fromString(json['estado']?.toString()),
      tipoServicio: TipoServicioViajeExtension.fromString(json['tipo_servicio']?.toString()),
      categoria: CategoriaViajeExtension.fromString(json['categoria']?.toString()),
      fechaSolicitud: parseDate(json['fecha_solicitud']),
      fechaAsignacion: json['fecha_asignacion'] != null ? parseDate(json['fecha_asignacion']) : null,
      fechaInicio: json['fecha_inicio'] != null ? parseDate(json['fecha_inicio']) : null,
      fechaFinalizacion: json['fecha_finalizacion'] != null ? parseDate(json['fecha_finalizacion']) : null,
      calificacionPasajero: parseDouble(json['calificacion_pasajero']),
      comentarioPasajero: json['comentario_pasajero']?.toString() ?? '',
      calificacionConductor: parseDouble(json['calificacion_conductor']),
      nota: json['nota']?.toString() ?? '',
    );
  }

  factory ViajeModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    return ViajeModel.fromJson(data, doc.id);
  }

  Map<String, dynamic> toFirestore() {
    return {
      'id': id,
      'pasajero_id': pasajeroId,
      'pasajero_nombre': pasajeroNombre,
      'pasajero_telefono': pasajeroTelefono,
      'conductor_id': conductorId,
      'conductor_nombre': conductorNombre,
      'conductor_telefono': conductorTelefono,
      'vehiculo_placa': vehiculoPlaca,
      'vehiculo_modelo': vehiculoModelo,
      'origen_direccion': origenDireccion,
      'origen_lat': origenLat,
      'origen_lng': origenLng,
      'destino_direccion': destinoDireccion,
      'destino_lat': destinoLat,
      'destino_lng': destinoLng,
      'sector_origen_id': sectorOrigenId,
      'sector_destino_id': sectorDestinoId,
      'sector_nombre': sectorNombre,
      'tarifa_base': tarifaBase,
      'recargo_nocturno': recargoNocturno,
      'recargo_festivo': recargoFestivo,
      'recargo_aeropuerto': recargoAeropuerto,
      'tarifa_propuesta_pasajero': tarifaPropuestaPasajero,
      'tarifa_total': tarifaTotal,
      'metodo_pago': metodoPago,
      'codigo_convenio': codigoConvenio,
      'estado': estado.key,
      'tipo_servicio': tipoServicio.key,
      'categoria': categoria.key,
      'fecha_solicitud': Timestamp.fromDate(fechaSolicitud),
      if (fechaAsignacion != null) 'fecha_asignacion': Timestamp.fromDate(fechaAsignacion!),
      if (fechaInicio != null) 'fecha_inicio': Timestamp.fromDate(fechaInicio!),
      if (fechaFinalizacion != null) 'fecha_finalizacion': Timestamp.fromDate(fechaFinalizacion!),
      'calificacion_pasajero': calificacionPasajero,
      'comentario_pasajero': comentarioPasajero,
      'calificacion_conductor': calificacionConductor,
      'nota': nota,
    };
  }

  Map<String, dynamic> toJson() => toFirestore();

  ViajeModel copyWith({
    String? id,
    String? pasajeroId,
    String? pasajeroNombre,
    String? pasajeroTelefono,
    String? conductorId,
    String? conductorNombre,
    String? conductorTelefono,
    String? vehiculoPlaca,
    String? vehiculoModelo,
    String? origenDireccion,
    double? origenLat,
    double? origenLng,
    String? destinoDireccion,
    double? destinoLat,
    double? destinoLng,
    int? sectorOrigenId,
    int? sectorDestinoId,
    String? sectorNombre,
    double? tarifaBase,
    double? recargoNocturno,
    double? recargoFestivo,
    double? recargoAeropuerto,
    double? tarifaPropuestaPasajero,
    double? tarifaTotal,
    String? metodoPago,
    String? codigoConvenio,
    EstadoViaje? estado,
    TipoServicioViaje? tipoServicio,
    CategoriaViaje? categoria,
    DateTime? fechaSolicitud,
    DateTime? fechaAsignacion,
    DateTime? fechaInicio,
    DateTime? fechaFinalizacion,
    double? calificacionPasajero,
    String? comentarioPasajero,
    double? calificacionConductor,
    String? nota,
  }) {
    return ViajeModel(
      id: id ?? this.id,
      pasajeroId: pasajeroId ?? this.pasajeroId,
      pasajeroNombre: pasajeroNombre ?? this.pasajeroNombre,
      pasajeroTelefono: pasajeroTelefono ?? this.pasajeroTelefono,
      conductorId: conductorId ?? this.conductorId,
      conductorNombre: conductorNombre ?? this.conductorNombre,
      conductorTelefono: conductorTelefono ?? this.conductorTelefono,
      vehiculoPlaca: vehiculoPlaca ?? this.vehiculoPlaca,
      vehiculoModelo: vehiculoModelo ?? this.vehiculoModelo,
      origenDireccion: origenDireccion ?? this.origenDireccion,
      origenLat: origenLat ?? this.origenLat,
      origenLng: origenLng ?? this.origenLng,
      destinoDireccion: destinoDireccion ?? this.destinoDireccion,
      destinoLat: destinoLat ?? this.destinoLat,
      destinoLng: destinoLng ?? this.destinoLng,
      sectorOrigenId: sectorOrigenId ?? this.sectorOrigenId,
      sectorDestinoId: sectorDestinoId ?? this.sectorDestinoId,
      sectorNombre: sectorNombre ?? this.sectorNombre,
      tarifaBase: tarifaBase ?? this.tarifaBase,
      recargoNocturno: recargoNocturno ?? this.recargoNocturno,
      recargoFestivo: recargoFestivo ?? this.recargoFestivo,
      recargoAeropuerto: recargoAeropuerto ?? this.recargoAeropuerto,
      tarifaPropuestaPasajero: tarifaPropuestaPasajero ?? this.tarifaPropuestaPasajero,
      tarifaTotal: tarifaTotal ?? this.tarifaTotal,
      metodoPago: metodoPago ?? this.metodoPago,
      codigoConvenio: codigoConvenio ?? this.codigoConvenio,
      estado: estado ?? this.estado,
      tipoServicio: tipoServicio ?? this.tipoServicio,
      categoria: categoria ?? this.categoria,
      fechaSolicitud: fechaSolicitud ?? this.fechaSolicitud,
      fechaAsignacion: fechaAsignacion ?? this.fechaAsignacion,
      fechaInicio: fechaInicio ?? this.fechaInicio,
      fechaFinalizacion: fechaFinalizacion ?? this.fechaFinalizacion,
      calificacionPasajero: calificacionPasajero ?? this.calificacionPasajero,
      comentarioPasajero: comentarioPasajero ?? this.comentarioPasajero,
      calificacionConductor: calificacionConductor ?? this.calificacionConductor,
      nota: nota ?? this.nota,
    );
  }
}
