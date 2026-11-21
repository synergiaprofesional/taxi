# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)
#_logger.error()

class RetiroAhorro(models.Model):
	_name = 'fundetaxcol.retiro.ahorro'

	conductor_id = fields.Many2one(
		'res.partner',
		string='Conductor',
		required=True,
	)
	valor = fields.Float(string='Valor Retiro', compute='_compute_valor', store=True)
	concepto_final_id = fields.Many2one('fundetaxcol.concepto', string='Concepto Final')
	nota = fields.Text(string='Nota')
	ahorro_total = fields.Float(string='Ahorro Total')
	ahorro = fields.Float(string='Restante', related='conductor_id.ahorro')
	pago_ahorro_ids = fields.One2many(comodel_name='fundetaxcol.pago.concepto.ahorro', inverse_name='retiro_id', string='Ahorros')

	pago_ahorro_ids_copy = fields.One2many(comodel_name='fundetaxcol.pago.concepto.ahorro', inverse_name='retiro_id', string='Ahorros')

	state = fields.Selection([('aprobado','Aprobado'),('revertido','Revertido')], string='Estado')
	transaccion_id = fields.Many2one('fundetaxcol.transaccion', string='Transacción')

	@api.depends('pago_ahorro_ids')
	def _compute_valor(self):
		for rec in self:
			rec.valor = sum(rec.pago_ahorro_ids.mapped('valor'))

	#@api.depends('valor', 'ahorro_total')
	#def _compute_restante(self):
	#	for rec in self:
	#		rec.restante = rec.ahorro_total - rec.valor

	@api.multi
	def name_get(self):
		result = []
		for record in self:
			valor = str(record.valor)
			_valor = valor.split('.')
			if len(_valor) > 0:
				valor = _valor[0]
			result.append((record.id, 'RETIRO [' + record.conductor_id.name + ' - $' + valor + ']'))
		return result

	@api.onchange('conductor_id')
	def _onchange_conductor_id(self):
		for rec in self:
			rec.pago_ahorro_ids.unlink()
			if rec.conductor_id:
				rec.ahorro_total = sum(line.subtotal for line in rec.conductor_id.pago_ahorro_ids)
				ahorro_ids = rec.conductor_id.get_ahorro_ids()
				for ahorro in ahorro_ids:
					concepto_id = ahorro.get('concepto_id')
					valor = ahorro.get('subtotal')
					if valor > 0:
						rec.pago_ahorro_ids |= self.env['fundetaxcol.pago.concepto.ahorro'].new({
							'conductor_id': rec.conductor_id.id,
							'concepto_id': concepto_id.id,
							'cantidad': 1,
							'valor': valor,
						})
			else:
				rec.ahorro_total = 0

	def get_data(self):
		return {
			'conductor': self.conductor_id.name,
			'valor': self.valor,
			'ahorro_ids': self.conductor_id.get_ahorro(),
			'restante': self.ahorro,
			'user': self.create_uid.partner_id.name,
			'fecha': self.create_date,
			'company': {
				'name': self.env.user.company_id.name,
				'phone': self.env.user.company_id.phone,
				'email': self.env.user.company_id.email,
				'website': self.env.user.company_id.website,
				'report_footer': self.env.user.company_id.report_footer
			},
		}

	@api.multi
	def action_aceptar(self):
		return {
			"type": "ir.actions.act_url_print",
			"url": "/print/ticket_ahorro?qcontext=%s" %(self.get_data()),
			"target": "new",
		}

	def crear_transaccion(self, values):
		concepto_id = values.get('concepto_final_id')
		tercero_id = values.get('conductor_id')
		nota = values.get('nota', False)
		valor = values.get('valor', False)
		Transaccion = self.env['fundetaxcol.transaccion']
		transaccion_id = Transaccion.create({
			'concepto_id': concepto_id,
			'res_partner_id': tercero_id,
			'valor': valor,
			'detalle': nota,
			'retiro': True,
		})
		transaccion_id.set_consecutivo()
		values['transaccion_id'] = transaccion_id.id

	@api.multi
	def action_revertir(self):
		for rec in self:
			rec.state = 'revertido'
			if rec.transaccion_id:
				rec.transaccion_id.sudo().active = False
			for ahorro in rec.pago_ahorro_ids:
				ahorro.valor = 0
			rec.conductor_id._compute_ahorro()

	def _procesar_retiro(self, values):
		ResPartner = self.env['res.partner']
		conductor_id = values.get('conductor_id', False)
		concepto_final_id = values.get('concepto_final_id', False)
		pago_ahorro_ids = list(map(lambda x: x[2] , values.get('pago_ahorro_ids')))
		
		conductor_id = ResPartner.browse(conductor_id)
		ahorro_total = sum(line.subtotal for line in conductor_id.pago_ahorro_ids)
		retiro = sum(list(map(lambda x: x['valor'], pago_ahorro_ids)))
		if ahorro_total == 0:
			raise exceptions.ValidationError('El conductor seleccionado no tiene ahorros')
		if retiro > ahorro_total:
			raise exceptions.ValidationError('Por favor verifique el valor a retirar')
		ahorro_ids = conductor_id.get_ahorro_ids()
		#Recorrer ahorros del conductor para verificar que no saquen más de lo que tiene el concepto
		for ahorro in ahorro_ids:
			concepto_id = ahorro.get('concepto_id')
			#Subtotal del concepto que ya tiene el conductor
			subtotal = ahorro.get('subtotal')
			#Filtrar los conceptos en la lista de los conceptos agregados al registro actual (Solo encontrará un concepto)
			_ahorros = list(filter(lambda x: x['concepto_id'] == concepto_id.id, pago_ahorro_ids))
			#Sumar el campo valor del filtro
			valor_gui = sum(list(map(lambda x: x['valor'], _ahorros)))
			#Verificar si el valor de la interfaz es mayor al del concepto actual
			if valor_gui > subtotal:
				raise exceptions.ValidationError('El concepto \"%s\" tiene un saldo de $%s, por favor verifique el valor que está retirando' %(concepto_id.name, subtotal))
		values['state'] = 'aprobado'
		values['ahorro_total'] = ahorro_total
		values['valor'] = retiro
		#values['pago_ahorro_ids_copy'] = values['pago_ahorro_ids']
		if concepto_final_id:
			self.crear_transaccion(values)

	#def procesar_retiro(self):
	#	self.ahorro_total = sum(line.subtotal for line in self.conductor_id.pago_ahorro_ids)
	#	retiro = sum(self.pago_ahorro_ids.mapped('subtotal'))
	#	if self.ahorro_total - retiro == 0:
	#		raise exceptions.ValidationError('El conductor seleccionado no tiene ahorros')
	#	if self.valor > self.ahorro_total - retiro:
	#		raise exceptions.ValidationError('Por favor verifique el valor a retirar')
	#	ahorro_ids = self.conductor_id.get_ahorro_ids()
	#	for ahorro in ahorro_ids:
	#		concepto_id = ahorro.get('concepto_id')
	#		_ahorros = self.pago_ahorro_ids.filtered(lambda x: x.concepto_id.id == concepto_id.id)
	#		for x in _ahorros:
	#			valor = ahorro.get('subtotal') - x.subtotal
	#			if x.subtotal > valor:
	#				raise exceptions.ValidationError('El concepto %s tiene un saldo de $%s, por favor verifique el valor que está retirando' %(concepto_id.name, valor))

	@api.model
	def create(self, values):
		pago_ahorro_ids = values.get('pago_ahorro_ids')
		conductor_id = values.get('conductor_id')
		if not pago_ahorro_ids:
			raise exceptions.ValidationError('No se puede guardar el registro sin detalles')
		for ahorro in pago_ahorro_ids:
			new_ahorro = ahorro[2]
			new_ahorro['conductor_id'] = conductor_id
			new_ahorro['cantidad'] = -1
		self._procesar_retiro(values)

		#_logger.error(values)

		new_record = super(RetiroAhorro, self).create(values)
		#new_record.procesar_retiro()

		#raise exceptions.ValidationError('')
		return new_record

	@api.multi
	def unlink(self):
		for rec in self:
			if rec.transaccion_id:
				rec.transaccion_id.sudo().unlink()
			rec.pago_ahorro_ids.unlink()
		return super(RetiroAhorro, self).unlink()


