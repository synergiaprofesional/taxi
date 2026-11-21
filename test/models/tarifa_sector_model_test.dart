import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/tarifa_sector_model.dart';

void main() {
  group('TarifaSectorModel & Tarifas Oficiales Test', () {
    test('Serialización y deserialización de TarifaSectorModel con recargos de decreto', () {
      const tarifa = TarifaSectorModel(
        id: 15,
        name: 'Centro Histórico -> Terminal Metropolitana',
        valor: 14000.0,
        valorRecargo: 1000.0,
        nota: 'Tarifa aprobada por Decreto Distrital 2026',
        sectorOrigen: 'Centro',
        sectorDestino: 'Terminal',
        decretoReferencia: 'Decreto 0234 de 2026',
        recargoNocturno: 1000.0,
        recargoFestivo: 1000.0,
        recargoAeropuerto: 5000.0,
      );

      final map = tarifa.toJson();
      expect(map['id'], 15);
      expect(map['name'], 'Centro Histórico -> Terminal Metropolitana');
      expect(map['valor'], 14000.0);
      expect(map['decreto_referencia'], 'Decreto 0234 de 2026');
      expect(map['recargo_aeropuerto'], 5000.0);

      final deserializado = TarifaSectorModel.fromJson(map);
      expect(deserializado.name, 'Centro Histórico -> Terminal Metropolitana');
      expect(deserializado.valor, 14000.0);
      expect(deserializado.recargoNocturno, 1000.0);
      expect(deserializado.decretoReferencia, 'Decreto 0234 de 2026');
      expect(deserializado.toString(), 'Centro Histórico -> Terminal Metropolitana (\$ 14000)');
    });
  });
}
