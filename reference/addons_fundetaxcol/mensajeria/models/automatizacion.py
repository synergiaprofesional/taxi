# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

from ast import literal_eval
import inspect
import pytz
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class Automatizacion(models.Model):
	_name = 'mensaje.automatizacion'
	_description = 'Automatizacion de mensajes'

	name = fields.Char(string='Nombre', required=True,)
	model_id = fields.Many2one(
		'ir.model',
		string='Modelo',
		required=True,
	)
	hora = fields.Char(string='Hora', default='08:00', required=True,)
	dia = fields.Char(string='Ejecutar los', default=1, required=True,)
	to = fields.Char(string='Para', required=True, help='Campo de (los) tercero(s) a quien(es) se (les) envía el mensaje',) #many2one | one2many | many2many
	relacion = fields.Char(string='Relación',)
	mensaje = fields.Text(string='Mensaje', required=True,)
	cron_id = fields.Many2one('ir.cron', 'Acción relacionada', readonly=True, copy=False)
	campos = fields.Html(string='Campos', compute='_compute_campos')
	dominio = fields.Char(string='Dominio',)

	@api.multi
	def run_task(self):
		for rec in self:
			rec.enviar_mensaje()

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
	
	def get_campos(self, mensaje=False):
		msj = mensaje or self.mensaje
		campos = []
		while msj.find('}!') != -1:
			clave = msj[msj.find('${')+2:msj.find('}!')]
			valor = '${%s}!' % clave
			msj = msj[msj.find('}!')+2:]
			campos.append({ 'clave': clave, 'valor': valor })
		return campos

	def get_attrs(self, rec):
		attrs = inspect.getmembers(rec, lambda a:not(inspect.isroutine(a)))
		return [a for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]

	def get_val_attr(self, name, attributes):
		for attr in attributes:
			if name == str(attr[0]):
				return attr[1]
		return False

	def get_partners(self, attributes):
		partners = []
		partner = self.to
		if self.relacion:
			for attribute in attributes:
				if self.relacion in attribute:
					for p in attribute[1]:
						attrs_partner = self.get_attrs(p)
						for ap in attrs_partner:
							if partner == str(ap[0]):
								if ap[1]: partners.append(ap[1])
		else:
			for attribute in attributes:
				if partner in str(attribute[0]):
					if attribute[1]: partners.append(attribute[1])
		return partners

	def fecha_en_dia(self):
		Mensaje = self.env['mensaje.mensaje']
		fecha = Mensaje.get_fecha_actual()
		dia = Mensaje.get_dia_fecha(fecha)
		dias = self.dia.split(',')
		return str(dia) in dias

	def enviar_mensaje(self):
		if not self.fecha_en_dia(): return
		model_id = self.env[self.model_id.model]
		dominio = self.dominio or []
		domain = []
		if len(dominio) != 0:
			while dominio.find(')') != -1:
				clave = dominio[dominio.find('(')+1:dominio.find(')')]
				valor = '(%s)' % clave
				dominio = dominio[dominio.find(')')+1:]
				domain.append(literal_eval(valor))
		recs = model_id.search(domain)
		Mensaje = self.env['mensaje.mensaje']
		campo_tercero = self.to
		campo_relacion_id = self.get_field(self.relacion)
		modelo_relacion_id = False
		if campo_relacion_id:
			if campo_relacion_id.relation:
				modelo_relacion_id = self.env['ir.model'].search([('model','=',campo_relacion_id.relation)])
		campos = self.verificar_plantilla_mensaje()
		mensajes = []
		for rec in recs:
			attributes = self.get_attrs(rec)
			partners = self.get_partners(attributes)
			for partner in partners:
				new_msj = self.mensaje
				relacion = self.relacion
				for campo in campos:
					field = campo['field']
					name = field.name
					val = False
					if name == self.to:
						val = partner.name
					if field.ttype == 'many2one' and name != self.to:
						_field = self.get_val_attr(name, attributes)
						if _field: val = _field.name
						else: val = 'N/A'
					val = val or self.get_val_attr(name, attributes)
					new_msj = new_msj.replace(campo['valor'], str(val))
				mensajes.append({'tercero': partner, 'mensaje': new_msj})

		contador_mensajes = Mensaje.get_numero_mensajes()
		if contador_mensajes < len(mensajes):
			raise exceptions.ValidationError('Usted no cuenta con saldo suficiente para enviar %s mensajes' %len(mensajes))
		comprobar_partners = list(filter(lambda msj: not msj['tercero'].permitir_mensaje or not msj['tercero'].mobile, mensajes))
		if len(comprobar_partners) != 0:
			raise exceptions.ValidationError('Los terceros %s no tienen vinculado un número celular o no tienen permitido recibir SMS' 
				% list(map(lambda msj: msj['tercero'].name, comprobar_partners)))
		for mensaje in mensajes:
			partner_id = mensaje['tercero']
			_msj = mensaje['mensaje']
			mensaje_format = '''<div class="text-center"><p>%s</p></div>'''%_msj
			Mensaje.create({
				'name': 'Mensaje enviado a: %s' %partner_id.name,
				'partner_id': partner_id.id,
				'mensaje': _msj,
				'mensaje_format': mensaje_format,
			})

	def validar_campo(self, campo):
		nombre_campo = campo['clave']
		field = self.get_field(nombre_campo)
		if field:
			campo['validado'] = True
			campo['field'] = field
		else:
			campo_relacion_id = self.get_field(self.relacion)
			if campo_relacion_id:
				if campo_relacion_id.ttype == 'one2many' or campo_relacion_id.ttype == 'many2many':
					modelo_relacion_id = self.env['ir.model'].search([('model','=',campo_relacion_id.relation)])
					for field in modelo_relacion_id.field_id:
						if field.name == nombre_campo:
							if not self.is_respartner(field.name, modelo_relacion_id):
								raise exceptions.ValidationError('El campo %s no se puede utilizar en el mensaje' %field.name)
							campo['validado'] = True
							campo['field'] = field
							break
				else:
					raise exceptions.ValidationError('El campo de relación debe ser de tipo *2many')
			else:
				raise exceptions.ValidationError('El campo %s no fue encontrado' % nombre_campo)
			if not campo.get('validado'): campo['validado'] = False
		return campo

	def verificar_plantilla_mensaje(self, values={}):
		mensaje = values.get('mensaje', False) or self.mensaje
		campos = self.get_campos(mensaje)
		validacion_campos = []
		for campo in campos:
			validacion_campos.append(self.validar_campo(campo))
		for campo in validacion_campos:
			if not campo['validado']:
				raise exceptions.ValidationError('El campo %s, en el mensaje, no fue encontrado' % campo['clave'])
		return validacion_campos

	def crear_cron(self):
		nextcall = '%s %s:00' %(fields.Date.today(), self.hora)
		Cron = self.env['ir.cron'].sudo()
		model_id = self.env['ir.model'].search([('model','=',self._name)])
		record = {
			'name': self.name,
			'model_id': model_id.id,
			'state': 'code',
			'interval_number': 1,
			'interval_type': 'days',
			'nextcall': nextcall,
			'numbercall': -1,
			'priority': 1,
			'doall': True,
			'active': True,
			'code': '''env['%s'].browse(%s).enviar_mensaje()''' % (self._name, self.id)
		}
		cron_id = Cron.create(record)
		self.write({'cron_id': cron_id.id})
		cron_id.method_direct_trigger()

	def get_field(self, field):
		if not field: return False
		for f in self.model_id.field_id:
			if f.name == field:
				return f
		return False

	def is_respartner(self, field, model):
		for f in model.field_id:
			if f.name == field:
				if f.ttype == 'many2one':
					if f.relation == 'res.partner':
						return True
		return False

	def verificar_partner_id(self, value=False, relacion=False):
		campo_tercero = value or self.to
		campo_relacion = relacion or self.relacion
		result = False
		campo_relacion_id = self.get_field(campo_relacion)
		if campo_relacion_id:
			if campo_relacion_id.relation:
				modelo_relacion_id = self.env['ir.model'].search([('model','=',campo_relacion_id.relation)])
				result = self.is_respartner(campo_tercero, modelo_relacion_id)
		else:
			result = self.is_respartner(campo_tercero, self.model_id)
		if not result:
			raise exceptions.ValidationError('No se ha encontrado tercero(s) vinculado(s), por favor verifique el campo a quien se envía el mensaje')

	def unlink_cron(self):
		if self.cron_id:
			self.cron_id.sudo().unlink()

	@api.model
	def create(self, values):
		new_record = super(Automatizacion, self).create(values)
		new_record.verificar_partner_id()
		new_record.verificar_plantilla_mensaje()
		new_record.crear_cron()
		return new_record

	@api.multi
	def write(self, values):
		for rec in self:
			rec.verificar_partner_id(values.get('to', False),values.get('relacion', False))
			rec.verificar_plantilla_mensaje(values)
		return super(Automatizacion, self).write(values)

	@api.multi
	def unlink(self):
		self.unlink_cron()
		return super(Automatizacion, self).unlink()