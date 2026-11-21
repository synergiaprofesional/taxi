# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
import urllib.request

import pytz
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class Mensaje(models.Model):
	_name = 'mensaje.mensaje'
	_description = 'Mensaje'

	ESTADO = [('no_enviado','No enviado'), ('ok','Enviado'), ('reenviado','Reenviado')]

	name = fields.Char(string='Nombre')
	partner_id = fields.Many2one(
		'res.partner',
		string='Destinatario',
		required=True,
	)
	state = fields.Selection(ESTADO, 'Estado', default='no_enviado')
	mensaje = fields.Text(string='Mensaje', required=True)
	mensaje_format = fields.Html(string='Mensaje')
	celular = fields.Char(string='Nº Celular', related='partner_id.mobile')

	def get_fecha_actual(self, fecha=False):
		fecha = fecha or fields.Datetime.now()
		diff = datetime.now(pytz.timezone(self.env.user.tz or 'UTC')).utcoffset()
		return str(datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S') + diff)

	def get_dia_fecha(self, fecha):
		return datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').day

	def get_numero_mensajes(self):
		ICPSudo = self.env['ir.config_parameter'].sudo()
		contador_mensaje = int(ICPSudo.get_param('mensaje.contador'))
		if contador_mensaje <= 0 or not contador_mensaje:
			raise exceptions.ValidationError('Usted no cuenta con saldo suficiente para enviar mensajes')
		return contador_mensaje

	def actualizar_numero_mensajes(self, numero_mensajes, cantidad):
		ICPSudo = self.env['ir.config_parameter'].sudo()
		ICPSudo.set_param('mensaje.contador', numero_mensajes + cantidad)

	def get_request(self):
		#https://sistemasmasivos.com/itcloud/api/sendsms/send.php
		ICPSudo = self.env['ir.config_parameter'].sudo()
		url = ICPSudo.get_param('mensaje.url')
		usuario = ICPSudo.get_param('mensaje.usuario')
		password = ICPSudo.get_param('mensaje.password')
		if url and usuario and password:
			mensaje = self.mensaje.lstrip(' ')
			if not self.partner_id.mobile:
				raise exceptions.ValidationError('Por favor configure número de celular para el tercero')
			if not self.partner_id.permitir_mensaje:
				raise exceptions.ValidationError('El tercero %s no tiene permitido recibir SMS' %self.partner_id.name)
			celular = '57%s'%self.partner_id.mobile
			data = urllib.parse.urlencode({'user': usuario, 'password': password, 'GSM' : celular, 'SMSText': mensaje})
			request = '%s?%s' %(url,data)
			return request
		else:
			raise exceptions.ValidationError('Por favor configure la mensajería')

	def enviar_mensaje(self):
		contador_mensaje = self.get_numero_mensajes()
		request = self.get_request()
		try:
			result = urllib.request.urlopen(request).read()
			try:
				r = int(result)
				if r < 0:
					if r == -1:
						raise exceptions.ValidationError('Falló la autenticación al servidor de mensajes')
					elif r == -2:
						raise exceptions.ValidationError('Por instrucciones de la CRC los mensajes deben ser enviados entre el horario 8am y 9pm')
					elif r == -3:
						raise exceptions.ValidationError('No tiene saldo en la cuenta para realizar el envio.')
					elif r == -6:
						raise exceptions.ValidationError('Sistema en mantenimiento. Este SMS no tiene cobro ni fue enviado.')
					elif r == -8:
						raise exceptions.ValidationError('El número de celular se encuentra en lista de bloqueo')
				elif r == 0:
					raise exceptions.ValidationError('Operador no existe o está desactivado')
				else:
					raise exceptions.ValidationError('El tercero %s no tiene permitido recibir mensajes SMS'%(self.partner_id.name))
			except ValueError:
				#if str(celular) in str(result):
				#	return {'error': False, 'mensaje': 'Mensaje enviado exitosamente!'}
				self.actualizar_numero_mensajes(contador_mensaje, -1)
				if self.state == 'ok':
					self.state = 'reenviado'
				else:
					self.state = 'ok'
		except ValueError:
			raise exceptions.ValidationError('Error verifique su conexión a Internet')

	@api.model
	def create(self, values):
		new_record = super(Mensaje, self).create(values)
		new_record.enviar_mensaje()
		return new_record

class Plantilla(models.Model):
	_name = 'mensaje.plantilla'
	_description = 'Plantillas de mensaje'

	name = fields.Char(string='Nombre', required=True)
	model_id = fields.Many2one(
		'ir.model',
		string='Aplicar a',
		required=True,
	)
	campos = fields.Html(string='Campos', compute='_compute_campos')
	campo_tercero = fields.Char(string='Campo tercero', required=True, help='Este campo se tomará para obtener el número de celular del Tercero asociado al registro del modelo seleccionado', )
	cabecera = fields.Char(string='Cabeza mensaje')
	cuerpo = fields.Text(string='Cuerpo mensaje', required=True)
	pie = fields.Char(string='Pie mensaje')
	nombre_completo = fields.Boolean(string='Nombre completo en mensaje', help='Nombre completo del tercero en el mensaje',)
	mensaje = fields.Html(string='Mensaje', compute='_get_mensaje_format')
	#model_ids = fields.Many2many('ir.model', string='Modelos a excluir', compute='_compute_modelos')
	menu = fields.Boolean(string='Menú')
	ref_ir_server = fields.Many2one('ir.actions.server', 'Acción relacionada', readonly=True, copy=False)

	def unlink_action(self):
		if self.ref_ir_server:
			self.ref_ir_server.sudo().unlink()

	@api.multi
	def unlink(self):
		self.unlink_action()
		return super(Plantilla, self).unlink()

	def verificar_partner_id(self, value=False):
		campo_tercero = value or self.campo_tercero
		result = False
		for field in self.model_id.field_id:
			if field.name == campo_tercero:
				if field.ttype == 'many2one':
					if field.relation == 'res.partner':
						result = True
						break
		if not result:
			raise exceptions.ValidationError('No se ha encontrado un tercero vinculado, por favor verifique el campo del tercero')

	def get_campo_relacional(self, campo):
		for _campo in self.model_id.field_id:
			if _campo.name == campo:
				if _campo.relation:
					return '%s.name'%campo
		return campo

	def get_mensaje(self):
		msj = self.cuerpo
		campos = []
		while msj.find('}!') != -1:
			clave = msj[msj.find('${')+2:msj.find('}!')]
			valor = '${%s}!' % clave
			msj = msj[msj.find('}!')+2:]
			x = { 'clave': clave, 'valor': valor }
			campos.append(x)
		new_msj = self.cuerpo
		claves = []
		for campo in campos:
			clave = self.get_campo_relacional(campo['clave'])
			valor = campo['valor']
			new_msj = new_msj.replace(valor, '%s')
			claves.append('record.%s'%clave)

		_ext = '%('
		for clave in claves:
			_ext += '%s,'%clave
		_ext = '%s)'%_ext[0:len(_ext)-1]

		mensaje_format = '''\'<div class="text-center"><h3>%s</h3><p>%s</p><small><i>%s</i></small></div>\'%s'''%(self.cabecera or '',new_msj,self.pie or '',_ext)
		new_msj = '\'%s %s %s\'%s'%(self.cabecera or '',new_msj,self.pie or '',_ext)

		return new_msj, mensaje_format

	def set_codigo_enviar_sms(self):
		mensaje, mensaje_format = self.get_mensaje()
		code = '''env['mensaje.mensaje'].sudo().create({
		'name': 'Mensaje enviado a: ' + record.%s.name,
		'partner_id': record.%s.id,
		'mensaje': %s,
		'mensaje_format': %s
		})''' %(self.campo_tercero,self.campo_tercero, mensaje, mensaje_format)
		return code

	@api.one
	def crear_menu_contextual(self):
		if self.menu:
			self.unlink_action()
		else:
			ActServerSudo = self.env['ir.actions.server'].sudo()
			nombre_boton = self.name
			action = ActServerSudo.create({
				'name': nombre_boton,
				'state': 'code',
				'model_id': self.model_id.id,
				'code': self.set_codigo_enviar_sms()
			})
			action.create_action()
			self.write({'ref_ir_server': action.id})
		self.menu = not self.menu

	#def get_model(self, model):
	#	for field in model.field_id:
	#		if field.ttype == 'many2one':
	#			if field.relation == 'res.partner':
	#				return True
	#	return False

	#@api.one
	#@api.depends('model_id')
	#def _compute_modelos(self):
	#	self.model_ids = None
	#	for model in self.env['ir.model'].search([]):
	#		if not self.get_model(model):
	#			self.model_ids |= model

	@api.one
	@api.depends('cabecera','cuerpo','pie')
	def _get_mensaje_format(self):
		html = '''<div class="text-center">
			<h3>%s</h3>
			<p>%s</p>
			<small><i>%s</i></small>
			</div>''' %(self.cabecera or '', self.cuerpo, self.pie or '')
		self.mensaje = html

	@api.one
	@api.depends('model_id')
	def _compute_campos(self):
		html = '''<h3 class="text-center">Campos disponibles en el modelo</h3>
				  <table class="table">
					<tr>
						<th>Nombre</th>
						<th>Descripción</th>
						<th>Relación</th>
					</tr>'''
		fields_exclude = ['id','display_name','create_uid','create_date','__last_update','write_date','write_uid']
		for field in self.model_id.field_id:
			if field.name not in fields_exclude:
				html += '''<tr>
							<td>%s</td>
							<td>%s</td>
							<td>%s</td>
						   </tr>''' %(field.name, field.field_description, field.relation or 'N/A')
		html += "</table>"
		if not self.model_id:
			html = None
		self.campos = html

	@api.model
	def create(self, values):
		new_record = super(Plantilla, self).create(values)
		new_record.verificar_partner_id()
		return new_record

	@api.multi
	def write(self, values):
		for rec in self:
			rec.verificar_partner_id(values.get('campo_tercero', False))
		return super(Plantilla, self).write(values)

class MensajeConfig(models.TransientModel):
	_inherit = 'res.config.settings'
	_name = 'mensaje.ajuste'

	url = fields.Char('Url')
	usuario = fields.Char('Usuario')
	password = fields.Char('Contraseña')
	celular = fields.Char('Nº celular para test')
	contador_mensaje = fields.Integer('Contador mensajes')

	@api.multi
	def set_values(self):
		super(MensajeConfig, self).set_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		ICPSudo.set_param('mensaje.url', self.url)
		ICPSudo.set_param('mensaje.usuario', self.usuario)
		ICPSudo.set_param('mensaje.password', self.password)
		ICPSudo.set_param('mensaje.contador', self.contador_mensaje)

	@api.model
	def get_values(self):
		res = super(MensajeConfig, self).get_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		res.update(
			url = ICPSudo.get_param('mensaje.url'),
			usuario = ICPSudo.get_param('mensaje.usuario'),
			password = ICPSudo.get_param('mensaje.password'),
			contador_mensaje = int(ICPSudo.get_param('mensaje.contador'))
		)
		return res




	#def test_mensaje(self, celular, mensaje):
	#	Mensaje = self.env['prestamo.mensaje']
	#	if self.saldo_mensaje <= 0:
	#		raise exceptions.Warning(_('No cuenta con saldo para enviar mensaje'))
	#	_url = self.env['ir.config_parameter'].get_param('url_mens')
	#	usuario = self.env['ir.config_parameter'].get_param('usuario_mens')
	#	password = self.env['ir.config_parameter'].get_param('pass_mens')
	#	url = '{0}?user={1}&password={2}&GSM={3}&SMSText={4}'.format(_url, usuario, password, celular, mensaje)
	#	result = ''
	#	try:
	#		result = urllib2.urlopen(url).read()
	#	except urllib2.URLError:
	#		raise exceptions.ValidationError(_('Por favor verifique su conexión a Internet'))
	#	r = -100
	#	try:
	#		r = int(result)
	#	except ValueError:
	#		if str(celular) in str(result):
	#			Mensaje.actualizar_saldo_mensajeria()
	#	if r < 0:
	#		if r == -1:
	#			raise exceptions.ValidationError(_('Autenticación Fallida'))
	#		elif r == -2:
	#			raise exceptions.ValidationError(_('Por instrucciones de la CRC los mensajes deben ser enviados entre el horario 8am y 9pm'))
	#		elif r == -3:
	#			raise exceptions.ValidationError(_('No tiene saldo en la cuenta para realizar el envio.'))
	#		elif r == -6:
	#			raise exceptions.ValidationError(_('Sistema en mantenimiento. Este SMS no tiene cobro ni fue enviado.'))
	#		elif r == -8:
	#			raise exceptions.ValidationError(_('El número de celular se encuentra en lista de bloqueo'))
	#	elif r == 0:
	#		raise exceptions.ValidationError(_('Operador no existe o está desactivado'))
	#	elif r > 0:
	#		Mensaje.actualizar_saldo_mensajeria()
	#	raise exceptions.ValidationError(_('Error del sistema, vuelva a intentarlo...'))

class ResPartner(models.Model):
	_inherit = 'res.partner'

	permitir_mensaje = fields.Boolean(string='Permitir SMS')