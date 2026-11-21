# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Tarifa(models.Model):
    _name = 'fundetaxcol.tarifa'
    _description = 'Tarifa'

    name = fields.Char(string='Nombre',)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.user.company_id)
    barrio_id = fields.Many2one(
        'fundetaxcol.barrio',
        string='Barrio',
        required=True,
    )
    sector_ids = fields.One2many(
        'fundetaxcol.tarifa.sector',
        'tarifa_id',
        string='Tarifas',
    )

    @api.onchange('barrio_id')
    def _onchange_barrio_id(self):
    	self.sector_ids = None
    	if self.barrio_id:
    		self.name = self.barrio_id.name
    		for sector in self.barrio_id.sector_ids:
    			self.sector_ids |= self.env['fundetaxcol.tarifa.sector'].new({
                    'name': ' / '.join([self.name,sector.name]),
    				'sector_id': sector.id,
    			})

    @api.model
    def create(self, values):
    	values['name'] = 'Tarifas ' + values.get('name')
    	return super(Tarifa, self).create(values)

class TarifaSector(models.Model):
    _name = 'fundetaxcol.tarifa.sector'
    _description = 'Tarifa por sector'

    name = fields.Char(string='Nombre',)
    sector_id = fields.Many2one(
        'fundetaxcol.barrio.sector',
        string='Sector',
    )
    icono = fields.Binary(string='Icono',related="sector_id.icono")
    valor = fields.Float(string='Valor',)
    valor_recargo = fields.Float(string='Valor Recargo',)
    nota = fields.Char(string='Nota',)
    tarifa_id = fields.Many2one(
        'fundetaxcol.tarifa',
        string='Tarifa',
        ondelete='cascade',
    )

    def set_name(self):
    	self.name = ' / '.join([self.tarifa_id.barrio_id.name,self.sector_id.name])

    @api.model
    def create(self, values):
    	new_rec = super(TarifaSector, self).create(values)
    	new_rec.set_name()
    	return new_rec