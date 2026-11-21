import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../core/utils/local_storage.dart';

class ThemeController extends GetxController {
  static const String _storageKey = 'app_theme_mode';

  final Rx<ThemeMode> themeMode = ThemeMode.system.obs;

  @override
  void onInit() {
    super.onInit();
    _loadTheme();
  }

  void _loadTheme() {
    final savedMode = LocalStorage.getString(_storageKey);
    if (savedMode == 'light') {
      themeMode.value = ThemeMode.light;
    } else if (savedMode == 'dark') {
      themeMode.value = ThemeMode.dark;
    } else {
      themeMode.value = ThemeMode.dark; // Default para Synergia Móvil
    }
  }

  void setThemeMode(ThemeMode mode) {
    themeMode.value = mode;
    Get.changeThemeMode(mode);
    String modeString = 'system';
    if (mode == ThemeMode.light) modeString = 'light';
    if (mode == ThemeMode.dark) modeString = 'dark';
    LocalStorage.setString(_storageKey, modeString);
  }

  bool get isDarkMode {
    if (themeMode.value == ThemeMode.system) {
      return WidgetsBinding.instance.platformDispatcher.platformBrightness == Brightness.dark;
    }
    return themeMode.value == ThemeMode.dark;
  }
}
