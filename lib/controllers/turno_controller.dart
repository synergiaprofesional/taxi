import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:get/get.dart';
import '../models/bay_model.dart';
import '../models/payment_model.dart';
import '../models/recaudo_model.dart';
import '../models/tarifa_sector_model.dart';
import '../models/ticket_data_model.dart';
import '../models/turno_model.dart';
import '../services/firebase_service.dart';
import '../services/firestore_repository.dart';
import '../services/odoo_service.dart';
import '../services/printer_service.dart';
import '../services/socket_service.dart';

class TurnoController extends GetxController {
  final bool autoConnectSockets;

  TurnoController({this.autoConnectSockets = true});

  final odooService = Get.put(OdooService(), permanent: true);
  final socketService = Get.put(SocketService(), permanent: true);
  final printerService = Get.put(PrinterService(), permanent: true);
  final firestoreRepository = Get.put(FirestoreRepository(), permanent: true);

  StreamSubscription? _turnosFirestoreSub;
  StreamSubscription? _bahiasFirestoreSub;
  StreamSubscription? _tarifasFirestoreSub;

  var isLoading = false.obs;
  var turnos = <TurnoModel>[].obs;
  var pagos = <PagoRecaudoModel>[].obs;
  var pagosHistoricosRemotos = <PagoRecaudoModel>[].obs;
  var isSearchingRemotePagos = false.obs;
  var bahiasDisponibles = <BahiaModel>[].obs;
  var tarifasDisponibles = <TarifaSectorModel>[].obs;
  var bahiaSeleccionada = 'Seleccionar Bahía'.obs;
  var bahiaIdActual = 0.obs;
  var ultimoTicketImpreso = Rxn<TicketDataModel>();

  /// Vehículos que están físicamente en espera en la fila de la bahía (sin despachar ni cancelar)
  List<TurnoModel> get turnosEnCola {
    final list = bahiaIdActual.value > 0
        ? turnos.where((t) => t.enFila && (t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value)).toList()
        : turnos.where((t) => t.enFila).toList();
    list.sort((a, b) => a.numeroTurno.compareTo(b.numeroTurno));
    return list;
  }

  /// Historial de vehículos despachados en la sesión (con destino / tarifa asignada o done)
  List<TurnoModel> get turnosDespachados {
    final list = bahiaIdActual.value > 0
        ? turnos.where((t) => (t.esDespacho || t.estado == EstadoTurno.despachado) && (t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value)).toList()
        : turnos.where((t) => t.esDespacho || t.estado == EstadoTurno.despachado).toList();
    list.sort((a, b) => b.fechaCreacion.compareTo(a.fechaCreacion));
    return list;
  }

  /// Turnos cancelados o anulados en la bahía
  List<TurnoModel> get turnosCancelados {
    return turnos.where((t) => t.estado == EstadoTurno.cancelado).toList();
  }

  /// Total de recaudo para la empresa de la bahía activa (o global si no hay bahía seleccionada)
  double get totalRecaudoEmpresa {
    final list = bahiaIdActual.value > 0
        ? pagos.where((p) => p.bahiaSesionId == bahiaIdActual.value || p.bahiaId == bahiaIdActual.value)
        : pagos;
    return list.fold<double>(0.0, (sum, p) => sum + p.total);
  }

  /// Total de tarifas de servicios prestados a clientes por turnos despachados en la bahía activa
  double get totalServiciosClientes {
    final list = bahiaIdActual.value > 0
        ? turnosDespachados.where((t) => t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value)
        : turnosDespachados;
    return list.fold<double>(0.0, (sum, t) => sum + t.valorTotal);
  }

