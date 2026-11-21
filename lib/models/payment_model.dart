class AhorroModel {
  final String concepto;
  final double valor;

  AhorroModel({
    required this.concepto,
    required this.valor,
  });

  factory AhorroModel.fromJson(Map<String, dynamic> json) {
    return AhorroModel(
      concepto: (json['concepto'] ?? json['name'] ?? 'Ahorro').toString(),
      valor: (json['valor'] ?? json['amount'] ?? 0.0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() => {
    'concepto': concepto,
    'valor': valor,
  };
}

class CompanyModel {
  final String name;
  final String phone;
  final String email;
  final String website;
  final String reportFooter;

  CompanyModel({
    this.name = 'FUNDETAXCOL',
    this.phone = '',
    this.email = '',
    this.website = '',
    this.reportFooter = 'Régimen Común - Sistema de Despacho y Recaudo',
  });

  factory CompanyModel.fromJson(Map<String, dynamic>? json) {
    if (json == null) return CompanyModel();
    return CompanyModel(
      name: (json['name'] ?? 'FUNDETAXCOL').toString(),
      phone: (json['phone'] ?? '').toString(),
      email: (json['email'] ?? '').toString(),
      website: (json['website'] ?? '').toString(),
      reportFooter: (json['report_footer'] ?? 'Régimen Común - Sistema de Despacho y Recaudo').toString(),
    );
  }
}

class ConceptoCobroModel {
  final int id;
  final String nombre;
  final double valorPorDefecto;
  final bool obligatorio;

  ConceptoCobroModel({
    required this.id,
    required this.nombre,
    required this.valorPorDefecto,
    this.obligatorio = false,
  });

  factory ConceptoCobroModel.fromJson(Map<String, dynamic> json) {
    return ConceptoCobroModel(
      id: json['id'] is int ? json['id'] : int.tryParse(json['id'].toString()) ?? 0,
      nombre: (json['name'] ?? json['nombre'] ?? 'Concepto').toString(),
      valorPorDefecto: (json['valor'] ?? json['price'] ?? 0.0).toDouble(),
      obligatorio: json['obligatorio'] ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': nombre,
    'valor': valorPorDefecto,
  };
}

class PaymentConceptLine {
  final ConceptoCobroModel concepto;
  int cantidad;
  double valorUnitario;

  PaymentConceptLine({
    required this.concepto,
    this.cantidad = 1,
    required this.valorUnitario,
  });

  double get subtotal => cantidad * valorUnitario;

  Map<String, dynamic> toOdooRpc() => {
    'concepto_id': concepto.id > 0 ? concepto.id : 1,
    'cantidad': cantidad,
    'valor': valorUnitario,
    if (concepto.nombre.isNotEmpty) 'name': concepto.nombre,
  };
}

DateTime parseOdooDateTime(dynamic raw) {
  if (raw == null || raw == false) return DateTime.now();
  var str = raw.toString().trim();
  if (str.isEmpty) return DateTime.now();
  str = str.replaceFirst(' ', 'T');
  final dt = DateTime.tryParse(str);
  if (dt != null) {
    return dt.isUtc ? dt.toLocal() : dt;
  }
  return DateTime.now();
}

class PagoRecaudoModel {
  final int id;
  final String consecutivo;
  final int bahiaId;
  final int bahiaSesionId;
  final String bahiaNombre;
  final int vehiculoId;
  final String placa;
  final int conductorId;
  final String conductorNombre;
  final String conceptoNombre;
  final DateTime fecha;
  final double total;
  final double totalAhorro;
  final int ingreso;
  final List<PaymentConceptLine> lineas;
  final List<AhorroModel> ahorros;
  final CompanyModel company;
  final String estado; // 'borrador', 'pagado', 'anulado'

  PagoRecaudoModel({
    required this.id,
    required this.consecutivo,
    required this.bahiaId,
    this.bahiaSesionId = 0,
    required this.bahiaNombre,
    required this.vehiculoId,
    required this.placa,
    required this.conductorId,
    required this.conductorNombre,
    this.conceptoNombre = 'Recaudo',
    required this.fecha,
    required this.total,
    this.totalAhorro = 0.0,
    this.ingreso = 1,
    required this.lineas,
    this.ahorros = const [],
    CompanyModel? company,
    this.estado = 'pagado',
  }) : company = company ?? CompanyModel();

  factory PagoRecaudoModel.fromJson(Map<String, dynamic> json) {
    final rawAhorros = json['ahorro_ids'] ?? [];
    List<AhorroModel> ahorroList = [];
    if (rawAhorros is List) {
      ahorroList = rawAhorros.map((e) => AhorroModel.fromJson(Map<String, dynamic>.from(e))).toList();
    }

    // bahia_id y bahia_sesion_id
    int bId = 0;
    String bNom = 'Bahía';
    final rawBahia = json['bahia_id'];
    if (rawBahia is Map) {
      bId = rawBahia['id'] is int ? rawBahia['id'] : int.tryParse(rawBahia['id'].toString()) ?? 0;
      bNom = rawBahia['name']?.toString() ?? 'Bahía';
    } else if (rawBahia is List && rawBahia.length >= 2) {
      bId = rawBahia[0] is int ? rawBahia[0] : int.tryParse(rawBahia[0].toString()) ?? 0;
      bNom = rawBahia[1]?.toString() ?? 'Bahía';
    } else if (rawBahia is int) {
      bId = rawBahia;
    }

    final int bSesId = json['bahia_sesion_id'] is int
        ? json['bahia_sesion_id']
        : (int.tryParse(json['bahia_sesion_id']?.toString() ?? '') ?? bId);

    // vehiculo_id y placa
    int vId = 0;
    String vPlaca = '';
    final rawVeh = json['vehiculo_id'];
    if (rawVeh is Map) {
      vId = rawVeh['id'] is int ? rawVeh['id'] : int.tryParse(rawVeh['id'].toString()) ?? 0;
      vPlaca = rawVeh['name']?.toString() ?? '';
    } else if (rawVeh is List && rawVeh.length >= 2) {
      vId = rawVeh[0] is int ? rawVeh[0] : int.tryParse(rawVeh[0].toString()) ?? 0;
      vPlaca = rawVeh[1]?.toString() ?? '';
    } else if (rawVeh is int) {
      vId = rawVeh;
    }
    if (vPlaca.isEmpty) {
      vPlaca = (json['placa'] ?? '').toString();
    }

    // conductor_id y nombre
    int cId = 0;
    String cNom = '';
    final rawCond = json['conductor_id'];
    if (rawCond is Map) {
      cId = rawCond['id'] is int ? rawCond['id'] : int.tryParse(rawCond['id'].toString()) ?? 0;
      cNom = rawCond['name']?.toString() ?? '';
    } else if (rawCond is List && rawCond.length >= 2) {
      cId = rawCond[0] is int ? rawCond[0] : int.tryParse(rawCond[0].toString()) ?? 0;
      cNom = rawCond[1]?.toString() ?? '';
    } else if (rawCond is int) {
      cId = rawCond;
    }
    if (cNom.isEmpty) {
      cNom = (json['conductor'] ?? '').toString();
    }

    // total / valor
    double totalParsed = 0.0;
    if (json['total'] != null) {
      totalParsed = (json['total'] is num) ? (json['total'] as num).toDouble() : (double.tryParse(json['total'].toString()) ?? 0.0);
    } else if (json['valor'] != null) {
      totalParsed = (json['valor'] is num) ? (json['valor'] as num).toDouble() : (double.tryParse(json['valor'].toString()) ?? 0.0);
    }

    // ahorro
    double ahorroParsed = 0.0;
    if (json['ahorro'] != null) {
      ahorroParsed = (json['ahorro'] is num) ? (json['ahorro'] as num).toDouble() : (double.tryParse(json['ahorro'].toString()) ?? 0.0);
    }

    // ingreso
    int ingresoParsed = 1;
    if (json['ingreso'] != null) {
      ingresoParsed = (json['ingreso'] is int) ? json['ingreso'] : (int.tryParse(json['ingreso'].toString()) ?? 1);
    }

    // Parseo de conceptos y líneas de recaudo
    final List<PaymentConceptLine> lineasList = [];
    String conceptoDetectado = '';

    final rawConceptos = json['concepto_ids'];
    if (rawConceptos is List && rawConceptos.isNotEmpty) {
      for (final rawItem in rawConceptos) {
        if (rawItem is Map) {
          final itemMap = Map<String, dynamic>.from(rawItem);
          final rawConc = itemMap['concepto_id'] ?? itemMap['concepto'];
          ConceptoCobroModel conceptoModel;
          if (rawConc is Map) {
            conceptoModel = ConceptoCobroModel.fromJson(Map<String, dynamic>.from(rawConc));
          } else if (rawConc is List && rawConc.length >= 2) {
            conceptoModel = ConceptoCobroModel(
              id: rawConc[0] is int ? rawConc[0] : (int.tryParse(rawConc[0].toString()) ?? 0),
              nombre: rawConc[1].toString(),
              valorPorDefecto: (itemMap['valor'] is num) ? (itemMap['valor'] as num).toDouble() : 0.0,
            );
          } else if (rawConc is int) {
            conceptoModel = ConceptoCobroModel(
              id: rawConc,
              nombre: (itemMap['name'] ?? itemMap['nombre'] ?? 'Concepto #$rawConc').toString(),
              valorPorDefecto: (itemMap['valor'] is num) ? (itemMap['valor'] as num).toDouble() : 0.0,
            );
          } else if (rawConc is String && rawConc.isNotEmpty) {
            conceptoModel = ConceptoCobroModel(
              id: 0,
              nombre: rawConc,
              valorPorDefecto: (itemMap['valor'] is num) ? (itemMap['valor'] as num).toDouble() : 0.0,
            );
          } else {
            final nombreFallback = (itemMap['name'] ?? itemMap['nombre'] ?? 'Recaudo').toString();
            conceptoModel = ConceptoCobroModel(
              id: 0,
              nombre: nombreFallback,
              valorPorDefecto: (itemMap['valor'] is num) ? (itemMap['valor'] as num).toDouble() : 0.0,
            );
          }

          final cant = itemMap['cantidad'] is int ? itemMap['cantidad'] as int : (int.tryParse(itemMap['cantidad']?.toString() ?? '1') ?? 1);
          final val = (itemMap['valor'] is num) ? (itemMap['valor'] as num).toDouble() : (double.tryParse(itemMap['valor']?.toString() ?? '0') ?? 0.0);

          lineasList.add(PaymentConceptLine(
            concepto: conceptoModel,
            cantidad: cant,
            valorUnitario: val > 0 ? val : conceptoModel.valorPorDefecto,
          ));

          if (conceptoDetectado.isEmpty && conceptoModel.nombre.isNotEmpty && conceptoModel.nombre != 'Concepto') {
            conceptoDetectado = conceptoModel.nombre;
          }
        }
      }
    }

    // Prioridad de concepto: Si el despachador escribió un texto manual (guardado en 'nota'),
    // ese texto tiene precedencia absoluta sobre el ID genérico devuelto por Odoo.
    final String notaLimpia = (json['nota'] ?? '').toString().trim();
    if (notaLimpia.isNotEmpty && notaLimpia.toLowerCase() != 'false' && notaLimpia.toLowerCase() != 'recaudo') {
      conceptoDetectado = notaLimpia;
    }

    if (conceptoDetectado.isEmpty) {
      if (json['concepto'] != null && json['concepto'].toString().trim().isNotEmpty) {
        conceptoDetectado = json['concepto'].toString().trim();
      } else if (json['tipo_pago'] != null && json['tipo_pago'].toString().trim().isNotEmpty) {
        conceptoDetectado = json['tipo_pago'].toString().trim();
      } else if (notaLimpia.isNotEmpty && notaLimpia.toLowerCase() != 'false') {
        conceptoDetectado = notaLimpia;
      } else {
        conceptoDetectado = 'Recaudo';
      }
    }

    return PagoRecaudoModel(
      id: json['id'] is int ? json['id'] : int.tryParse(json['id'].toString()) ?? 0,
      consecutivo: (json['consecutivo'] ?? json['name'] ?? 'REC-0000').toString(),
      bahiaId: bId,
      bahiaSesionId: bSesId,
      bahiaNombre: bNom,
      vehiculoId: vId,
      placa: vPlaca,
      conductorId: cId,
      conductorNombre: cNom,
      conceptoNombre: conceptoDetectado,
      fecha: parseOdooDateTime(json['fecha']),
      total: totalParsed,
      totalAhorro: ahorroParsed,
      ingreso: ingresoParsed,
      lineas: lineasList,
      ahorros: ahorroList,
      company: CompanyModel.fromJson(json['company']),
      estado: json['state'] ?? 'pagado',
    );
  }

  Map<String, dynamic> toOdooJson() => {
    'bahia_id': bahiaId,
    'vehiculo_id': vehiculoId,
    'conductor_id': conductorId,
    'concepto_ids': lineas.map((l) => [0, 0, l.toOdooRpc()]).toList(),
  };
}
