odoo.define('fundetaxcol.ActionManager', function (require) {
"use strict";

/**
 * ActionManager
 *
 * The action manager is quite important: it makes sure that actions (the Odoo
 * objects, such as a client action, or a act_window) are properly started,
 * and coordinated.
 */

    var actionManager = require('web.ActionManager');
    var framework = require('web.framework');
    var session = require('web.session');
    var WebClient = require('web.AbstractWebClient');
    var bus = require('bus.bus').bus;

    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var qweb = core.qweb;

    var PrintTicketClienteWidget = Widget.extend({
        template: 'fundetaxcol.print.cliente',
        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.context = options.context || {};
            this.fecha = options.fecha || '0001/01/01 00:00:00';
        },
        
    });

    var ActionManager = actionManager.include({
        ir_actions_act_url_print: function (action, options) {
            var url = action.url;
            if (session.debug && url && url.length && url[0] === '/') {
                url = $.param.querystring(url, {debug: session.debug});
            }
            if (action.target === 'self') {
                framework.redirect(url);
                return $.Deferred(); // The action is finished only when the redirection is done
            } else {
                window.open(url, '_blank');
                this.ir_actions_act_window_close(action, options);
            }
            return $.when();
        },
        ir_actions_act_window: function (action, options) {
            var data_to_print = action.data_to_print;
            if (data_to_print) {
                this.imprimir(data_to_print);
            }
            return this._super(action, options);            
        },
        imprimir: function (data_to_print) {
            ajax.loadXML('/fundetaxcol/static/src/xml/fundetaxcol.xml', qweb).done(function () {
                var impresion = window.open(data_to_print.url, '_blank');

                impresion.onload = function() {
                    var doc = impresion.document;
                    var newDiv = doc.createElement("div");

                    var data = data_to_print.data;

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
                    app.appendTo(newDiv);
                    doc.body.appendChild(newDiv);

                    impresion.print();
                    impresion.close();
                };
            });
        },
        ir_actions_client_print: function(action, options) {
            $('.o_loading').addClass('no_imprimir');
            $('.o_view_manager_content').addClass('no_imprimir');
            
            $('.para_imprimir').addClass('printable');
            window.print();
        },
    });

    var FundetaxcolWebClient = WebClient.include({
        bind_events: function() {
            var self = this;
            bus.on('notification', this, function (notifications) {
                var data = notifications.filter(function (item) {
                    return item[0][1] === 'fundetaxcol.print_for_url';
                }).map(function (item) {
                    return item[1];
                });
                var flat_data = _.reduceRight(data, function (a, b) {
                    return a.concat(b);
                }, []);
                for (var index in flat_data) {
                    self.on_notificacion_impresion(flat_data[index]);
                }
            });
            this._super();
        },
        on_notificacion_impresion: function(url) {
            window.open(url,'Impresión',
                'height=200,width=200,resizable=no,scrollbars=no,toolbar=no,menubar=no,location=no,directories=no,status=yes'
            );
        },
    });

return { 
    ActionManager: ActionManager,
    FundetaxcolWebClient: FundetaxcolWebClient
}

});