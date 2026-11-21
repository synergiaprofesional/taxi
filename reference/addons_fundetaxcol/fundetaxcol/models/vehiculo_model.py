# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta
import logging, string
_logger = logging.getLogger(__name__)

class Vehiculo(models.Model):
    _name = 'fundetaxcol.vehiculo'
    _description = 'Vehiculo'

    TipoCombustible = [('gas','Gas'),('gasolina','Gasolina'),('acpm','ACPM')]
    Tipo = [('automovil','Automovil'),('camioneta','Camioneta')]

    name = fields.Char(string='Placa', required=True,)
    marca_vehiculo_id = fields.Many2one(
        'fundetaxcol.vehiculo.marca',
        string='Marca',
    )
    modelo = fields.Char(string='Modelo',)
    cilindraje = fields.Float(string='Cilindraje',)
    tipo = fields.Selection(Tipo, string='Tipo', default='automovil')
    tipo_combustible = fields.Selection(TipoCombustible, string='Combustible', default='gasolina')
    propietario_id = fields.Many2one(
        'res.partner',
        string='Propietario',
        domain=[('propietario','=',True)]
    )
    ingreso = fields.Integer(string='Ingresos en el mes', compute='_get_ingresos', store=True,)
    conductor_ids = fields.One2many(
        'fundetaxcol.vehiculo.partner',
        'vehiculo_id',
        string='Conductores',
    )
    pago_ids = fields.One2many(
        'fundetaxcol.pago',
        'vehiculo_id',
        string='Pagos',
    )
    turno_ids = fields.One2many(
        'fundetaxcol.turno',
        'vehiculo_id',
        string='Despachos',
    )

    pago_count = fields.Integer(string='Pagos', compute='_compute_counts')
    turno_count = fields.Integer(string='Despachos', compute='_compute_counts')

    def _compute_counts(self):
        Pago = self.env['fundetaxcol.pago']
        Turno = self.env['fundetaxcol.turno']
        for rec in self:
            rec.pago_count = Pago.search_count([('vehiculo_id', '=', rec.id)])
            rec.turno_count = Turno.search_count([('vehiculo_id', '=', rec.id)])

    def action_view_pagos(self):
        self.ensure_one()
        return {
            'name': 'Pagos de Vehículo (%s)' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'fundetaxcol.pago',
            'view_mode': 'tree,form',
            'domain': [('vehiculo_id', '=', self.id)],
            'context': {'default_vehiculo_id': self.id},
        }

    def action_view_despachos(self):
        self.ensure_one()
        return {
            'name': 'Despachos de Vehículo (%s)' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'fundetaxcol.turno',
            'view_mode': 'tree,form',
            'domain': [('vehiculo_id', '=', self.id)],
            'context': {'default_vehiculo_id': self.id},
        }


    #ingresos = fields.Integer(string='Ingresos', compute='_get_ingresos')
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('vehiculo_name_uniq',
         'UNIQUE (name)',
         'La placa digitada ya existe!')]

    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) != 6:
            raise exceptions.ValidationError('La placa debe contener 6 caracteres')
        letras = self.name[0:3]
        for l in letras:
            if not l in string.ascii_letters:
                raise exceptions.ValidationError('El formato de la placa no es apropiado')
        numeros = self.name[3:]
        try:
            int(numeros)
        except Exception as e:
            raise exceptions.ValidationError('El formato de la placa no es apropiado')

    @api.multi
    def action_calc_ing(self):
        for rec in self:
            rec.obtener_ingresos()

    def obtener_ingresos(self):
        pago_ids = self.pago_ids.sorted("fecha", reverse=True).filtered(lambda x: self.es_pago_de_este_mes(x))
        concepto_ids = pago_ids.mapped("concepto_ids").filtered(lambda x: x.concepto_id.clasificacion == 'ingreso' or x.concepto_id.clasificacion == 'abono_cr_ingreso')
        self.ingreso = sum(concepto_ids.mapped('cantidad'))

    def es_pago_de_este_mes(self, pago):
        App = self.env['fundetaxcol.fundetaxcol']
        fecha = datetime.strptime(App.get_fecha_actual(pago.fecha), '%Y-%m-%d %H:%M:%S')
        year = datetime.now().year
        month = datetime.now().month
        return fecha.year == year and fecha.month == month

    @api.multi
    @api.depends("pago_ids")
    def _get_ingresos(self):
        for rec in self:
            rec.obtener_ingresos()

    #@api.one
    #@api.depends('pago_ids')
    #def _get_ingreso(self):
    #	ingresos = 0
    #	rango_fecha = self.get_periodo()
        #_ingresos = []
    #	App = self.env['fundetaxcol.fundetaxcol']
    #	for pago in self.pago_ids:
    #		_fecha_pago_local = App.get_fecha_actual(pago.fecha)
    #		fecha_pago = str(datetime.strptime(_fecha_pago_local.split(' ')[0], '%Y-%m-%d')).split(' ')[0]
    #		if fecha_pago in rango_fecha:
    #			concepto_pagos = pago.concepto_ids.filtered(lambda x: x.concepto_id.id == pago.concepto_tarifa_base_id.id)
    #			for cp in concepto_pagos:
    #				ingresos += cp.cantidad

    #			ICPSudo = self.env['ir.config_parameter'].sudo()
    #			plantilla_ingreso_id = ICPSudo.get_param('fundetaxcol.plantilla_ingreso_id')
    #			if plantilla_ingreso_id:
    #				plantilla_ingreso_id = self.env['fundetaxcol.concepto.conductor'].browse(int(plantilla_ingreso_id))
    #				if plantilla_ingreso_id.exists():
    #					concepto_ingreso_ids = plantilla_ingreso_id.concepto_ids.mapped('id')
    #					concepto_pagos = pago.concepto_ids.filtered(lambda x: x.concepto_id.id in concepto_ingreso_ids)
    #					for cp in concepto_pagos:
    #						ingresos += cp.cantidad

        #		_ingresos.append(fecha_pago)
    #	self.ingreso = ingresos

    def get_periodo(self, fecha=False):
        _fecha = fecha or fields.Datetime.now()
        dia_inicial = new_fecha = self.primer_dia_mes(_fecha)
        dia_final = self.ultimo_dia_mes(_fecha)
        rango_fecha = []
        while new_fecha != dia_final:
            rango_fecha.append(str(new_fecha).split(' ')[0])
            new_fecha += timedelta(days=1)
        return rango_fecha

    def get_fecha(self, fecha):
        fecha = str(fecha).split(' ')[0]
        year = str(datetime.strptime(fecha, '%Y-%m-%d').year)
        mes = str(datetime.strptime(fecha, '%Y-%m-%d').month)
        dia = str(datetime.strptime(fecha, '%Y-%m-%d').day)
        return '-'.join([year,mes,dia])

    def primer_dia_mes(self, fecha):
        year = str(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').year)
        mes = str(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').month)
        fi = '-'.join([year,mes,'01'])
        return datetime.strptime(fi, '%Y-%m-%d')

    def ultimo_dia_mes(self, fecha):
        new_fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        mes = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').month
        while mes == new_fecha.month:
            new_fecha = datetime.strptime(self.get_fecha(new_fecha), '%Y-%m-%d') + timedelta(days=1)
        return new_fecha

    def get_primera_fecha(self, fecha):
        fecha = fecha.split(' ')[0]
        year = str(datetime.strptime(fecha, '%Y-%m-%d').year)
        mes = datetime.strptime(fecha, '%Y-%m-%d').month
        if mes < 10:
            mes = ''.join(['0',str(mes)])
        mes = str(mes)
        return '-'.join([year,mes,'01 00:00:00'])

    @api.model
    def create(self, values):
        new_rec = super(Vehiculo, self).create(values)
        new_rec.name = new_rec.name.upper()
        return new_rec


class Marca(models.Model):
    _name = 'fundetaxcol.vehiculo.marca'
    _description = 'Marca Vehiculo'

    name = fields.Char(string='Nombre', required=True,)

class VehiculoPartner(models.Model):
    _name = 'fundetaxcol.vehiculo.partner'
    _description = 'Vehiculo Conductor'
    _order = 'sequence'

    sequence = fields.Integer(string='Secuencia',)
    vehiculo_id = fields.Many2one(
        'fundetaxcol.vehiculo',
        string='Vehículo',
    )
    conductor_id = fields.Many2one(
        'res.partner',
        string='Conductor',
        domain=[('conductor','=',True),]
    )