  /// Filtrado dual reactivo de pagos:
  /// Sin búsqueda => Pagos de la bahía activa (orden consecutivo descendente)
  /// Con búsqueda => Búsqueda transversal en TODAS las bahías por placa, conductor o consecutivo
  /// Fallback => Si no hay locales, integra resultados históricos remotos de Odoo
  List<PagoRecaudoModel> pagosFiltrados(String query) {
    final q = query.trim().toUpperCase();
    if (q.isEmpty) {
      final list = pagos.where((p) => p.bahiaSesionId == bahiaIdActual.value || p.bahiaId == bahiaIdActual.value).toList();
      list.sort((a, b) => b.consecutivo.compareTo(a.consecutivo));
      return list;
    }

    // 1. Coincidencias en memoria de la sesión activa
    final list = pagos.where((p) {
      return p.placa.toUpperCase().contains(q) ||
          p.conductorNombre.toUpperCase().contains(q) ||
          p.consecutivo.toUpperCase().contains(q);
    }).toList();

    if (list.isNotEmpty) {
      list.sort((a, b) => b.consecutivo.compareTo(a.consecutivo));
      return list;
    }

    // 2. Si no hay en sesión activa, devolver los históricos remotos traídos del servidor
    final remotos = pagosHistoricosRemotos.where((p) {
      return p.placa.toUpperCase().contains(q) ||
          p.conductorNombre.toUpperCase().contains(q) ||
          p.consecutivo.toUpperCase().contains(q);
    }).toList();
    remotos.sort((a, b) => b.consecutivo.compareTo(a.consecutivo));
    return remotos;
  }

  /// Filtrado dual reactivo de turnos en espera:
  /// Sin búsqueda => Fila activa de la bahía seleccionada (orden secuencial ascendente)
  /// Con búsqueda => Búsqueda global de vehículos enturnados en cualquier bahía
  List<TurnoModel> turnosEnColaFiltrados(String query) {
    if (query.trim().isEmpty) {
      final list = turnos
          .where((t) => t.enFila && (t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value))
          .toList();
      list.sort((a, b) => a.numeroTurno.compareTo(b.numeroTurno));
      return list;
    }
    final q = query.trim().toUpperCase();
    final list = turnos.where((t) => t.enFila).where((t) {
      return t.placaVisible.toUpperCase().contains(q) ||
          t.conductorNombre.toUpperCase().contains(q) ||
          t.numeroTurno.toString().contains(q) ||
          t.name.toUpperCase().contains(q);
    }).toList();
    list.sort((a, b) => a.numeroTurno.compareTo(b.numeroTurno));
    return list;
  }

  /// Filtrado dual reactivo de despachos:
  /// Sin búsqueda => Despachos efectuados en la bahía activa
  /// Con búsqueda => Historial transversal de todos los despachos del conductor/vehículo en el día
  List<TurnoModel> turnosDespachadosFiltrados(String query) {
    if (query.trim().isEmpty) {
      final list = turnos
          .where((t) =>
              (t.esDespacho || t.estado == EstadoTurno.despachado) &&
              (t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value))
          .toList();
      list.sort((a, b) => b.numeroTurno.compareTo(a.numeroTurno));
      return list;
    }
    final q = query.trim().toUpperCase();
    final list = turnos
        .where((t) => (t.esDespacho || t.estado == EstadoTurno.despachado))
        .where((t) {
          return t.placaVisible.toUpperCase().contains(q) ||
              t.conductorNombre.toUpperCase().contains(q) ||
              t.tarifaNombre.toUpperCase().contains(q) ||
              t.numeroTurno.toString().contains(q) ||
              t.name.toUpperCase().contains(q);
        }).toList();
    list.sort((a, b) => b.numeroTurno.compareTo(a.numeroTurno));
    return list;
  }

  /// Turno en atención activa o primero de la fila
  TurnoModel? get turnoEnAtencion {
    return turnos.firstWhereOrNull((t) =>
            t.estado == EstadoTurno.actual &&
            (t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value)) ??
        turnosEnCola.firstOrNull;
  }

  @override
  void onInit() {
    super.onInit();
    _iniciarServicios();
    _iniciarSuscripcionesFirestore();

    // Reacciona al estado de autenticación
    ever(odooService.isAuthenticated, (authed) {
      if (authed) {
        debugPrint('[TurnoController] Autenticado, descargando bahías, turnos y tarifas reales...');
        cargarBahiasDesdeServidor();
        cargarTarifasDesdeServidor();
        final user = odooService.usuarioActivo.value;
        if (user.isNotEmpty && user != 'Operador') {
          printerService.loadUserConfig(user);
        }
      } else {
        turnos.clear();
        pagos.clear();
        bahiasDisponibles.clear();
        tarifasDisponibles.clear();
      }
    });

    // Reacciona a cambios del usuario activo para cargar su perfil de hardware
    ever(odooService.usuarioActivo, (user) {
      if (user.isNotEmpty && user != 'Operador') {
        printerService.loadUserConfig(user);
      }
    });

    if (odooService.isAuthenticated.value) {
      cargarBahiasDesdeServidor();
      cargarTarifasDesdeServidor();
      final user = odooService.usuarioActivo.value;
      if (user.isNotEmpty && user != 'Operador') {
        printerService.loadUserConfig(user);
      }
    }
  }

