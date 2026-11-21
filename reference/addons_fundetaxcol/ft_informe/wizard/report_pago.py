# -*- coding: utf-8 -*-

from odoo import api, fields, models

import pytz
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)


class WizardPagoXls(models.TransientModel):
    _name = 'wizard.informe.fundetaxcol.pago'
    _description = 'Informe Xls Pagos Por Periodo'

    start_at = fields.Date(string='Fecha Inicial',
                           required=True, default=fields.Date.today)
    stop_at = fields.Date(string='Fecha Final',
                          required=True, default=fields.Date.today)
    agrupar = fields.Boolean(
        string='Agrupar por Conductor/Placa', default=True)
    mostrar_ingresos_del_mes = fields.Boolean(
        string='Mostrar ingresos en el mes', default=True)

    def get_fecha(self, fecha=False):
        fecha = fecha or fields.Date.today()
        diff = datetime.now(pytz.timezone(
            self.env.user.tz or 'UTC')).utcoffset()
        return str(datetime.strptime(fecha, '%Y-%m-%d') + diff)

    @api.multi
    def get_data_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?start_at=%s&stop_at=%s&group=%s&mostrar_ingresos_del_mes=%s' % (self.start_at, self.stop_at, self.agrupar, self.mostrar_ingresos_del_mes),
            'target': 'self',
        }
