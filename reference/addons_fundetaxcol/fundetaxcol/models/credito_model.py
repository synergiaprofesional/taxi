# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)


class ConductorCreditoIngreso(models.Model):
    _name = 'res.partner.cr_ingreso'

    name = fields.Char(string="Etiqueta", readonly=True)
    pago_id = fields.Many2one('fundetaxcol.pago', string='Pago')
    partner_id = fields.Many2one(
        'res.partner', string="Conductor", required=True)
    concepto_id = fields.Many2one(
        'fundetaxcol.concepto', string="Concepto", required=True)
    cantidad = fields.Integer(string='Cant.')
    valor = fields.Float(string="Valor")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal")
    tipo = fields.Char(string="Tipo")

    @api.multi
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.cantidad * rec.valor


class ConductorCreditoPrestamo(models.Model):
    _name = 'res.partner.cr_prestamo'

    name = fields.Char(string="Etiqueta", readonly=True)
    pago_id = fields.Many2one('fundetaxcol.pago', string='Pago')
    partner_id = fields.Many2one(
        'res.partner', string="Conductor", required=True)
    concepto_id = fields.Many2one(
        'fundetaxcol.concepto', string="Concepto", required=True)
    cantidad = fields.Integer(string='Cant.')
    valor = fields.Float(string="Valor")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal")
    tipo = fields.Char(string="Tipo")

    @api.multi
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.cantidad * rec.valor


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credito_ids = fields.One2many('res.partner.cr_ingreso', 'partner_id')
    prestamo_ids = fields.One2many('res.partner.cr_prestamo', 'partner_id')
    num_credito = fields.Integer(string="Número créditos", compute='_compute_total_credito', store=True)
    total_credito = fields.Float(string="Total crédito", compute='_compute_total_credito', store=True)
    total_prestamo = fields.Float(string="Total préstamo", compute='_compute_total_prestamo', store=True)

    @api.multi
    @api.depends('credito_ids')
    def _compute_total_credito(self):
        for rec in self:
            cr_ingresos = rec.credito_ids.filtered(lambda x: x.tipo == 'cr_ingreso')
            abono_cr_ingresos = rec.credito_ids.filtered(lambda x: x.tipo == 'abono_cr_ingreso')

            creditos = cr_ingresos.mapped(lambda x: x.subtotal)
            abonos = abono_cr_ingresos.mapped(lambda x: x.subtotal)

            num_creditos = cr_ingresos.mapped(lambda x: x.cantidad)
            num_abonos = abono_cr_ingresos.mapped(lambda x: x.cantidad)
            
            rec.total_credito = sum(creditos) - sum(abonos)
            rec.num_credito = sum(num_creditos) - sum(num_abonos)

    @api.multi
    @api.depends('prestamo_ids')
    def _compute_total_prestamo(self):
        for rec in self:
            cr_prestamos = rec.prestamo_ids.filtered(lambda x: x.tipo == 'cr_prestamo')
            abono_cr_prestamos = rec.prestamo_ids.filtered(lambda x: x.tipo == 'abono_cr_prestamo')

            prestamos = cr_prestamos.mapped(lambda x: x.subtotal)
            abonos = abono_cr_prestamos.mapped(lambda x: x.subtotal)
            
            rec.total_prestamo = sum(prestamos) - sum(abonos)


