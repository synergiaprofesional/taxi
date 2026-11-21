odoo.define('fundetaxcol.tablero_turnos', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var qweb = core.qweb;
    var Widget = require('web.Widget');
    var bus = require('bus.bus').bus;

    var TurnoWidget = Widget.extend({
        template: 'fundetaxcol.turno.actual',
        init: function (turno) {
            this._super.apply(this, arguments);
            this.turno_actual = turno;
        },
        set_turno: function (turno) {
            const animar = this.turno_actual != turno;
            this.turno_actual = turno;
            this.appendTo($('.fundetaxcol_turno_actual'));
            if (animar) this.animar_turno_actual();
        },
        animar_turno_actual: function () {
            $('.o_turno_actual_internal').css({
                'animation-play-state': 'running'
            });
        },
    });


    var TurnoListWidget = Widget.extend({
        template: 'fundetaxcol.turno.list',
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.name = parent.name;
            this.bahia_id = parent.bahia_id;
            this.turnos_by_id = {};
            this.turnos = [];
            this.turnoWidget = new TurnoWidget(null);
        },
        load_turnos: function (company_id) {
            var self = this;
            return rpc.query({
                model: 'fundetaxcol.turno',
                method: 'search_read',
                args: [
                    [
                        ['bahia_id', '=', self.bahia_id],
                        ['state', 'not in', ['cancelado', 'despachado']],
                    ]
                ],
                kwargs: {
                    fields: ['id', 'state', 'sequence', 'vehiculo_id', 'conductor_id', 'bahia_id', 'anonimo']
                },
            }).then(function (turnos) {
                self.turnos = turnos.sort(function (a, b) {
                    return a.sequence - b.sequence;
                });
                const turno_actual = turnos.find(x => x.state == 'actual');
                self.turnoWidget.set_turno(turno_actual);
                self.appendTo($('.fundetaxcol_turno_list'));
            });
        },
    });

    var TableroTurnoWidget = Widget.extend({
        template: 'fundetaxcol.tablero.turnos',
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.name = options.name;
            this.bahia_id = options.bahia_id;
            this.user_id = odoo.session_info.user_id;
            this.company_id = odoo.session_info.company_id;
            this.listWidget = new TurnoListWidget(this);
        },
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                bus.on('notification', this, function (notifications) {
                    var turno = notifications.filter(function (item) {
                        return item[0][1] === 'fundetaxcol.turno.channel';
                    }).map(function (item) {
                        return item[1];
                    });
                    var flat_turno = _.reduceRight(turno, function (a, b) {
                        return a.concat(b);
                    }, []);
                    for (var index in flat_turno) {
                        if (self.bahia_id === flat_turno[index].bahia_id[0]) {
                            self.listWidget.load_turnos(self.company_id);
                        }
                    }

                });
                self.listWidget.load_turnos(self.company_id);
            });
        },
    });

    ajax.loadXML('/fundetaxcol/static/src/xml/fundetaxcol_tablero_turno.xml', qweb).done(function () {
        var $elem = $('.o_fundetaxcol_tablero_turnos');
        var data = $elem.attr('data_sesion_bahia_id');
        var name = $elem.attr('data-name');
        if (data !== undefined) {
            data = JSON.parse(data);
            var app = new TableroTurnoWidget(null, {
                bahia_id: data,
                name,
            });
            app.appendTo($elem).then(function () {});
        }
    });

});