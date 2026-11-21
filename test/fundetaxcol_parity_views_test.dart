import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:taxi/controllers/turno_controller.dart';
import 'package:taxi/models/bay_model.dart';
import 'package:taxi/models/payment_model.dart';
import 'package:taxi/models/turno_model.dart';
import 'package:taxi/services/odoo_service.dart';
import 'package:taxi/ui/views/main/bahia_selected_view.dart';
import 'package:taxi/ui/widgets/pago_card_widget.dart';
import 'package:taxi/ui/widgets/despacho_card_widget.dart';

void main() {
  group('Pruebas de Vistas Paridad Fundetaxcol', () {
    late TurnoController turnoController;

    setUp(() {
      Get.reset();
      final odooService = Get.put(OdooService(), permanent: true);
      odooService.isAuthenticated.value = true;
      turnoController = Get.put(TurnoController(autoConnectSockets: false));

      // Configuración de bahía inicial
      turnoController.bahiasDisponibles.assignAll([
        BahiaModel(id: 8815, name: '29D', codigo: '29D'),
      ]);
      turnoController.bahiaIdActual.value = 8815;
      turnoController.bahiaSeleccionada.value = '29D';

      // Turnos de prueba
      turnoController.turnos.assignAll([
        TurnoModel(
          id: 101,
          name: 'T-0001',
          vehiculoPlaca: 'WBD512',
          conductorNombre: 'Carlos Ramírez',
          bahiaNombre: '29D',
          bahiaSesionId: 8815,
          bahiaBaseId: 8815,
          numeroTurno: 1,
          estado: EstadoTurno.actual,
          fechaCreacion: DateTime.now(),
        ),
        TurnoModel(
          id: 102,
          name: 'T-0002',
          vehiculoPlaca: 'FXS830',
          conductorNombre: 'Juan Pérez',
          bahiaNombre: '29D',
          bahiaSesionId: 8815,
          bahiaBaseId: 8815,
          numeroTurno: 2,
          estado: EstadoTurno.despachado,
          tarifaId: 1,
          tarifaNombre: 'Aeropuerto',
          valorTotal: 18000.0,
          fechaCreacion: DateTime.now(),
        ),
      ]);

      // Pagos de prueba
      turnoController.pagos.assignAll([
        PagoRecaudoModel(
          id: 201,
          consecutivo: 'REC-00124',
          bahiaId: 8815,
          bahiaNombre: '29D',
          vehiculoId: 50,
          placa: 'WBD512',
          conductorId: 30,
          conductorNombre: 'Carlos Ramírez',
          fecha: DateTime.now(),
          total: 15000.0,
          lineas: [],
        ),
      ]);
    });

    tearDown(() {
      Get.reset();
    });

    testWidgets('1. BahiaSelectedView renderiza BottomNavigationBar con 3 pestañas (Pagos, Turnos, Despachos)', (WidgetTester tester) async {
      await tester.pumpWidget(const GetMaterialApp(
        home: BahiaSelectedView(initialTabIndex: 1),
      ));
      await tester.pumpAndSettle();

      // Debe encontrar las 3 pestañas
      expect(find.text('Pagos'), findsOneWidget);
      expect(find.text('Turnos'), findsOneWidget);
      expect(find.text('Despachos'), findsOneWidget);

      // Pestaña inicial Turnos muestra el turno en espera
      expect(find.text('WBD512'), findsOneWidget);
      expect(find.text('Carlos Ramírez'), findsOneWidget);
    });

    testWidgets('2. Navegación entre pestañas de BahiaSelectedView', (WidgetTester tester) async {
      await tester.pumpWidget(const GetMaterialApp(
        home: BahiaSelectedView(initialTabIndex: 1),
      ));
      await tester.pumpAndSettle();

      // Cambiar a la pestaña de Pagos
      await tester.tap(find.text('Pagos'));
      await tester.pumpAndSettle();

      expect(find.text('REC-00124'), findsOneWidget);

      // Cambiar a la pestaña de Despachos
      await tester.tap(find.text('Despachos'));
      await tester.pumpAndSettle();

      expect(find.text('FXS830'), findsOneWidget);
      expect(find.text('AEROPUERTO'), findsOneWidget);
    });

    testWidgets('3. DespachoCardWidget muestra placa, número de secuencia y formato de despacho', (WidgetTester tester) async {
      final turnoDespacho = TurnoModel(
        id: 99,
        name: 'T-0099',
        vehiculoPlaca: 'ABC123',
        conductorNombre: 'Pedro Gómez',
        bahiaNombre: '29D',
        numeroTurno: 5,
        estado: EstadoTurno.despachado,
        tarifaId: 2,
        tarifaNombre: 'Bocagrande',
        valorTotal: 15000.0,
        fechaCreacion: DateTime.now(),
      );

      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: DespachoCardWidget(turno: turnoDespacho),
        ),
      ));
      await tester.pumpAndSettle();

      expect(find.text('ABC123'), findsOneWidget);
      expect(find.text('5'), findsOneWidget);
      expect(find.text('BOCAGRANDE'), findsOneWidget);
      expect(find.text('Pedro Gómez'), findsOneWidget);
    });

    testWidgets('4. PagoCardWidget muestra consecutivo oficial y monto recaudado', (WidgetTester tester) async {
      final pago = PagoRecaudoModel(
        id: 301,
        consecutivo: 'REC-00999',
        bahiaId: 8815,
        bahiaNombre: '29D',
        vehiculoId: 10,
        placa: 'XYZ789',
        conductorId: 15,
        conductorNombre: 'Mario Casas',
        fecha: DateTime.now(),
        total: 25000.0,
        lineas: [],
      );

      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: PagoCardWidget(pago: pago),
        ),
      ));
      await tester.pumpAndSettle();

      expect(find.text('REC-00999'), findsOneWidget);
      expect(find.text('XYZ789'), findsOneWidget);
      expect(find.text('Mario Casas'), findsOneWidget);
    });
  });
}
