# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

CLASIFICACION = [('ingreso','Ingreso'), ('ahorro','Ahorro'), ('transaccion','Transacción')]

class WizardUtilidadConcepto(models.TransientModel):
	_name = 'wizard.ft_cpto_clasificacion'

	clasificacion = fields.Selection(CLASIFICACION, 'Clasificación', default='ingreso', required=True)
	concepto_ids = fields.Many2many("fundetaxcol.concepto", string="Conceptos")

	@api.multi
	def btn_aceptar(self):
		domain = [('id','in',self.concepto_ids.ids)]
		self.env['fundetaxcol.concepto'].search(domain).write({'clasificacion': self.clasificacion})
		return True
