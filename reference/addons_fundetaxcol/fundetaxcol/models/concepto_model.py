# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

class Concepto(models.Model):
    _name = 'fundetaxcol.concepto'
    _description = 'Concepto'

    TIPO_CONCEPTO = [('valor_fijo','Valor fijo'),('porcentaje','Porcentaje'),('valor_variable','Valor variable')]
    AFECTACION = [('db','Débito'), ('cr','Crédito')]
    CLASIFICACION = [
        ('ingreso','Ingreso'), 
        ('ahorro','Ahorro'), 
        ('transaccion','Transacción'),
        ('cr_ingreso','Crédito Ingreso'),
        ('abono_cr_ingreso','Abono Crédito Ingreso'),
        ('cr_prestamo','Crédito Préstamo'),
        ('abono_cr_prestamo','Abono Crédito Préstamo')
    ]

    name = fields.Char('Nombre', required=True)
    tipo = fields.Selection(TIPO_CONCEPTO, 'Tipo', default='valor_fijo')
    valor = fields.Float('Valor')
    afectacion = fields.Selection(AFECTACION, 'Afectación', default='db')
    clasificacion = fields.Selection(CLASIFICACION, 'Clasificación', default='ingreso', required=True)
    template_concepto_id = fields.Many2one(
        'fundetaxcol.concepto.conductor',
        string='Plantilla concepto conductor',
    )
    #is_transaccion = fields.Boolean(string='Concepto de Transacción',)

    @api.onchange('tipo')
    def _onchange_tipo(self):
    	self.valor = 0

    @api.model
    def concepto_ahorro_ids(self):
        return self.search([('clasificacion','=','ahorro')]).ids

class TemplateConcepto(models.Model):
    _name = 'fundetaxcol.concepto.conductor'
    _description = 'Concepto por conductor'

    name = fields.Char(string='Nombre', required=True,)
    concepto_ids = fields.One2many(
        'fundetaxcol.concepto',
        'template_concepto_id',
        string='Conceptos',
        required=True,
        #domain=[('is_transaccion','=',False), ]
    )

    @api.constrains("concepto_ids")
    def verificar_concepto_ingreso(self):
        ingreso = len(self.concepto_ids.filtered(lambda x: x.clasificacion == 'ingreso'))
        if ingreso != 1:
            raise exceptions.ValidationError("Debe seleccionar 1 concepto de ingreso")

    #def verificar_plantilla_ahorro(self):
    #    app = self.env['fundetaxcol.fundetaxcol']
    #    param = app.get_configuracion('fundetaxcol.plantilla_ahorro_id')
    #    if param:
    #        if int(param) == self.id:
    #            raise exceptions.ValidationError('No se puede modificar o eliminar esta plantilla porque está configurada como Plantilla de Ahorros')

    #@api.model
    #def create(self, values):
    #    new_rec = super(TemplateConcepto, self).create(values)
    #    return new_rec

    #@api.multi
    #def write(self, values):
    #    for rec in self:
    #        rec.verificar_plantilla_ahorro()
    #    return super(TemplateConcepto, self).write(values)

    #@api.multi
    #def unlink(self):
    #    for rec in self:
    #        rec.verificar_plantilla_ahorro()
    #    return super(TemplateConcepto, self).unlink()
