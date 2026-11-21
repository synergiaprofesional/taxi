import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/core/network/network_config.dart';
import 'package:taxi/models/ticket_data_model.dart';
import 'package:taxi/services/printer_service.dart';

void main() {
  group('NetworkConfig Tests', () {
    test('Normaliza host eliminando http:// previo', () {
      final config = NetworkConfig(host: 'http://pidemeaqui.com', useHttps: true);
      expect(config.rawHost, 'pidemeaqui.com');
      expect(config.buildUrl('/web/login'), 'https://pidemeaqui.com/web/login');
    });

    test('Alterna entre HTTPS y HTTP correctamente', () {
      final config = NetworkConfig(host: 'pidemeaqui.com', useHttps: false);
      expect(config.buildUrl('/web/login'), 'http://pidemeaqui.com/web/login');

      config.setUseHttps(true);
      expect(config.buildUrl('/web/login'), 'https://pidemeaqui.com/web/login');
    });
  });

  group('PrinterService ESC/POS Tests', () {
    test('Genera bytes binarios ESC/POS con init y autocorte', () {
      final service = PrinterService();
      final ticket = TicketDataModel(
        bahiaNombre: 'Bahía Principal',
        turnoNumero: 'T-0099',
        placa: 'XYZ-123',
        conductor: 'Pedro Pérez',
        fechaHora: DateTime(2026, 10, 17, 19, 30),
        valorTotal: 15000.0,
      );

      final bytes = service.generarBytesEscPos(ticket);
      expect(bytes.isNotEmpty, true);

      // Byte 0 y 1 deben ser ESC @ (0x1B, 0x40)
      expect(bytes[0], 0x1B);
      expect(bytes[1], 0x40);

      // Los últimos 4 bytes con autocorte deben ser GS V 66 0 (0x1D, 0x56, 0x42, 0x00)
      expect(bytes[bytes.length - 4], 0x1D);
      expect(bytes[bytes.length - 3], 0x56);
      expect(bytes[bytes.length - 2], 0x42);
      expect(bytes[bytes.length - 1], 0x00);
    });

    test('Genera texto de tiquete con ancho de papel de 58mm', () {
      final service = PrinterService();
      final ticket = TicketDataModel(
        bahiaNombre: 'Bahía Norte',
        turnoNumero: 'T-0042',
        placa: 'WBD-512',
        conductor: 'Carlos Ramírez',
        fechaHora: DateTime(2026, 10, 17, 19, 0),
        valorTotal: 15000.0,
      );

      final texto = service.generarTextoTiquete(ticket);
      expect(texto.contains('TURNO:'), true);
      expect(texto.contains('T-0042'), true);
      expect(texto.contains('WBD-512'), true);
      expect(texto.contains('Carlos Ramirez'), true);
    });
  });
}
