import paramiko

def apply_optimization():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=30)

    print("=== 1. MODIFICANDO VEHICULO_MODEL.PY EN EL SERVIDOR ===")
    patch_vehiculo_py = '''
# Adición de counts y smart buttons
'''
    # Leemos vehiculo_model.py actual
    sftp = ssh.open_sftp()
    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/vehiculo_model.py', 'r') as f:
        vehiculo_code = f.read().decode('utf-8')

    # 1.1 Corregir comodel 'fundetaxcol' a 'fundetaxcol.vehiculo' en VehiculoPartner
    vehiculo_code = vehiculo_code.replace(
        "vehiculo_id = fields.Many2one(\n        'fundetaxcol',\n        string='Vehículo',\n    )",
        "vehiculo_id = fields.Many2one(\n        'fundetaxcol.vehiculo',\n        string='Vehículo',\n    )"
    )

    # 1.2 Agregar campos pago_count y turno_count en Vehiculo
    fields_to_add = """    pago_count = fields.Integer(string='Pagos', compute='_compute_counts')
    turno_count = fields.Integer(string='Despachos', compute='_compute_counts')

    def _compute_counts(self):
        Pago = self.env['fundetaxcol.pago']
        Turno = self.env['fundetaxcol.turno']
        for rec in self:
            rec.pago_count = Pago.search_count([('vehiculo_id', '=', rec.id)])
            rec.turno_count = Turno.search_count([('vehiculo_id', '=', rec.id)])

    def action_view_pagos(self):
        self.ensure_one()
        return {
            'name': 'Pagos de Vehículo (%s)' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'fundetaxcol.pago',
            'view_mode': 'tree,form',
            'domain': [('vehiculo_id', '=', self.id)],
            'context': {'default_vehiculo_id': self.id},
        }

    def action_view_despachos(self):
        self.ensure_one()
        return {
            'name': 'Despachos de Vehículo (%s)' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'fundetaxcol.turno',
            'view_mode': 'tree,form',
            'domain': [('vehiculo_id', '=', self.id)],
            'context': {'default_vehiculo_id': self.id},
        }
"""
    if "pago_count = fields.Integer" not in vehiculo_code:
        target_str = "    turno_ids = fields.One2many(\n        'fundetaxcol.turno',\n        'vehiculo_id',\n        string='Despachos',\n    )"
        vehiculo_code = vehiculo_code.replace(target_str, target_str + "\n\n" + fields_to_add)

    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/vehiculo_model.py', 'w') as f:
        f.write(vehiculo_code.encode('utf-8'))
    print("vehiculo_model.py actualizado.")

    # ==============================================================
    # 2. MODIFICANDO VEHICULO_VIEW.XML EN EL SERVIDOR
    # ==============================================================
    print("=== 2. MODIFICANDO VEHICULO_VIEW.XML EN EL SERVIDOR ===")
    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/views/vehiculo_view.xml', 'r') as f:
        vehiculo_view_xml = f.read().decode('utf-8')

    # Añadir smart buttons en oe_button_box
    smart_buttons = """                        <div class="oe_button_box" name="button_box">
                            <button name="action_view_pagos" type="object"
                                    class="oe_stat_button" icon="fa-money">
                                <field name="pago_count" widget="statinfo" string="Pagos"/>
                            </button>
                            <button name="action_view_despachos" type="object"
                                    class="oe_stat_button" icon="fa-car">
                                <field name="turno_count" widget="statinfo" string="Despachos"/>
                            </button>
                            <button name="toggle_active" type="object"
                                    class="oe_stat_button" icon="fa-archive">
                                <field name="active" widget="boolean_button"
                                    options='{"terminology": "archive"}'/>
                            </button>
                        </div>"""

    old_button_box = """                        <div class="oe_button_box" name="button_box">
                            <button name="toggle_active" type="object"
                                    class="oe_stat_button" icon="fa-archive">
                                <field name="active" widget="boolean_button"
                                    options='{"terminology": "archive"}'/>
                            </button>
                        </div>"""
    vehiculo_view_xml = vehiculo_view_xml.replace(old_button_box, smart_buttons)

    # Reemplazar el notebook pesado por la pestaña ligera de conductores
    old_notebook = """                        <notebook>
                            <page string="Conductores">
                                <field name="conductor_ids" nolabel="1" domain="[('conductor','=',True)]">
                                    <tree editable="bottom">
                                        <field name="sequence" widget="handle"/>
                                        <field name="conductor_id" required="1" options="{'no_create': True, 'no_open': True, 'no_create_edit': True}" />
                                    </tree>
                                </field>
                            </page>
                            <page string="Pagos" class="oe_read_only">
                                <field name="pago_ids">
                                    <tree default_order="fecha desc">
                                        <field name="consecutivo"/>
                                        <field name="fecha"/>
                                        <field name="conductor_id"/>
                                        <field name="valor" sum="Total"/>
                                    </tree>
                                </field>
                            </page>
                            <page string="Despachos" class="oe_read_only">
                                <field name="turno_ids">
                                    <tree default_order="fecha_asignacion desc">
                                        <field name="conductor_id"/>
                                        <field name="fecha_asignacion"/>
                                        <field name="tarifa_id"/>
                                        <field name="valor" sum="Total"/>
                                    </tree>
                                </field>
                            </page>
                        </notebook>"""

    new_notebook = """                        <notebook>
                            <page string="Conductores">
                                <field name="conductor_ids" nolabel="1" domain="[('conductor','=',True)]">
                                    <tree editable="bottom">
                                        <field name="sequence" widget="handle"/>
                                        <field name="conductor_id" required="1" options="{'no_create': True, 'no_open': True, 'no_create_edit': True}" />
                                    </tree>
                                </field>
                            </page>
                        </notebook>"""
    vehiculo_view_xml = vehiculo_view_xml.replace(old_notebook, new_notebook)

    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/views/vehiculo_view.xml', 'w') as f:
        f.write(vehiculo_view_xml.encode('utf-8'))
    print("vehiculo_view.xml actualizado.")

    # ==============================================================
    # 3. MODIFICANDO TURNO_MODEL.PY (ONCHANGE VEHICULO_ID ÁGIL)
    # ==============================================================
    print("=== 3. OPTIMIZANDO TURNO_MODEL.PY EN EL SERVIDOR ===")
    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py', 'r') as f:
        turno_code = f.read().decode('utf-8')

    old_onchange_vehiculo = """    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id:
            self.conductor_ids = None
            for x in self.vehiculo_id.conductor_ids:
                self.conductor_ids |= x.conductor_id
            if self.vehiculo_id.conductor_ids:
                self.conductor_id = self.vehiculo_id.conductor_ids[0].conductor_id.id"""

    new_onchange_vehiculo = """    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id:
            conductores = self.vehiculo_id.conductor_ids.mapped('conductor_id')
            self.conductor_ids = conductores
            if conductores:
                self.conductor_id = conductores[0]
            elif self.vehiculo_id.propietario_id and self.vehiculo_id.propietario_id.conductor:
                self.conductor_id = self.vehiculo_id.propietario_id
            else:
                self.conductor_id = False"""

    turno_code = turno_code.replace(old_onchange_vehiculo, new_onchange_vehiculo)
    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py', 'w') as f:
        f.write(turno_code.encode('utf-8'))
    print("turno_model.py actualizado.")

    # ==============================================================
    # 4. FLEXIBILIZANDO TURNO_VIEW.XML (BÚSQUEDA POR NOMBRE LIBRE)
    # ==============================================================
    print("=== 4. FLEXIBILIZANDO TURNO_VIEW.XML EN EL SERVIDOR ===")
    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml', 'r') as f:
        turno_view_xml = f.read().decode('utf-8')

    # En asignar_turno_form:
    turno_view_xml = turno_view_xml.replace(
        '<field name="conductor_id" required="1" domain="[(\'id\',\'in\',conductor_ids)]" options="{\'no_create\': True, \'no_open\': True, \'no_create_edit\': True}" />',
        '<field name="conductor_id" required="1" domain="[(\'conductor\',\'=\',True)]" options="{\'no_create\': True, \'no_open\': True, \'no_create_edit\': True}" />'
    )
    # En despachar_turno_form:
    turno_view_xml = turno_view_xml.replace(
        '<field name="conductor_id" required="1" domain="[(\'id\',\'in\',conductor_ids)]" options="{\'no_create\': True, \'no_open\': True, \'no_create_edit\': True}" />',
        '<field name="conductor_id" required="1" domain="[(\'conductor\',\'=\',True)]" options="{\'no_create\': True, \'no_open\': True, \'no_create_edit\': True}" />'
    )

    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml', 'w') as f:
        f.write(turno_view_xml.encode('utf-8'))
    print("turno_view.xml actualizado.")

    # ==============================================================
    # 5. ACTUALIZAR CONDUCTOR_MODEL.PY (NAME_SEARCH CON CÉDULA/NOMBRE)
    # ==============================================================
    print("=== 5. MEJORANDO NAME_SEARCH EN CONDUCTOR_MODEL.PY ===")
    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/conductor_model.py', 'r') as f:
        cond_code = f.read().decode('utf-8')

    name_search_method = """    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('identificacion', operator, name)] + args
        return super(Conductor, self).name_search(name, args=args, operator=operator, limit=limit)
"""
    if "def name_search" not in cond_code:
        cond_code = cond_code.replace("class Conductor(models.Model):\n    _inherit = 'res.partner'\n    _description = 'Conductor'\n", "class Conductor(models.Model):\n    _inherit = 'res.partner'\n    _description = 'Conductor'\n\n" + name_search_method + "\n")

    with sftp.file('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/conductor_model.py', 'w') as f:
        f.write(cond_code.encode('utf-8'))
    print("conductor_model.py actualizado.")

    sftp.close()
    ssh.close()
    print("Todos los archivos actualizados en el servidor.")

if __name__ == '__main__':
    apply_optimization()