  void _iniciarServicios() {
    if (autoConnectSockets) {
      socketService.conectar();
    }

    // Escucha reactiva desacoplada a través de eventSequence para no perder eventos repetidos
    debounce(
      socketService.eventSequence,
      (_) {
        final evento = socketService.lastEventName.value;
        if (evento.isEmpty) return;

        if (evento == 'turnId' ||
            evento == 'dispatchId' ||
            evento == 'new_turno' ||
            evento == 'dispatch_turno' ||
            evento == 'turn' ||
            evento == 'dispatch') {
          debugPrint('[TurnoController] Procesando evento realtime de turno: $evento');
          cargarTurnosDesdeServidor();
        } else if (evento == 'payment' || evento == 'paymentId') {
          debugPrint('[TurnoController] Procesando evento realtime de pago: $evento');
          cargarPagosDesdeServidor();
        } else if (evento == 'sessionId' || evento == 'session') {
          debugPrint('[TurnoController] Sesión de bahía actualizada en servidor.');
          cargarBahiasDesdeServidor();
        }
      },
      time: const Duration(milliseconds: 400),
    );
  }

  void cambiarBahia(BahiaModel bahia) {
    bahiaIdActual.value = bahia.id;
    bahiaSeleccionada.value = bahia.name;
    // Sincronizar en Odoo 11 el estado del usuario (set_state current_bay)
    odooService.setBahiaActiva(bahia.id);
    _sincronizarTurnosFirestore();
    cargarTurnosDesdeServidor();
    cargarPagosDesdeServidor();
  }

  void _iniciarSuscripcionesFirestore() {
    if (!FirebaseService.isInitialized) return;
    try {
      _bahiasFirestoreSub = firestoreRepository.streamBahias().listen((lista) {
        if (lista.isNotEmpty) {
          bahiasDisponibles.assignAll(lista);
          if (!lista.any((b) => b.id == bahiaIdActual.value)) {
            bahiaIdActual.value = lista.first.id;
            bahiaSeleccionada.value = lista.first.name;
          }
        }
      }, onError: (e) => debugPrint('[TurnoController] Error en streamBahias: $e'));

      _tarifasFirestoreSub = firestoreRepository.streamTarifas().listen((lista) {
        if (lista.isNotEmpty) {
          tarifasDisponibles.assignAll(lista);
        }
      }, onError: (e) => debugPrint('[TurnoController] Error en streamTarifas: $e'));

      _sincronizarTurnosFirestore();
    } catch (e) {
      debugPrint('[TurnoController] Error iniciando suscripciones Firestore: $e');
    }
  }

  void _sincronizarTurnosFirestore() {
    if (!FirebaseService.isInitialized) return;
    _turnosFirestoreSub?.cancel();
    _turnosFirestoreSub = firestoreRepository.streamTurnosBahia(bahiaIdActual.value).listen((lista) {
      if (lista.isNotEmpty) {
        turnos.assignAll(lista);
      }
    }, onError: (e) => debugPrint('[TurnoController] Error en streamTurnosBahia: $e'));
  }

  /// Carga las tarifas sectoriales de transporte oficiales desde Odoo
  Future<void> cargarTarifasDesdeServidor() async {
    try {
      final list = await odooService.getTarifasSector();
      if (list.isNotEmpty) {
        tarifasDisponibles.assignAll(list);
        debugPrint('[TurnoController] ${list.length} tarifas de sector cargadas.');
      }
    } catch (e) {
      debugPrint('[TurnoController] Error cargando tarifas de sector: $e');
    }
  }

