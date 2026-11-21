odoo.define('fundetaxcol.models', function (require) {
'use strict';

var Class = require('web.Class');
var rpc = require('web.rpc');
var core = require('web.core');

function add_cero(num) {
	if (num < 10) return '0' + num;
	return num;
};

function get_fecha() {
	var f = new Date();
	var dia = add_cero(f.getDate());
	var mes = add_cero(f.getMonth()+1);
	var year = f.getFullYear();
	var hora = add_cero(f.getHours());
	var minuto = add_cero(f.getMinutes());
	var segundo = add_cero(f.getSeconds());
	return year +"/"+ mes +"/"+ dia +" "+ hora +":"+ minuto +":"+ segundo;
};

var Sesion = Class.extend({
	init: function() {
		this.bahia_id = null;
		this.pagos = [];
		this.sesion_bahia_by_id = [];
	},
	load_context: function(bahia_id, bahia_ids) {
		var self = this;
		this.bahia_id = bahia_id;
		return rpc.query({
			model: 'fundetaxcol.pago',
			method: 'search_read',
			args: [[['bahia_id','in',bahia_ids]]],
			kwargs: {fields: ['id','vehiculo_id','conductor_id','bahia_id']}
		}).then(function(pagos) {
			self.pagos = pagos;
			return rpc.query({
				model: 'fundetaxcol.sesion.bahia',
				method: 'search_read',
				args: [[['id','in',bahia_ids]]],
				kwargs: {fields: ['id','bahia_id']}
			}).then(function(result) {
				for (var index in result) {
	    			self.sesion_bahia_by_id[result[index].bahia_id[0]] = result[index];
	    		}
			});
		});
	},
});

var Turno = Class.extend({
	init: function(options) {
		this.id = options.id || null;
		this.name = options.name || '';
		this.fecha_asignacion = options.fecha_asignacion || get_fecha();
		this.fecha_despacho = options.fecha_despacho || false;
		this.vehiculo_id = options.vehiculo_id || null;
		this.conductor_id = options.conductor_id || null;
		this.sequence = options.sequence || null;
		this.state = options.state || 'espera';
		this.bahia_id = options.bahia_id || null;
	}
});

var Model = Class.extend({
    init: function () {
        this.turnos_by_id = {};
        this.vehiculos_by_id = {};
        this.conductores_by_id = {};
        this.tarifas_by_id = {};
        this.load_models();
        this.conductores_by_vehiculo_id = {};
    },
    load_turno: function(turno_id) {
    	var self = this;
    	return rpc.query({
			model: 'fundetaxcol.turno',
			method: 'search_read',
			args: [[['id','=',turno_id]]],
			kwargs: {fields: ['id','bahia_id','name','fecha_asignacion','fecha_despacho','vehiculo_id','conductor_id','sequence','state']}
		}).then(function(turno) {
			for (var index in turno) {
				if (self.turnos_by_id.hasOwnProperty(turno[index].id)) {
					if (turno[index].state === 'despachado') {
						delete self.turnos_by_id[turno[index].id];
					}
				} else if (turno[index].state === 'espera') {
					self.turnos_by_id[turno[index].id] = turno[index];
				}
			}
		});
    },
    rpc_query: function(params, loaded) {
    	var self = this;
    	return rpc.query(params).then(function(result) {
    		loaded(self,result);
    	});
    },
    load_models: function () {
        var self = this;
        for (var index in this.models) {
        	this.rpc_query(this.models[index].params,self.models[index].loaded);
        }
    },
    models: [
    {
    	params: {
    		model: 'fundetaxcol.turno',
    		method: 'search_read',
    		args: [],
    		kwargs: {fields: ['id','bahia_id','name','fecha_asignacion','fecha_despacho','vehiculo_id','conductor_id','sequence','state','tarifa_id']}
    	},
    	loaded: function(self, turnos) {
    		for (var index in turnos) {
    			self.turnos_by_id[turnos[index].id] = turnos[index];
    		}
    	}
    },
    {
    	params: {
    		model: 'fundetaxcol.vehiculo',
    		method: 'search_read',
    		args: [],
    		kwargs: {fields: ['id', 'name']}
    	},
    	loaded: function(self, vehiculos) {
    		for (var index in vehiculos) {
    			self.vehiculos_by_id[vehiculos[index].id] = vehiculos[index];
    		}
    	}
    },
    {
    	params: {
    		model: 'res.partner',
    		method: 'search_read',
    		args: [[['conductor','=',true]]],
    		kwargs: {fields: ['id', 'name', 'fecha_vinculacion']}
    	},
    	loaded: function(self, conductores) {
    		for (var index in conductores) {
    			self.conductores_by_id[conductores[index].id] = conductores[index];
    		}
    	}
    },
    {
    	params: {
    		model: 'fundetaxcol.tarifa.sector',
    		method: 'search_read',
    		args: [],
    		kwargs: {fields: ['id', 'name', 'valor']}
    	},
    	loaded: function(self, tarifas) {
    		for (var index in tarifas) {
    			self.tarifas_by_id[tarifas[index].id] = tarifas[index];
    		}
    	}
    },
    {
    	params: {
    		model: 'fundetaxcol.vehiculo.conductor',
    		method: 'search_read',
    		args: [],
    		kwargs: {fields: ['id', 'conductor_id', 'vehiculo_id']}
    	},
    	loaded: function(self, vehiculo_conductor) {
    		for (var index in vehiculo_conductor) {
    			self.conductores_by_vehiculo_id[vehiculo_conductor[index].vehiculo_id[0]] = vehiculo_conductor[index];
    		}
    	}
    },
    ],
});

return {
    Models: Model,
    Turno: Turno,
    Sesion: Sesion,
};

});