# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from babel import numbers
import logging
import json
import requests
_logger = logging.getLogger(__name__)


LIMIT = 2

ESTADO = [('progreso', 'Progreso'), ('cerrado', 'Cerrado')]
VIEWS = [
    ('home', 'Inicio'),
    ('bays', 'Bahías'),
    ('bay', 'Bahía'),
]

URL_SOCKET_SERVER = 'http://localhost:3000'


def send_data_to_socket(path, data):
    try:
        url = URL_SOCKET_SERVER + path
        requests.post(url, json=data)
    except:
        pass


class App(models.Model):
    _inherit = 'fundetaxcol.fundetaxcol'

    state = fields.Selection(
        ESTADO,
        string='Estado',
        related='sesion_id.state'
    )

    @api.model
    def abrir_sesion_movil(self, **values):
        id = values.get('id', False)
        if id:
            Sesion = self.env['fundetaxcol.sesion'].sudo()
            sesion_open = Sesion.search_count(
                [('fundetaxcol_id', '=', int(id)), ('state', '=', 'progreso')]) != 0
            if not sesion_open:
                bahia_ids = self.env['fundetaxcol.bahia'].search(
                    []).mapped('id')
                Sesion.create({
                    'fundetaxcol_id': int(id),
                    'fecha_apertura': fields.Datetime.now(),
                    'bahia_ids': [(6, 0, bahia_ids)]
                })
                return True
        return False

    @api.model
    def load_bay(self, **values):
        uid = values.get('uid')
        rec = self.env['fundetaxcol.settings.mobile'].search(
            [('user_id', '=', uid)]
        )
        return self.env['fundetaxcol.sesion.bahia'].browse(rec.current_bay).read(['id', 'name_sec'])

    @api.model
    def load_bays(self, **values):
        uid = values.get('uid')
        rec = self.env['fundetaxcol.settings.mobile'].search(
            [('user_id', '=', uid)]
        )
        domain = [
            ('state', '=', 'progreso'),
            ('sesion_id', '=', rec.current_session)
        ]
        return self.env['fundetaxcol.sesion.bahia'].search(domain).read(['id', 'name_sec'])

    @api.model
    def get_bahia_ids(self):
        app = self.search([], limit=1)
        domain = [
            ('state', '=', 'progreso'),
            ('sesion_id', '=', app.sesion_id.id)
        ]
        return self.env['fundetaxcol.sesion.bahia'].search(domain)

    @api.model
    def get_format_currency(self, value):
        user_id = self.env.user
        locale = user_id.lang
        currency_id = user_id.company_id.currency_id
        formato = currency_id.name
        result = numbers.format_currency(value, formato, locale=locale)
        return result.replace(u'\xa0', u' ')


