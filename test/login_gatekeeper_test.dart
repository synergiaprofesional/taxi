import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:taxi/controllers/theme_controller.dart';
import 'package:taxi/services/odoo_service.dart';
import 'package:taxi/ui/views/auth/auth_gatekeeper.dart';
import 'package:taxi/ui/views/auth/login_view.dart';
import 'package:taxi/ui/views/home/home_view.dart';

void main() {
  setUp(() {
    Get.reset();
    Get.put(ThemeController());
    final odooService = Get.put(OdooService(), permanent: true);
    odooService.isAuthenticated.value = false;
    odooService.isLoggingIn.value = false;
  });

  tearDown(() {
    Get.reset();
  });

  testWidgets('AuthGatekeeper bloquea la interfaz operativa y muestra LoginView si no está autenticado', (tester) async {
    tester.view.physicalSize = const Size(1280, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(
      const GetMaterialApp(
        home: AuthGatekeeper(autoConnectSockets: false),
      ),
    );
    await tester.pump();

    // Debe existir LoginView y NO HomeView
    expect(find.byType(LoginView), findsOneWidget);
    expect(find.byType(HomeView), findsNothing);
    expect(find.text('SYNERGIA MÓVIL'), findsWidgets);
    expect(find.text('INGRESAR A BAHÍA'), findsOneWidget);
  });

  testWidgets('AuthGatekeeper desbloquea HomeView de inmediato al autenticar', (tester) async {
    tester.view.physicalSize = const Size(1280, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    final odooService = Get.find<OdooService>();
    odooService.isAuthenticated.value = true;

    await tester.pumpWidget(
      const GetMaterialApp(
        home: AuthGatekeeper(autoConnectSockets: false),
      ),
    );
    await tester.pump();

    // Debe existir HomeView y NO LoginView
    expect(find.byType(HomeView), findsOneWidget);
    expect(find.byType(LoginView), findsNothing);
  });

  testWidgets('Cerrar sesión devuelve reactivamente a LoginView', (tester) async {
    tester.view.physicalSize = const Size(1280, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    final odooService = Get.find<OdooService>();
    odooService.isAuthenticated.value = true;

    await tester.pumpWidget(
      const GetMaterialApp(
        home: AuthGatekeeper(autoConnectSockets: false),
      ),
    );
    await tester.pump();
    expect(find.byType(HomeView), findsOneWidget);

    // Cierra sesión
    await odooService.cerrarSesion();
    await tester.pump();

    // Vuelve inmediatamente a LoginView
    expect(find.byType(LoginView), findsOneWidget);
    expect(find.byType(HomeView), findsNothing);
  });
}
