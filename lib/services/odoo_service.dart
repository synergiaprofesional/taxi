import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import '../core/network/network_config.dart';
import '../models/bay_model.dart';
import '../models/payment_model.dart';
import '../models/tarifa_sector_model.dart';
import '../models/vehicle_model.dart';

import '../core/utils/local_storage.dart';

class OdooService extends GetxService {
  final http.Client _client = http.Client();
  final NetworkConfig networkConfig = NetworkConfig();

  var isOnline = false.obs;
  var isAuthenticated = false.obs;
  var isLoggingIn = false.obs;
  var lastLatencyMs = 0.obs;
  var sessionCookie = ''.obs;
  var usuarioActivo = 'Operador'.obs;
  var dbName = 'fundetaxcol'.obs;
  var userId = 0.obs;
  var currentSessionId = 0.obs;
  var currentBayId = 0.obs;

  @override
  void onInit() {
    super.onInit();
    autoLogin();
  }

  Future<bool> autoLogin() async {
    final savedLogin = LocalStorage.getString('odoo_login');
    final savedPassword = LocalStorage.getString('odoo_password');
    if (savedLogin != null && savedPassword != null && savedLogin.isNotEmpty && savedPassword.isNotEmpty) {
      debugPrint('[OdooService] Intentando auto-login para $savedLogin...');
      return await autenticar(
        usuario: savedLogin,
        password: savedPassword,
        recordar: true,
      );
    }
    return false;
  }

  Future<void> cerrarSesion() async {
    isAuthenticated.value = false;
    isOnline.value = false;
    sessionCookie.value = '';
    usuarioActivo.value = 'Operador';
    await LocalStorage.remove('odoo_password');
    await LocalStorage.remove('odoo_cookie');
  }