class SettingsMobile(models.Model):
    _name = 'fundetaxcol.settings.mobile'

    user_id = fields.Many2one("res.users", string="Usuario")
    name = fields.Char(related="user_id.name")
    mac = fields.Char(string="Mac Bluetooth Printer")
    auto_print = fields.Boolean()
    concepto_id = fields.Many2one('fundetaxcol.concepto')
    current_view = fields.Selection(VIEWS, default='home')
    current_session = fields.Integer()
    current_bay = fields.Integer()
    bay_name = fields.Char()

    @api.model
    def set_state(self, **values):
        uid = values.get('uid', False)
        current_bay = values.get('current_bay', False)
        current_session = values.get('current_session', False)
        go_to_bays = values.get('go_to_bays', False)
        rec = self.search([('user_id', '=', uid)])
        if rec and current_bay:
            rec.write({
                'current_bay': current_bay,
                'current_view': 'bay',
                'bay_name': self.env['fundetaxcol.sesion.bahia'].browse(int(current_bay)).name_sec,
            })
        if rec and go_to_bays:
            rec.write({
                'current_bay': False,
                'current_view': 'bays',
                'bay_name': False,
            })
        if rec and current_session:
            app = self.env['fundetaxcol.fundetaxcol'].browse(current_session)
            rec.write({
                'current_session': app.sesion_id.id,
                'current_view': 'bays',
                'bay_name': False,
            })

    @api.model
    def reload_data(self, **values):
        uid = values.get('uid', False)
        rec_id = self.search([('user_id', '=', uid)])
        if not rec_id:
            return True
        current_view = values.get('current_view', False)
        current_bay = values.get('current_bay', 0)
        current_session = values.get('current_session', 0)
        v = current_view != rec_id.current_view
        b = int(current_bay) != rec_id.current_bay
        s = int(current_session) != rec_id.current_session
        return v or b or s

    @api.model
    def get_data(self, **values):
        uid = values.get('uid', False)
        rec_id = self.search([('user_id', '=', uid)])
        if not rec_id:
            return self.set_data(**values)
        mac = rec_id.mac or '00:00:00:00:00:00'
        ICPSudo = self.env['ir.config_parameter'].sudo()
        hora_recargo = ICPSudo.get_param(
            'fundetaxcol.hora_recargo',
            default=False
        ) + ':00'
        anonimo_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id')
        conductor_id = False
        if anonimo_id:
            conductor_id = self.env['res.partner'].search(
                [('id', '=', int(anonimo_id))], limit=1)
            conductor_id = {
                'id': conductor_id.id,
                'name': conductor_id.name,
            }
        return {
            'user_id': uid,
            'name': rec_id.name,
            'email': rec_id.user_id.email,
            'mac': mac,
            'auto_print': rec_id.auto_print,
            'hora_recargo': hora_recargo,
            'concepto_id': {
                'id': rec_id.concepto_id.id,
                'name': rec_id.concepto_id.name or '',
                'valor': rec_id.concepto_id.valor or 0,
                'tipo': rec_id.concepto_id.tipo,
            },
            'current_view': rec_id.current_view,
            'current_bay': rec_id.current_bay,
            'current_session': rec_id.current_session,
            'bay_name': rec_id.bay_name,
            'anonimo': conductor_id,
            'bahia_ids': self.env['fundetaxcol.fundetaxcol'].get_bahia_ids().ids,
        }

    @api.model
    def set_data(self, **values):
        uid = values.get('uid', False)
        mac = values.get('mac', False)
        auto_print = values.get('auto_print', False)
        concepto_id = values.get('concepto_id', False)
        rec_id = self.search([('user_id', '=', uid)])
        if rec_id:
            rec_id.write({
                'mac': mac,
                'concepto_id': concepto_id,
                'auto_print': auto_print,
            })
        else:
            self.create({
                'user_id': uid,
                'mac': mac,
                'concepto_id': concepto_id,
                'auto_print': auto_print,
            })
        return self.get_data(**values)


class Sesion(models.Model):
    _inherit = 'fundetaxcol.sesion'

    @api.model
    def create(self, values):
        record = super(Sesion, self).create(values)
        send_data_to_socket('/session', {})
        return record

    @api.multi
    def cerrar_sesion(self):
        super(Sesion, self).cerrar_sesion()
        self.env['fundetaxcol.settings.mobile'].search([]).write({
            'current_view': 'home',
            'current_bay': False,
            'current_session': False,
            'bay_name': False,
        })
        send_data_to_socket('/session', {})


class BahiaSesionMovil(models.Model):
    _inherit = 'fundetaxcol.sesion.bahia'

    # selected = fields.Boolean(string="Seleccionada", default=False)
    user_ids = fields.Many2many("res.users", string="Usuarios")

    @api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)

    @api.multi
    def deselected(self, user_id):
        for rec in self:
            rec.user_ids = rec.user_ids - \
                self.env['res.users'].browse(user_id).sudo()
            # rec.selected = False

    @api.model
    def selected_bahia_id(self, **values):
        id = values.get('id', False)
        uid = values.get('uid', False)
        bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
        bahia_ids.deselected(uid)
        if id:
            bahia_id = self.browse(id)
            bahia_id.user_ids |= self.env['res.users'].browse(uid).sudo()
        return self.get_bahia_id(**values)

    @api.model
    def get_current_bay(self):
        domain = [('user_id','=',self.env.user.id)]
        bahia_id = self.env['fundetaxcol.settings.mobile'].search(domain, limit=1).current_bay
        # TODO verificar estado de bahía
        if not bahia_id:
            raise exceptions.ValidationError('No hay bahía seleccionada')
        return bahia_id

    @api.model
    def get_bahia_id(self, **values):
        uid = values.get('uid', False)
        bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
        bahia_id = False
        for _id in bahia_ids:
            if uid in _id.user_ids.ids:
                return {
                    'id': _id.id,
                    'name': _id.name_sec,
                    'state': _id.state
                }
        return {}

    @api.model
    def get_bahia_ids(self):
        bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
        return bahia_ids.mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name_sec,
            'state': rec.state
        })


