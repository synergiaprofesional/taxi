# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

import logging, base64
_logger = logging.getLogger(__name__)


class PagoTaxi(models.Model):
    _name = 'fundetaxcol.pago'
    _description = 'Pago Taxi'
    _order = 'fecha desc'

    ESTADO = [('pendiente', 'Pendiente'), ('autorizado', 'Autorizado'), ]

    name = fields.Char(string='Nombre')
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    company_id = fields.Many2one('res.company', string='Compañía',
                                 required=True, default=lambda self: self.env.user.company_id)
    secuencia_ticket_id = fields.Many2one(
        'fundetaxcol.secuencia.ticket',
        string='Secuencia Tickete',
        required=True,
    )
    bahia_id = fields.Many2one(
        'fundetaxcol.sesion.bahia',
        string='Bahía',
        ondelete='cascade',
        required=True,
    )
    vehiculo_id = fields.Many2one(
        'fundetaxcol.vehiculo',
        string='Vehículo',
        required=True,
    )
    vehiculo_ids = fields.Many2many(
        'fundetaxcol.vehiculo',
        string='Vehiculos',
    )
    conductor_id = fields.Many2one(
        'res.partner',
        string='Conductor',
        required=True,
    )
    conductor_ids = fields.Many2many(
        'res.partner',
        string='Filtro conductores',
    )
    concepto_ids = fields.One2many(
        'fundetaxcol.pago.concepto',
        'pago_id',
        string='Conceptos',
    )
    concepto_tarifa_base_id = fields.Many2one(
        'fundetaxcol.concepto',
        string='Concepto Tarifa Base',
    )
    consecutivo = fields.Char(string='Consecutivo')
    valor = fields.Float(string='Valor',)
    enturnar = fields.Boolean(string='Enturnar')
    puede_editar = fields.Boolean(
        string='Puede editar', compute='_compute_puede_editar', default=True)

    ajuste_id = fields.Many2one(
        'fundetaxcol.ajuste',
        string='Ajuste',
        ondelete='cascade',
    )
    concepto_log_ids = fields.One2many(
        'fundetaxcol.pago.concepto.log',
        'pago_id',
        string='Log',
    )
    concepto_ahorro_ids = fields.One2many(
        'fundetaxcol.pago.concepto.ahorro',
        'pago_id',
        string='Ahorros',
    )
    ingreso = fields.Integer(string='Ingresos en el mes')

    sesion_en_progreso = fields.Boolean(string="En progreso", compute="_compute_en_progreso", store=True)
    nota = fields.Char(string="Observación")

    @api.multi
    @api.depends('bahia_id')
    def _compute_en_progreso(self):
        for rec in self:
            sesion_progreso_ids = self.env['fundetaxcol.sesion.bahia'].search([('state','=','progreso')]).ids
            rec.sesion_en_progreso = rec.bahia_id.id in sesion_progreso_ids

    @api.model
    def pago_en_progreso(self):
        sesion_ids = self.env['fundetaxcol.sesion.bahia'].search([('state','=','progreso')]).ids
        domain = [('bahia_id','in',sesion_ids)]
        return self.search(domain)
    
    @api.model
    def ingreso_sesion_vehiculo(self, vehiculo_id):
        pago_ids = self.pago_en_progreso()
        domain = [('vehiculo_id','=',vehiculo_id)]
        return pago_ids.search_count(domain) != 0

    @api.model
    def ingreso_sesion_conductor(self, conductor_id):
        pago_ids = self.pago_en_progreso()
        domain = [('conductor_id','=',conductor_id)]
        return pago_ids.search_count(domain) != 0

    @api.model
    def limpieza_conductor_vehiculo(self, fecha_inicio, activar=False):
        if activar:
            self.env['fundetaxcol.vehiculo'].search(['|',('active','=',True),('active','=',False)]).write({'active': True})
            self.env['res.partner'].search(['|',('active','=',True),('active','=',False)]).write({'active': True})
        else:
            domain = [('fecha','>=',fecha_inicio)]
            pago_ids = self.search(domain)
            vehiculo_ids = pago_ids.mapped('vehiculo_id').ids
            conductor_ids = pago_ids.mapped('conductor_id').ids
            self.env['fundetaxcol.vehiculo'].search([('id','not in',vehiculo_ids)]).write({'active': False})
            self.env['res.partner'].search([('id','not in',conductor_ids)]).write({'active': False})

    @api.multi
    def _compute_puede_editar(self):
        for rec in self:
            rec.puede_editar = not self.env.user.has_group(
                'fundetaxcol.group_empleado')
            if not rec.puede_editar:
                if not self.create_date:
                    rec.puede_editar = True

    @api.onchange('conductor_id')
    def _onchange_conductor_id(self):
        for rec in self:
            rec.concepto_ids = None
            if rec.conductor_id:
                for concepto in rec.conductor_id.template_concepto_id.concepto_ids:
                    concepto_pago = self.env['fundetaxcol.pago.concepto'].new({
                        'concepto_id': concepto.id,
                        'cantidad': 1,
                    })
                    #valor = 0
                    #if concepto.tipo == 'valor_fijo':
                    #	valor = concepto.valor
                    #rec.add_log('Creación', concepto.id, 1, valor)
                    concepto_pago._onchange_concepto_id()
                    rec.concepto_ids |= concepto_pago
            if not rec.concepto_ids:
                rec.set_tarifa_base()

    @api.onchange('bahia_id')
    def _onchange_bahia_id(self):
        for sesion_bahia in self.bahia_id.sesion_id.sesion_bahia_ids:
            for pago in sesion_bahia.pago_ids:
                ingreso = len(pago.concepto_ids.filtered(lambda x: \
                    x.concepto_id.clasificacion == 'cr_ingreso' \
                        or x.concepto_id.clasificacion == 'ingreso'))
                if ingreso != 0:
                    self.vehiculo_ids |= pago.vehiculo_id

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        for rec in self:
            rec.conductor_ids = None
            if rec.vehiculo_id:
                for x in rec.vehiculo_id.conductor_ids:
                    rec.conductor_ids |= x.conductor_id
                if rec.conductor_ids:
                    rec.conductor_id = rec.conductor_ids[0]

    def set_tarifa_base(self):
        if self.concepto_tarifa_base_id:
            concepto_pago = self.env['fundetaxcol.pago.concepto'].new({
                'concepto_id': self.concepto_tarifa_base_id.id,
                'cantidad': 1,
            })
            #if not self.concepto_ids:
            #	valor = 0
            #	if self.concepto_tarifa_base_id.tipo == 'valor_fijo':
            #		valor = self.concepto_tarifa_base_id.valor
            #	self.add_log('Creación', self.concepto_tarifa_base_id.id, 1, valor)
            concepto_pago._onchange_concepto_id()
            self.concepto_ids |= concepto_pago

    @api.onchange('concepto_ids')
    def _onchange_concepto_ids(self):
        for rec in self:
            rec.valor = sum(concepto.subtotal for concepto in rec.concepto_ids)

    def set_name(self):
        self.name = '[%s] %s' % (
            self.vehiculo_id.name, self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.fecha))

    def get_data(self):
        _conceptos = []
        for concepto in self.concepto_ids:
            _conceptos.append({
                'name': concepto.concepto_id.name,
                'subtotal': concepto.subtotal,
            })
        return {
            'seq': self.consecutivo,
            'date': self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.fecha),
            # 'date': self.fecha,
            'user': self.create_uid.name,
            'car': self.vehiculo_id.name,
            'driver': self.conductor_id.name,
            'in': self.ingreso,
            'company': {
                'name': self.company_id.name,
                'phone': self.company_id.phone,
                'email': self.company_id.email,
                'website': self.company_id.website,
                'report_footer': self.company_id.report_footer
            },
            'concepts': _conceptos,
            'total': self.valor,
            'ahorro_ids': self.conductor_id.get_ahorro(),
            'ahorro': self.conductor_id.ahorro,
        }

    @api.model
    def get_pdf(self, id):
        REPORT_NAME = 'fundetaxcol.menu_report_pago'
        pdf = self.env.ref(REPORT_NAME).sudo().render_qweb_pdf([id])
        return base64.encodestring(pdf[0])

    @api.multi
    def print_pago(self):
        printer = self.env['impresora'].get_predeterminada()
        if printer:
            b64_pdf = self.get_pdf(self.id)
            return printer.imprimir_pdf(b64_pdf, '%s[%s]' %(self._name, self.id))
        return {
            "type": "ir.actions.act_url",
            "url": "/print/ticket?qcontext=%s" % (self.get_data()),
            "target": "new",
        }

    def crear_turno(self):
        new_turno = self.env['fundetaxcol.turno'].create({
            'fecha_asignacion': fields.Datetime.now(),
            'vehiculo_id': self.vehiculo_id.id,
            'conductor_id': self.conductor_id.id,
            'bahia_id': self.bahia_id.id,
        })

    def set_consecutivo(self):
        self.consecutivo = self.secuencia_ticket_id.numero_str
        self.secuencia_ticket_id.actualizar_consecutivo()

    #Busca la plantilla de ahorro configurada y devuelve los conceptos en ella
    @api.model
    def get_conceptos_ahorro(self, ajuste=True):
        #concepto_ahorro_ids = []
        #ICPSudo = self.env['ir.config_parameter'].sudo()
        #plantilla_ahorro_id = ICPSudo.get_param('fundetaxcol.plantilla_ahorro_id')
        #if plantilla_ahorro_id:
        #	plantilla_ahorro_id = self.env['fundetaxcol.concepto.conductor'].browse(int(plantilla_ahorro_id))
        #	if plantilla_ahorro_id.exists():
        #		#Mapear los ids de los registros de conceptos por plantilla
        #		concepto_ahorro_ids = plantilla_ahorro_id.concepto_ids.mapped('id')
        #concepto_ajuste_ahorro_id = ICPSudo.get_param('fundetaxcol.ajuste.ahorro')
        #if concepto_ajuste_ahorro_id and ajuste:
        #	concepto_ahorro_ids.append(int(concepto_ajuste_ahorro_id))
        #return concepto_ahorro_ids
        return self.env['fundetaxcol.concepto'].concepto_ahorro_ids()

    def validar_sesion(self):
        domain = [
            ('id','!=',self.id),
            ('vehiculo_id','=',self.vehiculo_id.id),
            ('bahia_id.sesion_id','=',self.bahia_id.sesion_id.id)
        ]
        result = self.search(domain).mapped('concepto_ids')\
            .filtered(lambda x: x.concepto_id.clasificacion == 'cr_ingreso' \
                or x.concepto_id.clasificacion == 'ingreso')
        if result:
            raise exceptions.ValidationError('El vehículo ya registró pago')

    def obtener_ingreso(self):
        return sum(self.concepto_ids\
            .filtered(lambda x: x.concepto_id.clasificacion == 'ingreso')\
            .mapped('subtotal'))

    def obtener_credito(self):
        return sum(self.concepto_ids\
            .filtered(lambda x: x.concepto_id.clasificacion == 'cr_ingreso')\
            .mapped('subtotal'))

    @api.model
    def create(self, values):
        concepto_ids = values.get('concepto_ids', False)
        new_rec = super(PagoTaxi, self).create(values)
        new_rec.validar_sesion()
        #for concepto in new_rec.concepto_ids:
            #new_rec.get_ahorro(concepto, concepto.id)
        if concepto_ids:
            for concepto in concepto_ids:
                new_rec.get_log(concepto)
                #new_rec.get_ahorro(concepto)
        if len(new_rec.concepto_ids) == 0:
            raise exceptions.ValidationError(
                'Por favor seleccione por lo menos un concepto de pago')
        new_rec.ingreso = new_rec.vehiculo_id.ingreso
        new_rec.set_name()
        new_rec._onchange_concepto_ids()
        if new_rec.enturnar:
            new_rec.crear_turno()
        new_rec.set_consecutivo()
        return new_rec

    #Obtener campos de conceptos nuevos, actualizados o eliminados para el log
    def get_log(self, record):
        ConceptoPago = self.env['fundetaxcol.pago.concepto']
        ind = record[0]
        if ind == 0: # Registro nuevo
            record = record[2]
            etiqueta = 'Creación'
            concepto_id = record.get('concepto_id', False)
            concepto = self.env['fundetaxcol.concepto'].browse(concepto_id)
            cantidad = record.get('cantidad', False)
            valor = record.get('valor', False)
            if concepto.tipo == 'valor_fijo':
                valor = concepto.valor
            self.add_log(etiqueta, concepto_id, cantidad, valor)
        elif ind == 1: # Registro modificado
            record_id = ConceptoPago.browse(record[1])
            self.add_log('Modificación', record_id.concepto_id, record_id.cantidad, record_id.valor)
        elif ind == 2: # Registro eliminado
            record_id = ConceptoPago.browse(record[1])
            self.add_log('Eliminación', record_id.concepto_id, record_id.cantidad, record_id.valor)

    @api.multi
    def write(self, values):
        concepto_ids = values.get('concepto_ids', False)
        if concepto_ids:
            for concepto in concepto_ids:
                self.get_log(concepto)
                #concepto = self.get_ahorro(concepto)
        return super(PagoTaxi, self).write(values)

    def add_log(self, etiqueta, concepto_id, cantidad, valor):
        self.concepto_log_ids |= self.env['fundetaxcol.pago.concepto.log'].new({
            'etiqueta': etiqueta,
            'concepto_id': concepto_id,
            'cantidad': cantidad,
            'valor': valor,
            'subtotal': cantidad * valor,
        })

