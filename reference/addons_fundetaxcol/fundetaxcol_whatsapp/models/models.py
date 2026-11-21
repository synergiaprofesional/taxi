# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions

import requests

import logging
_logger = logging.getLogger(__name__)


def send_pdf_to_whatsapp(host, data):
    URL_SERVER_PING = host + '/ping'
    URL_SERVER_SEND_MESSAGE = host + '/send_message'
    response = requests.post(URL_SERVER_PING, json={'user': data.get('user')})
    result = response.json().get('status', False)
    if result == 'CONNECTED':
        requests.post(URL_SERVER_SEND_MESSAGE, json=data)


class ResCompany(models.Model):
    _inherit = 'res.company'

    host_whatsapp = fields.Char(string="Host WhatsApp")
    mobile = fields.Char(related='partner_id.mobile')


class App(models.Model):
    _inherit = 'fundetaxcol.fundetaxcol'

    host_whatsapp = fields.Char(related='company_id.host_whatsapp')
    mobile = fields.Char(related='company_id.mobile')

    @api.multi
    def open_scan_whatsapp(self):
        return {
            "type": "ir.actions.act_url",
            "url": self.host_whatsapp + '?phone=57' + self.mobile,
            "target": "new",
        }


class PagoTaxi(models.Model):
    _inherit = 'fundetaxcol.pago'

    @api.model
    def create(self, values):
        new_rec = super(PagoTaxi, self).create(values)
        user = new_rec.conductor_id.mobile
        host = new_rec.company_id.host_whatsapp
        mobile = new_rec.company_id.mobile
        if host and mobile and user:
            file = self.get_pdf(new_rec.id)
            data = {
                'user': user,
                'file': file.decode(),
                'filename': new_rec.name
            }
            send_pdf_to_whatsapp(host, data)
        return new_rec


class TurnoTaxi(models.Model):
    _inherit = 'fundetaxcol.turno'

    @api.multi
    def write(self, values):
        result = super(TurnoTaxi, self).write(values)
        for rec in self:
            conductor = rec.conductor_id
            vehiculo = rec.vehiculo_id
            tarifa = rec.tarifa_id
            if conductor and vehiculo and tarifa:
                host = rec.company_id.host_whatsapp
                mobile = rec.company_id.mobile
                user = conductor.mobile
                if host and mobile and user:
                    file = self.get_pdf(rec.id)
                    data = {
                        'user': user,
                        'file': file.decode(),
                        'filename': rec.name
                    }
                    send_pdf_to_whatsapp(host, data)
        return result
