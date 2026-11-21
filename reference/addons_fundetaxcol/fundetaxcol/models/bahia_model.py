# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class Bahia(models.Model):
    _name = 'fundetaxcol.bahia'
    _description = 'Bahia'

    name = fields.Char(string='Nombre', required=True,)
    company_id = fields.Many2one('res.company', string='Compañía',
                                 required=True, default=lambda self: self.env.user.company_id)
    sesion_bahia_id = fields.Many2one(
        'fundetaxcol.sesion.bahia',
        string='Sesion bahia',
    )
    sesion_bahia_ids = fields.One2many(
        'fundetaxcol.sesion.bahia',
        'bahia_id',
        string='Sesiones',
    )
    sesion_ids = fields.Many2many(
        'fundetaxcol.sesion',
        string='Sesiones',
    )
    turno_actual_id = fields.Many2one(
        'fundetaxcol.turno',
        string='Turno Actual',
    )
    sesion_actual_id = fields.Many2one(
        'fundetaxcol.sesion',
        string='Turno Actual',
    )
    turno_desorden = fields.Boolean(
        string='Turnos en desorden', compute='_get_orden_turno')

    def actualizar_turno_actual(self, turno_actual):
        self.turno_actual_id = turno_actual

    def _get_orden_turno(self):
        for bahia in self:
            for t in bahia.sesion_bahia_id.turno_ids:
                if t.state == 'espera':
                    bahia.turno_desorden = t.id != bahia.turno_actual_id.id
                    break

    def get_sesion_id(self):
        domain = [('sesion_id', 'in', self.sesion_ids._ids), ]
        sesion_bahia_ids = self.env['fundetaxcol.sesion.bahia'].search(domain)
        sb_ids = []
        for sb in sesion_bahia_ids:
            sb_ids.append(sb.id)
        return sb_ids

    @api.multi
    def open_ui(self):
        sb_ids = self.get_sesion_id()
        return {
            'type': 'ir.actions.act_url',
            'url': '/tickets?qcontext=%s' % ({"bahia_id": self.id, "sesion_bahia_ids": sb_ids, }),
            'target': 'self',
        }

    @api.multi
    def open_tablero_turnos(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/tablero_turnos?sesion_bahia_id=%s&name=%s' % (self.sesion_bahia_id.id, self.name),
            'target': 'new',
        }

    @api.multi
    def open_new_pay(self):
        return {
            'name': 'Pago',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.pago',
            'target': 'current',
            'context': {'default_bahia_id': self.sesion_bahia_id.id}
        }

    @api.multi
    def asignar_turno(self):
        return {
            'name': 'Asignar Turno',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.turno',
            'target': 'current',
            'context': {
                'default_bahia_id': self.sesion_bahia_id.id,
            }
        }

    @api.multi
    def despachar_turno(self):
        return self.sesion_bahia_id.turno_actual_id.btn_despachar_turno(self.sesion_bahia_id.id)

        #despachar_turno_form = self.env.ref('fundetaxcol.despachar_turno_form', False)
        # if not self.sesion_bahia_id.turno_actual_id:
        #	return False
        # return {
        #	'name': 'Despachar Turno',
        #	'type': 'ir.actions.act_window',
        #	'view_mode': 'form',
        #	'res_model': 'fundetaxcol.turno',
        #	'res_id': self.sesion_bahia_id.turno_actual_id.id,
        #	'views': [(despachar_turno_form.id,'form')],
        #	'target': 'inline',
        #	'context': {
        #		'default_fecha_despacho': fields.Datetime.now(),
        #	}
        # }

    @api.multi
    def crear_turno_anonimo(self):
        despachar_turno_form = self.env.ref(
            'fundetaxcol.despachar_turno_form', False)
        return {
            'name': 'Crear Turno Anónimo',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.turno',
            'views': [(despachar_turno_form.id, 'form')],
            'target': 'new',
            'context': {
                'default_bahia_id': self.sesion_bahia_id.id,
                'default_fecha_despacho': fields.Datetime.now(),
                'default_anonimo': True,
            }
        }

    @api.multi
    def cancelar_turno(self):
        self.turno_actual_id.state = 'cancelado'
        self.sesion_bahia_id.update_turno_actual()

    @api.multi
    def ceder_turno(self):
        turno = self.turno_actual_id
        turnos = self.sesion_bahia_id.turno_ids._ids
        index = turnos.index(turno.id)
        while index+1 < len(turnos):
            _turno = self.env['fundetaxcol.turno'].browse(turnos[index+1])
            if _turno.state == 'espera':
                _turno.state = 'actual'
                self.sesion_bahia_id.turno_actual_id = self.turno_actual_id = _turno.id
                break
            index += 1
        self.env['fundetaxcol.turno'].browse(turno.id).state = 'espera'

    @api.multi
    def pausar_turno(self):
        self.turno_actual_id.state = 'pausa'
        self.sesion_bahia_id.update_turno_actual()

    @api.multi
    def reiniciar_turnos(self):
        if (self.turno_actual_id):
            self.turno_actual_id.state = 'espera'
            self.sesion_bahia_id.update_turno_actual()

    @api.multi
    def get_turnos(self):
        turno_tree = self.env.ref('fundetaxcol.turno_view_tree', False)
        turno_form = self.env.ref('fundetaxcol.despachar_turno_form', False)
        return {
            'name': 'Turnos',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'fundetaxcol.turno',
            'views': [(turno_tree.id, 'tree'), (turno_form.id, 'form')],
            'target': 'self',
            'domain': [
                ('id', 'in', self.sesion_bahia_id.turno_ids._ids),
                '|',
                ('state', '=', 'actual'),
                '|',
                ('state', '=', 'espera'),
                ('state', '=', 'pausa'),
            ]
        }

    @api.multi
    def get_turnos_despachados(self):
        turno_tree = self.env.ref('fundetaxcol.turno_view_tree', False)
        return {
            'name': 'Cancelar Despacho',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.turno',
            'views': [(turno_tree.id, 'tree')],
            'target': 'self',
            'domain': [
                ('id', 'in', self.sesion_bahia_id.turno_ids._ids),
                '|',
                ('state', '=', 'cancelado'),
                ('state', '=', 'despachado'),
            ]
        }

    @api.multi
    def btn_pagos(self):
        return self.sesion_bahia_id.btn_pagos()

    @api.multi
    def btn_ahorro(self):
        return self.sesion_bahia_id.action_ahorro()


