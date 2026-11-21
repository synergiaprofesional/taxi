import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/turno_model.dart';
import '../models/bay_model.dart';
import '../models/tarifa_sector_model.dart';
import '../models/viaje_model.dart';
import '../models/recaudo_model.dart';
import '../models/user_model.dart';

class FirestoreRepository {
  final FirebaseFirestore? _customFirestore;

  FirestoreRepository({FirebaseFirestore? firestore})
      : _customFirestore = firestore;

  FirebaseFirestore get _firestore => _customFirestore ?? FirebaseFirestore.instance;

  // Colecciones canónicas
  CollectionReference get turnosCol => _firestore.collection('turnos');
  CollectionReference get bahiasCol => _firestore.collection('bahias');
  CollectionReference get tarifasCol => _firestore.collection('tarifas_sector');
  CollectionReference get viajesCol => _firestore.collection('viajes');
  CollectionReference get recaudosCol => _firestore.collection('recaudos');
  CollectionReference get vehiculosCol => _firestore.collection('vehiculos');
  CollectionReference get conductoresCol => _firestore.collection('conductores');
  CollectionReference get organizacionesCol => _firestore.collection('organizaciones');
  CollectionReference get usersCol => _firestore.collection('users');
  CollectionReference get panicoCol => _firestore.collection('alertas_panico');

  CollectionReference get _turnosCol => turnosCol;
  CollectionReference get _bahiasCol => bahiasCol;
  CollectionReference get _tarifasCol => tarifasCol;
  CollectionReference get _viajesCol => viajesCol;
  CollectionReference get _recaudosCol => recaudosCol;
  CollectionReference get _usersCol => usersCol;
  CollectionReference get _panicoCol => panicoCol;

  // =========================================================================
  // 1. CAPA 0: GARITA, BAHÍAS Y TURNOS
  // =========================================================================

