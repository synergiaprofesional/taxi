import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/tarifa_sector_model.dart';
import 'package:taxi/services/firestore_repository.dart';

void main() {
  group('FirestoreRepository Motor Tarifario Test', () {
    late FirestoreRepository repository;

    setUp(() {
      repository = FirestoreRepository();
    });

    test('Cálculo estandarizado y legal de tarifas: tarifa base plana sin recargos', () {
      const sector = TarifaSectorModel(
        id: 1,
        name: 'Prado -> Buenavista',
        valor: 10000.0,
        recargoNocturno: 1000.0,
        recargoFestivo: 1000.0,
        recargoAeropuerto: 5000.0,
      );

      final total = repository.calcularTarifaLegal(
        sector: sector,
        esNocturno: false,
        esFestivo: false,
        esAeropuerto: false,
      );

      expect(total, 10000.0);
    });

    test('Cálculo de tarifas con recargo nocturno y festivo', () {
      const sector = TarifaSectorModel(
        id: 1,
        name: 'Prado -> Buenavista',
        valor: 10000.0,
        recargoNocturno: 1000.0,
        recargoFestivo: 1000.0,
        recargoAeropuerto: 5000.0,
      );

      final total = repository.calcularTarifaLegal(
        sector: sector,
        esNocturno: true,
        esFestivo: true,
        esAeropuerto: false,
      );

      expect(total, 12000.0); // 10.000 + 1.000 + 1.000
    });

    test('Cálculo de tarifas con recargo aeropuerto oficial', () {
      const sectorAeropuerto = TarifaSectorModel(
        id: 99,
        name: 'Norte -> Aeropuerto Ernesto Cortissoz',
        valor: 28000.0,
        recargoNocturno: 1000.0,
        recargoFestivo: 1000.0,
        recargoAeropuerto: 5000.0,
      );

      final total = repository.calcularTarifaLegal(
        sector: sectorAeropuerto,
        esNocturno: true,
        esFestivo: false,
        esAeropuerto: true,
      );

      expect(total, 34000.0); // 28.000 + 1.000 + 5.000
    });
  });
}
