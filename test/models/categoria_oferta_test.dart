import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/viaje_model.dart';

void main() {
  group('Sprint A: Categorias & ConductorOfertaModel Tests', () {
    test('Serialización y deserialización de CategoriaViaje', () {
      expect(CategoriaViajeExtension.fromString('taxi_estandar'), CategoriaViaje.taxiEstandar);
      expect(CategoriaViajeExtension.fromString('bahia_prioritaria'), CategoriaViaje.bahiaPrioritaria);
      expect(CategoriaViajeExtension.fromString('ejecutivo_vip'), CategoriaViaje.ejecutivoVip);
      expect(CategoriaViajeExtension.fromString('envio_express'), CategoriaViaje.envioExpress);
      expect(CategoriaViajeExtension.fromString('intermunicipal'), CategoriaViaje.intermunicipal);

      expect(CategoriaViaje.taxiEstandar.key, 'taxi_estandar');
      expect(CategoriaViaje.ejecutivoVip.label, 'Ejecutivo VIP');
    });

    test('Serialización y deserialización de ConductorOfertaModel', () {
      final now = DateTime(2026, 11, 21, 11, 40, 0);
      final oferta = ConductorOfertaModel(
        conductorId: 'cond_777',
        conductorNombre: 'Carlos Ramírez',
        conductorFotoUrl: 'https://cdn.taxi.co/fotos/cond_777.jpg',
        conductorCalificacion: 4.95,
        vehiculoPlaca: 'WBD-512',
        vehiculoModelo: 'Kia Rio 2024',
        distanciaMetros: 450,
        tiempoMinutos: 2,
        precioPropuesto: 18000.0,
        fechaOferta: now,
      );

      final map = oferta.toJson();
      expect(map['conductor_id'], 'cond_777');
      expect(map['vehiculo_placa'], 'WBD-512');
      expect(map['distancia_metros'], 450);
      expect(map['tiempo_minutos'], 2);
      expect(map['precio_propuesto'], 18000.0);

      final parsed = ConductorOfertaModel.fromJson(map);
      expect(parsed.conductorNombre, 'Carlos Ramírez');
      expect(parsed.conductorCalificacion, 4.95);
      expect(parsed.precioPropuesto, 18000.0);
    });

    test('ViajeModel conserva categoria y tarifaPropuestaPasajero en JSON/Firestore', () {
      final now = DateTime(2026, 11, 21, 11, 42, 0);
      final viaje = ViajeModel(
        id: 'viaje_oferta_01',
        pasajeroId: 'pas_123',
        pasajeroNombre: 'Ana Martínez',
        origenDireccion: 'Calle 72 # 54 - 20',
        destinoDireccion: 'Aeropuerto',
        tarifaBase: 25000.0,
        tarifaPropuestaPasajero: 28000.0,
        tarifaTotal: 28000.0,
        categoria: CategoriaViaje.bahiaPrioritaria,
        fechaSolicitud: now,
      );

      final json = viaje.toJson();
      expect(json['categoria'], 'bahia_prioritaria');
      expect(json['tarifa_propuesta_pasajero'], 28000.0);
      expect(json['tarifa_total'], 28000.0);

      final deserializado = ViajeModel.fromJson(json, 'viaje_oferta_01');
      expect(deserializado.categoria, CategoriaViaje.bahiaPrioritaria);
      expect(deserializado.tarifaPropuestaPasajero, 28000.0);
    });
  });
}
