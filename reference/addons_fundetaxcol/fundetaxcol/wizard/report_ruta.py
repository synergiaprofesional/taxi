# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

from datetime import datetime, timedelta
import pytz

import logging
_logger = logging.getLogger(__name__)

class ReporteRuta(models.TransientModel):
	_name = 'wizard.report.turno'

	periodo = fields.Date('Mes y Año')
	year = fields.Integer('Año')
	mes = fields.Selection([
		('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), 
		('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),
		('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
		], 'Mes')
	tarifa_id = fields.Many2one(
		'fundetaxcol.tarifa.sector',
		string='Ruta',
	)
	imprimir_sumario = fields.Boolean(string='Imprimir sumario',)
	orden = fields.Selection([('name','Nombre'),('qty','Cantidad'),('price','Valor')], 'Ordenado por', default='name')

	@api.onchange('periodo')
	def _onchange_periodo(self):
		if self.periodo:
			self.year = datetime.strptime(self.periodo, '%Y-%m-%d').year
			self.mes = str(datetime.strptime(self.periodo, '%Y-%m-%d').month)
		else:
			self.year = 0
			self.mes = False

	@api.multi
	def generate_report(self):
		_fecha = '%s 00:00:00'%self.periodo
		App = self.env['fundetaxcol.fundetaxcol']
		fecha_inicial = fecha_final = False
		if self.periodo:
			rango_fecha = list(map(lambda f: '%s 00:00:00'%f, App.get_periodo(_fecha)))
			fecha_inicial = rango_fecha[0]
			fecha_final = rango_fecha[len(rango_fecha)-1]
		data = {
			'fecha_inicial': fecha_inicial,
			'fecha_final': fecha_final,
			'orden': self.orden,
			'imprimir_sumario': self.imprimir_sumario,
			'tarifa_id': self.tarifa_id.id,
		}
		return self.env.ref('fundetaxcol.report_ruta').report_action([], data=data)

class ReportRutaAbstract(models.AbstractModel):
	_name = 'report.fundetaxcol.report_rutas'

	@api.model
	def get_turnos(self, date_start, date_stop, tarifa_id, orden='name'):
		domain=[('tarifa_id','!=',False),('state','=','despachado')]
		
		if date_start: domain.append(('fecha_despacho','>=', date_start))
		if date_stop: domain.append(('fecha_despacho','<=', date_stop))
		if tarifa_id: domain.append(('tarifa_id','=', tarifa_id))

		
		turnos = self.env['fundetaxcol.turno'].search(domain)
		lista = []
		sumario = []

		for turno in turnos:
			salir = False
			for l in lista:
				salir = len(list(filter(lambda t: t == turno, l.get('detail',False)))) != 0
			if salir: continue
			query = list(filter(lambda t: t.tarifa_id == turno.tarifa_id, turnos))
			if not query in lista and len(query) > 1:
				lista.append(dict({
					'header': turno.tarifa_id.name,
					'detail': query,
					'qty': len(query),
					'price': sum(line.valor for line in query)
				}))
				sumario.append(dict({
					'header': turno.tarifa_id.name,
					'qty': len(query),
					'price': sum(line.valor for line in query),
				}))
		return lista, sumario

	@api.multi
	def get_report_values(self, docids, data=None):
		data = dict(data or {})

		date_start = data['fecha_inicial']
		date_stop = data['fecha_final']
		tarifa_id = data['tarifa_id']
		imprimir_sumario = data['imprimir_sumario']
		orden = data['orden']

		user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
		today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
		today = today.astimezone(pytz.timezone('UTC'))
		if date_start:
			date_start = fields.Datetime.from_string(date_start)
		#else:
		#	date_start = today

		if date_stop:
			# set time to 23:59:59
			date_stop = fields.Datetime.from_string(date_stop)
		else:
			# stop by default today 23:59:59
			date_stop = today + timedelta(days=1, seconds=-1)

		# avoid a date_stop smaller than date_start
		#date_stop = max(date_stop, date_start)

		date_start = fields.Datetime.to_string(date_start)
		date_stop = fields.Datetime.to_string(date_stop)


		turnos, sumario = self.get_turnos(date_start, date_stop, tarifa_id, orden)
		if tarifa_id:
			tarifa_id = self.env['fundetaxcol.tarifa.sector'].browse(tarifa_id)

		return {
			'date_start': date_start,
			'date_stop': date_stop,
			'tarifa_id': tarifa_id,
			'turnos': turnos,
			'sumario': sumario,
			'imprimir_sumario': imprimir_sumario,
		}