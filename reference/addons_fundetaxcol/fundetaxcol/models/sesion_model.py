# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class Sesion(models.Model):
	_name = 'fundetaxcol.sesion'
	_description = 'Sesion'
	_order = 'name desc'

	ESTADO = [('progreso','Progreso'),('cerrado','Cerrado')]

	name = fields.Char(string='Nombre',)
	company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.user.company_id)
	fecha_apertura = fields.Datetime(string='Fecha de Apertura', default=fields.Datetime.now)
	fecha_cierre = fields.Datetime(string='Fecha de Cierre',)
	fecha = fields.Date(string='Fecha', compute='_get_fecha')
	state = fields.Selection(ESTADO, string='Estado')
	fundetaxcol_id = fields.Many2one(
		'fundetaxcol.fundetaxcol',
		string='Fundetaxcol',
		required=True,
	)
	bahia_ids = fields.Many2many(
		'fundetaxcol.bahia',
		string='Bahías',
		default=lambda self: self.get_bahias(),
	)
	sesion_bahia_ids = fields.One2many(
		'fundetaxcol.sesion.bahia',
		'sesion_id',
		string='Sesiones por bahia',
	)
	total_pago = fields.Float(string='Total Pagos', compute='_get_total_')
	total_transaccion = fields.Float(string='Total Transacciones', compute='_get_total_')
	total_turno = fields.Float(string='Total Despachos', compute='_get_total_')
	cantidad_pago = fields.Integer(string='Cantidad Pagos', compute='_get_total_')
	cantidad_transaccion = fields.Integer(string='Cantidad Transacciones', compute='_get_total_')
	cantidad_turno = fields.Integer(string='Cantidad Despachos', compute='_get_total_')
	pendiente = fields.Boolean(string='Pendiente', help='Este campo es para el modulo de ajustes en caso de crear la sesion y cancelar el ajuste', )
	ajuste_id = fields.Many2one(
		'fundetaxcol.ajuste',
		string='Ajuste',
		ondelete='cascade',
	)

	def _get_fecha(self):
		for sesion in self:
			sesion.fecha = sesion.fecha_apertura

	def _get_total_(self):
		for sesion in self:
			sesion.total_pago = sesion.total_transaccion = sesion.total_turno = 0
			sesion.cantidad_pago = sesion.cantidad_transaccion = sesion.cantidad_turno = 0
			for bahia in sesion.sesion_bahia_ids:
				sesion.total_pago += bahia.total_pago
				sesion.total_transaccion += bahia.total_transaccion
				sesion.total_turno += bahia.total_turno
				sesion.cantidad_pago += len(bahia.pago_ids)
				sesion.cantidad_transaccion += len(bahia.transaccion_ids)
				sesion.cantidad_turno += len(bahia.turno_ids)

	def get_bahias(self):
		return self.env['fundetaxcol.bahia'].search([])

	def get_name(self):
		self.name = ''.join(['Sesión [', self.fecha_apertura.split(' ')[0], ']'])
		self.fundetaxcol_id.sesion_id = self.id
		self.state = 'progreso'

	def create_sesion_bahia(self):
		for bahia in self.bahia_ids:
			self.sesion_bahia_ids |= self.env['fundetaxcol.sesion.bahia'].new({
				'state': 'progreso',
				'bahia_id': bahia.id,
				'sesion_id': self.id,
			})

	@api.model
	def create(self, values):
		new_rec = super(Sesion, self).create(values)
		if not new_rec.name: new_rec.get_name()
		new_rec.create_sesion_bahia()
		return new_rec

	def reset_bahia_ids(self):
		for sesion_bahia in self.sesion_bahia_ids:
			sesion_bahia.state = 'cerrado'
			sesion_bahia.turno_actual = 1
			sesion_bahia.turno_actual_id = sesion_bahia.bahia_id.turno_actual_id = None
			for turno in sesion_bahia.turno_ids:
				if turno.state == 'espera' or turno.state == 'pausa' or turno.state == 'actual':
					turno.state = 'cancelado'
			sesion_bahia.pago_ids._compute_en_progreso()

	@api.multi
	def cerrar_sesion_confirm(self):
		self.cerrar_sesion()
		#sesion_view_form = self.env.ref('fundetaxcol.confirm_cerrar_sesion_form')
		#return {
		#	'name': 'Cerrar sesión',
		#	'type': 'ir.actions.act_window',
		#	'view_mode': 'form',
		#	'res_model': 'fundetaxcol.sesion',
		#	'views': [(sesion_view_form.id,'form')],
		#	'target': 'new',
		#	'res_id': self.id,
		#}

	@api.multi
	def cerrar_sesion(self):
		self.state = 'cerrado'
		self.reset_bahia_ids()
		self.fecha_cierre = fields.Datetime.now()
		self.fundetaxcol_id.sesion_id = False