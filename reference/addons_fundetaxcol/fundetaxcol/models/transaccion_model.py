# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
import logging
_logger = logging.getLogger(__name__)

class Transaccion(models.Model):
	_name = 'fundetaxcol.transaccion'
	_description = 'Transaccion'

	name = fields.Char(string='Nombre')
	fecha = fields.Date(string='Fecha', required=True, default=fields.Date.today)
	company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.user.company_id)
	res_partner_id = fields.Many2one(
		'res.partner',
		string='Tercero',
		domain=['|', ('conductor','=',True), ('propietario','=',True),],
		required=True,
	)
	bahia_id = fields.Many2one(
		'fundetaxcol.sesion.bahia',
		string='Bahía',
		#required=True, no obligatorio para los retiros
		ondelete='cascade',
	)
	sesion_id = fields.Many2one(
		'fundetaxcol.sesion',
		string='Sesión',
		related='bahia_id.sesion_id',
	)
	concepto_id = fields.Many2one(
		'fundetaxcol.concepto',
		string='Concepto',
		required=True,
		#domain=[('is_transaccion','=',True), ]
		domain=[('clasificacion','=','transaccion'), ]
	)
	secuencia_transaccion_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia Transaccion',
		#required=True, no obligatorio para los retiros
	)
	valor = fields.Float(string='Valor',)
	valor_real = fields.Float(string='Valor',)
	detalle = fields.Char(string='Detalle',)
	consecutivo = fields.Char(string='Consecutivo')
	tipo = fields.Selection(string='Tipo', related='concepto_id.tipo')
	retiro = fields.Boolean(string='Retiro', default=False) #Para identificar cual vino de los retiros
	active = fields.Boolean(string='Activo', default=True)

	ajuste_id = fields.Many2one(
	    'fundetaxcol.ajuste',
	    string='Ajuste',
	    ondelete='cascade',
	)

	@api.onchange('concepto_id')
	def _onchange_concepto_id(self):
		if not self.concepto_id:
			self.valor = self.valor_real = 0
		if self.concepto_id.tipo == 'valor_fijo':
			self.valor = self.concepto_id.valor
		if self.concepto_id.afectacion == 'cr':
			self.valor_real = self.valor
		else:
			self.valor_real = -self.valor

	def set_consecutivo(self):
		self.consecutivo = self.secuencia_transaccion_id.numero_str
		self.secuencia_transaccion_id.actualizar_consecutivo()

	def set_name(self):
		self.name = self.concepto_id.name
		if self.detalle:
			self.name += ' [%s]' %(self.detalle)

	@api.model
	def create(self, values):
		new_rec = super(Transaccion, self).create(values)
		new_rec.set_name()
		new_rec.set_consecutivo()
		if not new_rec.retiro:
			new_rec._onchange_concepto_id()
		if new_rec.valor <= 0:
			raise exceptions.ValidationError('El valor debe ser mayor que cero')
		return new_rec