#*************************************Ajuste ahorros*************************************#
class AjusteAhorro(models.Model):
	_name = 'fundetaxcol.ajuste.ahorro'

	fecha = fields.Date(string='Fecha', required=True, default=fields.Date.today)
	concepto_id = fields.Many2one('fundetaxcol.concepto', string='Concepto', required=True)
	conductor_ids = fields.One2many(comodel_name='fundetaxcol.ajuste.ahorro.detalle', inverse_name='ajuste_id', string='Conductores')
	mantener_ajustes = fields.Boolean(string='Mantener Otros Ajustes', default=True)

	@api.onchange('fecha')
	def _onchange_fecha(self):
		ICPSudo = self.env['ir.config_parameter'].sudo()
		concepto_ajuste_ahorro_id = ICPSudo.get_param('fundetaxcol.ajuste.ahorro')
		for rec in self:
			if concepto_ajuste_ahorro_id:
				rec.concepto_id = int(concepto_ajuste_ahorro_id)

	@api.model
	def create(self, values):
		ICPSudo = self.env['ir.config_parameter'].sudo()
		concepto_ajuste_ahorro_id = ICPSudo.get_param('fundetaxcol.ajuste.ahorro')
		if concepto_ajuste_ahorro_id:
			values['concepto_id'] = int(concepto_ajuste_ahorro_id)
		return super(AjusteAhorro, self).create(values)

	#@api.model
	#def new(self, values={}, ref=None):
	#	record = super(AjusteAhorro, self).new(values, ref)
	#	concepto_ajuste_ahorro_id = ICPSudo.get_param('fundetaxcol.ajuste.ahorro')
	#	if concepto_ajuste_ahorro_id:
	#		record.concepto_id = int(concepto_ajuste_ahorro_id)
	#	return record

	@api.multi
	def action_aceptar(self):
		self.actualizar_ahorro()

	def actualizar_ahorro(self):
		concepto_inicial = False
		if self.mantener_ajustes:
			concepto_inicial = self.concepto_id.id
		self.env['res.partner'].calcular_ahorros(self.fecha, concepto_inicial=concepto_inicial, ids=self.conductor_ids.mapped('conductor_id.id'))
		for rec in self.conductor_ids:
			ahorro_id = self.env['fundetaxcol.pago.concepto.ahorro'].create({
				'conductor_id': rec.conductor_id.id,
				'concepto_id': self.concepto_id.id,
				'cantidad': 1,
				'valor': rec.valor,
			})
			rec.conductor_id._compute_ahorro()

class AjusteAhorroDetalle(models.Model):
	_name = 'fundetaxcol.ajuste.ahorro.detalle'

	ajuste_id = fields.Many2one('fundetaxcol.ajuste.ahorro', required=True, ondelete='cascade')
	conductor_id = fields.Many2one('res.partner', string='Conductor', required=True)
	valor = fields.Float(string='Valor')

#*************************************Ajuste ahorros*************************************#