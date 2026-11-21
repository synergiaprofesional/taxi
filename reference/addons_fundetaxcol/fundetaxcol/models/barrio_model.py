# -*- coding: utf-8 -*-

from odoo import fields, models

class Barrio(models.Model):
    _name = 'fundetaxcol.barrio'
    _description = 'Barrio'

    name = fields.Char(string='Nombre', required=True,)
    sector_ids = fields.One2many(
        'fundetaxcol.barrio.sector',
        'barrio_id',
        string='Sectores',
    )

class Sector(models.Model):
    _name = 'fundetaxcol.barrio.sector'
    _description = 'Sector'

    name = fields.Char(string='Nombre', required=True,)
    barrio_id = fields.Many2one(
        'fundetaxcol.barrio',
        string='Barrio',
        ondelete='cascade',
    )
    categoria_id = fields.Many2one(
        'fundetaxcol.barrio.categoria.sector',
        string='Categoría',
    )
    icono = fields.Binary(string='Icono', related='categoria_id.image')

class CategoriaSector(models.Model):
    _name = 'fundetaxcol.barrio.categoria.sector'
    _description = 'Categoria Sector'

    name = fields.Char(string='Nombre', required=True,)
    image = fields.Binary(string='Icono',)