class PagoMovil(models.Model):
    _inherit = 'fundetaxcol.pago'

    bahia_name = fields.Char(related='bahia_id.bahia_id.name')

    @api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)

    @api.model
    def to_update(self, **values):
        bahia_ids = values.get('bahia_ids', [])
        length = values.get('length', 0)
        domain = [
            ('bahia_id', 'in', bahia_ids)
        ]
        return self.search_count(domain) != length

    @api.model
    def get_all(self, **values):
        bahia_ids = values.get('bahia_ids', [])
        domain = [
            ('bahia_id', 'in', bahia_ids)
        ]
        return self.search(domain).mapped(lambda rec: rec._get_data())

    @api.model
    def get_pago_ids(self, **values):
        selected = values.get('selected', False)
        filter = values.get('filter', False)
        if selected:
            bahia_id = self.env['fundetaxcol.sesion.bahia'].get_current_bay()
            domain = [('bahia_id', '=', bahia_id)]
        else:
            bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
            domain = [('bahia_id', 'in', bahia_ids.ids)]
        if filter and len(filter) != 0:
            domain.append('|')
            domain.append(('conductor_id.name', 'ilike', filter))
            domain.append(('vehiculo_id.name', 'ilike', filter))
        return self.search(domain, order='id desc').mapped(lambda rec: rec._get_data())

    @ api.model
    def get_by_bahia_ids(self, **values):
        filtro = values.get('filtro', False)
        bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
        domain = [('bahia_id', 'in', bahia_ids.ids)]
        _domain = [('bahia_id', 'in', bahia_ids.ids),
                   ('tarifa_id', '=', False)]
        vehiculo_ids = self.env['fundetaxcol.turno'].search(
            _domain).mapped('vehiculo_id').ids
        if vehiculo_ids:
            domain.append(('vehiculo_id', 'not in', vehiculo_ids))
        result = self.search(domain)
        if filtro:
            filtro = filtro.lower()
            result = result.filtered(lambda x: filtro in x.vehiculo_id.name.lower(
            ) or filtro in x.conductor_id.name.lower())
        return result.mapped(lambda x: {
            'name': '%s - %s' % (x.vehiculo_id.name, x.conductor_id.name),
            'vehiculo_id': {
                'id': x.vehiculo_id.id,
                'name': x.vehiculo_id.name,
                'conductor_id': {
                    'id': x.conductor_id.id,
                    'name': x.conductor_id.name,
                }
            },
            'conductor_id': {
                'id': x.conductor_id.id,
                'name': x.conductor_id.name,
                'vehiculo_id': {
                    'id': x.vehiculo_id.id,
                    'name': x.vehiculo_id.name,
                },
            }
        })

    def _get_data(self):
        return {
            'id': self.id,
            'company': {
                'name': self.company_id.name,
                'phone': self.company_id.phone,
                'email': self.company_id.email,
                'website': self.company_id.website,
                'report_footer': self.company_id.report_footer
            },
            'user': self.create_uid.name,
            'consecutivo': self.consecutivo,
            'fecha': self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.create_date),
            'vehiculo_id': {
                'id': self.vehiculo_id.id,
                'name': self.vehiculo_id.name,
                'conductor_ids': self.vehiculo_id.conductor_ids.mapped(lambda x: {
                    'id': x.conductor_id.id,
                    'name': x.conductor_id.name
                })
            },
            'conductor_id': {
                'id': self.conductor_id.id,
                'name': self.conductor_id.name
            },
            'concepto_ids': self.concepto_ids.mapped(lambda concepto: {
                'id': concepto.id,
                'concepto_id': {
                    'id': concepto.concepto_id.id,
                    'name': concepto.concepto_id.name
                },
                'cantidad': concepto.cantidad,
                'valor': concepto.valor,
            }),
            'ahorro_ids': self.conductor_id.get_ahorro(),
            'total': self.valor,
            'ingreso': self.ingreso,
            'ahorro': self.conductor_id.ahorro,
            'bahia_sesion_id': self.bahia_id.id,
            'bahia_id': {
                'name': self.bahia_id.bahia_id.name,
                'id': self.bahia_id.bahia_id.id,
            }
        }

    @ api.model
    def get_pago_by_id(self, **values):
        ids = values.get('ids', [])
        return self.browse(ids).mapped(lambda rec: rec._get_data())

    @ api.model
    def actualizar(self, **values):
        bahia_id = self.env['fundetaxcol.sesion.bahia'].get_current_bay()
        values['bahia_id'] = bahia_id
        rec = self.create(values)
        return rec._get_data()

    @ api.model
    def crear(self, **values):
        id = values.get('id', False)
        if id:
            rec = self.browse(id)
        else:
            values['bahia_id'] = self.env['fundetaxcol.sesion.bahia'].get_current_bay()
            rec = self.create(values)        
        return rec._get_data()

    @api.model
    def create(self, values):
        rec = super(PagoMovil, self).create(values)
        send_data_to_socket('/payment', rec._get_data())
        return rec


