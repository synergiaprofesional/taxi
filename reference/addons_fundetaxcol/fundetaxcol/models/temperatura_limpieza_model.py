# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

class Temperatura(models.Model):
    _name = 'fundetaxcol.temperatura'

    temperatura = fields.Integer(string="Temperatura")
    conductor_id = fields.Many2one('res.partner', string="Conductor")
    pago_id = fields.Many2one('fundetaxcol.pago', string="Pago", ondelete="cascade")

class Limpieza(models.Model):
    _name = 'fundetaxcol.limpieza'
    _order = 'id desc'

    vehiculo_id = fields.Many2one('fundetaxcol.vehiculo', string="Vehículo")
    pago_id = fields.Many2one('fundetaxcol.pago', string="Pago", ondelete="cascade")

class Pago(models.Model):
    _inherit = 'fundetaxcol.pago'

    temperatura = fields.Integer(string="Temperatura")
    limpieza = fields.Boolean(string="Limpieza")

    def obtener_limpieza(self):
        Limpieza = self.env['fundetaxcol.limpieza']
        limpieza = Limpieza.search([('pago_id','=',self.id)], limit=1)
        if not limpieza:
            domain = [('vehiculo_id','=',self.vehiculo_id.id)]
            limpieza = Limpieza.search(domain, limit=1)
        if limpieza:
            return limpieza.create_date
        return False

    def registro_temperatura_y_limpieza(self):
        self._registro_temperatura()
        self._registro_limpieza()
    
    def _registro_temperatura(self):
        Temperatura = self.env['fundetaxcol.temperatura']
        temp = Temperatura.search([('pago_id','=',self.id)], limit=1)
        if temp:
            if not self.temperatura:
                temp.unlink()
            else:
                temp.temperatura = self.temperatura
        else:
            if self.temperatura:
                Temperatura.create({
                    'temperatura': self.temperatura,
                    'conductor_id': self.conductor_id.id,
                    'pago_id': self.id,
                })
    
    def _registro_limpieza(self):
        Limpieza = self.env['fundetaxcol.limpieza']
        limpieza = Limpieza.search([('pago_id','=',self.id)], limit=1)
        if limpieza:
            if not self.limpieza:
                limpieza.unlink()
        else:
            if self.limpieza:
                Limpieza.create({
                    'vehiculo_id': self.vehiculo_id.id,
                    'pago_id': self.id,
                })

    @api.model
    def create(self, values):
        record = super(Pago, self).create(values)
        record.registro_temperatura_y_limpieza()
        return record

    @api.multi
    def write(self, values):
        result = super(Pago, self).write(values)
        for rec in self:
            rec.registro_temperatura_y_limpieza()
        return result
