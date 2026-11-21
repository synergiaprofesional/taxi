import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:taxi/core/utils/local_storage.dart';
import 'package:taxi/models/printer_config_model.dart';
import 'package:taxi/services/printer_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    await LocalStorage.initialize();
  });

  tearDown(() {
    Get.reset();
  });

  group('Pruebas de Persistencia por Usuario (Key Scoping)', () {
    test('REQ-001: Guarda y carga configuración de impresora para usuario específico', () async {
      final printerService = PrinterService();
      const configOperador1 = PrinterConfigModel(
        tipo: TipoImpresora.spoolerWindows,
        nombreODireccion: 'TIQUETES',
        puerto: 9100,
        anchoPapel: 80,
        autoCorte: true,
      );

      await printerService.saveUserConfig('29d@fundetaxcol.co', configOperador1);

      // Verificamos en un nuevo servicio que cargue la configuración de ese usuario
      final nuevoPrinterService = PrinterService();
      final loaded = await nuevoPrinterService.loadUserConfig('29d@fundetaxcol.co');

      expect(loaded.tipo, TipoImpresora.spoolerWindows);
      expect(loaded.nombreODireccion, 'TIQUETES');
      expect(loaded.anchoPapel, 80);
      expect(loaded.autoCorte, isTrue);
    });

    test('REQ-002: Aislamiento estricto entre múltiples operadores', () async {
      final printerService = PrinterService();

      const configUserA = PrinterConfigModel(
        tipo: TipoImpresora.spoolerWindows,
        nombreODireccion: 'TIQUETES',
        anchoPapel: 80,
        autoCorte: true,
      );

      const configUserB = PrinterConfigModel(
        tipo: TipoImpresora.bluetooth,
        nombreODireccion: '66:32:88:AB:12:90',
        anchoPapel: 58,
        autoCorte: false,
      );

      await printerService.saveUserConfig('user_a@fundetaxcol.co', configUserA);
      await printerService.saveUserConfig('user_b@fundetaxcol.co', configUserB);

      final loadedA = await printerService.loadUserConfig('user_a@fundetaxcol.co');
      expect(loadedA.nombreODireccion, 'TIQUETES');
      expect(loadedA.anchoPapel, 80);

      final loadedB = await printerService.loadUserConfig('user_b@fundetaxcol.co');
      expect(loadedB.nombreODireccion, '66:32:88:AB:12:90');
      expect(loadedB.anchoPapel, 58);
      expect(loadedB.autoCorte, isFalse);
    });
  });
}