class ResPartnerMovil(models.Model):
    _inherit = 'res.partner'

    @ api.model
    def get_all(self, **kwargs):
        domain = [
            ('conductor', '=', True)
        ]
        return self.search(domain, order='id').mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'concepto_ids': rec.template_concepto_id.get_concepto_ids()
        })

    @ api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)

    @ api.model
    def find_partner_from_vehiculo(self, **kwargs):
        fields = kwargs.get('fields')
        domain = kwargs.get('domain')
        VehiculoPartner = self.env['fundetaxcol.vehiculo.partner']
        if kwargs.get('with_concepts', False):
            partners = VehiculoPartner.search(domain).mapped(
                'conductor_id').get_concepto_ids()
        else:
            partners = VehiculoPartner.search(domain)\
                .mapped('conductor_id')\
                .read(fields)
        return partners

    @ api.model
    def get_conductor_ids(self, **values):
        domain = values.get('domain', {})
        name = domain.get('name', False)
        excluir = domain.get('excluir', False)
        domain = [('conductor', '=', True)]
        if name:
            domain.append(('name', 'ilike', name))
        if excluir:
            domain.append(('id', 'not in', excluir))
        return self.search(domain, order='id').mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'concepto_ids': rec.template_concepto_id.get_concepto_ids()
        })

    @ api.multi
    def get_concepto_ids(self):
        result = self.mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'concepto_ids': rec.template_concepto_id.get_concepto_ids()
        })
        return result


