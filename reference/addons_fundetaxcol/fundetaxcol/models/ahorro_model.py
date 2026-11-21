# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

import logging
_logger = logging.getLogger(__name__)


class PagoAhorro(models.Model):
	_name = 'fundetaxcol.ahorro'

	name = fields.Char(string='Nombre')
	company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.user.company_id)
	bahia_id = fields.Many2one('fundetaxcol.sesion.bahia', string='Bahía', ondelete='cascade', required=True,)
	conductor_id = fields.Many2one('res.partner', string='Conductor', required=True,)
	conductor_ids = fields.Many2many('res.partner', string='Filtro conductores', compute='_compute_partner_to_exclude')
	concepto_detalle_ids = fields.One2many('fundetaxcol.ahorro.detalle','ahorro_id',string='Conceptos',)
	valor = fields.Float('Valor', compute='_get_valor', store=True)

	@api.onchange('conductor_id')
	def _onchange_conductor_id(self):
		for rec in self:
			rec._compute_partner_to_exclude()

	def _compute_partner_to_exclude(self):
		for rec in self:
			user_ids = self.env['res.users'].search([]).mapped('partner_id').ids
			rec.conductor_ids = self.env['res.partner'].browse(user_ids)

			ICPSudo = self.env['ir.config_parameter'].sudo()
			conductor_anonimo_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id')
			if conductor_anonimo_id:
				rec.conductor_ids |= self.env['res.partner'].browse(int(conductor_anonimo_id))

	@api.depends('concepto_detalle_ids')
	def _get_valor(self):
		for rec in self:
			rec.valor = sum(rec.concepto_detalle_ids.mapped('valor'))

	def get_conductor(self, id):
		return self.env['res.partner'].browse(id).name

	@api.model
	def create(self, values):
		values['name'] = 'AHORRO [%s] [%s]' % (self.get_conductor(values.get('conductor_id', False)), fields.Datetime.now())
		new_rec = super(PagoAhorro, self).create(values)
		return new_rec

	def go_to_bahias(self):
		return {
			'name': 'Bahías',
			'type': 'ir.actions.act_window',
			'view_mode': 'kanban',
			'res_model': 'fundetaxcol.bahia',
			'target': 'main',
			'domain': [['sesion_ids','in',self.bahia_id.sesion_id.id]]
		}

	def get_data(self):
		_conceptos = []
		for concepto in self.concepto_detalle_ids:
			_conceptos.append({
				'name': concepto.concepto_id.name,
				'valor': concepto.valor,
			})
		return {
			'fecha': self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.create_date),
			'user': self.create_uid.name,
			'conductor': self.conductor_id.name,
			'company': {
				'name': self.company_id.name,
				'phone': self.company_id.phone,
				'email': self.company_id.email,
				'website': self.company_id.website,
				'report_footer': self.company_id.report_footer
			},
			'conceptos': _conceptos,
			'valor': self.valor,
			'ahorro_ids': self.conductor_id.get_ahorro(),
			'ahorro': self.conductor_id.ahorro,
		}

	@api.multi
	def print_pago(self):
		url = "/print/ahorro?qcontext=%s" % (self.get_data())
		self.env['bus.bus'].sendone((self._cr.dbname, 'fundetaxcol.print_for_url'), url)
		return self.go_to_bahias()

class ConceptoAhorro(models.Model):
	_name = 'fundetaxcol.ahorro.detalle'

	ahorro_id = fields.Many2one('fundetaxcol.ahorro', 'Ahorro', ondelete='cascade')
	concepto_id = fields.Many2one('fundetaxcol.concepto', 'Concepto', required=True)
	concepto_ids = fields.Many2many('fundetaxcol.concepto', string='Filtro Conceptos', compute='_compute_concepto_to_exclude')
	valor = fields.Float('Valor')
	pago_concepto_ahorro_id = fields.Many2one('fundetaxcol.pago.concepto.ahorro', string='Ahorro',)

	acumulado = fields.Float(string="Acumulado", compute="_compute_acumulado", store=True)

	@api.depends('concepto_id')
	def _compute_acumulado(self):
		for rec in self:
			concepto = rec.ahorro_id.conductor_id.pago_ahorro_ids.filtered(lambda x: x.concepto_id.id == rec.concepto_id.id)
			rec.acumulado = sum(concepto.mapped(lambda x: x.cantidad * x.valor))
			if rec.id:
				rec.acumulado -= rec.valor

	def _compute_concepto_to_exclude(self):
		for rec in self:
			Pago = self.env['fundetaxcol.pago']
			concepto_ahorro_ids = Pago.get_conceptos_ahorro(ajuste=False)
			rec.concepto_ids = self.env['fundetaxcol.concepto'].browse(concepto_ahorro_ids)

	@api.onchange('concepto_id')
	def _onchange_concepto_id(self):
		for rec in self:
			rec._compute_concepto_to_exclude()

	def crear_ahorro(self):
		self.pago_concepto_ahorro_id = self.env['fundetaxcol.pago.concepto.ahorro'].create({
				'conductor_id': self.ahorro_id.conductor_id.id,
				'concepto_id': self.concepto_id.id,
				'cantidad': 1,
				'valor': self.valor,
			})
		self.pago_concepto_ahorro_id.conductor_id._compute_ahorro()

	def modificar_ahorro(self, values):
		if self.pago_concepto_ahorro_id:
			self.pago_concepto_ahorro_id.valor = values.get('valor', False) or self.valor
			self.pago_concepto_ahorro_id.conductor_id._compute_ahorro()

	def eliminar_ahorro(self):
		self.pago_concepto_ahorro_id.unlink()
		self.pago_concepto_ahorro_id.conductor_id._compute_ahorro()

	@api.model
	def create(self, values):
		new_rec = super(ConceptoAhorro, self).create(values)
		new_rec.crear_ahorro()
		return new_rec

	@api.multi
	def write(self, values):
		for rec in self:
			rec.modificar_ahorro(values)
		return super(ConceptoAhorro, self).write(values)

	@api.multi
	def unlink(self):
		for rec in self:
			rec.eliminar_ahorro()
		return super(ConceptoAhorro, self).unlink()