import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/user_model.dart';

void main() {
  group('UserModel & Roles Gremiales Test', () {
    test('Serialización y deserialización de UserModel con rol Conductor y Gremio', () {
      final now = DateTime(2026, 11, 21, 10, 0, 0);
      final user = UserModel(
        id: 'usr_cond_101',
        email: 'conductor@fundetaxcol.co',
        nombre: 'Carlos Ramírez',
        telefono: '3001234567',
        cedula: '1047896541',
        rol: UserRole.conductor,
        organizacionId: 'org_gremio_01',
        gremioNombre: 'Gremio Taxistas del Norte',
        esConductorPrivado: false,
        vehiculoAsignadoPlaca: 'WBD-512',
        activo: true,
        calificacionPromedio: 4.95,
        codigoReferido: 'COND-CR512',
        codigoConvenio: '',
        fechaCreacion: now,
      );

      final map = user.toJson();
      expect(map['id'], 'usr_cond_101');
      expect(map['rol'], 'conductor');
      expect(map['es_conductor_privado'], false);
      expect(map['vehiculo_placa'], 'WBD-512');
      expect(map['gremio_nombre'], 'Gremio Taxistas del Norte');

      final deserializado = UserModel.fromJson(map, 'usr_cond_101');
      expect(deserializado.nombre, 'Carlos Ramírez');
      expect(deserializado.rol, UserRole.conductor);
      expect(deserializado.esConductor, true);
      expect(deserializado.esAdmin, false);
      expect(deserializado.esPasajero, false);
    });

    test('Identificación de conductor privado para convenios VIP', () {
      final conductorPrivado = UserModel(
        id: 'cond_priv_02',
        email: 'vip@fundetaxcol.co',
        nombre: 'Mario Estrada',
        rol: UserRole.conductor,
        esConductorPrivado: true,
        codigoConvenio: 'HOTEL-DEL-PRADO-VIP',
        fechaCreacion: DateTime.now(),
      );

      expect(conductorPrivado.esConductorPrivado, true);
      expect(conductorPrivado.codigoConvenio, 'HOTEL-DEL-PRADO-VIP');
    });

    test('Parseo robusto de roles polimórficos', () {
      expect(UserRoleExtension.fromString('admin_garita'), UserRole.adminGarita);
      expect(UserRoleExtension.fromString('despachador'), UserRole.adminGarita);
      expect(UserRoleExtension.fromString('taxista'), UserRole.conductor);
      expect(UserRoleExtension.fromString('driver'), UserRole.conductor);
      expect(UserRoleExtension.fromString('cliente'), UserRole.pasajero);
      expect(UserRoleExtension.fromString('unknown'), UserRole.pasajero);
    });
  });
}
