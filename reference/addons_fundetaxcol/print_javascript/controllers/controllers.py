# -*- coding: utf-8 -*-
from odoo import http
request = http.request

from odoo.addons.bus.controllers.main import BusController

class Controller(BusController):
	def _poll(self, dbname, channels, last, options):
		if request.session.uid:
			channels = list(channels)
			channels.append((request.db, 'imprimir'))
		return super(Controller, self)._poll(dbname, channels, last, options)