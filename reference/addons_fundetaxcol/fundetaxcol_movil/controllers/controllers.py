# -*- coding: utf-8 -*-

import json
import select

import odoo
from odoo import http
from odoo.http import request
from odoo.addons.bus.controllers.main import BusController

import logging
_logger = logging.getLogger(__name__)

# class PollController(BusController):

#     def _poll(self, dbname, channels, last, options):
#         if request.session.uid:
#             channels = list(channels)
#         return super(PollController, self)._poll(dbname, channels, last, options)

# class ApiController(http.Controller):

#     @http.route('/api/session', type='http', auth='none')
#     def get_data(self, **k):
#         with odoo.sql_db.db_connect('postgres').cursor() as cr:
#             conn = cr._cnx
#             cr.execute("listen imbus")
#             cr.commit();
#             while True:
#                 if select.select([conn], [], [], 50) == ([], [], []):
#                     pass
#                 else:
#                     conn.poll()
#                     channels = []
#                     while conn.notifies:
#                         channels.extend(json.loads(conn.notifies.pop().payload))
#                     temp = [x for x in channels if "api" in x[1]]
#                     if len(temp) != 0:
#                         data = temp[0]
#                         if data and len(data) > 1:
#                             return data[1].split('api.')[1]
