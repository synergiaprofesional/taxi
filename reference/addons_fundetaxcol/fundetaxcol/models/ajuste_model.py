# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
import logging
_logger = logging.getLogger(__name__)

class Ajuste(models.Model):
	_name = 'fundetaxcol.ajuste'
	_description = 'Ajuste de sesion'

	NOTA = {
		'nueva_sesion': 'No existe una sesión con la fecha indicada, por tal motivo se creará para registrar los pagos',
		'sesion_existente': 'Advertencia: ya existe una sesión con la fecha indicada',
	}

	name = fields.Char(string='Nombre',)
	fecha = fields.Date(string='Fecha', default=fields.Date.today, required=True,)
	sesion_id = fields.Many2one(
		'fundetaxcol.sesion',
		string='Sesión',
	)
	bahia_id = fields.Many2one(
		'fundetaxcol.bahia',
		string='Bahía',
		required=True,
	)
	sesion_bahia_id = fields.Many2one(
		'fundetaxcol.sesion.bahia',
		string='Sesión bahía',
	)
	pago_ids = fields.One2many(
		'fundetaxcol.pago',
		'ajuste_id',
		string='Pagos',
	)
	transaccion_ids = fields.One2many(
		'fundetaxcol.transaccion',
		'ajuste_id',
		string='Transacciones',
	)
	secuencia_ajuste_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia ajuste para pagos',
		required=True,
	)
	secuencia_ajuste_transaccion_id = fields.Many2one(
		'fundetaxcol.secuencia.ticket',
		string='Secuencia ajuste para transacciones',
		required=True,
	)
	nota = fields.Text(string='Nota',)

	@api.onchange('fecha')
	def _onchange_fecha(self):
		self._onchange_bahia_id()

	@api.onchange('bahia_id')
	def _onchange_bahia_id(self):
		if self.fecha and self.bahia_id:
			self.sesion_id = self._get_sesion()
			if not self.sesion_id:
				self.sesion_id = self._crear_sesion()
				self.nota = self.NOTA['nueva_sesion']
			else:
				self.nota = self.NOTA['sesion_existente']
			self.sesion_bahia_id = self._get_sesion_bahia()
		self._onchange_pago_ids()
		self._onchange_transaccion_ids()

	@api.onchange('pago_ids')
	def _onchange_pago_ids(self):
		for pago in self.pago_ids:
			#pago.secuencia_ticket_id = self.secuencia_ajuste_id
			pago.bahia_id = self.sesion_bahia_id

	@api.onchange('transaccion_ids')
	def _onchange_transaccion_ids(self):
		for transaccion in self.transaccion_ids:
			#transaccion.secuencia_transaccion_id = self.secuencia_ajuste_transaccion_id
			transaccion.bahia_id = self.sesion_bahia_id

	#Tener en cuenta multicompañia
	def _get_app(self):
		return self.env['fundetaxcol.fundetaxcol'].search([], limit=1).id

	def _get_sesion_bahia(self):
		if self.sesion_id.pendiente:
			self.sesion_id.bahia_ids = self.sesion_id.sesion_bahia_ids = False
			self.sesion_id.bahia_ids |= self.bahia_id
			for bahia in self.sesion_id.bahia_ids:
				self.sesion_id.sesion_bahia_ids |= self.env['fundetaxcol.sesion.bahia'].create({
					'name': ' '.join([self.bahia_id.name, self.sesion_id.name]),
					'state': 'cerrado',
					'bahia_id': bahia.id,
					'sesion_id': self.sesion_id.id,
				})
		for sesion_bahia in self.sesion_id.sesion_bahia_ids:
			if sesion_bahia.bahia_id.id == self.bahia_id.id:
				return sesion_bahia.id
		return False

	def _verificar_sesiones(self):
		domain=[('state','=','cerrado'), ('pendiente','=',True), ('ajuste_id','=',False)]
		sesiones = self.env['fundetaxcol.sesion'].search(domain)
		for sesion in sesiones:
			sesion.unlink()

	def _update_sesion(self):
		if self.sesion_id.pendiente:
			self.sesion_id.ajuste_id = self.id
			self.nota = self.NOTA['nueva_sesion']
		else:
			self.nota = self.NOTA['sesion_existente']
		self._verificar_sesiones()

	def _crear_sesion(self):
		sesion = {
			'name': 'Sesión [%s]' %(self.fecha),
			'fecha_apertura': self.fecha,
			'fecha_cierre': self.fecha,
			'state': 'cerrado',
			'fundetaxcol_id': self._get_app(),
			'pendiente': True,
		}
		return self.env['fundetaxcol.sesion'].create(sesion)

	def _get_sesion(self):
		for sesion in self.env['fundetaxcol.sesion'].search([]):
			if sesion.fecha == self.fecha:
				return sesion
		return False

	def _validar_registro(self):
		if len(self.pago_ids) == 0:
			if len(self.transaccion_ids) == 0:
				raise exceptions.ValidationError('No se puede crear el ajuste sin pagos o transacciones')

	def _set_nombre(self):
		self.name = 'Ajuste [%s]' %(self.fecha)

	@api.model
	def create(self, values):
		new_ajuste = super(Ajuste, self).create(values)
		new_ajuste._set_nombre()
		new_ajuste._validar_registro()
		new_ajuste._update_sesion()
		return new_ajuste

	@api.multi
	def unlink(self):
		for ajuste in self:
			sesion = ajuste.sesion_id
			if sesion.pendiente and sesion.fecha_apertura == sesion.fecha_cierre:
				sesion.unlink()
		return super(Ajuste, self).unlink()