  Future<void> cargarBahiasDesdeServidor() async {
    try {
      if (!odooService.isAuthenticated.value) return;

      // Obtiene las bahías operativas de la sesión activa de hoy (nombre limpio y filtro de sesión)
      final list = await odooService.getBahias();
      if (list.isNotEmpty) {
        bahiasDisponibles.assignAll(list);
        if (!list.any((b) => b.id == bahiaIdActual.value)) {
          bahiaIdActual.value = list.first.id;
          bahiaSeleccionada.value = list.first.name;
        }
      }
      await cargarTurnosDesdeServidor();
      await cargarPagosDesdeServidor();
    } catch (e) {
      debugPrint('[TurnoController] Error cargando bahías reales: $e');
    }
  }

  Future<void> cargarPagosDesdeServidor() async {
    try {
      if (!odooService.isAuthenticated.value) return;

      final bahiaIds = bahiasDisponibles.map((b) => b.id).toList();
      final targetIds = bahiaIds.isNotEmpty ? bahiaIds : (bahiaIdActual.value > 0 ? [bahiaIdActual.value] : <int>[]);

      // Intento 1: Invocación RPC oficial fundetaxcol.pago.get_all
      if (targetIds.isNotEmpty) {
        final rpcResult = await odooService.callKw(
          model: 'fundetaxcol.pago',
          method: 'get_all',
          kwargs: {'bahia_ids': targetIds},
        );
        if (rpcResult != null && rpcResult is List && rpcResult.isNotEmpty) {
          final List<PagoRecaudoModel> list = [];
          for (final item in rpcResult) {
            if (item is Map) {
              list.add(PagoRecaudoModel.fromJson(Map<String, dynamic>.from(item)));
            }
          }
          pagos.assignAll(list);
          return;
        }
      }

      // Intento 2: Respaldo search_read transversal multi-bahía
      final domain = targetIds.isNotEmpty ? <dynamic>[['bahia_id', 'in', targetIds]] : <dynamic>[];
      final res = await odooService.searchRead(
        model: 'fundetaxcol.pago',
        domain: domain,
        fields: [
          'id',
          'consecutivo',
          'bahia_id',
          'vehiculo_id',
          'conductor_id',
          'valor',
          'fecha',
          'enturnar',
          'nota',
          'concepto_ids',
        ],
        order: 'consecutivo desc, id desc',
        limit: 150,
      );

      if (res != null && res.isNotEmpty) {
        final List<PagoRecaudoModel> list = [];
        for (final item in res) {
          if (item is Map) {
            list.add(PagoRecaudoModel.fromJson(Map<String, dynamic>.from(item)));
          }
        }
        pagos.assignAll(list);
      }
    } catch (e) {
      debugPrint('[TurnoController] Error cargando pagos de Odoo: $e');
    }
  }

  /// Búsqueda histórica remota en el servidor Odoo (sin importar la fecha ni sesión)
  Future<void> buscarPagosHistoricosRemotos(String query) async {
    final q = query.trim();
    if (q.length < 3) {
      pagosHistoricosRemotos.clear();
      return;
    }
    try {
      isSearchingRemotePagos.value = true;
      final domain = <dynamic>[
        '|',
        ['consecutivo', 'ilike', q],
        '|',
        ['vehiculo_id.name', 'ilike', q],
        ['conductor_id.name', 'ilike', q],
      ];
      final res = await odooService.searchRead(
        model: 'fundetaxcol.pago',
        domain: domain,
        fields: [
          'id',
          'consecutivo',
          'bahia_id',
          'vehiculo_id',
          'conductor_id',
          'valor',
          'fecha',
          'enturnar',
          'nota',
          'concepto_ids',
        ],
        order: 'consecutivo desc, id desc',
        limit: 50,
      );
      if (res != null) {
        final List<PagoRecaudoModel> list = [];
        for (final item in res) {
          if (item is Map) {
            list.add(PagoRecaudoModel.fromJson(Map<String, dynamic>.from(item)));
          }
        }
        pagosHistoricosRemotos.assignAll(list);
      }
    } catch (e) {
      debugPrint('[TurnoController] Error en búsqueda histórica remota de pagos: $e');
    } finally {
      isSearchingRemotePagos.value = false;
    }
  }

