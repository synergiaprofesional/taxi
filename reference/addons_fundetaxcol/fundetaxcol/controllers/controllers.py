# -*- encoding: utf-8 -*-
from odoo.addons.bus.controllers.main import BusController
from odoo.http import request, route
import json
import logging
_logger = logging.getLogger(__name__)

ids = []


class FundetaxcolController(BusController):

    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'fundetaxcol.turno.channel'))
            channels.append((request.db, 'fundetaxcol.print_for_url'))
        return super(FundetaxcolController, self)._poll(dbname, channels, last, options)

    @route('/tickets', auth='user')
    def view_tickets(self, **kwargs):
        return request.render('fundetaxcol.index', {'data': json.dumps(eval(kwargs.get('qcontext')))})

    @route('/print/ticket', auth='user')
    def print_ticket(self, **kwargs):
        return request.render('fundetaxcol.ticket', {'data': json.dumps(eval(kwargs.get('qcontext')))})
        # return request.render('fundetaxcol.ticket', {'data': kwargs.get('pago_id')})

    @route('/print/ticket_client', auth='user')
    def print_ticket_client(self, **kwargs):
        return request.render('fundetaxcol.ticket_client')

    @route('/print/ahorro', auth='user')
    def print_ahorro(self, **kwargs):
        return request.render('fundetaxcol.ahorro', {'data': json.dumps(eval(kwargs.get('qcontext')))})

    @route('/print/ticket_ahorro', auth='user')
    def print_ticket_ahorro(self, **kwargs):
        return request.render('fundetaxcol.ticket_ahorro', {'data': json.dumps(eval(kwargs.get('qcontext')))})

    @route('/tablero_turnos', aut='user')
    def tablero_turno(self, **kwargs):
        return request.render('fundetaxcol.tablero_turnos', {'id': kwargs.get('sesion_bahia_id'), 'name': kwargs.get('name')})
