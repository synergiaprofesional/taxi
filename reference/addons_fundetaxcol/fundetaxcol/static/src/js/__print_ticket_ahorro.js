odoo.define('fundetaxcol.ticket_ahorro', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var qweb = core.qweb;
var Widget = require('web.Widget');

var PrintAhorroWidget = Widget.extend({
    template: 'fundetaxcol.ahorro',
    init: function(parent, options) {
        this._super.apply(this, arguments);
        this.context = options.context || {};
        this.fecha = options.fecha || '2000/01/01 00:00:00';
    },
    
});

var PrintTicketAhorroWidget = Widget.extend({
	template: 'fundetaxcol.print.ahorro',
	init: function(parent, options) {
		this._super.apply(this, arguments);
		this.context = options.context || {};
		this.fecha = options.fecha || '0001/01/01 00:00:00';
	},
	
});

var data = null;

ajax.loadXML('/fundetaxcol/static/src/xml/fundetaxcol.xml', qweb).done(function () {


    var $elem = $('.o_fundetaxcol_print_ahorro');
    if (data === null) {
        data = $elem.attr('data_ahorro');
        if (data !== undefined) {
            data = JSON.parse(data);
            let footer = data.company.report_footer;
            if (footer !== '') {
                let footers = footer.split('\n');
                if (footers.length !== 0) {
                    data.company.report_footer = footers;
                }
            }
            var app = new PrintAhorroWidget(null, {
                context: data,
            });
            app.appendTo($elem);
            window.print();
            window.close();
        }
    }


	var $elem = $('.o_fundetaxcol_print_ticket_ahorro');
	if (data === null) {
		data = $elem.attr('data_ticket_ahorro');
		if (data !== undefined) {
            data = JSON.parse(data);
            let footer = data.company.report_footer;
            if (footer !== '') {
                let footers = footer.split('\n');
                if (footers.length !== 0) {
                    data.company.report_footer = footers;
                }
            }
            var app = new PrintTicketAhorroWidget(null, {
                context: data,
            });
            app.appendTo($elem);
            window.print();
            window.close();
		}
	}
});

});