  Future<void> cargarTurnosDesdeServidor() async {
    try {
      if (!odooService.isAuthenticated.value) return;
      isLoading.value = true;

      final bahiaIds = bahiasDisponibles.map((b) => b.id).toList();
      final targetIds = bahiaIds.isNotEmpty ? bahiaIds : (bahiaIdActual.value > 0 ? [bahiaIdActual.value] : <int>[]);

      // Invocación RPC primaria: fundetaxcol.turno.get_all con todas las bahías de la sesión
      if (targetIds.isNotEmpty) {
        final result = await odooService.callKw(
          model: 'fundetaxcol.turno',
          method: 'get_all',
          kwargs: {
            'bahia_ids': targetIds,
          },
        );

        if (result != null && result is List && result.isNotEmpty) {
          final List<TurnoModel> list = [];
          for (final item in result) {
            if (item is Map) {
              list.add(TurnoModel.fromJson(Map<String, dynamic>.from(item)));
            }
          }
          turnos.assignAll(list);
          return;
        }
      }

      // Respaldo directo search_read transversal por bahías de la sesión
      final domain = targetIds.isNotEmpty ? <dynamic>[['bahia_id', 'in', targetIds]] : <dynamic>[];
      final srResult = await odooService.searchRead(
        model: 'fundetaxcol.turno',
        domain: domain,
        fields: [
          'id',
          'name',
          'sequence',
          'state',
          'fecha',
          'fecha_despacho',
          'bahia_id',
          'vehiculo_id',
          'conductor_id',
          'tarifa_id',
          'total',
          'anonimo',
          'placa_anonima'
        ],
        order: 'sequence asc, id asc',
        limit: 200,
      );

      if (srResult != null) {
        final List<TurnoModel> list = [];
        for (final item in srResult) {
          if (item is Map) {
            list.add(TurnoModel.fromJson(Map<String, dynamic>.from(item)));
          }
        }
        turnos.assignAll(list);
      }
    } catch (e) {
      debugPrint('[TurnoController] Error cargando turnos de Odoo: $e');
    } finally {
      isLoading.value = false;
    }
  }

  void despacharTurnoActual() {
    final target = turnoEnAtencion;
    if (target != null) {
      despacharTurno(target.id);
    }
  }

  Future<void> despacharTurno(int turnoId, {int? tarifaId, double? valor, String? nota}) async {
    final index = turnos.indexWhere((t) => t.id == turnoId);
    if (index != -1) {
      final turno = turnos[index];

      if (odooService.isAuthenticated.value) {
        try {
          final kwargs = <String, dynamic>{
            'id': turnoId,
            'state': 'despachado',
          };
          if (tarifaId != null && tarifaId > 0) {
            kwargs['tarifa_id'] = tarifaId;
          }
          if (valor != null && valor > 0) {
            kwargs['valor'] = valor;
            kwargs['total'] = valor;
          }
          if (nota != null && nota.isNotEmpty) {
            kwargs['nota'] = nota;
          }

          await odooService.callKw(
            model: 'fundetaxcol.turno',
            method: 'actualizar',
            kwargs: kwargs,
          );
        } catch (e) {
          debugPrint('[TurnoController] Error despachando turno en Odoo: $e');
        }
      }

      // Resolver nombre de tarifa si se pasó un ID
      String tarifaNombreResolved = turno.tarifaNombre;
      if (tarifaId != null && tarifaId > 0) {
        final tMatch = tarifasDisponibles.firstWhereOrNull((t) => t.id == tarifaId);
        if (tMatch != null) tarifaNombreResolved = tMatch.name;
      }

      // Actualizar a despachado para que salga de la cola y pase a historial
      turnos[index] = TurnoModel(
        id: turno.id,
        name: turno.name,
        vehiculoPlaca: turno.vehiculoPlaca,
        conductorNombre: turno.conductorNombre,
        bahiaNombre: turno.bahiaNombre,
        numeroTurno: turno.numeroTurno,
        estado: EstadoTurno.despachado,
        fechaCreacion: turno.fechaCreacion,
        fechaDespacho: DateTime.now(),
        valorTotal: valor ?? turno.valorTotal,
        tarifaId: (tarifaId != null && tarifaId > 0) ? tarifaId : (turno.tarifaId != 0 ? turno.tarifaId : 1),
        tarifaNombre: tarifaNombreResolved.isNotEmpty ? tarifaNombreResolved : turno.tarifaNombre,
        nota: nota ?? turno.nota,
        esAnonimo: turno.esAnonimo,
        placaAnonima: turno.placaAnonima,
        bahiaSesionId: turno.bahiaSesionId,
        bahiaBaseId: turno.bahiaBaseId,
        vehiculoId: turno.vehiculoId,
        conductorId: turno.conductorId,
      );
      socketService.emitirEvento('dispatch', {'id': turnoId, 'turno': turno.name});

      if (FirebaseService.isInitialized) {
        firestoreRepository.despacharTurno(
          turnoId.toString(),
          tarifaId: (tarifaId != null && tarifaId > 0) ? tarifaId : (turno.tarifaId != 0 ? turno.tarifaId : 1),
          tarifaNombre: tarifaNombreResolved.isNotEmpty ? tarifaNombreResolved : turno.tarifaNombre,
          valorTotal: valor ?? turno.valorTotal,
        ).catchError((e) => debugPrint('[TurnoController] Firestore despachar error: $e'));
      }

      cargarTurnosDesdeServidor();
    }
  }