class Vehiculo(models.Model):
    _inherit = 'fundetaxcol.vehiculo'

    @api.multi
    @api.depends("pago_ids")
    def _get_ingresos(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        credito_cuenta_ingreso = ICPSudo.get_param('fundetaxcol.credito.ingreso')
        for rec in self:
            pago_ids = rec.pago_ids.sorted("fecha", reverse=True).filtered(lambda x: self.es_pago_de_este_mes(x))
            if credito_cuenta_ingreso:
                concepto_ids = pago_ids.mapped("concepto_ids").filtered(lambda x: 
                    x.concepto_id.clasificacion == 'ingreso' or x.concepto_id.clasificacion == 'cr_ingreso'
                )
            else:
                concepto_ids = pago_ids.mapped("concepto_ids").filtered(lambda x: 
                    x.concepto_id.clasificacion == 'ingreso'
                )
            rec.ingreso = sum(concepto_ids.mapped('cantidad'))


class Pago(models.Model):
    _inherit = 'fundetaxcol.pago'

    tiene_cr_ingreso = fields.Boolean(compute='_compute_tiene_credito', store=True)
    tiene_cr_prestamo = fields.Boolean(compute='_compute_tiene_credito', store=True)
    saldo_cr_ingreso = fields.Float(string="Saldo Ingreso", compute='_compute_tiene_credito', store=True)
    saldo_cr_prestamo = fields.Float(string="Saldo Préstamo", compute='_compute_tiene_credito', store=True)

    @api.constrains("conductor_id")
    def constrains_conductor_id(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        num_max_credito = int(ICPSudo.get_param('fundetaxcol.credito.maximo') or 0)
        no_ingreso_antes_de_credito = ICPSudo.get_param('fundetaxcol.no.credito.ingreso')
        if num_max_credito > 0:
            ingresos = len(self.concepto_ids.filtered(lambda x: x.concepto_id.clasificacion == 'ingreso'))
            if self.conductor_id.num_credito > 0 and ingresos != 0 and no_ingreso_antes_de_credito:
                raise exceptions.ValidationError('Este conductor debe ponerse al día con el crédito de ingreso')
            if self.conductor_id.num_credito > num_max_credito:
                raise exceptions.ValidationError('Este conductor no tiene cupo para crédito')

    @api.multi
    @api.depends('conductor_id')
    def _compute_tiene_credito(self):
        for rec in self:
            rec.tiene_cr_ingreso = False
            rec.tiene_cr_prestamo = False
            if rec.conductor_id:
                total_cr_ingreso = sum(self.env['res.partner.cr_ingreso'].\
                    search([('partner_id','=', rec.conductor_id.id),('tipo','=','cr_ingreso')]).\
                    mapped(lambda x: x.cantidad * x.valor))
                total_abono_cr_ingreso = sum(self.env['res.partner.cr_ingreso'].\
                    search([('partner_id','=', rec.conductor_id.id),('tipo','=','abono_cr_ingreso')]).\
                    mapped(lambda x: x.cantidad * x.valor))
                rec.saldo_cr_ingreso = total_cr_ingreso - total_abono_cr_ingreso
                total_cr_prestamo = sum(self.env['res.partner.cr_prestamo'].\
                    search([('partner_id','=', rec.conductor_id.id),('tipo','=','cr_prestamo')]).\
                    mapped(lambda x: x.cantidad * x.valor))
                total_abono_cr_prestamo = sum(self.env['res.partner.cr_prestamo'].\
                    search([('partner_id','=', rec.conductor_id.id),('tipo','=','abono_cr_prestamo')]).\
                    mapped(lambda x: x.cantidad * x.valor))
                rec.saldo_cr_prestamo = total_cr_prestamo - total_abono_cr_prestamo
                rec.tiene_cr_ingreso = rec.saldo_cr_ingreso > 0
                rec.tiene_cr_prestamo = rec.saldo_cr_prestamo > 0


class PagoConcepto(models.Model):
    _inherit = 'fundetaxcol.pago.concepto'

    def crear_credito(self, modelo, cantidad=0, valor=0):
        self.env[modelo].create({
            'name': self.concepto_id.name,
            'pago_id': self.pago_id.id,
            'partner_id': self.pago_id.conductor_id.id,
            'concepto_id': self.concepto_id.id,
            'cantidad': cantidad or self.cantidad,
            'valor': valor or self.valor,
            'tipo': self.concepto_id.clasificacion
        })

    def concepto_credito(self):
        return self.concepto_id.clasificacion == 'cr_ingreso' \
            or self.concepto_id.clasificacion == 'abono_cr_ingreso' \
            or self.concepto_id.clasificacion == 'cr_prestamo' \
            or self.concepto_id.clasificacion == 'abono_cr_prestamo'

    @api.model
    def create(self, values):
        rec = super(PagoConcepto, self).create(values)
        if rec.concepto_credito:
            if rec.concepto_id.clasificacion == 'cr_ingreso' or rec.concepto_id.clasificacion == 'abono_cr_ingreso':
                rec.crear_credito('res.partner.cr_ingreso')
            elif rec.concepto_id.clasificacion == 'cr_prestamo' or rec.concepto_id.clasificacion == 'abono_cr_prestamo':
                rec.crear_credito('res.partner.cr_prestamo')
        return rec

    @api.multi
    def write(self, values):
        if self.concepto_credito:
            cantidad = values.get('cantidad', False)
            valor = values.get('valor', False)
            if cantidad: cantidad -= self.cantidad
            else: cantidad = self.cantidad
            if valor: valor -= self.valor
            else: valor = self.valor
            if self.concepto_id.clasificacion == 'cr_ingreso' or self.concepto_id.clasificacion == 'abono_cr_ingreso':
                self.crear_credito('res.partner.cr_ingreso', cantidad=cantidad, valor=valor)
            elif self.concepto_id.clasificacion == 'cr_prestamo' or self.concepto_id.clasificacion == 'abono_cr_prestamo':
                self.crear_credito('res.partner.cr_prestamo', cantidad=cantidad, valor=valor)
        return super(PagoConcepto, self).write(values)

    @api.multi
    def unlink(self):
        if self.concepto_credito:
            if self.concepto_id.clasificacion == 'cr_ingreso' or self.concepto_id.clasificacion == 'abono_cr_ingreso':
                self.crear_credito('res.partner.cr_ingreso', cantidad=-self.cantidad)
            elif self.concepto_id.clasificacion == 'cr_prestamo' or self.concepto_id.clasificacion == 'abono_cr_prestamo':
                self.crear_credito('res.partner.cr_prestamo', cantidad=-self.cantidad)
        return super(PagoConcepto, self).unlink()
