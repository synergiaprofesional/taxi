# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

import base64

class Impresora(models.Model):
	_name = 'impresora'

	name = fields.Char(string='Nombre', required=True)
	proxy_ip = fields.Char(string='Proxy', required=True)
	predeterminada = fields.Boolean(copy=False)

	@api.model
	def get_predeterminada(self):
		return self.search([('predeterminada','=',True)], limit=1)

	@api.multi
	def no_predeterminada(self):
		for rec in self:
			rec.predeterminada = False

	@api.multi
	def action_pred(self):
		self.ensure_one()
		self.search([]).no_predeterminada()
		self.predeterminada = True
		return True

	def imprimir_pdf(self, pdf, id=False, retorno=False):
		user = self.get_user_id()
		if 'http://' in self.proxy_ip:
			url = self.proxy_ip
		else:
			url = 'http://%s' % self.proxy_ip
		data = {
			'id': id,
			'uid': user.id,
			'impresora': self.name,
			'pdf': pdf.decode('utf-8')
		}
		if retorno:
			retorno['receipt'] = data
			retorno['print_server'] = True
			retorno['url'] = url
			return retorno
		return {
			'type': 'ir.actions.act_url',
			'print_server': True,
			'receipt': data,
			'url': url,
		}

	def get_printer(self):
		return {
			'nombre': self.name,
			'proxy_ip': self.proxy_ip,
		}

	def get_user_id(self):
		current_uid = self._context.get('uid')
		return self.env['res.users'].sudo().browse(current_uid)

	def get_data(self, company=True):
		user = self.get_user_id()
		data = self.get_data_company(user)
		return {
			'uid': user.id,
			'header': data,
			'impresora': self.get_printer()
		}

	@api.model
	def get_data_company(self, user):
		company_id = user.company_id
		if not company_id: return []
		data = []
		data.append([
			{'content': company_id.name, 'styles': { 'halign': 'center', 'fontStyle': 'bold' } }
		])
		if company_id.phone:
			data.append([
				{'content': 'Telefono: %s' % company_id.phone, 'styles': { 'halign': 'center', 'fontStyle': 'bold' } }
			])
		if company_id.street:
			data.append([
				{'content': company_id.street, 'styles': { 'halign': 'center', 'fontStyle': 'bold' } }
			])
		if company_id.website:
			data.append([
				{'content': company_id.website, 'styles': { 'halign': 'center', 'fontStyle': 'bold' } }
			])
		return data

	@api.multi
	def test(self):
		pass