  Future<bool> cancelarTurno(int turnoId) async {
    final index = turnos.indexWhere((t) => t.id == turnoId);
    if (index == -1) return false;

    if (odooService.isAuthenticated.value) {
      try {
        await odooService.callKw(
          model: 'fundetaxcol.turno',
          method: 'cancelar',
          kwargs: {'id': turnoId},
        );
      } catch (e) {
        debugPrint('[TurnoController] Error cancelando turno en Odoo: $e');
      }
    }

    if (FirebaseService.isInitialized) {
      firestoreRepository.cancelarTurno(turnoId.toString())
          .catchError((e) => debugPrint('[TurnoController] Firestore cancelar error: $e'));
    }

    turnos.removeAt(index);
    socketService.emitirEvento('turn', {'id': turnoId, 'action': 'cancel'});
    return true;
  }

  Future<void> enturnarVehiculo({
    required String placa,
    required String conductor,
    int? vehiculoId,
    int? conductorId,
    double valor = 0.0,
  }) async {
    final placaClean = placa.trim().toUpperCase();
    int resolvedVehiculoId = vehiculoId ?? 0;
    int resolvedConductorId = conductorId ?? 0;

    // Si no se pasaron IDs explícitos, intentar resolverlos por placa en Odoo
    if (resolvedVehiculoId == 0 && odooService.isAuthenticated.value && placaClean.isNotEmpty) {
      try {
        final matches = await odooService.buscarVehiculos(placaClean);
        for (final v in matches) {
          if (v.placa.toUpperCase() == placaClean) {
            resolvedVehiculoId = v.id;
            if (resolvedConductorId == 0 && v.conductores.isNotEmpty) {
              resolvedConductorId = v.conductores.first.id;
            }
            break;
          }
        }
      } catch (e) {
        debugPrint('[TurnoController] Error resolviendo vehículo $placaClean: $e');
      }
    }

    final bool esAnon = placaClean.isEmpty;
    final nuevoNumero = turnos.where((t) => t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value).length + 1;
    final nuevoTurno = TurnoModel(
      id: DateTime.now().millisecondsSinceEpoch,
      name: 'Turno #$nuevoNumero [$placaClean - $conductor]',
      vehiculoPlaca: placaClean,
      conductorNombre: conductor,
      bahiaNombre: bahiaSeleccionada.value,
      numeroTurno: nuevoNumero,
      estado: turnos.any((t) => t.estado == EstadoTurno.actual && (t.bahiaSesionId == bahiaIdActual.value || t.bahiaBaseId == bahiaIdActual.value))
          ? EstadoTurno.espera
          : EstadoTurno.actual,
      fechaCreacion: DateTime.now(),
      valorTotal: valor,
      bahiaSesionId: bahiaIdActual.value,
      bahiaBaseId: bahiaIdActual.value,
      vehiculoId: resolvedVehiculoId,
      conductorId: resolvedConductorId,
      esAnonimo: esAnon,
      placaAnonima: esAnon ? placaClean : '',
    );

    turnos.add(nuevoTurno);

    if (FirebaseService.isInitialized) {
      firestoreRepository.crearTurno(nuevoTurno).catchError((e) {
        debugPrint('[TurnoController] Firestore crearTurno error: $e');
        return nuevoTurno;
      });
    }

    socketService.emitirEvento('turn', {
      'id': nuevoTurno.id,
      'turno': nuevoTurno.name,
      'placa': nuevoTurno.vehiculoPlaca,
      'conductor': nuevoTurno.conductorNombre,
      'valor': valor,
      'bahia': bahiaSeleccionada.value,
    });

    if (odooService.isAuthenticated.value) {
      try {
        final kwargs = <String, dynamic>{
          'bahia_id': bahiaIdActual.value,
          'anonimo': false,
          'tarifa_id': false,
          'state': nuevoTurno.estado.name,
          'total': valor,
        };

        if (resolvedVehiculoId > 0) {
          kwargs['vehiculo_id'] = resolvedVehiculoId;
        } else {
          kwargs['vehiculo_id'] = false;
          kwargs['placa_anonima'] = placaClean;
        }

        if (resolvedConductorId > 0) {
          kwargs['conductor_id'] = resolvedConductorId;
        } else {
          kwargs['conductor_id'] = false;
        }

        await odooService.callKw(
          model: 'fundetaxcol.turno',
          method: 'actualizar',
          kwargs: kwargs,
        );
      } catch (e) {
        debugPrint('[TurnoController] Error creando turno en Odoo: $e');
      }
      await cargarTurnosDesdeServidor();
    }
  }

