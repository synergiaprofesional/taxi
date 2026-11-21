import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/turno_model.dart';

void main() {
  group('TurnoModel Parsing Tests (Paridad fundetaxcol_flutter)', () {
    test('Extrae placa y conductor cuando vehiculo_id y conductor_id son Map (Odoo get_all)', () {
      final json = {
        'id': 249451,
        'name': 'Turno #285 [WGL872 - ORLANDO JOSE BLANQUICETT ORTEGA]',
        'sequence': 285,
        'state': 'espera',
        'vehiculo_id': {'id': 5992, 'name': 'WGL872'},
        'conductor_id': {'id': 3938, 'name': 'ORLANDO JOSE BLANQUICETT ORTEGA'},
        'bahia_id': {'id': 1, 'name': 'Bahía 29D'},
      };

      final turno = TurnoModel.fromJson(json);
      expect(turno.vehiculoPlaca, 'WGL872');
      expect(turno.placaVisible, 'WGL872');
      expect(turno.conductorNombre, 'ORLANDO JOSE BLANQUICETT ORTEGA');
      expect(turno.bahiaNombre, 'Bahía 29D');
      expect(turno.numeroTurno, 285);
    });

    test('Extrae placa y conductor cuando vehiculo_id y conductor_id son List (Odoo search_read)', () {
      final json = {
        'id': 281490,
        'name': 'Turno #120 [FXS830 - JUAN PEREZ]',
        'sequence': 120,
        'state': 'actual',
        'vehiculo_id': [6212, 'FXS830'],
        'conductor_id': [4001, 'JUAN PEREZ'],
        'bahia_id': [2, 'Bahía Garita'],
      };

      final turno = TurnoModel.fromJson(json);
      expect(turno.vehiculoPlaca, 'FXS830');
      expect(turno.placaVisible, 'FXS830');
      expect(turno.conductorNombre, 'JUAN PEREZ');
    });

    test('Fallback: Extrae placa y conductor desde name cuando vehiculo_id es null o false', () {
      final json = {
        'id': 281493,
        'name': 'Turno #125 [FXU168 - VEHICULO DE APOYO]',
        'sequence': 125,
        'state': 'espera',
        'vehiculo_id': false,
        'conductor_id': false,
        'bahia_id': false,
      };

      final turno = TurnoModel.fromJson(json);
      expect(turno.vehiculoPlaca, 'FXU168');
      expect(turno.placaVisible, 'FXU168');
      expect(turno.conductorNombre, 'VEHICULO DE APOYO');
    });

    test('Manejo de turno anónimo con placa personalizada', () {
      final json = {
        'id': 281500,
        'name': 'Turno #126 [ANONIMO]',
        'sequence': 126,
        'state': 'espera',
        'anonimo': true,
        'placa_anonima': 'TAXI-777',
        'vehiculo_id': false,
        'conductor_id': false,
      };

      final turno = TurnoModel.fromJson(json);
      expect(turno.esAnonimo, true);
      expect(turno.placaAnonima, 'TAXI-777');
      expect(turno.placaVisible, 'TAXI-777');
    });

    test('Calibración de hora: Odoo entrega hora local COT sin restar 5 horas adicionales', () {
      final json = {
        'id': 281501,
        'name': 'Turno #3 [FXU910 - RAFAEL EDUARDO GARCIA PAYARES]',
        'sequence': 3,
        'state': 'espera',
        'fecha': '2026-11-02 10:11:58',
        'fecha_despacho': '2026-11-02 10:20:15',
        'vehiculo_id': [5001, 'FXU910'],
        'conductor_id': [3001, 'RAFAEL EDUARDO GARCIA PAYARES'],
      };

      final turno = TurnoModel.fromJson(json);
      // Debe conservar 10:11:58 y no restar 5 horas (que daría 05:11:58)
      expect(turno.fechaCreacion.hour, 10);
      expect(turno.fechaCreacion.minute, 11);
      expect(turno.fechaCreacion.second, 58);

      // Deserialización de fechaDespacho
      expect(turno.fechaDespacho, isNotNull);
      expect(turno.fechaDespacho!.hour, 10);
      expect(turno.fechaDespacho!.minute, 20);
      expect(turno.fechaDespacho!.second, 15);
    });
  });
}