class ConceptoPago(models.Model):
    _name = 'fundetaxcol.pago.concepto'
    _description = 'Concepto Pago'

    Tipo = [('valor_variable', 'Valor variable'),
            ('valor_fijo', 'Valor fijo'), ('porcentaje', 'Porcentaje')]

    pago_id = fields.Many2one(
        'fundetaxcol.pago',
        string='Pago',
        ondelete='cascade'
    )
    concepto_id = fields.Many2one(
        'fundetaxcol.concepto',
        string='Concepto',
        required=True,
        #domain=[('is_transaccion', '=', False), ]
        domain=[('clasificacion','!=','transaccion'), ]
    )
    cantidad = fields.Integer(string='Cant.', default=1)
    valor = fields.Float(string='Valor',)
    subtotal = fields.Float(string='SubTotal', compute='_compute_subtotal', store=True)
    tipo = fields.Selection(Tipo, string='Tipo', related='concepto_id.tipo')
    ahorro_id = fields.Many2one('fundetaxcol.pago.concepto.ahorro', string='Ahorro')

    def crear_ahorro(self):
        #Pago = self.env['fundetaxcol.pago']
        #concepto_ahorro_ids = Pago.get_conceptos_ahorro()
        
        concepto_ahorro_ids = self.env['fundetaxcol.concepto'].concepto_ahorro_ids()
        
        if self.concepto_id.id in concepto_ahorro_ids:
            self.ahorro_id = self.env['fundetaxcol.pago.concepto.ahorro'].create({
                'pago_id': self.pago_id.id,
                'conductor_id': self.pago_id.conductor_id.id,
                'concepto_id': self.concepto_id.id,
                'cantidad': self.cantidad,
                'valor': self.valor,
            })
        self.pago_id.conductor_id._compute_ahorro()

    def modificar_ahorro(self, values):
        if self.ahorro_id:
            cantidad = values.get('cantidad', False) or self.cantidad
            valor = values.get('valor', False) or self.valor
            self.ahorro_id.cantidad = cantidad
            self.ahorro_id.valor = valor
            self.pago_id.conductor_id._compute_ahorro()

    def eliminar_ahorro(self):
        self.ahorro_id.unlink()
        self.pago_id.conductor_id._compute_ahorro()

    @api.depends('cantidad', 'valor')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.cantidad * rec.valor

    @api.onchange('concepto_id')
    def _onchange_concepto_id(self):
        for rec in self:
            if rec.concepto_id.tipo == 'valor_fijo' or rec.concepto_id.tipo == 'valor_variable':
                rec.valor = rec.concepto_id.valor

    @api.model
    def create(self, values):
        concepto_id = self.env['fundetaxcol.concepto'].browse(int(values.get('concepto_id',False)))
        if concepto_id.tipo == 'valor_fijo':
            values['valor'] = concepto_id.valor
        new_rec = super(ConceptoPago, self).create(values)
        new_rec.crear_ahorro()
        return new_rec

    @api.multi
    def write(self, values):
        for rec in self:
            rec.modificar_ahorro(values)
        return super(ConceptoPago, self).write(values)

    @api.multi
    def unlink(self):
        for rec in self:
            rec.eliminar_ahorro()
        return super(ConceptoPago, self).unlink()	

