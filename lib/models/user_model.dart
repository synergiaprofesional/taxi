import 'package:cloud_firestore/cloud_firestore.dart';

enum UserRole {
  adminGarita,
  conductor,
  pasajero,
}

extension UserRoleExtension on UserRole {
  String get key {
    switch (this) {
      case UserRole.adminGarita:
        return 'admin_garita';
      case UserRole.conductor:
        return 'conductor';
      case UserRole.pasajero:
        return 'pasajero';
    }
  }

  String get label {
    switch (this) {
      case UserRole.adminGarita:
        return 'Administrador / Garita';
      case UserRole.conductor:
        return 'Conductor de Taxi';
      case UserRole.pasajero:
        return 'Pasajero';
    }
  }

  static UserRole fromString(String? role) {
    switch (role?.toLowerCase()) {
      case 'admin_garita':
      case 'admin':
      case 'garita':
      case 'despachador':
        return UserRole.adminGarita;
      case 'conductor':
      case 'driver':
      case 'taxista':
        return UserRole.conductor;
      case 'pasajero':
      case 'cliente':
      case 'client':
      default:
        return UserRole.pasajero;
    }
  }
}

class UserModel {
  final String id;
  final String email;
  final String nombre;
  final String telefono;
  final String cedula;
  final UserRole rol;
  final String organizacionId;
  final String gremioNombre;
  final bool esConductorPrivado;
  final String vehiculoAsignadoPlaca;
  final bool activo;
  final double calificacionPromedio;
  final String codigoReferido;
  final String codigoConvenio;
  final String fotoUrl;
  final DateTime fechaCreacion;

  const UserModel({
    required this.id,
    required this.email,
    required this.nombre,
    this.telefono = '',
    this.cedula = '',
    this.rol = UserRole.pasajero,
    this.organizacionId = '',
    this.gremioNombre = '',
    this.esConductorPrivado = false,
    this.vehiculoAsignadoPlaca = '',
    this.activo = true,
    this.calificacionPromedio = 5.0,
    this.codigoReferido = '',
    this.codigoConvenio = '',
    this.fotoUrl = '',
    required this.fechaCreacion,
  });

  bool get esAdmin => rol == UserRole.adminGarita;
  bool get esConductor => rol == UserRole.conductor;
  bool get esPasajero => rol == UserRole.pasajero;

  factory UserModel.fromJson(Map<String, dynamic> json, [String? docId]) {
    DateTime parseDate(dynamic val) {
      if (val is Timestamp) return val.toDate();
      if (val is DateTime) return val;
      if (val is String && val.isNotEmpty) {
        return DateTime.tryParse(val) ?? DateTime.now();
      }
      return DateTime.now();
    }

    return UserModel(
      id: docId ?? json['id']?.toString() ?? '',
      email: json['email']?.toString() ?? '',
      nombre: json['nombre']?.toString() ?? json['name']?.toString() ?? 'Usuario',
      telefono: json['telefono']?.toString() ?? json['phone']?.toString() ?? '',
      cedula: json['cedula']?.toString() ?? json['vat']?.toString() ?? '',
      rol: UserRoleExtension.fromString(json['rol']?.toString() ?? json['role']?.toString()),
      organizacionId: json['organizacion_id']?.toString() ?? '',
      gremioNombre: json['gremio_nombre']?.toString() ?? '',
      esConductorPrivado: json['es_conductor_privado'] == true,
      vehiculoAsignadoPlaca: json['vehiculo_placa']?.toString() ?? '',
      activo: json['activo'] ?? true,
      calificacionPromedio: (json['calificacion_promedio'] ?? 5.0).toDouble(),
      codigoReferido: json['codigo_referido']?.toString() ?? '',
      codigoConvenio: json['codigo_convenio']?.toString() ?? '',
      fotoUrl: json['foto_url']?.toString() ?? '',
      fechaCreacion: parseDate(json['fecha_creacion'] ?? json['created_at']),
    );
  }

  factory UserModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    return UserModel.fromJson(data, doc.id);
  }

  Map<String, dynamic> toFirestore() {
    return {
      'id': id,
      'email': email,
      'nombre': nombre,
      'telefono': telefono,
      'cedula': cedula,
      'rol': rol.key,
      'organizacion_id': organizacionId,
      'gremio_nombre': gremioNombre,
      'es_conductor_privado': esConductorPrivado,
      'vehiculo_placa': vehiculoAsignadoPlaca,
      'activo': activo,
      'calificacion_promedio': calificacionPromedio,
      'codigo_referido': codigoReferido,
      'codigo_convenio': codigoConvenio,
      'foto_url': fotoUrl,
      'fecha_creacion': Timestamp.fromDate(fechaCreacion),
    };
  }

  Map<String, dynamic> toJson() => toFirestore();

  UserModel copyWith({
    String? id,
    String? email,
    String? nombre,
    String? telefono,
    String? cedula,
    UserRole? rol,
    String? organizacionId,
    String? gremioNombre,
    bool? esConductorPrivado,
    String? vehiculoAsignadoPlaca,
    bool? activo,
    double? calificacionPromedio,
    String? codigoReferido,
    String? codigoConvenio,
    String? fotoUrl,
    DateTime? fechaCreacion,
  }) {
    return UserModel(
      id: id ?? this.id,
      email: email ?? this.email,
      nombre: nombre ?? this.nombre,
      telefono: telefono ?? this.telefono,
      cedula: cedula ?? this.cedula,
      rol: rol ?? this.rol,
      organizacionId: organizacionId ?? this.organizacionId,
      gremioNombre: gremioNombre ?? this.gremioNombre,
      esConductorPrivado: esConductorPrivado ?? this.esConductorPrivado,
      vehiculoAsignadoPlaca: vehiculoAsignadoPlaca ?? this.vehiculoAsignadoPlaca,
      activo: activo ?? this.activo,
      calificacionPromedio: calificacionPromedio ?? this.calificacionPromedio,
      codigoReferido: codigoReferido ?? this.codigoReferido,
      codigoConvenio: codigoConvenio ?? this.codigoConvenio,
      fotoUrl: fotoUrl ?? this.fotoUrl,
      fechaCreacion: fechaCreacion ?? this.fechaCreacion,
    );
  }
}
