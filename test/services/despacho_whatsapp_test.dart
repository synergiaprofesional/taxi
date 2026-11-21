import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/core/utils/whatsapp_tracking_helper.dart';
import 'package:taxi/models/viaje_model.dart';

void main() {
  group('WhatsAppTrackingHelper Unit Tests', () {
    test('formatearNumeroColombia limpia y añade prefijo 57 a números de 10 dígitos', () {
      expect(WhatsAppTrackingHelper.formatearNumeroColombia('3001234567'), equals('573001234567'));
      expect(WhatsAppTrackingHelper.formatearNumeroColombia('+57 310 987 6543'), equals('573109876543'));
      expect(WhatsAppTrackingHelper.formatearNumeroColombia('300-123-4567'), equals('573001234567'));
      expect(WhatsAppTrackingHelper.formatearNumeroColombia('573001234567'), equals('573001234567'));
      expect(WhatsAppTrackingHelper.formatearNumeroColombia(''), equals(''));
    });

    test('generarUrlWebTracking produce URL canónica de seguimiento', () {
      final url = WhatsAppTrackingHelper.generarUrlWebTracking('viaje_abc_789');
      expect(url, equals('https://pidemeaqui.com/t/viaje_abc_789'));

      final urlCustom = WhatsAppTrackingHelper.generarUrlWebTracking('viaje_xyz', baseUrl: 'https://m.taxi.co/');
      expect(urlCustom, equals('https://m.taxi.co/t/viaje_xyz'));
    });

    test('construirMensajeDespacho genera texto formal con todos los datos de seguridad vial', () {
      final mensaje = WhatsAppTrackingHelper.construirMensajeDespacho(
        bahiaNombre: 'Caribe Plaza',
        placa: 'WGM776',
        conductor: 'Antonio Banderas',
        destino: 'Bocagrande',
        valorTotal: 18000.0,
        urlTracking: 'https://pidemeaqui.com/t/viaje_123',
      );

      expect(mensaje, contains('¡Tu Taxi Formal en Bahía Caribe Plaza está listo!'));
      expect(mensaje, contains('WGM776'));
      expect(mensaje, contains('Antonio Banderas'));
      expect(mensaje, contains('Bocagrande'));
      expect(mensaje, contains('18.000 COP'));
      expect(mensaje, contains('https://pidemeaqui.com/t/viaje_123'));
    });

    test('generarUrlWhatsApp codifica apropiadamente la URI con el prefijo telefónico', () {
      final url = WhatsAppTrackingHelper.generarUrlWhatsApp(
        telefono: '3001234567',
        mensaje: 'Hola Taxi',
      );

      expect(url, startsWith('https://api.whatsapp.com/send?phone=573001234567&text=Hola'));
      expect(url, contains(Uri.encodeComponent('Hola Taxi')));
    });

    test('ViajeModel para bahiaPrioritaria serializa campos de tracking para pasajero sin app', () {
      final viaje = ViajeModel(
        id: 'viaje_test_bahia',
        pasajeroId: 'pasajero_bahia_573001234567',
        pasajeroNombre: 'Pasajero Bahía Caribe Plaza',
        pasajeroTelefono: '573001234567',
        categoria: CategoriaViaje.bahiaPrioritaria,
        estado: EstadoViaje.asignado,
        origen: 'Bahía Caribe Plaza',
        destino: 'Manga',
        precioSugerido: 18000.0,
        precioAcordado: 18000.0,
        conductorId: 'cond_456',
        conductorNombre: 'José Pérez',
        conductorTelefono: '',
        vehiculoPlaca: 'WGN842',
        vehiculoModelo: 'Kia Rio Taxi',
        fechaSolicitud: DateTime(2026, 11, 21, 12, 30),
      );

      final json = viaje.toJson();
      expect(json['categoria'], equals('bahia_prioritaria'));
      expect(json['estado'], equals('asignado'));
      expect(json['vehiculo_placa'], equals('WGN842'));
      expect(json['pasajero_telefono'], equals('573001234567'));
      expect(json['tarifa_total'], equals(18000.0));

      final reconstruido = ViajeModel.fromJson(json);
      expect(reconstruido.categoria, equals(CategoriaViaje.bahiaPrioritaria));
      expect(reconstruido.pasajeroTelefono, equals('573001234567'));
    });
  });
}
