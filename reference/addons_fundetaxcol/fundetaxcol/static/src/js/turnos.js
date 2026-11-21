odoo.define('fundetaxcol.turnos', function (require) {
'use strict';

var Widget = require('web.Widget');
var core = require('web.core');
var Dialog = require('web.Dialog');
var models = require('fundetaxcol.models');
var rpc = require('web.rpc');
var qweb = core.qweb;

var TurnoWidget = Widget.extend({
	template: 'fundetaxcol.turno',
	events: {
		'click a[name=despachar_turno]': '_onDespacharTurno',
		'click a[name=ceder_turno]': '_onCederTurno',
		'click a[name=pausar_turno]': '_onPausarTurno',
		'click a[name=cancelar_turno]': '_onCancelarTurno',
		'click a[name=reanudar_turno]': '_onReaundarTurno',
	},
	_onDespacharTurno: function() {
		var content = qweb.render('fundetaxcol.despachar.turno', {widget: this});
		var asignar_turno = new AsignarTurnoDialog(this, {
			title: 'Despachar Turno',
			$content: content,
			buttons: [{
				text: 'Aceptar',
				click: function() {
					this._onDespacharTurno();
				},
			},],
		});
		asignar_turno.parent = this;
		asignar_turno.open();
	},
	_onCederTurno: function() {
		console.log(this)
	},
	_onPausarTurno: function() {
		console.log(this)
	},
	_onCancelarTurno: function() {
		console.log(this)
	},
	_onReaundarTurno: function() {
		console.log(this)
	},
	init: function(parent, options) {
		this._super.apply(this, arguments);
		this.turno = null;
		this.turnos = [];
		this.tarifas = [];
		this.parent = parent;
		this.pagos = parent.context.pagos;
		for (var index in parent.models.tarifas_by_id) {
			this.tarifas.push(parent.models.tarifas_by_id[index]);
		}
		let turnos_by_id = parent.models.turnos_by_id;
		for (var index in turnos_by_id) {
			if (options != null) {
				if (options.states !== null) {
					if (options.states.indexOf(turnos_by_id[index].state) != -1) {
						this.turnos.push(turnos_by_id[index]);
					}
				}
			}
		}
		this.vehiculos = [];
		for (var index in parent.models.vehiculos_by_id) {
			let v = parent.models.vehiculos_by_id[index];
			if (!this.vehiculo_en_turno(v.id)) {
				this.vehiculos.push(v);
			}
		}
		this.conductores = [];
		for (var index in parent.models.conductores_by_id) {
			let c = parent.models.conductores_by_id[index];
			if (!this.conductor_en_turno(c.id)) {
				this.conductores.push(c);
			}
		}
		this.ordenar_turnos();

		//this.print_ticket_client();
	},
	ordenar_turnos: function() {
		var turnos = this.turnos.sort(function(a,b) {
			return a.sequence - b.sequence;
		});
		this.select_turno();
		//buscar estado [pausa] y ponerlos al final, por orden de secuencia
		//excluir estados [cancelado, despachado]
	},
	print_ticket_client: function() {
		window.open('/print/ticket_client');
	},
	select_turno: function() {
		if (this.turnos.length != 0) {
			this.turno = this.turnos[0];
			for (var index in this.turnos) {
				if (this.turnos[index].state == 'espera') {
					this.turno = this.turnos[index];
					this.turno.state = 'actual';
					break;
				}
			}
		}
	},
	conductor_en_turno: function(conductor_id) {
		for (var index in this.turnos) {
			if (this.turnos[index].conductor_id[0] == conductor_id) {
				return true;
			}
		}
		return false;
	},
	vehiculo_en_turno: function(vehiculo_id) {
		let pago = false;
		for (var index in this.pagos) {
			if (this.pagos[index].vehiculo_id[0] === vehiculo_id) {
				pago = true;
				break;
			}
		}
		if (!pago) return true;
		for (var index in this.turnos) {
			if (this.turnos[index].vehiculo_id[0] == vehiculo_id) {
				return true;
			}
		}
		return false;
	},
	get_numero_turno: function(sesion_bahia_id) {
		return rpc.query({
			model: 'fundetaxcol.sesion.bahia',
			method: 'search_read',
			args: [[['id','=',sesion_bahia_id]]],
			kwargs: {fields: ['turno_actual']}
		}).then(function(result) {
			return result[0].turno_actual;
		})
	},
	new_turno: function(bahia_id) {
		var self = this;
		this.get_numero_turno(bahia_id).done(function(turno) {
			self.turno = new models.Turno({'bahia_id': bahia_id, 'sequence': turno,});
			var content = qweb.render('fundetaxcol.asignar.turno', {widget: self,});
			var new_turno = new AsignarTurnoDialog(self, {
				title: 'Asignar Turno',
				$content: content,
				buttons: [{
					text: 'Aceptar',
					click: function() {
						this._onAsignarTurno();
					},
				},],
			});
			new_turno.parent = self;
			new_turno.open();
		});
	}
});

var PrintTicketCliente = Widget.extend({
	template: 'fundetaxcol.print.ticket.cliente',
	init: function(parent, options) {},
});

var AsignarTurnoDialog = Dialog.extend({
	events: {
		'change select[name=vehiculo_id]': 'select_conductor',
	},
	open: function() {
		this._super();
	},
	select_conductor: function() {
		var vehiculo_id = $('select[name=vehiculo_id]').val();
		$('select[name=conductor_id]').val(this.parent.parent.models.conductores_by_vehiculo_id[vehiculo_id].conductor_id[0])
	},
	_onDespacharTurno: function() {
		var self = this;
		this.parent.turno.tarifa_id = $('select[name=tarifa_id]').val();
		console.log(this.parent.turno)
		this.query('despachar_from_ui', this.parent.turno, function(id) {
			core.bus.trigger('nuevo_turno', id);
		})
	},
	query : function(method, turno, callback) {
		var self = this;
		rpc.query({
				model: 'fundetaxcol.turno',
	    		method: method,
	    		args: [turno],
			}).then(function(result) {
	    		callback(result);
	    		self.close();
	    	}, function(err) {
	    		new Dialog(self, {
	    			title: 'Error',
	    			$content: "<p>Ha ocurrido un error, por favor intente de nuevo...</p>",
	    			buttons: [{
	    				text: 'Ok',
	    				close: true,
	    			}]
	    		}).open();
	    		console.log(err);
	    	});
	},
	_onAsignarTurno: function() {
		var self = this;
		this.parent.turno.vehiculo_id = $('select[name=vehiculo_id]').val();
		this.parent.turno.conductor_id = $('select[name=conductor_id]').val();
		if (this.parent.turno.vehiculo_id == null || this.parent.turno.conductor_id == null) {
			new Dialog(self, {
	    			title: 'Error',
	    			$content: "<p>Todos los campos son obligatorios...</p>",
	    			buttons: [{
	    				text: 'Ok',
	    				close: true,
	    			}]
	    		}).open();
		} else {
			this.query('create',this.parent.turno, function(id) {
				core.bus.trigger('nuevo_turno', id);
			});
		}
	},
});

return {
	TurnoWidget: TurnoWidget,
}

});