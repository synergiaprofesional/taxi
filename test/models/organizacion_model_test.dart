import 'package:flutter_test/flutter_test.dart';
import 'package:taxi/models/organizacion_model.dart';

void main() {
  group('OrganizacionModel & Jerarquía Gremial Test', () {
    test('Serialización y deserialización de OrganizacionModel', () {
      final now = DateTime(2026, 11, 21, 9, 0, 0);
      final org = OrganizacionModel(
        id: 'org_fundetaxcol',
        nombre: 'Fundación Gremial de Taxistas de Colombia (FUNDETAXCOL)',
        nit: '900.876.543-1',
        tipo: TipoOrganizacion.gremio,
        codigoConvenio: 'CONV-FUNDETAXCOL',
        direccion: 'Calle 45 # 21 - 08',
        telefono: '3157778899',
        flotaPublicaHabilitada: true,
        flotaPrivadaHabilitada: true,
        totalVehiculos: 450,
        totalConductores: 620,
        activa: true,
        fechaCreacion: now,
      );

      final map = org.toJson();
      expect(map['id'], 'org_fundetaxcol');
      expect(map['tipo'], 'gremio');
      expect(map['flota_publica_habilitada'], true);
      expect(map['flota_privada_habilitada'], true);
      expect(map['total_vehiculos'], 450);

      final deserializado = OrganizacionModel.fromJson(map, 'org_fundetaxcol');
      expect(deserializado.nombre, 'Fundación Gremial de Taxistas de Colombia (FUNDETAXCOL)');
      expect(deserializado.tipo, TipoOrganizacion.gremio);
      expect(deserializado.codigoConvenio, 'CONV-FUNDETAXCOL');
    });

    test('Parseo de tipos de organización gremial', () {
      expect(TipoOrganizacionExtension.fromString('cooperativa'), TipoOrganizacion.cooperativa);
      expect(TipoOrganizacionExtension.fromString('empresa_privada'), TipoOrganizacion.empresaPrivada);
      expect(TipoOrganizacionExtension.fromString('asociacion'), TipoOrganizacion.asociacion);
      expect(TipoOrganizacionExtension.fromString('gremio'), TipoOrganizacion.gremio);
    });
  });
}