class BahiaSesion(models.Model):
    _name = 'fundetaxcol.sesion.bahia'
    _description = 'Bahia Sesion'

    ESTADO = [('progreso', 'Progreso'), ('cerrado', 'Cerrado')]

    name = fields.Char(string='Nombre')
    state = fields.Selection(ESTADO, string='Estado')
    company_id = fields.Many2one('res.company', string='Compañía',
                                 required=True, default=lambda self: self.env.user.company_id)
    sesion_id = fields.Many2one(
        'fundetaxcol.sesion',
        string='Sesion',
        ondelete='cascade',
    )
    bahia_id = fields.Many2one(
        'fundetaxcol.bahia',
        string='Bahía',
        ondelete='cascade',
    )
    turno_ids = fields.One2many(
        'fundetaxcol.turno',
        'bahia_id',
        string='Turnos',
    )
    pago_ids = fields.One2many(
        'fundetaxcol.pago',
        'bahia_id',
        string='Pagos',
    )
    transaccion_ids = fields.One2many(
        'fundetaxcol.transaccion',
        'bahia_id',
        string='Transacciones',
    )
    turno_actual = fields.Integer(string='#Turno', default=1)
    turno_actual_id = fields.Many2one(
        'fundetaxcol.turno',
        string='Turno Actual',
    )
    name_sec = fields.Char(string='Nombre', related='bahia_id.name')
    total_pago = fields.Float(string='Total pagos', compute='_get_total_')
    total_transaccion = fields.Float(
        string='Total transacciones', compute='_get_total_')
    total_turno = fields.Float(string='Total turnos', compute='_get_total_')
    promedio_pago = fields.Float(
        string='Promedio pagos', compute='_get_total_')
    promedio_transaccion = fields.Float(
        string='Promedio transacciones', compute='_get_total_')
    promedio_turno = fields.Float(
        string='Promedio turnos', compute='_get_total_')

    def obtener_conceptos(self):
        def result(concepto):
            cpto_ids = self.pago_ids.mapped('concepto_ids').filtered(
                lambda x: x.concepto_id.id == concepto.id)
            return {
                'concepto': concepto.name,
                'cantidad': sum(cpto_ids.mapped('cantidad')),
                'valor': sum(cpto_ids.mapped('valor')),
                'total': sum(cpto_ids.mapped('subtotal'))
            }
        conceptos = self.pago_ids.mapped("concepto_ids").mapped(
            'concepto_id').mapped(lambda x: result(x))
        return {
            'conceptos': conceptos,
            'total': sum(map(lambda x: x['total'], conceptos)),
        }

    def _get_total_(self):
        for sb in self:
            sb.total_pago = sum(pago.valor for pago in sb.pago_ids)
            sb.total_transaccion = sum(
                transaccion.valor_real for transaccion in sb.transaccion_ids)
            sbtotal_turno = 0
            for turno in sb.turno_ids:
                if turno.state == 'despachado':
                    sb.total_turno += turno.valor
            if len(sb.pago_ids) != 0:
                sb.promedio_pago = sb.total_pago / len(sb.pago_ids)
            else:
                sb.promedio_pago = 0
            if len(sb.transaccion_ids) != 0:
                sb.promedio_transaccion = sb.total_transaccion / \
                    len(sb.transaccion_ids)
            else:
                sb.promedio_transaccion = 0
            if len(sb.turno_ids) != 0:
                sb.promedio_turno = sb.total_turno / len(sb.turno_ids)
            else:
                sb.promedio_turno = 0

    def update_numero_turno(self):
        self.turno_actual += 1

    def get_turno_actual(self, obj):
        return obj.state == 'actual'

    def get_turno_espera(self, obj):
        return obj.state == 'espera'

    def update_turno_actual(self):
        for turno in self.turno_ids:
            if turno.state == 'actual':
                self.turno_actual_id = self.bahia_id.turno_actual_id = turno
                break
        if self.turno_actual_id.state != 'actual':
            for turno in self.turno_ids:
                if turno.state == 'espera':
                    turno.state = 'actual'
                    self.turno_actual_id = self.bahia_id.turno_actual_id = turno
                    break
        if self.turno_actual_id.state != 'actual':
            self.turno_actual_id = self.bahia_id.turno_actual_id = None

    def set_name(self):
        self.name = ' '.join([self.bahia_id.name, self.sesion_id.name])
        self.bahia_id.sesion_actual_id = self.sesion_id
        self.bahia_id.sesion_bahia_id = self.id

    @api.multi
    def print_sesion_bahia(self):
        return self.env.ref('fundetaxcol.report_sesion_bahia_menu').report_action(self, data=None)

    @api.multi
    def btn_pagos(self):
        return {
            'name': 'Pagos de bahía (%s)' % (self.name_sec),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'fundetaxcol.pago',
            'target': 'self',
            'domain': [
                ('bahia_id', '=', self.id),
            ]
        }

    @api.multi
    def btn_transacciones(self):
        return {
            'name': 'Transacciones de bahía (%s)' % (self.name_sec),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'fundetaxcol.transaccion',
            'target': 'self',
            'domain': [
                ('bahia_id', '=', self.id),
            ]
        }

    @api.multi
    def btn_turnos(self):
        return {
            'name': 'Despachos de bahía (%s)' % (self.name_sec),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'fundetaxcol.turno',
            'target': 'self',
            'domain': [
                ('bahia_id', '=', self.id),
            ]
        }

    @api.model
    def create(self, values):
        new_rec = super(BahiaSesion, self).create(values)
        if not new_rec.name:
            new_rec.set_name()
        return new_rec

    @api.multi
    def action_ahorro(self):
        return {
            'name': 'Ahorro (%s)' % (self.name_sec),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.ahorro',
            'target': 'self',
            'context': {
                'default_bahia_id': self.id,
            }
        }