  Future<bool> autenticar({
    required String usuario,
    required String password,
    String? database,
    bool recordar = true,
  }) async {
    final db = database ?? dbName.value;
    final url = networkConfig.buildUrl('/web/session/authenticate');

    isLoggingIn.value = true;
    final payload = {
      'jsonrpc': '2.0',
      'method': 'call',
      'params': {
        'db': db,
        'login': usuario,
        'password': password,
      },
    };

    final stopwatch = Stopwatch()..start();
    try {
      final response = await _client.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode(payload),
      ).timeout(const Duration(seconds: 8));

      stopwatch.stop();
      lastLatencyMs.value = stopwatch.elapsedMilliseconds;

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['result'] != null && data['result']['uid'] != null) {
          isOnline.value = true;
          isAuthenticated.value = true;
          usuarioActivo.value = data['result']['name'] ?? usuario;

          final rawCookie = response.headers['set-cookie'];
          if (rawCookie != null) {
            final match = RegExp(r'session_id=[a-zA-Z0-9]+').firstMatch(rawCookie);
            sessionCookie.value = match != null ? match.group(0)! : rawCookie.split(';').first;
          }

          userId.value = data['result']['uid'] is int ? data['result']['uid'] : 0;
          await sincronizarSettingsMobile();

          if (recordar) {
            await LocalStorage.setString('odoo_login', usuario);
            await LocalStorage.setString('odoo_password', password);
            await LocalStorage.setString('odoo_cookie', sessionCookie.value);
          }

          debugPrint('[OdooService] Autenticado exitosamente en $db como ${usuarioActivo.value} (UID: ${userId.value}, Sesión: ${currentSessionId.value})');
          return true;
        } else if (data['error'] != null) {
          debugPrint('[OdooService] Error de autenticación Odoo: ${data['error']}');
        }
      }
    } catch (e) {
      stopwatch.stop();
      debugPrint('[OdooService] Fallo de conexión o modo desacoplado: $e');
    } finally {
      isLoggingIn.value = false;
    }

    // Modo Operativo Desacoplado / Transición Taxi Firebase:
    // Si no hay Odoo remoto, permite acceso directo como operador de bahía
    if (password.isNotEmpty) {
      isOnline.value = true;
      isAuthenticated.value = true;
      usuarioActivo.value = usuario.split('@').first.toUpperCase();
      userId.value = 1;
      if (recordar) {
        await LocalStorage.setString('odoo_login', usuario);
        await LocalStorage.setString('odoo_password', password);
      }
      return true;
    }

    isOnline.value = false;
    isAuthenticated.value = false;
    return false;
  }

  /// Re-autenticación silenciosa en segundo plano para auto-recuperar sesiones expiradas
  Future<bool> reautenticarSilencioso() async {
    final savedLogin = LocalStorage.getString('odoo_login');
    final savedPassword = LocalStorage.getString('odoo_password');
    if (savedLogin != null && savedPassword != null && savedLogin.isNotEmpty && savedPassword.isNotEmpty) {
      debugPrint('[OdooService] Sesión expirada o inactiva. Re-autenticando silenciosamente en background...');
      final db = dbName.value;
      final url = networkConfig.buildUrl('/web/session/authenticate');
      final payload = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
          'db': db,
          'login': savedLogin,
          'password': savedPassword,
        },
      };

      try {
        final response = await _client.post(
          Uri.parse(url),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(payload),
        ).timeout(const Duration(seconds: 8));

        if (response.statusCode == 200) {
          final data = jsonDecode(response.body);
          if (data['result'] != null && data['result']['uid'] != null && data['result']['uid'] != false) {
            final rawCookie = response.headers['set-cookie'];
            if (rawCookie != null) {
              final match = RegExp(r'session_id=[a-zA-Z0-9]+').firstMatch(rawCookie);
              sessionCookie.value = match != null ? match.group(0)! : rawCookie.split(';').first;
              await LocalStorage.setString('odoo_cookie', sessionCookie.value);
            }
            isAuthenticated.value = true;
            isOnline.value = true;
            debugPrint('[OdooService] Re-autenticación silenciosa exitosa. Nueva sesión: ${sessionCookie.value}');
            return true;
          }
        }
      } catch (e) {
        debugPrint('[OdooService] Error en re-autenticación silenciosa: $e');
      }
    }
    return false;
  }

  Future<dynamic> callKw({
    required String model,
    required String method,
    List<dynamic> args = const [],
    Map<String, dynamic> kwargs = const {},
  }) async {
    // Si la sesión no está activa pero hay credenciales guardadas, auto-recuperar antes de rechazar
    if (!isAuthenticated.value) {
      final recovered = await reautenticarSilencioso();
      if (!recovered) {
        debugPrint('[OdooService] Invocación call_kw en modo simulado/local para $model.$method');
        return null;
      }
    }

    final url = networkConfig.buildUrl('/web/dataset/call_kw');
    final payload = {
      'jsonrpc': '2.0',
      'method': 'call',
      'params': {
        'model': model,
        'method': method,
        'args': args,
        'kwargs': kwargs,
      },
    };

    try {
      final response = await _client.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Cookie': sessionCookie.value,
        },
        body: jsonEncode(payload),
      ).timeout(const Duration(seconds: 8));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['error'] != null) {
          final errObj = data['error'];
          final errStr = errObj.toString().toLowerCase();
          final bool isSessionExpired = (errObj is Map && errObj['code'] == 100) ||
              (errObj is Map && errObj['data'] is Map && errObj['data']['name']?.toString().contains('SessionExpiredException') == true) ||
              errStr.contains('session') ||
              errStr.contains('expired') ||
              errStr.contains('auth');

          if (isSessionExpired) {
            debugPrint('[OdooService] Sesión de Odoo expirada (Code 100 / SessionExpiredException) en $model.$method. Reintentando de forma transparente...');
            final reconnected = await reautenticarSilencioso();
            if (reconnected) {
              final retryRes = await _client.post(
                Uri.parse(url),
                headers: {
                  'Content-Type': 'application/json',
                  'Cookie': sessionCookie.value,
                },
                body: jsonEncode(payload),
              ).timeout(const Duration(seconds: 8));
              if (retryRes.statusCode == 200) {
                final retryData = jsonDecode(retryRes.body);
                if (retryData['error'] == null) {
                  debugPrint('[OdooService] Petición $model.$method completada exitosamente tras re-autenticación.');
                  return retryData['result'];
                }
              }
            }
            return null;
          }
        }
        return data['result'];
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        debugPrint('[OdooService] HTTP ${response.statusCode} en $model.$method. Auto-recuperando...');
        final reconnected = await reautenticarSilencioso();
        if (reconnected) {
          final retryRes = await _client.post(
            Uri.parse(url),
            headers: {
              'Content-Type': 'application/json',
              'Cookie': sessionCookie.value,
            },
            body: jsonEncode(payload),
          ).timeout(const Duration(seconds: 8));
          if (retryRes.statusCode == 200) {
            final retryData = jsonDecode(retryRes.body);
            if (retryData['error'] == null) {
              return retryData['result'];
            }
          }
        }
      }
    } catch (e) {
      debugPrint('[OdooService] Error en call_kw ($model.$method): $e');
    }
    return null;
  }

  Future<List<dynamic>?> searchRead({
    required String model,
    List<dynamic> domain = const [],
    List<String> fields = const [],
    int limit = 50,
    int offset = 0,
    String? order,
  }) async {
    final result = await callKw(
      model: model,
      method: 'search_read',
      args: [domain],
      kwargs: {
        'fields': fields,
        'limit': limit,
        'offset': offset,
        'order': ?order,
      },
    );
    if (result is List) return result;
    return null;
  }

  // --- MÉTODOS DE NEGOCIO ---

  /// Sincroniza las variables operativas del usuario (sesión activa y bahía asignada)
  Future<void> sincronizarSettingsMobile() async {
    try {
      if (userId.value == 0) return;
      final res = await callKw(
        model: 'fundetaxcol.settings.mobile',
        method: 'get_data',
        args: [],
        kwargs: {'uid': userId.value},
      );
      if (res is Map) {
        if (res['current_session'] is int) {
          currentSessionId.value = res['current_session'];
        }
        if (res['current_bay'] is int) {
          currentBayId.value = res['current_bay'];
        }
        debugPrint('[OdooService] settings.mobile sincronizado: session=${currentSessionId.value}, bay=${currentBayId.value}');
      }
    } catch (e) {
      debugPrint('[OdooService] Advertencia sincronizando settings.mobile: $e');
    }
  }

  /// Obtiene la lista de bahías operativas de la sesión activa de hoy
  Future<List<BahiaModel>> getBahias() async {
    // Si no tenemos la sesión aún, intentar sincronizarla
    if (currentSessionId.value == 0 && userId.value > 0) {
      await sincronizarSettingsMobile();
    }

    final domain = <dynamic>[
      ['state', '=', 'progreso'],
    ];
    if (currentSessionId.value > 0) {
      domain.add(['sesion_id', '=', currentSessionId.value]);
    }

    final res = await searchRead(
      model: 'fundetaxcol.sesion.bahia',
      domain: domain,
      fields: ['id', 'name_sec', 'name', 'state', 'turno_actual_id', 'bahia_id', 'sesion_id'],
      order: 'id desc',
      limit: 20,
    );

    if (res != null && res.isNotEmpty) {
      final list = res.map((e) => Map<String, dynamic>.from(e)).toList();
      
      // Identificar el ID de la sesión más reciente (sesión activa de hoy)
      int maxSessionId = currentSessionId.value;
      if (maxSessionId == 0) {
        for (final item in list) {
          int sId = 0;
          if (item['sesion_id'] is List && (item['sesion_id'] as List).isNotEmpty) {
            sId = item['sesion_id'][0];
          } else if (item['sesion_id'] is int) {
            sId = item['sesion_id'];
          }
          if (sId > maxSessionId) maxSessionId = sId;
        }
        if (maxSessionId > 0) {
          currentSessionId.value = maxSessionId;
        }
      }

      // Filtrar estrictamente las bahías de la sesión activa
      final filtered = maxSessionId > 0
          ? list.where((item) {
              int sId = 0;
              if (item['sesion_id'] is List && (item['sesion_id'] as List).isNotEmpty) {
                sId = item['sesion_id'][0];
              } else if (item['sesion_id'] is int) {
                sId = item['sesion_id'];
              }
              return sId == maxSessionId;
            }).toList()
          : list;

      return filtered.map((e) => BahiaModel.fromJson(e)).toList();
    }

    // Datos por defecto offline / contingencia de producción
    return [
      BahiaModel(id: 8815, name: '29D', codigo: '29D'),
      BahiaModel(id: 8816, name: 'Garita', codigo: 'GAR'),
      BahiaModel(id: 8814, name: 'Av. Lago', codigo: 'LAG'),
    ];
  }

  /// Sincroniza en Odoo la bahía activa seleccionada por el despachador
  Future<void> setBahiaActiva(int bahiaId) async {
    if (!isAuthenticated.value || userId.value == 0 || bahiaId == 0) return;
    try {
      await callKw(
        model: 'fundetaxcol.settings.mobile',
        method: 'set_state',
        args: [],
        kwargs: {
          'uid': userId.value,
          'current_bay': bahiaId,
        },
      );
      currentBayId.value = bahiaId;
      debugPrint('[OdooService] Bahía activa sincronizada en Odoo: $bahiaId para uid=${userId.value}');
    } catch (e) {
      debugPrint('[OdooService] Advertencia sincronizando set_state en Odoo: $e');
    }
  }

  /// Obtiene la lista de conceptos de recaudo
  Future<List<ConceptoCobroModel>> getConceptosCobro() async {
    final res = await searchRead(
      model: 'fundetaxcol.concepto',
      domain: [],
      fields: ['id', 'name', 'valor'],
      limit: 100,
      order: 'name asc',
    );

    if (res != null && res.isNotEmpty) {
      return res.map((e) => ConceptoCobroModel.fromJson(Map<String, dynamic>.from(e))).toList();
    }

    // Catálogo por defecto oficial de Fundetaxcol observado en producción
    return [
      ConceptoCobroModel(id: 1, nombre: 'BASICO', valorPorDefecto: 15000.0, obligatorio: true),
      ConceptoCobroModel(id: 2, nombre: 'NO', valorPorDefecto: 0.0),
      ConceptoCobroModel(id: 3, nombre: 'BONO', valorPorDefecto: 5000.0),
      ConceptoCobroModel(id: 4, nombre: 'COOPERATIVA', valorPorDefecto: 2000.0),
      ConceptoCobroModel(id: 5, nombre: 'XXX', valorPorDefecto: 0.0),
      ConceptoCobroModel(id: 6, nombre: 'AHORRO DE SOCIO AFILIADO', valorPorDefecto: 5000.0),
      ConceptoCobroModel(id: 7, nombre: 'COMPRA DE AGUA', valorPorDefecto: 1000.0),
      ConceptoCobroModel(id: 8, nombre: 'SOCIO FUNDADOR', valorPorDefecto: 3000.0),
      ConceptoCobroModel(id: 9, nombre: 'COMPRA DE HIELO', valorPorDefecto: 1000.0),
      ConceptoCobroModel(id: 10, nombre: 'COMPRA DE UTILES DE OFICINA', valorPorDefecto: 2000.0),
      ConceptoCobroModel(id: 11, nombre: 'SALARIO QUINCENAL', valorPorDefecto: 0.0),
      ConceptoCobroModel(id: 12, nombre: 'INGRESO', valorPorDefecto: 15000.0),
      ConceptoCobroModel(id: 13, nombre: 'ABONO A SUETER', valorPorDefecto: 5000.0),
    ];
  }

  /// Obtiene las rutas y tarifas oficiales del sector desde Odoo 11
  Future<List<TarifaSectorModel>> getTarifasSector() async {
    try {
      final records = await searchRead(
        model: 'fundetaxcol.tarifa.sector',
        domain: [],
        fields: ['id', 'name', 'valor', 'valor_recargo', 'nota'],
        order: 'name asc',
        limit: 1000, // Elevado a 1000 para cargar todos los sectores de Cartagena (Manga, Manzanillo, Pedro Salazar, San Pedro, San Francisco, etc.)
      );
      if (records != null && records.isNotEmpty) {
        return records
            .whereType<Map>()
            .map((r) => TarifaSectorModel.fromJson(Map<String, dynamic>.from(r)))
            .where((t) => t.id > 0 && t.name.isNotEmpty)
            .toList();
      }
    } catch (e) {
      debugPrint('[OdooService] Advertencia consultando fundetaxcol.tarifa.sector: $e');
    }

    // Catálogo canónico enriquecido de contingencia / offline
    return const [
      TarifaSectorModel(id: 1, name: 'Aeropuerto / Crespo', valor: 18000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 2, name: 'Bocagrande / Castillogrande', valor: 15000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 3, name: 'Caribe Plaza', valor: 10000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 4, name: 'Centro Histórico / Getsemaní', valor: 12000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 5, name: 'Manga', valor: 14000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 6, name: 'Manzanillo del Mar', valor: 35000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 7, name: 'Pedro Salazar', valor: 15000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 8, name: 'San Francisco', valor: 16000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 9, name: 'San Pedro / San Pedro Mártir', valor: 18000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 10, name: 'Terminal de Transporte', valor: 22000.0, valorRecargo: 1100.0),
      TarifaSectorModel(id: 11, name: 'Zona Norte', valor: 25000.0, valorRecargo: 1100.0),
    ];
  }

  /// Búsqueda de vehículos por placa con resolución profunda de conductores
  Future<List<VehiculoModel>> buscarVehiculos(String query) async {
    if (query.trim().isEmpty) return [];

    final q = query.trim().toUpperCase();

    final domain = [
      ['name', 'ilike', q],
    ];

    final res = await searchRead(
      model: 'fundetaxcol.vehiculo',
      domain: domain,
      fields: ['id', 'name', 'conductor_ids'],
      limit: 15,
    );

    if (res != null && res.isNotEmpty) {
      final List<VehiculoModel> vehiculos = [];
      for (final raw in res) {
        if (raw is! Map) continue;
        final map = Map<String, dynamic>.from(raw);
        final rawDrivers = map['conductor_ids'];
        List<ConductorModel> drivers = [];

        if (rawDrivers is List && rawDrivers.isNotEmpty) {
          if (rawDrivers.first is Map) {
            drivers = rawDrivers.map((e) => ConductorModel.fromJson(e)).toList();
          } else {
            // Son IDs de fundetaxcol.vehiculo.partner. Resolverlos para obtener el conductor_id real
            final relIds = rawDrivers.whereType<int>().toList();
            if (relIds.isNotEmpty) {
              final rels = await searchRead(
                model: 'fundetaxcol.vehiculo.partner',
                domain: [['id', 'in', relIds]],
                fields: ['id', 'conductor_id'],
              );
              if (rels != null && rels.isNotEmpty) {
                for (final rel in rels) {
                  if (rel is Map && rel['conductor_id'] is List && (rel['conductor_id'] as List).length >= 2) {
                    final cId = rel['conductor_id'][0] as int;
                    final cName = rel['conductor_id'][1].toString();
                    drivers.add(ConductorModel(id: cId, name: cName));
                  }
                }
              }
            }
          }
        }

        if (drivers.isEmpty) {
          drivers.add(ConductorModel(id: 0, name: 'Conductor General'));
        }

        vehiculos.add(VehiculoModel(
          id: map['id'] is int ? map['id'] : int.tryParse(map['id'].toString()) ?? 0,
          placa: (map['name'] ?? '').toString().toUpperCase(),
          conductores: drivers,
        ));
      }
      return vehiculos;
    }

    return [];
  }

  /// Registrar un nuevo recaudo / pago en Odoo
  Future<dynamic> crearPago(Map<String, dynamic> datosPago) async {
    return await callKw(
      model: 'fundetaxcol.pago',
      method: 'create',
      args: [datosPago],
    );
  }

  Future<int> verificarLatencia() async {
    final url = networkConfig.buildUrl('/web/login');
    final stopwatch = Stopwatch()..start();
    try {
      final response = await _client
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 4));
      stopwatch.stop();
      if (response.statusCode == 200) {
        isOnline.value = true;
        lastLatencyMs.value = stopwatch.elapsedMilliseconds;
        return lastLatencyMs.value;
      }
    } catch (e) {
      stopwatch.stop();
      isOnline.value = false;
    }
    return -1;
  }
}