class VehiculoMovil(models.Model):
    _inherit = 'fundetaxcol.vehiculo'

    @ api.model
    def get_all(self, **kwargs):
        domain = [
            ('name', 'not ilike', 'BORA'),
            ('name', 'not ilike', 'BORRA'),
        ]
        return self.search(domain).mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'conductor_ids': rec.conductor_ids.mapped(lambda x: {
                'id': x.conductor_id.id,
                'name': x.conductor_id.name,
                'concepto_ids': x.conductor_id.template_concepto_id.get_concepto_ids()
            })
        })

    @ api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)

    @ api.model
    def get_by_bahia_ids(self):
        pass

    @ api.model
    def get_vehiculo_ids(self, **values):
        _filter = values.get('domain', {})
        pago = _filter.get('pago', False)
        turno = _filter.get('turno', False)
        name = _filter.get('name', False)
        domain = []
        bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
        if pago:
            pago_ids = self.env['fundetaxcol.pago'].search(
                [('bahia_id', 'in', bahia_ids.ids)])
            # vehiculo_pago_ids = pago_ids.filtered(lambda x:
            #     len(x.concepto_ids.filtered(lambda c: c.concepto_id.clasificacion == 'ingreso' \
            #         or c.concepto_id.clasificacion == 'cr_ingreso')) != 0
            # ).mapped('vehiculo_id').ids

            domain = [('id', 'not in', pago_ids.mapped('vehiculo_id').ids)]
        elif turno:
            pago_ids = self.env['fundetaxcol.pago'].search(
                [('bahia_id', 'in', bahia_ids.ids)])
            turno_ids = self.env['fundetaxcol.turno'].search([
                ('bahia_id', 'in', bahia_ids.ids),
                ('state', 'in', ['actual', 'espera', 'siguiente', 'pausa'])
            ])
            domain = [('id', 'in', pago_ids.mapped('vehiculo_id').ids),
                      ('id', 'not in', turno_ids.mapped('vehiculo_id').ids)]
        if name:
            domain.append(('name', 'ilike', name))
        return self.search(domain).mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'conductor_ids': rec.conductor_ids.mapped(lambda x: {
                'id': x.conductor_id.id,
                'name': x.conductor_id.name,
                'concepto_ids': x.conductor_id.template_concepto_id.get_concepto_para_pago()
            })
        })

    @ api.model
    def get_para_pago(self, **values):
        name = values.get('name', False)
        bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
        pago_ids = self.env['fundetaxcol.pago'].search(
            [('bahia_id', 'in', bahia_ids.ids)]
        )
        domain = [('id', 'not in', pago_ids.mapped('vehiculo_id').ids)]
        if name:
            domain.append(('name', 'ilike', name))
        return self.search(domain, limit=100).mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'conductor_ids': rec.conductor_ids.mapped(lambda x: {
                'id': x.conductor_id.id,
                'name': x.conductor_id.name,
                'concepto_ids': x.conductor_id.template_concepto_id.get_concepto_para_pago()
            })
        })

    @ api.model
    def get_vehiculo_by_id(self, **args):
        name = args.get('name', False)
        bahia_ids = args.get('bahia_ids', False)
        if bahia_ids:
            domain_pago = [('bahia_id', 'in', bahia_ids)]
            ids = self.env['fundetaxcol.pago'].search(domain_pago).mapped('vehiculo_id').ids
            domain = [('id', 'not in', ids)]
            if name:
                domain.append(('name', 'ilike', name))
            return self.search(domain, limit=7).mapped(lambda rec: {
                'id': rec.id,
                'name': rec.name,
                'conductor_ids': rec.conductor_ids.mapped('conductor_id').ids
            })
        return False

    @ api.multi
    def get_partner_id(self):
        return self.mapped(lambda rec: {
            'id': rec.id,
            'name': rec.name,
            'conductor_ids': rec.conductor_ids.mapped(lambda x: x.conductor_id.id)
        })


class ConceptoConductorMovil(models.Model):
    _inherit = 'fundetaxcol.concepto.conductor'

    def get_concepto_para_pago(self):
        result = []
        index = 0
        for concepto in self.concepto_ids:
            result.append({
                'index': index,
                'concepto_id': {
                    'id': concepto.id,
                    'name': concepto.name,
                    'valor': concepto.valor,
                    'tipo': concepto.tipo
                },
                'cantidad': 1,
                'valor': concepto.valor,
                'tipo': concepto.tipo
            })
            index += 1
        return result

    def get_concepto_ids(self):
        return self.concepto_ids.mapped(lambda x: {
            'id': x.id,
            'name': x.name,
            'valor': x.valor,
            'tipo': x.tipo
        })


class TarifaSectorMovil(models.Model):
    _inherit = 'fundetaxcol.tarifa.sector'

    @ api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)

    def _get_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'valor': self.valor,
            'valor_recargo': self.valor_recargo,
            'nota': self.nota,
        }

    def get_by_values(self, **values):
        ids = values.get('ids', False)
        name = values.get('name', False)
        domain = []
        if ids:
            domain.append(('id', 'in', ids))
        if name:
            domain.append(('name', 'ilike', name))
        return self.search(domain).mapped(lambda rec: rec._get_data())


