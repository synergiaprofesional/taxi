import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/viaje_model.dart';

void main() {
  group('ViajeModel & Pantalla Espejo Test', () {
    test('Serialización y deserialización de ViajeModel con tarifa desglosada', () {
      final now = DateTime(2026, 11, 21, 10, 30, 0);
      final viaje = ViajeModel(
        id: 'viaje_789',
        pasajeroId: 'pas_01',
        pasajeroNombre: 'Ana Martínez',
        pasajeroTelefono: '3109876543',
        conductorId: 'cond_01',
        conductorNombre: 'Carlos Ramírez',
        conductorTelefono: '3001234567',
        vehiculoPlaca: 'WBD-512',
        vehiculoModelo: 'Kia Rio 2024',
        origenDireccion: 'Calle 72 # 54 - 20',
        destinoDireccion: 'Aeropuerto Ernesto Cortissoz',
        sectorDestinoId: 10,
        sectorNombre: 'Sector Aeropuerto',
        tarifaBase: 25000.0,
        recargoNocturno: 1000.0,
        recargoFestivo: 1000.0,
        recargoAeropuerto: 5000.0,
        tarifaTotal: 32000.0,
        metodoPago: 'efectivo',
        estado: EstadoViaje.aBordo,
        tipoServicio: TipoServicioViaje.calle,
        fechaSolicitud: now,
      );

      final map = viaje.toJson();
      expect(map['id'], 'viaje_789');
      expect(map['tarifa_base'], 25000.0);
      expect(map['recargo_aeropuerto'], 5000.0);
      expect(map['tarifa_total'], 32000.0);
      expect(map['estado'], 'a_bordo');
      expect(viaje.estaActivo, true);

      final deserializado = ViajeModel.fromJson(map, 'viaje_789');
      expect(deserializado.destinoDireccion, 'Aeropuerto Ernesto Cortissoz');
      expect(deserializado.tarifaTotal, 32000.0);
      expect(deserializado.estado, EstadoViaje.aBordo);
    });

    test('Parseo de estados de ciclo de vida del viaje', () {
      expect(EstadoViajeExtension.fromString('solicitado'), EstadoViaje.solicitado);
      expect(EstadoViajeExtension.fromString('assigned'), EstadoViaje.asignado);
      expect(EstadoViajeExtension.fromString('en_camino'), EstadoViaje.enCamino);
      expect(EstadoViajeExtension.fromString('a_bordo'), EstadoViaje.aBordo);
      expect(EstadoViajeExtension.fromString('completed'), EstadoViaje.finalizado);
      expect(EstadoViajeExtension.fromString('cancel'), EstadoViaje.cancelado);
    });
  });
}
