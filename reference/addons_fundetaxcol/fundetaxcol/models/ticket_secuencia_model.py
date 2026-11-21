# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

class SecuenciaTicket(models.Model):
    _name = 'fundetaxcol.secuencia.ticket'
    _description = 'Secuencia Ticket'

    name = fields.Char(string='Nombre', required=True,)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.user.company_id)
    numero = fields.Integer(string='Número', default=1, required=True)
    padding = fields.Integer(string='Relleno', default=4, required=True)
    numero_str = fields.Char(string='Consecutivo')
    prefijo = fields.Char(string='Prefijo',)

    @api.onchange('numero', 'padding')
    def _onchange_num_pad(self):
        self.numero_str = self.get_numero_str(self.numero, self.padding, self.prefijo)

    def get_numero_str(self, num, pad, pre):
        longitud_numero = len(str(num))
        if longitud_numero < pad:
            _padding = pad - longitud_numero
            x = '0' * _padding + str(num)
            if pre:
                x = pre + x
            return x
        return str(num)

    def actualizar_consecutivo(self):
        new_num = self.numero + 1
        self.write({
            'numero': new_num,
            'padding': self.padding
        })

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.numero > 1:
                raise exceptions.ValidationError('Esta Secuencia ya se usó, por seguridad No puede ser borrada')
        return super(SecuenciaTicket, self).unlink()

    @api.model
    def create(self, vals):
        vals['numero_str'] = self.get_numero_str(vals['numero'], vals['padding'], vals['prefijo'])
        new_sec = super(SecuenciaTicket, self).create(vals)
        return new_sec

    @api.multi
    def write(self, vals):
        for sec in self:
            num = vals.get('numero')
            pad = vals.get('padding')
            pre = vals.get('prefijo')
            if not num: num = sec.numero
            if not pad: pad = sec.padding
            if not pre: pre = sec.prefijo
            vals['numero_str'] = self.get_numero_str(num, pad, pre)
            upd_secuencia = super(SecuenciaTicket, sec).write(vals)
            if not upd_secuencia:
                return False
        return True