class TurnoMovil(models.Model):
    _inherit = 'fundetaxcol.turno'

    bahia_name = fields.Char(related='bahia_id.bahia_id.name')

    @api.model
    def to_update(self, **values):
        bahia_ids = values.get('bahia_ids', [])
        length = values.get('length', 0)
        domain = [
            ('bahia_id', 'in', bahia_ids)
        ]
        return self.search_count(domain) != length

    @api.model
    def get_all(self, **values):
        bahia_ids = values.get('bahia_ids', [])
        domain = [
            ('bahia_id', 'in', bahia_ids)
        ]
        return self.search(domain).mapped(lambda rec: rec._get_data())

    @ api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)

    @ api.model
    def get_by_id(self, **values):
        ids = values.get('ids', [])
        return self.browse(ids).mapped(lambda rec: rec._get_data())

    @ api.model
    def cancelar(self, **values):
        id = values.get('id', False)
        turno = self.browse(id)
        turno.write({'state': 'cancelado'})
        return turno._get_data()

    @ api.model
    def actualizar(self, **values):
        id = values.get('id', False)
        anonimo = values.get('anonimo', False)
        tarifa_id = values.get('tarifa_id', False)
        if anonimo or tarifa_id:
            values['state'] = 'despachado'
            values['fecha_despacho'] = fields.Datetime.now()
        if id:
            rec = self.browse(id)
            rec.write(values)
        else:
            rec = self.create(values)
        return rec._get_data()

    @ api.model
    def crear(self, **values):
        id = values.get('id', False)
        tarifa_id = values.get('tarifa_id', False)
        anonimo = values.get('anonimo', False)
        if tarifa_id:
            values['state'] = 'despachado'
            self.env['fundetaxcol.fundetaxcol'].get_fecha_actual()
            values['fecha_despacho'] = fields.Datetime.now()
        if anonimo:
            ICPSudo = self.env['ir.config_parameter'].sudo()
            c_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id')
            values['conductor_id'] = int(c_id)
            values['state'] = 'despachado'
            values['vehiculo_id'] = False
        values['bahia_id'] = self.env['fundetaxcol.sesion.bahia'].get_current_bay()
        if id:
            rec = self.browse(id)
            rec.write(values)
        else:
            rec = self.create(values)
        return rec._get_data()

    @ api.model
    def get_turno_ids(self, **values):
        selected = values.get('selected', False)
        despachado = values.get('despachado', False)
        filter = values.get('filter', False)
        if selected:
            bahia_id = self.env['fundetaxcol.sesion.bahia'].get_current_bay()
            domain = [('bahia_id', '=', bahia_id)]
        else:
            bahia_ids = self.env['fundetaxcol.fundetaxcol'].get_bahia_ids()
            domain = [('bahia_id', 'in', bahia_ids.ids)]
        if not despachado:
            domain.append(
                ('state', 'in', ['actual', 'espera', 'siguiente', 'pausa']))
        else:
            domain.append(('state', '=', 'despachado'))
        if filter and len(filter) != 0:
            domain.append('|')
            domain.append(('conductor_id.name', 'ilike', filter))
            domain.append('|')
            domain.append(('vehiculo_id.name', 'ilike', filter))
            domain.append(('tarifa_id.name', 'ilike', filter))
        return self.search(domain, order='id').mapped(lambda rec: rec._get_data())

    def _get_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'sequence': self.sequence,
            'fecha': self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.create_date),
            'fecha_despacho': self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.fecha_despacho),
            'state': self.state,
            'company': {
                'name': self.company_id.name,
                'phone': self.company_id.phone,
                'email': self.company_id.email,
                'website': self.company_id.website,
                'report_footer': self.company_id.report_footer
            },
            'user': self.create_uid.name,
            'vehiculo_id': {
                'id': self.vehiculo_id.id,
                'name': self.vehiculo_id.name,
                'conductor_ids': self.vehiculo_id.conductor_ids.mapped(lambda x: {
                    'id': x.conductor_id.id,
                    'name': x.conductor_id.name
                })
            },
            'placa_anonima': self.placa_anonima,
            'anonimo': self.anonimo,
            'conductor_id': {
                'id': self.conductor_id.id,
                'name': self.conductor_id.name
            },
            'tarifa_id': {
                'id': self.tarifa_id.id,
                'name': self.tarifa_id.name
            },
            'nota': self.nota,
            'total': self.valor,
            'bahia_sesion_id': self.bahia_id.id,
            'fecha_asignacion': self.fecha_asignacion,
            'bahia_id': {
                'name': self.bahia_id.bahia_id.name,
                'id': self.bahia_id.bahia_id.id,
            }
        }

    def send_data(self):
        if self.name:
            if self.tarifa_id:
                send_data_to_socket('/dispatch', self._get_data())
            else:
                send_data_to_socket('/turn', self._get_data())

    @api.model
    def create(self, values):
        rec = super(TurnoMovil, self).create(values)
        rec.send_data()
        return rec

    @api.multi
    def write(self, values):
        result = super(TurnoMovil, self).write(values)
        for rec in self:
            rec.send_data()
        return result


class ConceptoMovil(models.Model):
    _inherit = 'fundetaxcol.concepto'

    @ api.model
    def total_records(self, domain=[]):
        return self.search_count(domain)
