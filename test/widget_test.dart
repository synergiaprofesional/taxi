import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:taxi/controllers/theme_controller.dart';
import 'package:taxi/main.dart';
import 'package:taxi/services/odoo_service.dart';

void main() {
  setUp(() {
    Get.reset();
    Get.put(ThemeController());
    Get.put(OdooService(), permanent: true);
  });

  tearDown(() {
    Get.reset();
  });

  testWidgets('Smoke test de inicialización de Taxi', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1280, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(const TaxiApp(autoConnectSockets: false));
    await tester.pump();
    expect(find.byType(TaxiApp), findsOneWidget);
  });
}
