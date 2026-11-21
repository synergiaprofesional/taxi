# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
import logging, base64
_logger = logging.getLogger(__name__)

class Turno(models.Model):
    _name = 'fundetaxcol.turno'
    _description = 'Turno'
    _order = 'sequence'

    ESTADO = [('actual','Actual'),('espera','En espera'),('siguiente','Siguiente'),('despachado','Despachado'),('pausa','Pausado'),('cancelado','Cancelado')]

    name = fields.Char(string='Nombre',)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.user.company_id)
    fecha_asignacion = fields.Datetime(string='Fecha Asignación', default=fields.Datetime.now)
    fecha_despacho = fields.Datetime(string='Fecha Despacho',)
    placa_anonima = fields.Char(string='Placa Anónima',)
    vehiculo_id = fields.Many2one(
        'fundetaxcol.vehiculo',
        string='Placa',
    )
    vehiculo_ids = fields.Many2many(
        'fundetaxcol.vehiculo',
        string='Vehiculos',
    )
    conductor_id = fields.Many2one(
        'res.partner',
        string='Conductor',
    )
    conductor_ids = fields.Many2many(
        'res.partner',
        string='Filtro conductores',
    )
    tarifa_id = fields.Many2one(
        'fundetaxcol.tarifa.sector',
        string='Ruta',
    )
    valor = fields.Float(string='Valor')
    state = fields.Selection(ESTADO, string='Estado', default='espera')
    sequence = fields.Integer(string='Número')
    bahia_id = fields.Many2one(
        'fundetaxcol.sesion.bahia',
        string='Bahía',
        required=True,
    )
    sesion_id = fields.Many2one(
        'fundetaxcol.sesion',
        string='Sesion',
        ondelete='cascade',
        related='bahia_id.sesion_id',
    )
    anonimo = fields.Boolean(string='Anónimo',)
    nota = fields.Char(string='Nota', related='tarifa_id.nota')

    def _get_content_to_print(self, app):
        content = []
        content.append({'text': 'Turno: %s' % self.sequence})
        content.append({'text': 'Usuario: %s' % self.create_uid.name})
        content.append({'text': 'Destino: %s' % self.tarifa_id.name})
        content.append({'text': 'Tarifa sugerida: %s' % app.get_format_currency(self.valor)})
        if self.nota:
            content.append({'text': self.nota})
        content.append({'text': 'Vehículo: %s' % self.vehiculo_id.name})
        content.append({'text': 'Conductor: %s' % self.conductor_id.name})
        content.append({'text': ''})
        content.append({'text': 'Fecha - Hora'})
        content.append({'text': app.get_fecha_actual(self.fecha_despacho)})		
        return content

    #@api.multi
    #def print_despacho(self):
    #	App = self.env['fundetaxcol.fundetaxcol']
    #	Printer = self.env['impresora'].search([], limit=1)
    #	if Printer:
    #		data = Printer.get_data()
    #		data['content'] = self._get_content_to_print(App)
    #		Printer.imprimir(data)
    #	#return {
    #	#	"type": "ir.actions.act_url",
    #	#	"url": "/print/ticket_client?qcontext=%s" %(self.get_data()),
    #	#	"target": "new",
    #	#}

    def get_data(self):
        return {
            'id': self.id,
            'sequence': self.sequence,
            'fecha_despacho': self.env['fundetaxcol.fundetaxcol'].get_fecha_actual(self.fecha_despacho),
            'user': self.create_uid.name,
            'vehiculo': self.vehiculo_id.name,
            'anonimo': self.anonimo,
            'placa_anonima': self.placa_anonima,
            'conductor': self.conductor_id.name,
            'tarifa': self.tarifa_id.name,
            'company': {
                'name': self.company_id.name,
                'phone': self.company_id.phone,
                'email': self.company_id.email,
                'website': self.company_id.website,
                'report_footer': self.company_id.report_footer
            },
            'nota': self.nota,
            'valor': self.valor,
        }

    def go_to_bahias(self, data=False):
        return {
            'name': 'Bahías',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban',
            'res_model': 'fundetaxcol.bahia',
            'target': 'main',
            'domain': [['sesion_ids','in',self.sesion_id.id]],
            'data_to_print': data,
        }

    @api.model
    def get_pdf(self, id):
        REPORT_NAME = 'fundetaxcol.menu_report_despacho'
        pdf = self.env.ref(REPORT_NAME).sudo().render_qweb_pdf([id])
        return base64.encodestring(pdf[0])

    @api.multi
    def print_ticket_client(self):
        #url = "/print/ticket_client?qcontext=%s" %(self.get_data())
        #self.env['bus.bus'].sendone((self._cr.dbname, 'fundetaxcol.print_for_url'), url)
        printer = self.env['impresora'].get_predeterminada()
        if printer:
            b64_pdf = self.get_pdf(self.id)
            _return = {
                'name': 'Bahías',
                'type': 'ir.actions.act_window',
                'view_mode': 'kanban',
                'res_model': 'fundetaxcol.bahia',
                'target': 'main',
                'domain': [['sesion_ids','in',self.sesion_id.id]],
            }
            return printer.imprimir_pdf(b64_pdf, '%s[%s]' %(self._name, self.id), _return)
        data = {
            'url': "/print/ticket_client",
            'data': self.get_data(),
        }
        return self.go_to_bahias(data)

    @api.multi
    def btn_siguiente_despacho(self):
        return {
            "type": "ir.actions.act_url_print",
            "url": "/print/ticket_client?qcontext=%s" %(self.get_data()),
            "target": "new",
        }
        #self._context['active_id'] = self.bahia_id.turno_actual_id.id



        #despachar_turno_form = self.env.ref('fundetaxcol.despachar_turno_form', False)
        #if (self.bahia_id.turno_actual_id.id):
        #	return {
        #		'name': 'Despachar Turno',
        #		'type': 'ir.actions.act_window',
        #		'view_mode': 'form',
        #		'res_model': 'fundetaxcol.turno',
        #		'res_id': self.bahia_id.turno_actual_id.id,
        #		'views': [(despachar_turno_form.id,'form')],
        #		'target': 'new',
        #		'context': {
        #			'default_fecha_despacho': fields.Datetime.now(),
        #		}
        #	}

    @api.multi
    def btn_guardar_turno(self):
        return self.go_to_bahias()

    @api.multi
    def btn_cancel(self):
        return self.go_to_bahias()

    @api.multi
    def btn_imprimir(self):
        pass

    @api.multi
    def btn_despachar_turno(self, bahia_id=False):
        despachar_turno_form = self.env.ref('fundetaxcol.despachar_turno_form', False)
        return {
            'name': 'Despachar Turno',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'fundetaxcol.turno',
            'res_id': self.id,
            'views': [(despachar_turno_form.id,'form')],
            'target': 'current',
            'flags': {'form': {'action_buttons': True, 'initial_mode': 'edit', 'options': {'mode': 'edit'}}} ,
            'context': {
                'default_fecha_despacho': fields.Datetime.now(),
                'form_view_initial_mode': 'edit',
                'force_detailed_view': True,
                'default_bahia_id': self.bahia_id or bahia_id,
            }
        }

    def cancelar_despacho(self):
        for turno in self:
            if turno.state == 'despachado':
                turno.state = 'cancelado'

    def cambiar_estado(self):
        for turno in self:
            if turno.state != 'despachado':
                if turno.state == 'pausa':
                    turno.state = 'espera'

    def set_conductor_anonimo(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        conductor_id = ICPSudo.get_param('fundetaxcol.conductor_anonimo_id', default=False)
        self.conductor_id = self.env['res.partner'].browse(int(conductor_id))

    def set_valor(self):
        self.valor = self.tarifa_id.valor
        ICPSudo = self.env['ir.config_parameter'].sudo()
        hora_recargo = ICPSudo.get_param('fundetaxcol.hora_recargo', default=False) + ':00'
        hora_actual = self.env['fundetaxcol.fundetaxcol'].get_fecha_actual().split(' ')[1]
        if hora_actual >= hora_recargo:
            self.valor = self.tarifa_id.valor + self.tarifa_id.valor_recargo
        else:
            self.valor = self.tarifa_id.valor

    def get_valor(self, tarifa_id):
        tarifa = self.env['fundetaxcol.tarifa.sector'].browse(tarifa_id)
        ICPSudo = self.env['ir.config_parameter'].sudo()
        hora_recargo = ICPSudo.get_param('fundetaxcol.hora_recargo', default=False) + ':00'
        hora_actual = self.env['fundetaxcol.fundetaxcol'].get_fecha_actual().split(' ')[1]
        if hora_actual >= hora_recargo:
            return tarifa.valor + tarifa.valor_recargo
        return tarifa.valor

    @api.onchange('anonimo')
    def _onchange_anonimo(self):
        if self.anonimo:
            self.set_conductor_anonimo()

    @api.onchange('tarifa_id')
    def _onchange_tarifa_id(self):
        if self.tarifa_id:
            self.set_valor()

    @api.onchange('bahia_id')
    def _onchange_bahia_id(self):
        self.sequence = self.bahia_id.turno_actual

        # for sesion_bahia in self.bahia_id.sesion_id.sesion_bahia_ids:
        #     for pago in sesion_bahia.pago_ids:
        #         ingreso = len(pago.concepto_ids.filtered(lambda x: \
        #             x.concepto_id.clasificacion == 'cr_ingreso' \
        #                 or x.concepto_id.clasificacion == 'ingreso'))
        #         if ingreso != 0:
        #             self.vehiculo_ids |= pago.vehiculo_id
        #     for turno in sesion_bahia.turno_ids:
        #         if turno.state == 'actual' or turno.state == 'espera' or turno.state == 'pausa':
        #             self.vehiculo_ids -= turno.vehiculo_id

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id:
            conductores = self.vehiculo_id.conductor_ids.mapped('conductor_id')
            self.conductor_ids = conductores
            if conductores:
                self.conductor_id = conductores[0]
            elif self.vehiculo_id.propietario_id and self.vehiculo_id.propietario_id.conductor:
                self.conductor_id = self.vehiculo_id.propietario_id
            else:
                self.conductor_id = False

    def set_sequence(self):
        self.sequence = self.bahia_id.turno_actual
        name_vehiculo = self.vehiculo_id.name
        if self.placa_anonima:
            name_vehiculo = self.placa_anonima
        self.name = ''.join(['Turno #',str(self.sequence),' [',name_vehiculo,' - ',self.conductor_id.name,']'])
        self.bahia_id.update_numero_turno()
        self.bahia_id.update_turno_actual()

    @api.model
    def create(self, values):
        if values.get('tarifa_id'):
            values['state'] = 'despachado'
            values['fecha_despacho'] = fields.Datetime.now()
            valor = self.get_valor(int(values.get('tarifa_id')))
            values['valor'] = valor
        new_turno = super(Turno, self).create(values)
        if new_turno.anonimo:
            new_turno.set_conductor_anonimo()
            new_turno.write(values)
        new_turno.set_sequence()
        new_turno.broadcast()
        return new_turno

    @api.multi
    def write(self, values):
        for rec in self:
            if values.get('tarifa_id'):
                values['state'] = 'despachado'
                values['fecha_despacho'] = fields.Datetime.now()
                valor = self.get_valor(int(values.get('tarifa_id')))
                values['valor'] = valor
        result = super(Turno, self).write(values)
        for rec in self:
            rec.broadcast()
        return result

    @api.model
    def despachar_from_ui(self, turno):
        turno_id = turno.pop('id', False)
        tarifa_id = turno.pop('tarifa_id', False)
        if turno_id and tarifa_id:
            self.browse(turno_id).write({
                'tarifa_id': tarifa_id,
            })
        return turno_id

    def broadcast(self):
        self.bahia_id.update_turno_actual()
        data = self.read(['sequence','vehiculo_id','conductor_id','bahia_id','state','anonimo'])
        self.env['bus.bus'].sendone((self._cr.dbname, 'fundetaxcol.turno.channel'), data)
