# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

class ReporteCartera(models.TransientModel):
    _name = 'wizard.report.cartera'

    item_ids = fields.One2many('wizard.report.cartera.item', 'parent_id')

    @api.multi
    def generate_report(self):
        Item = self.env['wizard.report.cartera.item']
        Item.search([]).unlink()
        return self.env.ref('fundetaxcol.menu_reporte_cartera').report_action(self, data=None)

class ReporteCarteraItem(models.TransientModel):
    _name = 'wizard.report.cartera.item'

    parent_id = fields.Many2one('wizard.report.cartera', ondelete="cascade")
