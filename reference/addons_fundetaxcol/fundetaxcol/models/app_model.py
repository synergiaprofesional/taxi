# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
import pytz
from datetime import datetime, timedelta

from babel import numbers

import logging
_logger = logging.getLogger(__name__)


class App(models.Model):
    _name = 'fundetaxcol.fundetaxcol'
    _description = 'App fundetaxcol'

    name = fields.Char(string='Nombre', required=True,)
    company_id = fields.Many2one('res.company', string='Compañía',
                                 required=True, default=lambda self: self.env.user.company_id)
    sesion_id = fields.Many2one(
        'fundetaxcol.sesion',
        string='Sesión actual',
    )
    descripcion = fields.Char(string='Descripción', related='sesion_id.name')
    sesion_ids = fields.One2many(
        'fundetaxcol.sesion',
        'fundetaxcol_id',
        string='Sesiones',
    )

    def get_configuracion(self, name):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        param = ICPSudo.get_param(name)
        return param

    @api.multi
    def load_bahias(self):
        return {
            'name': 'Bahías',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban',
            'res_model': 'fundetaxcol.bahia',
            'target': 'current',
            'domain': [['sesion_ids', 'in', self.sesion_id.id]]
        }

    @api.multi
    def abrir_sesion(self):
        sesion_view_form = self.env.ref('fundetaxcol.sesion_form')
        return {
            'name': 'Sesión',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.sesion',
            'views': [(sesion_view_form.id, 'form')],
            'target': 'current',
            'context': {'default_fundetaxcol_id': self.id}
        }

    @api.multi
    def cerrar_sesion(self):
        sesion_view_form = self.env.ref('fundetaxcol.sesion_form')
        return {
            'name': 'Cerrar Sesión',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fundetaxcol.sesion',
            'views': [(sesion_view_form.id, 'form')],
            'res_id': self.sesion_id.id,
            'target': 'current',
        }

    def get_fecha_actual(self, fecha=False):
        fecha = fecha or fields.Datetime.now()
        diff = datetime.now(pytz.timezone(
            self.env.user.tz or 'UTC')).utcoffset()
        return str(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S') + diff)

    def get_fecha(self, fecha):
        fecha = str(fecha).split(' ')[0]
        year = str(datetime.strptime(fecha, '%Y-%m-%d').year)
        mes = str(datetime.strptime(fecha, '%Y-%m-%d').month)
        dia = str(datetime.strptime(fecha, '%Y-%m-%d').day)
        return '%s-%s-%s' % (year, mes, dia)

    def primer_dia_mes(self, fecha):
        year = str(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').year)
        mes = str(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').month)
        fi = '%s-%s-%s' % (year, mes, '01')
        return datetime.strptime(fi, '%Y-%m-%d')

    def ultimo_dia_mes(self, fecha):
        new_fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        mes = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').month
        while mes == new_fecha.month:
            new_fecha = datetime.strptime(self.get_fecha(
                new_fecha), '%Y-%m-%d') + timedelta(days=1)
        return new_fecha

    def get_periodo(self, fecha=False):
        _fecha = fecha or fields.Datetime.now()
        dia_inicial = new_fecha = self.primer_dia_mes(_fecha)
        dia_final = self.ultimo_dia_mes(_fecha)
        rango_fecha = []
        while new_fecha != dia_final:
            rango_fecha.append(str(new_fecha).split(' ')[0])
            new_fecha += timedelta(days=1)
        return rango_fecha

    @api.model
    def get_format_currency(self, value):
        user_id = self.env.user
        locale = user_id.lang
        currency_id = user_id.company_id.currency_id
        formato = currency_id.name
        result = numbers.format_currency(value, formato, locale=locale)
        return result.replace(u'\xa0', u' ')

    def limpiar_db(self, borrar):
        Vehiculo = self.env['fundetaxcol.vehiculo']
        vehiculos = Vehiculo.search([], order='name')
        lista = []
        for v1 in vehiculos:
            domain = [('name', '=', v1.name)]
            query = Vehiculo.search(domain)
            if not query in lista and len(query) > 1:
                lista.append(query)
        for l in lista:
            for vehiculo in l:
                for v2 in l:
                    if vehiculo.id == v2.id:
                        continue
                    for pago in self.env['fundetaxcol.pago'].search([('vehiculo_id', '=', v2.id)]):
                        pago.vehiculo_id = vehiculo.id
                    for turno in self.env['fundetaxcol.turno'].search([('vehiculo_id', '=', v2.id)]):
                        turno.vehiculo_id = vehiculo.id
                    for vp in self.env['fundetaxcol.vehiculo.partner']:
                        vp.vehiculo_id = vehiculo.id
                    v2.unlink()
                break
        if borrar:
            vehiculos = Vehiculo.search([], order='name')
            para_borrar = []
            for vehiculo in vehiculos:
                if len(vehiculo.conductor_ids) == 0 and len(vehiculo.pago_ids) == 0 and len(vehiculo.turno_ids) == 0:
                    para_borrar.append(vehiculo)
                elif len(vehiculo.conductor_ids) != 0:
                    for conductor in vehiculo.conductor_ids:
                        conductor.conductor = True
            for vehiculo in para_borrar:
                vehiculo.unlink()