  /// Stream reactivo de turnos por bahía ordenados por número de turno
  Stream<List<TurnoModel>> streamTurnosBahia(int bahiaSesionId) {
    Query query = _turnosCol;
    if (bahiaSesionId > 0) {
      query = query.where('bahia_sesion_id', isEqualTo: bahiaSesionId);
    }
    return query
        .orderBy('numero_turno', descending: false)
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => TurnoModel.fromFirestore(doc)).toList());
  }

  /// Stream de bahías activas
  Stream<List<BahiaModel>> streamBahias() {
    return _bahiasCol
        .where('activa', isEqualTo: true)
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => BahiaModel.fromFirestore(doc)).toList());
  }

  /// Crear un nuevo turno en la cola de la bahía (Transacción atómica)
  Future<TurnoModel> crearTurno(TurnoModel turno) async {
    final docRef = turno.id > 0 ? _turnosCol.doc(turno.id.toString()) : _turnosCol.doc();

    return await _firestore.runTransaction((transaction) async {
      // Calcular siguiente sequence si no viene asignado
      int sequence = turno.numeroTurno;
      if (sequence <= 0) {
        final querySnap = await _turnosCol
            .where('bahia_sesion_id', isEqualTo: turno.bahiaSesionId)
            .where('state', whereIn: ['espera', 'actual', 'siguiente'])
            .get();
        sequence = querySnap.docs.length + 1;
      }

      final nuevoTurno = TurnoModel(
        id: int.tryParse(docRef.id) ?? turno.id,
        name: turno.name.isNotEmpty ? turno.name : 'T-${sequence.toString().padLeft(3, '0')}',
        vehiculoPlaca: turno.placaVisible,
        conductorNombre: turno.conductorNombre,
        bahiaNombre: turno.bahiaNombre,
        numeroTurno: sequence,
        estado: sequence == 1 ? EstadoTurno.actual : (sequence == 2 ? EstadoTurno.siguiente : EstadoTurno.espera),
        fechaCreacion: DateTime.now(),
        valorTotal: turno.valorTotal,
        tarifaId: turno.tarifaId,
        tarifaNombre: turno.tarifaNombre,
        nota: turno.nota,
        esAnonimo: turno.esAnonimo,
        placaAnonima: turno.placaAnonima,
        bahiaSesionId: turno.bahiaSesionId,
        bahiaBaseId: turno.bahiaBaseId,
        vehiculoId: turno.vehiculoId,
        conductorId: turno.conductorId,
      );

      transaction.set(docRef, nuevoTurno.toFirestore());
      return nuevoTurno;
    });
  }

  /// Despachar un turno con destino oficial y valor total
  Future<void> despacharTurno(
    String turnoId, {
    required int tarifaId,
    required String tarifaNombre,
    required double valorTotal,
  }) async {
    await _turnosCol.doc(turnoId).update({
      'state': EstadoTurno.despachado.name,
      'tarifa_id': tarifaId,
      'tarifa_nombre': tarifaNombre,
      'valor_total': valorTotal,
      'fecha_despacho': FieldValue.serverTimestamp(),
    });
  }

  /// Despacha un turno de bahía y, si se suministra celular, crea automáticamente el ViajeModel en /viajes
  /// retornando el ID del viaje generado (para el enlace de WhatsApp y tracking web).
  Future<String?> despacharTurnoConViaje({
    required String turnoId,
    required int tarifaId,
    required String tarifaNombre,
    required double valorTotal,
    required String bahiaNombre,
    required String placa,
    required String conductorNombre,
    String? telefonoPasajero,
    String? nota,
  }) async {
    await despacharTurno(
      turnoId,
      tarifaId: tarifaId,
      tarifaNombre: tarifaNombre,
      valorTotal: valorTotal,
    );

    final celLimpio = telefonoPasajero?.trim() ?? '';
    if (celLimpio.isEmpty) {
      return null;
    }

    final docRef = _viajesCol.doc();
    final viaje = ViajeModel(
      id: docRef.id,
      pasajeroId: 'pasajero_bahia_$celLimpio',
      pasajeroNombre: 'Pasajero Bahía $bahiaNombre',
      pasajeroTelefono: celLimpio,
      categoria: CategoriaViaje.bahiaPrioritaria,
      estado: EstadoViaje.asignado,
      origen: 'Bahía $bahiaNombre',
      destino: tarifaNombre,
      precioSugerido: valorTotal,
      precioAcordado: valorTotal,
      conductorId: 'conductor_turno_$turnoId',
      conductorNombre: conductorNombre,
      conductorTelefono: '',
      vehiculoPlaca: placa,
      vehiculoModelo: 'Taxi Formal',
      fechaSolicitud: DateTime.now(),
      fechaAsignacion: DateTime.now(),
      metodoPago: 'efectivo',
    );

    await docRef.set(viaje.toFirestore());
    return docRef.id;
  }

  /// Cancelar un turno
  Future<void> cancelarTurno(String turnoId, {String motivo = ''}) async {
    await _turnosCol.doc(turnoId).update({
      'state': EstadoTurno.cancelado.name,
      if (motivo.isNotEmpty) 'nota': motivo,
    });
  }

  /// Reorganizar cola de turnos (pasar turno al final)
  Future<void> pasarTurnoAlFinal(String turnoId, int bahiaSesionId) async {
    final querySnap = await _turnosCol
        .where('bahia_sesion_id', isEqualTo: bahiaSesionId)
        .where('state', whereIn: ['espera', 'actual', 'siguiente'])
        .orderBy('numero_turno', descending: true)
        .limit(1)
        .get();

    int maxSeq = 1;
    if (querySnap.docs.isNotEmpty) {
      final ultimo = TurnoModel.fromFirestore(querySnap.docs.first);
      maxSeq = ultimo.numeroTurno + 1;
    }

    await _turnosCol.doc(turnoId).update({
      'numero_turno': maxSeq,
      'state': EstadoTurno.espera.name,
    });
  }

  // =========================================================================
  // 2. TARIFAS LEGALES Y SECTORES ESTANDARIZADOS
  // =========================================================================

  /// Stream de tarifas de sectores vigentes
  Stream<List<TarifaSectorModel>> streamTarifas() {
    return _tarifasCol.snapshots().map(
        (snapshot) => snapshot.docs.map((doc) => TarifaSectorModel.fromFirestore(doc)).toList());
  }

  /// Obtener lista de tarifas de sectores en memoria
  Future<List<TarifaSectorModel>> getTarifasSector() async {
    final snap = await _tarifasCol.get();
    return snap.docs.map((doc) => TarifaSectorModel.fromFirestore(doc)).toList();
  }

  /// Motor de cálculo estandarizado de tarifas (cero arbitrariedad)
  double calcularTarifaLegal({
    required TarifaSectorModel sector,
    required bool esNocturno,
    required bool esFestivo,
    required bool esAeropuerto,
  }) {
    double total = sector.valor;
    if (esNocturno) total += sector.recargoNocturno;
    if (esFestivo) total += sector.recargoFestivo;
    if (esAeropuerto) total += sector.recargoAeropuerto;
    return total;
  }

  // =========================================================================
  // 3. CAPA 2: VIAJES DEL PASAJERO Y DESPACHO EN CALLE
  // =========================================================================

  /// Solicitar un nuevo servicio de taxi desde la app de pasajero
  Future<ViajeModel> solicitarViaje(ViajeModel viaje) async {
    final docRef = viaje.id.isNotEmpty ? _viajesCol.doc(viaje.id) : _viajesCol.doc();
    final nuevo = viaje.copyWith(
      id: docRef.id,
      estado: EstadoViaje.solicitado,
      fechaSolicitud: DateTime.now(),
    );
    await docRef.set(nuevo.toFirestore());
    return nuevo;
  }

  /// Publicar una oferta o contraoferta de conductor para un viaje
  Future<void> proponerOfertaConductor(String viajeId, ConductorOfertaModel oferta) async {
    await _viajesCol
        .doc(viajeId)
        .collection('ofertas')
        .doc(oferta.conductorId)
        .set(oferta.toJson());
  }

  /// Stream reactivo de ofertas de conductores recibidas en tiempo real
  Stream<List<ConductorOfertaModel>> streamOfertasViaje(String viajeId) {
    return _viajesCol
        .doc(viajeId)
        .collection('ofertas')
        .orderBy('distancia_metros', descending: false)
        .snapshots()
        .map((snap) => snap.docs.map((d) => ConductorOfertaModel.fromJson(d.data())).toList());
  }

  /// El pasajero selecciona su conductor favorito del marketplace
  Future<void> seleccionarConductorViaje(String viajeId, ConductorOfertaModel oferta) async {
    await _viajesCol.doc(viajeId).update({
      'conductor_id': oferta.conductorId,
      'conductor_nombre': oferta.conductorNombre,
      'conductor_telefono': '3001234567',
      'vehiculo_placa': oferta.vehiculoPlaca,
      'vehiculo_modelo': oferta.vehiculoModelo,
      'tarifa_total': oferta.precioPropuesto,
      'estado': EstadoViaje.asignado.key,
      'fecha_asignacion': FieldValue.serverTimestamp(),
    });
  }

  /// Stream de viajes activos de un pasajero
  Stream<List<ViajeModel>> streamViajesPasajero(String pasajeroId) {
    return _viajesCol
        .where('pasajero_id', isEqualTo: pasajeroId)
        .orderBy('fecha_solicitud', descending: true)
        .limit(10)
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => ViajeModel.fromFirestore(doc)).toList());
  }

  /// Stream de viajes disponibles en calle para conductores (radar público)
  Stream<List<ViajeModel>> streamViajesDisponiblesCalle({String? gremioId}) {
    Query query = _viajesCol.where('estado', isEqualTo: 'solicitado');
    return query
        .orderBy('fecha_solicitud', descending: false)
        .limit(20)
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => ViajeModel.fromFirestore(doc)).toList());
  }

  // =========================================================================
  // 4. CAPA 1: OPERACIÓN DEL CONDUCTOR
  // =========================================================================

  /// Stream de viajes asignados a un conductor
  Stream<List<ViajeModel>> streamViajesConductor(String conductorId) {
    return _viajesCol
        .where('conductor_id', isEqualTo: conductorId)
        .orderBy('fecha_solicitud', descending: true)
        .limit(10)
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => ViajeModel.fromFirestore(doc)).toList());
  }

  /// Conductor acepta una carrera solicitada
  Future<void> aceptarViaje(
    String viajeId, {
    required String conductorId,
    required String conductorNombre,
    required String conductorTelefono,
    required String vehiculoPlaca,
    String vehiculoModelo = '',
  }) async {
    await _viajesCol.doc(viajeId).update({
      'conductor_id': conductorId,
      'conductor_nombre': conductorNombre,
      'conductor_telefono': conductorTelefono,
      'vehiculo_placa': vehiculoPlaca,
      'vehiculo_modelo': vehiculoModelo,
      'estado': EstadoViaje.asignado.key,
      'fecha_asignacion': FieldValue.serverTimestamp(),
    });
  }

  /// Actualizar estado de viaje en curso (en_camino, a_bordo, finalizado, cancelado)
  Future<void> actualizarEstadoViaje(String viajeId, EstadoViaje nuevoEstado) async {
    final Map<String, dynamic> data = {'estado': nuevoEstado.key};
    if (nuevoEstado == EstadoViaje.aBordo) {
      data['fecha_inicio'] = FieldValue.serverTimestamp();
    } else if (nuevoEstado == EstadoViaje.finalizado) {
      data['fecha_finalizacion'] = FieldValue.serverTimestamp();
    }
    await _viajesCol.doc(viajeId).update(data);
  }

  /// Calificar un viaje terminado
  Future<void> calificarViaje(
    String viajeId, {
    required double calificacion,
    String comentario = '',
    bool esPasajero = true,
  }) async {
    if (esPasajero) {
      await _viajesCol.doc(viajeId).update({
        'calificacion_conductor': calificacion,
        'comentario_pasajero': comentario,
      });
    } else {
      await _viajesCol.doc(viajeId).update({
        'calificacion_pasajero': calificacion,
      });
    }
  }

  /// Botón de Auxilio / Pánico Vial del taxista
  Future<void> registrarPanicoVial({
    required String conductorId,
    required String conductorNombre,
    required String vehiculoPlaca,
    required double lat,
    required double lng,
    String motivo = 'Auxilio vial activado',
  }) async {
    await _panicoCol.add({
      'conductor_id': conductorId,
      'conductor_nombre': conductorNombre,
      'vehiculo_placa': vehiculoPlaca,
      'lat': lat,
      'lng': lng,
      'motivo': motivo,
      'atendida': false,
      'fecha': FieldValue.serverTimestamp(),
    });
  }

  // =========================================================================
  // 5. RECAUDOS Y CAJA
  // =========================================================================

  /// Stream de recaudos
  Stream<List<RecaudoModel>> streamRecaudos({int? bahiaSesionId}) {
    Query query = _recaudosCol;
    if (bahiaSesionId != null && bahiaSesionId > 0) {
      query = query.where('bahia_sesion_id', isEqualTo: bahiaSesionId);
    }
    return query
        .orderBy('fecha', descending: true)
        .limit(50)
        .snapshots()
        .map((snapshot) => snapshot.docs.map((doc) => RecaudoModel.fromFirestore(doc)).toList());
  }

  /// Registrar nuevo recaudo en caja
  Future<RecaudoModel> crearRecaudo(RecaudoModel recaudo) async {
    final docRef = recaudo.id.isNotEmpty ? _recaudosCol.doc(recaudo.id) : _recaudosCol.doc();
    final nuevo = RecaudoModel(
      id: docRef.id,
      name: recaudo.name.isNotEmpty ? recaudo.name : 'REC-${DateTime.now().millisecondsSinceEpoch}',
      vehiculoPlaca: recaudo.vehiculoPlaca,
      conductorNombre: recaudo.conductorNombre,
      conductorCedula: recaudo.conductorCedula,
      bahiaSesionId: recaudo.bahiaSesionId,
      bahiaNombre: recaudo.bahiaNombre,
      cajeroNombre: recaudo.cajeroNombre,
      fecha: DateTime.now(),
      total: recaudo.total,
      totalAhorro: recaudo.totalAhorro,
      lineas: recaudo.lineas,
      metodoPago: recaudo.metodoPago,
      nota: recaudo.nota,
    );
    await docRef.set(nuevo.toFirestore());
    return nuevo;
  }

  // =========================================================================
  // 6. USUARIOS Y PERFILES
  // =========================================================================

  /// Obtener perfil de usuario por UID de Firebase Auth
  Future<UserModel?> getPerfilUsuario(String uid) async {
    final doc = await _usersCol.doc(uid).get();
    if (!doc.exists) return null;
    return UserModel.fromFirestore(doc);
  }

  /// Guardar o actualizar perfil de usuario
  Future<void> guardarPerfilUsuario(UserModel user) async {
    await _usersCol.doc(user.id).set(user.toFirestore(), SetOptions(merge: true));
  }
}
