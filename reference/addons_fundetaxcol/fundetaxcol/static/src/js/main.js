odoo.define('fundetaxcol.main', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var models = require('fundetaxcol.models');
var qweb = core.qweb;
var Widget = require('web.Widget');

var Turno = require('fundetaxcol.turnos');

var FundetaxcolApp = Widget.extend({
    template: 'fundetaxcol.app',
    events: {
    	'click a[name=turnos]': 'event_handler_turnos',
    	'click a[name=asignar_turno]': 'event_handler_asignar_turno',
    	'click a[name=turnos_despachados]': 'event_handler_turnos_despachados',
    },
    _onClickBody: function() {
    	console.log(this)
    },
    init: function (parent, options) {
    	var self = this;
        this._super.apply(this, arguments);
        this.models = options.models;
        this.context = options.context || {};
        var self = this;
        core.bus.on('nuevo_turno', this, function(id) {
        	self.models.load_turno(id).done(function() {
        		self.event_handler_turnos();
        	});
        });
    },
    event_handler_turnos: function() {
    	var self = this;
    	var turno_list = new Turno.TurnoWidget(this, {states: ['actual','espera']});
    	this.load_content(turno_list, function() {
    		$('div[name=fundetaxcol_turno]').each(function(index) {
    			var elemento = $('div[name=fundetaxcol_turno]')[index];
    			var turno_id = $(elemento).data('id');
    			var turno = self.models.turnos_by_id[turno_id];
    			if (turno.state === 'actual') {
    				$(elemento).addClass('turno_actual');
    			}
    		});
    	});
    	this.hide_menu();
    	$('.f_content').click(function() {
        	self.hide_menu();
        });
    	this.change_opacity();
    },
    event_handler_asignar_turno: function() {
    	var turno = new Turno.TurnoWidget(this);
    	var sesion_bahia_id = this.context.sesion_bahia_by_id[this.context.bahia_id].id;
    	turno.new_turno(sesion_bahia_id);
    	this.hide_menu();
    },
    event_handler_turnos_despachados: function() {
    	var self = this;
    	var turno_list = new Turno.TurnoWidget(this, {states: ['despachado']});
    	this.load_content(turno_list, function() {
    		//$('div[name=fundetaxcol_turno]').each(function(index) {
    		//	var elemento = $('div[name=fundetaxcol_turno]')[index];
    		//	var turno_id = $(elemento).data('id');
    		//	var turno = self.models.turnos_by_id[turno_id];
    		//	if (turno.state === 'actual') {
    		//		$(elemento).addClass('turno_actual');
    		//	}
    		//});
    	});
    	this.hide_menu();
    	$('.f_content').click(function() {
        	self.hide_menu();
        });
    	this.change_opacity();
    },
    change_opacity: function() {
    	$('#btn-menu').click(function() {
    		if (($('#btn-menu')[0].checked)) {
    			$('body').css({'background':'rgba(0,0,0,0.5)'});
    		} else {
    			$('body').css({'background':'rgba(0,0,0,0)'});
    		}
    	});
    },
    hide_menu: function() {
    	if ($('#btn-menu')[0].checked) $('#btn-menu').trigger('click');
    	$('body').css({'background':'rgba(0,0,0,0)'});
    },
    load_content: function(view, callback) {
    	var content = $('#content');
    	content.empty();
    	view.appendTo(content).then(callback);
    },
});

ajax.loadXML('/fundetaxcol/static/src/xml/fundetaxcol.xml', qweb).done(function () {
	var $elem = $('.o_fundetaxcol_app');
	var data = $elem.attr('data');
	if (data !== undefined) {
		data = JSON.parse(data);
		var sesion = new models.Sesion();
		var mds = new models.Models();
		sesion.load_context(data.bahia_id, data.sesion_bahia_ids).done(function () {
			var app = new FundetaxcolApp(null, {data: data, context: sesion, models: mds,});
			app.appendTo($elem).then(function() {
				app.event_handler_turnos();
			});
		});
	}
});

});