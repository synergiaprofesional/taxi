# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

class ReporteTemperatura(models.TransientModel):
    _name = 'wizard.report.temperatura'

    fecha_inicio = fields.Date("Fecha inicio", default=fields.Date.today, required=True)
    fecha_fin = fields.Date("Fecha fin", default=fields.Date.today, required=True)
    conductor_ids = fields.Many2many('res.partner', string="Conductores")
    item_ids = fields.One2many('wizard.report.temperatura.item', 'parent_id')

    @api.multi
    def generate_report(self):
        fecha_inicio = '%s 00:00:00' % (self.fecha_inicio)
        fecha_fin = '%s 23:59:59' % (self.fecha_fin)
        domain = [
            ('create_date', '>=', fecha_inicio),
            ('create_date', '<=', fecha_fin),
        ]
        if self.conductor_ids:
            domain.append(('conductor_id', 'in', self.conductor_ids.ids))
        temperaturas = self.env['fundetaxcol.temperatura'].search(domain)
        TempItem = self.env['wizard.report.temperatura.item']
        TempItem.search([]).unlink()
        for temperatura in temperaturas:
            TempItem.create({
                'parent_id': self.id,
                'temperatura_id': temperatura.id
            })
        return self.env.ref('fundetaxcol.menu_reporte_temperatura').report_action(self, data=None)

class ReporteTemperaturaItem(models.TransientModel):
    _name = 'wizard.report.temperatura.item'

    parent_id = fields.Many2one('wizard.report.temperatura', ondelete="cascade")
    temperatura_id = fields.Many2one('fundetaxcol.temperatura')

# ############################ Limpieza #######################################

class ReporteLimpieza(models.TransientModel):
    _name = 'wizard.report.limpieza'

    fecha_inicio = fields.Date("Fecha inicio", default=fields.Date.today, required=True)
    fecha_fin = fields.Date("Fecha fin", default=fields.Date.today, required=True)
    vehiculo_ids = fields.Many2many('fundetaxcol.vehiculo', string="Vehículos")
    item_ids = fields.One2many('wizard.report.limpieza.item', 'parent_id')

    @api.multi
    def generate_report(self):
        fecha_inicio = '%s 00:00:00' % (self.fecha_inicio)
        fecha_fin = '%s 23:59:59' % (self.fecha_fin)
        domain = [
            ('create_date', '>=', fecha_inicio),
            ('create_date', '<=', fecha_fin),
        ]
        if self.vehiculo_ids:
            domain.append(('vehiculo_id', 'in', self.vehiculo_ids.ids))
        limpieza_ids = self.env['fundetaxcol.limpieza'].search(domain)
        LimpiezaItem = self.env['wizard.report.limpieza.item']
        LimpiezaItem.search([]).unlink()
        for limpieza in limpieza_ids:
            LimpiezaItem.create({
                'parent_id': self.id,
                'limpieza_id': limpieza.id
            })
        return self.env.ref('fundetaxcol.menu_reporte_limpieza').report_action(self, data=None)

class ReporteLimpiezaItem(models.TransientModel):
    _name = 'wizard.report.limpieza.item'

    parent_id = fields.Many2one('wizard.report.limpieza', ondelete="cascade")
    limpieza_id = fields.Many2one('fundetaxcol.limpieza')
