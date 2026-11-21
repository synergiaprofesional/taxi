# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
import time

import logging
_logger = logging.getLogger(__name__)

class Config(models.TransientModel):
	_name = 'fundetaxcol.config.settings'
	_inherit = 'res.config.settings'

	default_concepto_tarifa_base_id = fields.Many2one(
		'fundetaxcol.concepto',
		string='Concepto Tarifa Base',
		default_model='fundetaxcol.pago'
	)
	default_secuencia_ticket_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia Tickete',
		default_model='fundetaxcol.pago'
	)

	default_secuencia_transaccion_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia Transacción',
		default_model='fundetaxcol.transaccion'
	)

	default_secuencia_ajuste_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia ajuste para pagos',
		default_model='fundetaxcol.ajuste',
	)
	default_secuencia_ajuste_transaccion_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia ajuste para transacciones',
		default_model='fundetaxcol.ajuste',
	)

	conductor_anonimo_id = fields.Many2one(
		'res.partner',
		string='Conductor anónimo',
		domain=[('conductor','=',True),]
	)

	concepto_ajuste_ahorro_id = fields.Many2one('fundetaxcol.concepto', string='Concepto Ajuste Ahorros')

	hora_recargo = fields.Char(string='Hora para recargo',)

	#plantilla_ahorro_id = fields.Many2one('fundetaxcol.concepto.conductor', string='Plantilla de ahorros')
	#plantilla_ingreso_id = fields.Many2one('fundetaxcol.concepto.conductor', string='Plantilla de ingresos')


	credito_cuenta_ingreso = fields.Boolean(string="Crédito cuenta como ingreso en el mes")
	num_max_credito = fields.Integer(string="Número máximo créditos por conductor")
	no_ingreso_antes_de_credito = fields.Boolean(string="No permitir concepto de ingreso antes de saldar crédito")

	@api.model
	def get_values(self):
		res = super(Config, self).get_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		conductor_anonimo_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id')
		
		#plantilla_ahorro_id = ICPSudo.get_param('fundetaxcol.plantilla_ahorro_id')
		#plantilla_ingreso_id = ICPSudo.get_param('fundetaxcol.plantilla_ingreso_id')

		concepto_ajuste_ahorro_id = ICPSudo.get_param('fundetaxcol.ajuste.ahorro')
		hora_recargo = ICPSudo.get_param('fundetaxcol.hora_recargo')
		if conductor_anonimo_id and not self.env['res.partner'].browse(int(conductor_anonimo_id)).exists():
			conductor_anonimo_id = False

		#if plantilla_ahorro_id and not self.env['fundetaxcol.concepto.conductor'].browse(int(plantilla_ahorro_id)).exists():
		#	plantilla_ahorro_id = False
		#if plantilla_ingreso_id and not self.env['fundetaxcol.concepto.conductor'].browse(int(plantilla_ingreso_id)).exists():
		#	plantilla_ingreso_id = False

		if concepto_ajuste_ahorro_id and not self.env['fundetaxcol.concepto'].browse(int(concepto_ajuste_ahorro_id)).exists():
			concepto_ajuste_ahorro_id = False

		credito_cuenta_ingreso = ICPSudo.get_param('fundetaxcol.credito.ingreso')
		num_max_credito = ICPSudo.get_param('fundetaxcol.credito.maximo')
		no_ingreso_antes_de_credito = ICPSudo.get_param('fundetaxcol.no.credito.ingreso')
		
		res.update(
			hora_recargo = hora_recargo,
			conductor_anonimo_id = int(conductor_anonimo_id),
			concepto_ajuste_ahorro_id = int(concepto_ajuste_ahorro_id),

			#plantilla_ahorro_id = int(plantilla_ahorro_id),
			#plantilla_ingreso_id = int(plantilla_ingreso_id),
			credito_cuenta_ingreso = credito_cuenta_ingreso,
			num_max_credito = int(num_max_credito),
			no_ingreso_antes_de_credito = no_ingreso_antes_de_credito
		)
		return res

	@api.multi
	def set_values(self):
		super(Config, self).set_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		if self.validar_hora(self.hora_recargo):
			ICPSudo.set_param('fundetaxcol.hora_recargo', self.hora_recargo)
		ICPSudo.set_param('fundetaxcol.conductor_anonimo_id', self.conductor_anonimo_id.id)

		#ICPSudo.set_param('fundetaxcol.plantilla_ahorro_id', self.plantilla_ahorro_id.id)
		#ICPSudo.set_param('fundetaxcol.plantilla_ingreso_id', self.plantilla_ingreso_id.id)

		ICPSudo.set_param('fundetaxcol.ajuste.ahorro', self.concepto_ajuste_ahorro_id.id)
		
		ICPSudo.set_param('fundetaxcol.credito.ingreso', self.credito_cuenta_ingreso)
		ICPSudo.set_param('fundetaxcol.credito.maximo', self.num_max_credito)
		ICPSudo.set_param('fundetaxcol.no.credito.ingreso', self.no_ingreso_antes_de_credito)

	def validar_hora(self, hora):
		try:
			time.strptime(hora, "%H:%M")
			return True
		except ValueError:
			raise exceptions.ValidationError('Por favor digite la hora correctamente.\nEjemplos: 20:00 o 01:30')
