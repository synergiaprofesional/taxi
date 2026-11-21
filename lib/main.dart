import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'controllers/theme_controller.dart';
import 'core/theme/app_theme.dart';
import 'core/utils/local_storage.dart';
import 'services/firebase_service.dart';
import 'services/odoo_service.dart';
import 'ui/views/auth/auth_gatekeeper.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    await LocalStorage.initialize();
  } catch (e) {
    debugPrint('[Main] Advertencia al inicializar LocalStorage: $e');
  }

  try {
    await FirebaseService.initialize();
  } catch (e) {
    debugPrint('[Main] Advertencia al inicializar FirebaseService: $e');
  }

  Get.put(ThemeController());
  Get.put(OdooService(), permanent: true);
  runApp(const TaxiApp());
}

class TaxiApp extends StatelessWidget {
  final bool autoConnectSockets;
  const TaxiApp({super.key, this.autoConnectSockets = true});

  @override
  Widget build(BuildContext context) {
    final themeController = Get.isRegistered<ThemeController>()
        ? Get.find<ThemeController>()
        : Get.put(ThemeController());
    return Obx(() => GetMaterialApp(
      title: 'Taxi',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeController.themeMode.value,
      home: AuthGatekeeper(autoConnectSockets: autoConnectSockets),
    ));
  }
}
