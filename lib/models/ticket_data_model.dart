class TicketDataModel {
  final String empresaNombre;
  final String nit;
  final String bahiaNombre;
  final String turnoNumero;
  final String placa;
  final String movilNumero;
  final String conductor;
  final String destino;
  final String direccion;
  final DateTime fechaHora;
  final double valorTotal;
  final String cajero;
  final String pieMensaje;
  final int turnoId;

  TicketDataModel({
    this.empresaNombre = 'FUNDETAXCOL / SYNERGIA MÓVIL',
    this.nit = 'NIT 900.542.188-4',
    required this.bahiaNombre,
    required this.turnoNumero,
    required this.placa,
    this.movilNumero = 'N/A',
    required this.conductor,
    this.destino = '',
    this.direccion = '',
    required this.fechaHora,
    required this.valorTotal,
    this.cajero = 'Operador 01',
    this.pieMensaje = '¡Feliz viaje! Sistema Synergia Móvil',
    this.turnoId = 0,
  });
}