class ConceptoPagoLog(models.Model):
    _name = 'fundetaxcol.pago.concepto.log'

    etiqueta = fields.Char(string='Etiqueta')
    pago_id = fields.Many2one(
        'fundetaxcol.pago',
        string='Pago',
    )
    concepto_id = fields.Many2one(
        'fundetaxcol.concepto',
        string='Concepto',
    )
    cantidad = fields.Integer(string='Cant.')
    valor = fields.Float(string='Valor',)
    subtotal = fields.Float(string='SubTotal',)

class ConceptoPagoAhorro(models.Model):
    _name = 'fundetaxcol.pago.concepto.ahorro'

    pago_id = fields.Many2one(
        'fundetaxcol.pago',
        string='Pago',
    )
    conductor_id = fields.Many2one(
        'res.partner',
        string='Conductor',
        required=True,
    )
    concepto_id = fields.Many2one(
        'fundetaxcol.concepto',
        string='Concepto',
        required=True,
    )
    retiro_id = fields.Many2one(
        'fundetaxcol.retiro.ahorro',
        string='Retiro',
    )
    cantidad = fields.Integer(string='Cant.', default=1)
    valor = fields.Float(string='Valor',)
    subtotal = fields.Float(string='SubTotal', compute='_compute_subtotal', store=True)
    _subtotal = fields.Float(string='Valor') #Para retiros cuando se haga reversión

    @api.depends('cantidad','valor')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.cantidad * rec.valor

    @api.model
    def create(self, values):
        cantidad = values.get('cantidad')
        valor = values.get('valor')
        subtotal = cantidad * valor
        if subtotal < 0:
            values['_subtotal'] = -1 * subtotal
        return super(ConceptoPagoAhorro, self).create(values)