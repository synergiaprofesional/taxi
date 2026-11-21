# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

class WizardUtilidadConductor(models.TransientModel):
	_name = 'wizard.fundetaxcol_conductor_repetido'

	vehiculo_id = fields.Many2one('fundetaxcol.vehiculo', 'Vahiculo', required=True)
	conductor_id = fields.Many2one('res.partner', 'Conductor Destino', required=True)
	conductor_ids = fields.Many2many('res.partner', string='Conductores a Transpasar')
	partner_exclude_ids = fields.Many2many('res.partner', string='Terceros a excluir', compute='_compute_partner_to_exclude')

	def _compute_partner_to_exclude(self):
		for rec in self:
			user_ids = self.env['res.users'].search([]).mapped('partner_id').ids
			rec.partner_exclude_ids = self.env['res.partner'].browse(user_ids)

			ICPSudo = self.env['ir.config_parameter'].sudo()
			conductor_anonimo_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id')
			if conductor_anonimo_id:
				rec.partner_exclude_ids |= self.env['res.partner'].browse(int(conductor_anonimo_id))

	@api.onchange('vehiculo_id')
	def _onchange_vehiculo_id(self):
		for rec in self:
			rec._compute_partner_to_exclude()
			if rec.vehiculo_id:
				if len(rec.vehiculo_id.conductor_ids) > 0:
					rec.conductor_id = rec.vehiculo_id.conductor_ids[0].conductor_id.id
				else:
					rec.conductor_id = False

	@api.onchange('conductor_id')
	def _onchange_conductor_id(self):
		for rec in self:
			rec.conductor_ids = False

	def inactivar_partner(self, partner_id):
		partner_id.conductor = False
		partner_id.active = False

	def modificar_tercero(self, obj, transaccion=False, ahorro=False):
		if obj:
			if not transaccion:
				obj.conductor_id = self.conductor_id.id
				if ahorro:
					for concepto_detalle_id in obj.concepto_detalle_ids:
						concepto_detalle_id.pago_concepto_ahorro_id.conductor_id = self.conductor_id.id
			else:
				obj.res_partner_id = self.conductor_id.id

	@api.multi
	def btn_aceptar(self):
		domain = [('conductor_id','in',self.conductor_ids.ids)]
		domain_transaccion = [('res_partner_id','in',self.conductor_ids.ids)]
		#Tareas a ejecutar: 
		#1. Pasar datos del campo conductor_ids a conductor_id, 
		#	a. Pagos
		pagos = self.env['fundetaxcol.pago'].search(domain).mapped(lambda x: self.modificar_tercero(x))
		#	b. Ahorros
		ahorros = self.env['fundetaxcol.pago.concepto.ahorro'].search(domain).mapped(lambda x: self.modificar_tercero(x))
		#	c. Turnos
		turnos = self.env['fundetaxcol.turno'].search(domain).mapped(lambda x: self.modificar_tercero(x))
		#	d. Transacciones
		transacciones = self.env['fundetaxcol.transaccion'].search(domain_transaccion).mapped(lambda x: self.modificar_tercero(x, transaccion=True))
		#	e. Ahorros
		ahorros = self.env['fundetaxcol.ahorro'].search(domain).mapped(lambda x: self.modificar_tercero(x, ahorro=True))
		#2. inactivar conductor_ids, quitar indicador conductor, 
		self.conductor_ids.mapped(lambda x: self.inactivar_partner(x))
		#3. calcular ahorro para conductor_id
		self.conductor_id.conductor = True
		self.conductor_id._compute_ahorro()