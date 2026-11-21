# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)

class Conductor(models.Model):
    _inherit = 'res.partner'
    _description = 'Conductor'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('identificacion', operator, name)] + args
        return super(Conductor, self).name_search(name, args=args, operator=operator, limit=limit)


    identificacion = fields.Char(string='Nº Identificación', required=True,)
    fecha_vinculacion = fields.Date(string='Fecha de Vinculación', default=fields.Date.today)
    numero_licencia = fields.Char(string='Número de Licencia')
    fecha_renovacion_licencia = fields.Date(string='Fecha Renovación')
    conductor = fields.Boolean(string='Conductor',)
    propietario = fields.Boolean(string='Conductor',)
    grupo_sanguineo = fields.Char(string='Grupo Sanguíneo',)
    template_concepto_id = fields.Many2one(
        'fundetaxcol.concepto.conductor',
        string='Plantilla concepto',
    )
    contacto_ids = fields.One2many(
        'res.partner.contacto',
        'res_partner_id',
        string='Contactos',
    )
    pago_ids = fields.One2many(comodel_name='fundetaxcol.pago', inverse_name='conductor_id', string='Pagos')
    ahorro = fields.Float(string='Ahorros', compute='_compute_ahorro', store=True)
    pago_ahorro_ids = fields.One2many(comodel_name='fundetaxcol.pago.concepto.ahorro', inverse_name='conductor_id', string='Ahorros')
    cr_ingreso_ids = fields.One2many('res.partner.cr_ingreso', 'partner_id')
    cr_prestamo_ids = fields.One2many('res.partner.cr_prestamo', 'partner_id')

    _sql_constraints = [
        ('conductor_identidad_uniq',
         'UNIQUE (identificacion)',
         'El número de identificación ya existe!')]

    @api.depends('pago_ahorro_ids')
    def _compute_ahorro(self):
        for rec in self:
            rec.ahorro = sum(line.subtotal for line in rec.pago_ahorro_ids)

    @api.multi
    def unlink(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        conductor_anonimo_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id')
        for rec in self:
            if conductor_anonimo_id:
                if rec.id == int(conductor_anonimo_id):
                    raise exceptions.ValidationError('No se puede eliminar %s porque está configurado como conductor Anónimo' % rec.name)
            if len(rec.pago_ids) != 0:
                raise exceptions.ValidationError('No se puede eliminar %s porque tiene pagos' % rec.name)
        return super(Conductor, self).unlink()

    def get_ahorro_ids(self):
        conceptos = []
        Pago = self.env['fundetaxcol.pago']
        #Llamar metodo de busqueda de conceptos de ahorros del modelo fundetaxcol.pago, el cual busca la plantilla de ahorros configurada
        concepto_ahorro_ids = Pago.get_conceptos_ahorro()
        if len(concepto_ahorro_ids) != 0:
            for id in concepto_ahorro_ids:
                _temp_conceptos = self.pago_ahorro_ids.filtered(lambda x: x.concepto_id.id == id)
                if _temp_conceptos:
                    concepto_id = _temp_conceptos.mapped('concepto_id')
                    subtotal = sum(_temp_conceptos.mapped('subtotal'))
                    conceptos.append({
                        'concepto_id': concepto_id,
                        'subtotal': subtotal,
                    })
        return conceptos

    #Devolver total conceptos de ahorro
    def get_ahorro(self):
        conceptos = []
        ahorro_ids = self.get_ahorro_ids()
        for ahorro in ahorro_ids:
            if ahorro.get('subtotal') > 0:
                conceptos.append({
                    'concepto': ahorro.get('concepto_id').name,
                    'valor': ahorro.get('subtotal')
                })

        #conceptos = []
        #Pago = self.env['fundetaxcol.pago']
        ##Llamar metodo de busqueda de conceptos de ahorros del modelo fundetaxcol.pago, el cual busca la plantilla de ahorros configurada
        #concepto_ahorro_ids = Pago.get_conceptos_ahorro()
        #if len(concepto_ahorro_ids) != 0:
        #	for id in concepto_ahorro_ids:
        #		_temp_conceptos = self.pago_ahorro_ids.filtered(lambda x: x.concepto_id.id == id)
        #		if _temp_conceptos:
        #			concepto = _temp_conceptos.mapped('concepto_id.name')[0]
        #			valor = sum(_temp_conceptos.mapped('subtotal'))
        #			conceptos.append({
        #				'concepto': concepto,
        #				'valor': valor,
        #			})
        return conceptos

    #Calcular los ahorros del conductor, desde una fecha
    @api.model
    def calcular_ahorros(self, fecha=False, concepto_inicial=False, ids=False):
        domain = []
        if ids:
            domain = [('id','in',ids)]
        partners = self.search(domain)
        Pago = self.env['fundetaxcol.pago']
        ConceptoAhorro = self.env['fundetaxcol.pago.concepto.ahorro']
        concepto_ahorro_ids = Pago.get_conceptos_ahorro()
        domain = []
        if fecha:
            domain = [('create_date','>', '%s 00:00:00' %fecha)]
        pagos = Pago.search(domain)
        #Para validar si el tercero tiene retiros
        Retiro = self.env['fundetaxcol.retiro.ahorro']
        for partner in partners:
            retiros = Retiro.search_count([('conductor_id','=',partner.id)])
            if retiros > 0:
                raise exceptions.ValidationError('No se puede ajustar el Saldo de Ahorros para el Conductor: %s, porque ya tiene Retiros' %partner.name)
            if concepto_inicial:
                partner.pago_ahorro_ids.filtered(lambda x: x.concepto_id.id != concepto_inicial).unlink()
            else:
                partner.pago_ahorro_ids.unlink()
            partner.ahorro = 0
            _pagos = pagos.filtered(lambda x: x.conductor_id.id == partner.id)
            for pago in _pagos:
                concepto_ids = pago.concepto_ids.filtered(lambda x: x.concepto_id.id in concepto_ahorro_ids)
                for concepto in concepto_ids:
                    if concepto.valor != 0:
                        new_ahorro = {
                            'pago_id': pago.id,
                            'conductor_id': partner.id,
                            'concepto_id': concepto.concepto_id.id,
                            'cantidad': concepto.cantidad,
                            'valor': concepto.valor,
                        }
                        new_rec_ahorro = ConceptoAhorro.create(new_ahorro)
                        concepto.ahorro_id = new_rec_ahorro.id
                        _logger.info('Ahorro agregado conductor: %s valor: $ %s' % (partner.name, concepto.subtotal))
            partner._compute_ahorro()

class Contacto(models.Model):
    _name = 'res.partner.contacto'
    _description = 'Contacto'

    name = fields.Char(string='Nombre', required=True,)
    telefono = fields.Char(string='Teléfono', required=True,)
    res_partner_id = fields.Many2one(
        'res.partner',
        string='Conductor',
    )
