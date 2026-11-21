enum TipoImpresora {
  bluetooth,
  tcp,
  spoolerWindows,
  emulador,
  url,
}

class PrinterConfigModel {
  final TipoImpresora tipo;
  final String nombreODireccion;
  final int puerto;
  final int anchoPapel; // 58 u 80
  final bool autoCorte;

  const PrinterConfigModel({
    this.tipo = TipoImpresora.emulador,
    this.nombreODireccion = 'Emulador Virtual Synergia',
    this.puerto = 9100,
    this.anchoPapel = 58,
    this.autoCorte = true,
  });

  Map<String, dynamic> toJson() => {
        'tipo': tipo.index,
        'nombreODireccion': nombreODireccion,
        'puerto': puerto,
        'anchoPapel': anchoPapel,
        'autoCorte': autoCorte,
      };

  factory PrinterConfigModel.fromJson(Map<String, dynamic> json) {
    final tipoIdx = json['tipo'] ?? 3;
    final tipo = (tipoIdx >= 0 && tipoIdx < TipoImpresora.values.length)
        ? TipoImpresora.values[tipoIdx]
        : TipoImpresora.emulador;
    return PrinterConfigModel(
      tipo: tipo,
      nombreODireccion: json['nombreODireccion'] ?? 'Emulador Virtual Synergia',
      puerto: json['puerto'] ?? 9100,
      anchoPapel: json['anchoPapel'] ?? 58,
      autoCorte: json['autoCorte'] ?? true,
    );
  }
}
