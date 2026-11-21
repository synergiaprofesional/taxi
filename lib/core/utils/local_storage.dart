import 'package:shared_preferences/shared_preferences.dart';

/// Almacenamiento local multiplataforma persistente (Android, Windows, iOS, Web).
class LocalStorage {
  static SharedPreferences? _prefs;

  static Future<void> initialize() async {
    _prefs ??= await SharedPreferences.getInstance();
  }

  static String? getString(String key) => _prefs?.getString(key);
  static Future<bool> setString(String key, String value) async =>
      await _prefs?.setString(key, value) ?? false;

  static int? getInt(String key) => _prefs?.getInt(key);
  static Future<bool> setInt(String key, int value) async =>
      await _prefs?.setInt(key, value) ?? false;

  static bool? getBool(String key) => _prefs?.getBool(key);
  static Future<bool> setBool(String key, bool value) async =>
      await _prefs?.setBool(key, value) ?? false;

  static Future<bool> remove(String key) async =>
      await _prefs?.remove(key) ?? false;

  static Future<bool> clear() async => await _prefs?.clear() ?? false;
}
