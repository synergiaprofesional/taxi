import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:taxi/main.dart';
import 'package:taxi/services/odoo_service.dart';

void main() {
  group('Pruebas de Responsividad para los 3 Dispositivos', () {
    setUp(() {
      Get.reset();
      final odooService = Get.put(OdooService(), permanent: true);
      odooService.isAuthenticated.value = true;
    });

    tearDown(() {
      Get.reset();
    });
    testWidgets('1. Dispositivo Móvil (< 650px) renderiza vista vertical con FAB', (WidgetTester tester) async {
      tester.view.physicalSize = const Size(400, 800);
      tester.view.devicePixelRatio = 1.0;

      await tester.pumpWidget(const TaxiApp(autoConnectSockets: false));
      await tester.pumpAndSettle();

      // Debe mostrar el FAB de 'PAGAR Y ENTURNAR'
      expect(find.byType(FloatingActionButton), findsOneWidget);
      expect(find.text('PAGAR Y ENTURNAR'), findsOneWidget);

      addTearDown(() => tester.view.resetPhysicalSize());
    });

    testWidgets('2. Dispositivo Tablet / POS Táctil (650px - 1050px) renderiza panel táctil POS', (WidgetTester tester) async {
      tester.view.physicalSize = const Size(800, 1024);
      tester.view.devicePixelRatio = 1.0;

      await tester.pumpWidget(const TaxiApp(autoConnectSockets: false));
      await tester.pumpAndSettle();

      // Debe mostrar la sección de TERMINAL TÁCTIL POS y botones grandes de acción táctil
      expect(find.text('TERMINAL TÁCTIL POS'), findsOneWidget);
      expect(find.text('DESPACHAR SALIDA'), findsOneWidget);
      // No debe tener FAB flotante
      expect(find.byType(FloatingActionButton), findsNothing);

      addTearDown(() => tester.view.resetPhysicalSize());
    });

    testWidgets('3. Dispositivo PC de Escritorio / Windows (> 1050px) renderiza 3 columnas con atajos', (WidgetTester tester) async {
      tester.view.physicalSize = const Size(1400, 900);
      tester.view.devicePixelRatio = 1.0;

      await tester.pumpWidget(const TaxiApp(autoConnectSockets: false));
      await tester.pumpAndSettle();

      // Debe mostrar las 3 columnas: CONTROL DE BAHÍA, COLA DE TURNOS EN BAHÍA, OPERACIÓN DE BAHÍA y Atajos F1-F12
      expect(find.text('CONTROL DE BAHÍA'), findsOneWidget);
      expect(find.text('COLA DE TURNOS EN BAHÍA'), findsOneWidget);
      expect(find.text('OPERACIÓN DE BAHÍA'), findsOneWidget);
      expect(find.text('• F1: Despachar Actual'), findsOneWidget);

      addTearDown(() => tester.view.resetPhysicalSize());
    });
  });
}
