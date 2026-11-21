/*odoo.define('impresora.AbstractWebClient', function (require) {
    "use strict";
    
    var WebClient = require('web.AbstractWebClient');
    var bus = require('bus.bus').bus;
    var Session = require('web.Session');

    var ImpresoraWebClient = WebClient.include({
        bind_events: function() {
            var self = this;
            bus.on('notification', this, function (notifications) {
                var data = notifications.filter(function (item) {
                    return item[0][1] === 'imprimir';
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
        on_notificacion_impresion: function(data) {

            if (odoo.session_info.uid == data.uid) {

                const header = data.header;
                const content = data.content;
                const impresora = data.impresora;
                const b64_pdf = data.pdf;
                const url = impresora.proxy_ip.indexOf('http://') == -1 ? 'http://' + impresora.proxy_ip : impresora.proxy_ip;
                this.connection = this.connection || new Session(undefined, url, { use_cors: true});

                const width = impresora.width || 50;
                var pdf = new jsPDF('p', 'mm', [width, 300]);

                if (header) {
                    pdf.autoTable({
                        theme: 'plain',
                        styles: { cellPadding: {top: 0, bottom: 0}, halign: 'center', fontSize: 9, fontStyle: 'bold' },
                        margin: { top: 0, left: 0, right: 0 },
                        body: header
                    });
                }
                if (content) {
                    pdf.autoTable({
                        theme: 'plain',
                        styles: { cellPadding: {top: 0, bottom: 0}, halign: 'center', fontSize: 9, fontStyle: 'bold' },
                        margin: { top: 0, left: 0, right: 0 },
                        body: content
                    });
                }
                const res = pdf.output('datauristring').split('data:application/pdf;base64,')[1];

                
                this.connection.rpc('/hw_proxy/print_xml_receipt',{ receipt: {
                    id: data.id,
                    impresora: impresora,
                    pdf: b64_pdf != null ? b64_pdf : res,
                    lines: data.lines
                }}, {timeout:5000});
            }
        },
    });
});*/

odoo.define('print_server.ActionManager', function (require) {
    "use strict";
    
    var ActionManager = require('web.ActionManager');
    var Session = require('web.Session');

    ActionManager.include({
        ir_actions_act_url: function (action, options) {
            if (action.print_server) {
                const connection = new Session(undefined, action.url, { use_cors: true });
                connection.rpc('/hw_proxy/print_xml_receipt', { receipt: action.receipt });
                return $.Deferred().resolve();
            }
            return this._super.apply(this, arguments);
        },
        ir_actions_act_window: function (action, options) {
            if (action.print_server) {
                const connection = new Session(undefined, action.url, { use_cors: true });
                connection.rpc('/hw_proxy/print_xml_receipt', { receipt: action.receipt });
            }
            return this._super.apply(this, arguments);
        },
    });
    
});