  Future<TicketDataModel> pagarYEnturnar(String placa, String conductor, double valor) async {
    final placaClean = placa.trim().toUpperCase();
    final conductorClean = conductor.trim().isEmpty ? 'Conductor General' : conductor.trim();

    // 1. Registro contable del pago en Odoo (fundetaxcol.pago con enturnar: true)
    if (odooService.isAuthenticated.value && valor > 0) {
      try {
        final catalogo = await odooService.getConceptosCobro();
        final conceptoBase = catalogo.isNotEmpty ? catalogo.first : null;
        final conceptoId = conceptoBase?.id ?? 1;

        await odooService.crearPago({
          'bahia_id': bahiaIdActual.value,
          'placa': placaClean,
          'conductor': conductorClean,
          'valor': valor,
          'total': valor,
          'enturnar': true,
          'concepto_ids': [
            [0, 0, {'concepto_id': conceptoId, 'cantidad': 1, 'valor': valor}]
          ],
        });
        await cargarPagosDesdeServidor();
      } catch (e) {
        debugPrint('[TurnoController] Advertencia registrando pago en pagarYEnturnar: $e');
      }
    }

    // Registro del recaudo en Firestore
    if (FirebaseService.isInitialized && valor > 0) {
      final recaudo = RecaudoModel(
        id: '',
        name: 'REC-${DateTime.now().millisecondsSinceEpoch}',
        vehiculoPlaca: placaClean,
        conductorNombre: conductorClean,
        bahiaSesionId: bahiaIdActual.value,
        bahiaNombre: bahiaSeleccionada.value,
        cajeroNombre: odooService.usuarioActivo.value,
        fecha: DateTime.now(),
        total: valor,
      );
      firestoreRepository.crearRecaudo(recaudo)
          .catchError((e) => debugPrint('[TurnoController] Firestore crearRecaudo error: $e'));
    }

    // 2. Posicionamiento en cola de turnos
    await enturnarVehiculo(placa: placaClean, conductor: conductorClean, valor: valor);

    final ticket = TicketDataModel(
      bahiaNombre: bahiaSeleccionada.value,
      turnoNumero: 'Turno en espera',
      placa: placaClean,
      conductor: conductorClean,
      fechaHora: DateTime.now(),
      valorTotal: valor,
      cajero: odooService.usuarioActivo.value,
    );

    ultimoTicketImpreso.value = ticket;
    await printerService.imprimirTicket(ticket);
    return ticket;
  }

  Future<void> reimprimirUltimoTicket() async {
    if (ultimoTicketImpreso.value != null) {
      await printerService.imprimirTicket(ultimoTicketImpreso.value!);
    }
  }

  @override
  void onClose() {
    _turnosFirestoreSub?.cancel();
    _bahiasFirestoreSub?.cancel();
    _tarifasFirestoreSub?.cancel();
    socketService.desconectar();
    super.onClose();
  }
}
