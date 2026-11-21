import 'package:cloud_firestore/cloud_firestore.dart';

enum TipoOrganizacion {
  gremio,
  cooperativa,
  empresaPrivada,
  asociacion,
}

extension TipoOrganizacionExtension on TipoOrganizacion {
  String get key {
    switch (this) {
      case TipoOrganizacion.gremio:
        return 'gremio';
      case TipoOrganizacion.cooperativa:
        return 'cooperativa';
      case TipoOrganizacion.empresaPrivada:
        return 'empresa_privada';
      case TipoOrganizacion.asociacion:
        return 'asociacion';
    }
  }

  String get label {
    switch (this) {
      case TipoOrganizacion.gremio:
        return 'Gremio Taxista';
      case TipoOrganizacion.cooperativa:
        return 'Cooperativa de Transporte';
      case TipoOrganizacion.empresaPrivada:
        return 'Empresa Privada';
      case TipoOrganizacion.asociacion:
        return 'Asociación';
    }
  }

  static TipoOrganizacion fromString(String? val) {
    switch (val?.toLowerCase()) {
      case 'cooperativa':
        return TipoOrganizacion.cooperativa;
      case 'empresa_privada':
      case 'empresa':
        return TipoOrganizacion.empresaPrivada;
      case 'asociacion':
        return TipoOrganizacion.asociacion;
      case 'gremio':
      default:
        return TipoOrganizacion.gremio;
    }
  }
}

class OrganizacionModel {
  final String id;
  final String nombre;
  final String nit;
  final TipoOrganizacion tipo;
  final String codigoConvenio;
  final String direccion;
  final String telefono;
  final bool flotaPublicaHabilitada;
  final bool flotaPrivadaHabilitada;
  final int totalVehiculos;
  final int totalConductores;
  final bool activa;
  final DateTime fechaCreacion;

  const OrganizacionModel({
    required this.id,
    required this.nombre,
    this.nit = '',
    this.tipo = TipoOrganizacion.gremio,
    this.codigoConvenio = '',
    this.direccion = '',
    this.telefono = '',
    this.flotaPublicaHabilitada = true,
    this.flotaPrivadaHabilitada = false,
    this.totalVehiculos = 0,
    this.totalConductores = 0,
    this.activa = true,
    required this.fechaCreacion,
  });

  factory OrganizacionModel.fromJson(Map<String, dynamic> json, [String? docId]) {
    DateTime parseDate(dynamic val) {
      if (val is Timestamp) return val.toDate();
      if (val is DateTime) return val;
      if (val is String && val.isNotEmpty) {
        return DateTime.tryParse(val) ?? DateTime.now();
      }
      return DateTime.now();
    }

    return OrganizacionModel(
      id: docId ?? json['id']?.toString() ?? '',
      nombre: json['nombre']?.toString() ?? json['name']?.toString() ?? 'Organización',
      nit: json['nit']?.toString() ?? '',
      tipo: TipoOrganizacionExtension.fromString(json['tipo']?.toString()),
      codigoConvenio: json['codigo_convenio']?.toString() ?? '',
      direccion: json['direccion']?.toString() ?? '',
      telefono: json['telefono']?.toString() ?? '',
      flotaPublicaHabilitada: json['flota_publica_habilitada'] ?? true,
      flotaPrivadaHabilitada: json['flota_privada_habilitada'] ?? false,
      totalVehiculos: (json['total_vehiculos'] ?? 0).toInt(),
      totalConductores: (json['total_conductores'] ?? 0).toInt(),
      activa: json['activa'] ?? true,
      fechaCreacion: parseDate(json['fecha_creacion']),
    );
  }

  factory OrganizacionModel.fromFirestore(DocumentSnapshot doc) {
    final data = (doc.data() as Map<String, dynamic>?) ?? {};
    return OrganizacionModel.fromJson(data, doc.id);
  }

  Map<String, dynamic> toFirestore() {
    return {
      'id': id,
      'nombre': nombre,
      'nit': nit,
      'tipo': tipo.key,
      'codigo_convenio': codigoConvenio,
      'direccion': direccion,
      'telefono': telefono,
      'flota_publica_habilitada': flotaPublicaHabilitada,
      'flota_privada_habilitada': flotaPrivadaHabilitada,
      'total_vehiculos': totalVehiculos,
      'total_conductores': totalConductores,
      'activa': activa,
      'fecha_creacion': Timestamp.fromDate(fechaCreacion),
    };
  }

  Map<String, dynamic> toJson() => toFirestore();
}
