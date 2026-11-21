odoo.define('fundetaxcol.print', function (require) {
'use strict';

var ajax = require('web.ajax');
var Class = require('web.Class');
var core = require('web.core');
var qweb = core.qweb;
var rpc = require('web.rpc');
var Widget = require('web.Widget');

var Model = Class.extend({
    init: function () {
		this.context = {};
		this.fecha = this.get_fecha();
    },
    add_cero: function(num) {
    	if (num < 10) return '0' + num;
    	return num;
    },
    get_fecha: function() {
    	var f = new Date();
    	var dia = this.add_cero(f.getDate());
    	var mes = this.add_cero(f.getMonth()+1);
    	var year = f.getFullYear();
    	var hora = this.add_cero(f.getHours());
    	var minuto = this.add_cero(f.getMinutes());
    	var segundo = this.add_cero(f.getSeconds());
    	return year +"-"+ mes +"-"+ dia +" "+ hora +":"+ minuto +":"+ segundo;
    },
    get_fecha_from_fundetaxcol: function(fecha) {
    },
    get_context: function(id) {
    	var self = this;
    	return rpc.query({
    		model: 'fundetaxcol.pago',
    		method: 'search_read',
    		args: [[['id','=',id]]],
    		kwargs: {fields: ['id','name','consecutivo','fecha','vehiculo_id','conductor_id','concepto_ids','valor','company_id', 'create_uid']}
    	}).then(function(pago) {
            var first_pago = pago[0];
    		return rpc.query({
    			model: 'res.company',
	    		method: 'search_read',
	    		args: [[['id','=',first_pago.company_id[0]]]],
	    		kwargs: {fields: ['id','name','logo','report_footer','website','email','phone']}
    		}).then(function(company) {
    			first_pago['company'] = company[0];
    			return rpc.query({
    				model: 'fundetaxcol.vehiculo',
    				method: 'search_read',
    				args: [[['id','=',first_pago.vehiculo_id[0]]]],
    				kwargs: {fields: ['id','name','ingreso']}
    			}).then(function(vehiculo) {
    				first_pago['vehiculo'] = vehiculo[0];
    				return rpc.query({
		    			model: 'fundetaxcol.pago.concepto',
			    		method: 'search_read',
			    		args: [[['id','in',first_pago.concepto_ids]]],
			    		kwargs: {fields: ['id','pago_id','concepto_id','cantidad','valor','subtotal']}
		    		}).then(function(conceptos) {
		    			first_pago['conceptos'] = conceptos;
                        return rpc.query({
                            model: 'fundetaxcol.fundetaxcol',
                            method: 'get_fecha_actual',
                            args: [null, first_pago.fecha],
                            kwargs: {},
                        }).then(function(result) {
                            first_pago.fecha = result;
                            self.context = first_pago;
                        });
		    		});
    			});
    		});
    	});
    },
});

var PrintTicketWidget = Widget.extend({
	template: 'fundetaxcol.print.pago',
	init: function(parent, options) {
		this._super.apply(this, arguments);
		this.context = options.context || {};
		this.fecha = options.fecha || '0001/01/01 00:00:00';
	},
	
});

var data = null;

ajax.loadXML('/fundetaxcol/static/src/xml/fundetaxcol.xml', qweb).done(function () {
	var $elem = $('.o_fundetaxcol_print_ticket');
	var models = new Model();
	if (data === null) {
		data = $elem.attr('data_pago');
		if (data !== undefined) {
            data = JSON.parse(data);
            let footer = data.company.report_footer;
            if (footer !== '') {
                let footers = footer.split('\n');
                if (footers.length !== 0) {
                    data.company.report_footer = footers;
                }
            }
            var app = new PrintTicketWidget(null, {
                context: data,
            });
            app.appendTo($elem);
            window.print();
            window.close();

			//var defered = models.get_context(parseInt(data));
			//defered.done(function() {
			//	var app = new PrintTicketWidget(null, {
			//		fecha_actual: models.fecha,
			//		context: models.context,
			//	});
			//	app.appendTo($elem);
			//	window.print();
            //    window.close();
			//});
		}
	}
});

});