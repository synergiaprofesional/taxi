odoo.define('fundetaxcol.ticket_client', function (require) {
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
    	return year +"/"+ mes +"/"+ dia +" "+ hora +":"+ minuto +":"+ segundo;
    },
    get_context: function(id) {
    	var self = this;
    	return rpc.query({
    		model: 'fundetaxcol.turno',
    		method: 'search_read',
    		args: [[['id','=',id]]],
    		kwargs: {fields: ['id','name','vehiculo_id','conductor_id','tarifa_id','valor','create_uid','sequence','fecha_despacho','company_id','anonimo','placa_anonima','nota']}
    	}).then(function(turno) {
            var first_turno = turno[0];
            return rpc.query({
                model: 'fundetaxcol.fundetaxcol',
                method: 'get_fecha_actual',
                args: [null, first_turno.fecha_despacho],
                kwargs: {},
            }).then(function(result) {
                first_turno.fecha_despacho = result;
                self.context = first_turno;
                return rpc.query({
                    model: 'res.company',
                    method: 'search_read',
                    args: [[['id','=',first_turno.company_id[0]]]],
                    kwargs: {fields: ['id','name','logo','report_footer','website','email','phone']}
                }).then(function(company) {
                    self.context['company'] = company[0];
                    return rpc.query({
                        model: 'fundetaxcol.vehiculo',
                        method: 'search_read',
                        args: [[['id','=',first_turno.vehiculo_id[0]]]],
                        kwargs: {fields: ['id','name','ingreso']}
                    }).then(function(vehiculo) {
                        self.context['vehiculo'] = vehiculo[0];
                    });
                });
            });
    	});
    },
});

var PrintTicketClienteWidget = Widget.extend({
	template: 'fundetaxcol.print.cliente',
	init: function(parent, options) {
		this._super.apply(this, arguments);
		this.context = options.context || {};
		this.fecha = options.fecha || '0001/01/01 00:00:00';
	},
	
});

var data = null;

ajax.loadXML('/fundetaxcol/static/src/xml/fundetaxcol.xml', qweb).done(function () {
	var $elem = $('.o_fundetaxcol_print_ticket_client');
	if (data === null) {
		data = $elem.attr('data_ticket_client');
		if (data !== undefined) {
            data = JSON.parse(data);
            if (data.flag) {
                $(window).focus(() => {
                   //window.close();
                });
                //window.close();
            }
            else {
                let footer = data.company.report_footer;
                if (footer !== '') {
                    let footers = footer.split('\n');
                    if (footers.length !== 0) {
                        data.company.report_footer = footers;
                    }
                }
                var app = new PrintTicketClienteWidget(null, {
                    context: data,
                });
                app.appendTo($elem);
                //window.print();
                //window.close();
            }
		}
	}
});

});