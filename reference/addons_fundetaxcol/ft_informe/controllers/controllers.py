# -*- coding: utf-8 -*-

from odoo import http, exceptions, api
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception, content_disposition

import io
import xlwt

from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class FtInforme(http.Controller):

    def update_row_dupl(self, pago, matriz, cols):
        if len(matriz) == 0:
            return False
        for i in range(1, len(matriz)):
            if matriz[i][0] == pago.conductor_id.id:
                if matriz[i][1] == pago.vehiculo_id.id:
                    row = matriz[i]
                    for concepto in pago.mapped('concepto_ids'):
                        row[cols.index(concepto.concepto_id.name)
                            ] += concepto.subtotal
                    return True
        return False

    @api.model
    def get_concepts(self, inicio, fin):
        sql_sttmt_ingresos = '''
            SELECT 
                c.id AS concepto_id,
                c.name AS concepto,
                conductor.id AS conductor_id,
                vehiculo.id AS vehiculo_id,
                SUM(conc.cantidad * conc.valor) AS total
            FROM 
                fundetaxcol_pago AS pago
            INNER JOIN 
                fundetaxcol_pago_concepto AS conc
            ON 
                pago.id = conc.pago_id
            INNER JOIN 
                res_partner AS conductor
            ON 
                pago.conductor_id = conductor.id
            INNER JOIN 
                fundetaxcol_vehiculo AS vehiculo
            ON 
                pago.vehiculo_id = vehiculo.id
            INNER JOIN 
                fundetaxcol_concepto AS c
            ON 
                c.id = conc.concepto_id
            WHERE 
                pago.fecha >= %s 
                AND pago.fecha <= %s
            GROUP BY 
                c.id,
                conductor.id,
                vehiculo.id;
        '''
        request.env.cr.execute(
            sql_sttmt_ingresos, (inicio, fin),
        )
        return request.env.cr.dictfetchall()

    @api.model
    def get_ins(self, inicio, fin):
        sql_sttmt_ingresos = '''
            SELECT 
                conductor.id AS conductor_id,
                vehiculo.id AS vehiculo_id,
                conductor.name AS conductor,
                vehiculo.name AS placa,
                conductor.identificacion AS identificacion,
                conductor.street AS direccion,
                conductor.phone AS telefono,
                conductor.mobile AS celular,
                conductor.email AS email, 
                SUM(conc.cantidad) AS ingresos
            FROM 
                fundetaxcol_pago AS pago
            INNER JOIN 
                fundetaxcol_pago_concepto AS conc
            ON 
                pago.id = conc.pago_id
            INNER JOIN 
                res_partner AS conductor
            ON 
                pago.conductor_id = conductor.id
            INNER JOIN 
                fundetaxcol_vehiculo AS vehiculo
            ON 
                pago.vehiculo_id = vehiculo.id
            INNER JOIN 
                fundetaxcol_concepto AS c
            ON 
                c.id = conc.concepto_id
            WHERE 
                pago.fecha >= %s
                AND pago.fecha <= %s
                AND c.clasificacion = 'ingreso'
            GROUP BY 
                conductor.id,
                vehiculo.id,
                conductor.name,
                vehiculo.name,
                conductor.identificacion,
                conductor.street,
                conductor.phone,
                conductor.mobile,
                conductor.email
            ORDER BY 
                conductor.name;
        '''
        request.env.cr.execute(
            sql_sttmt_ingresos, (inicio, fin),
        )
        return request.env.cr.dictfetchall()

    def get_data(self, start_at, stop_at, agrupar, mostrar_ingresos_del_mes):
        App = request.env['fundetaxcol.fundetaxcol']
        inicio = App.get_fecha_actual('%s 00:00:00' % start_at)
        fin = App.get_fecha_actual('%s 23:59:59' % stop_at)

        agrupado = agrupar == 'True'
        mostrar_ingresos = mostrar_ingresos_del_mes == 'True'

        ingresos = self.get_ins(inicio, fin)
        conceptos = self.get_concepts(inicio, fin)

        def compare_key(item1, item2, key):
            return item1.get(key) == item2.get(key)

        def get_concepto_id(concepto, ingreso):
            c = compare_key(concepto, ingreso, 'conductor_id')
            v = compare_key(concepto, ingreso, 'vehiculo_id')
            return c and v

        concept_ids = []
        for concepto in conceptos:
            exists = len(list(filter(
                lambda x: compare_key(x, concepto, 'concepto_id'),
                concept_ids,
            )))
            if not exists:
                concepto_copia = concepto.copy()
                concept_ids.append(concepto_copia)

        def update_ingreso(ingreso):
            conceptos_por_conductor = list(filter(
                lambda x: get_concepto_id(x, ingreso),
                conceptos,
            ))
            for concepto in concept_ids:
                exists = len(list(filter(
                    lambda x: compare_key(x, concepto, 'concepto_id'),
                    conceptos_por_conductor
                )))
                if not exists:
                    concepto_copy = concepto.copy()
                    concepto_copy.update({
                        'conductor_id': ingreso.get('conductor_id'),
                        'vehiculo_id': ingreso.get('vehiculo_id'),
                        'total': 0,
                    })
                    conceptos_por_conductor.append(concepto_copy)
            ingreso['concepto_ids'] = conceptos_por_conductor
            return ingreso

        ingresos = list(map(update_ingreso, ingresos))

        matriz = []
        keys = list(map(lambda x: x.get('concepto_id'), concept_ids))
        keys_sorted = sorted(keys)
        cols = [
            # '__cid__',
            # '__vid__',
            # 'FECHA',
            'CONDUCTOR',
            'PLACA',
            'IDENTIFICACION',
            'DIRECCION',
            'TELEFONO',
            'CELULAR',
            'EMAIL'
        ]
        if agrupado and mostrar_ingresos:
            cols.append('INGRESOS DESDE %s HASTA %s' % (start_at, stop_at))

        def get_concept_by_id(id, array):
            return list(filter(
                lambda x: x.get('concepto_id') == id,
                array,
            ))[0]

        for concept_id in keys_sorted:
            concepto = get_concept_by_id(concept_id, concept_ids)
            cols.append(concepto.get('concepto'))

        matriz.append(cols)

        def update_none(data):
            if 'None' == str(data):
                return ''
            return data

        for ingreso in ingresos:
            col = [
                ingreso.get('conductor'),
                ingreso.get('placa'),
                update_none(ingreso.get('identificacion', '')),
                update_none(ingreso.get('direccion', '')),
                update_none(ingreso.get('telefono', '')),
                update_none(ingreso.get('celular', '')),
                update_none(ingreso.get('email', '')),
                ingreso.get('ingresos', 0)
            ]
            for concept_id in keys_sorted:
                concepto = get_concept_by_id(
                    concept_id, ingreso.get('concepto_ids', []))
                col.append(concepto.get('total'))
            matriz.append(col)

        return matriz, len(cols), len(matriz)

    @http.route('/web/binary/download_document', type='http', auth='user')
    def download_document(self, start_at, stop_at, group, mostrar_ingresos_del_mes, **kw):
        filename = 'Pagos desde %s hasta %s.xls' % (start_at, stop_at)

        self.get_data(
            start_at, stop_at, group, mostrar_ingresos_del_mes)
        datas, cols, rows = self.get_data(
            start_at, stop_at, group, mostrar_ingresos_del_mes)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Pagos')

        for i in range(0, rows):
            for j in range(0, cols):
                ws.write(i, j, datas[i][j])

        fp = io.BytesIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()

        return request.make_response(
            data,
            headers=[
                ('Content-Disposition', content_disposition(filename)),
                ('Content-Type', 'application/octet-stream')
            ],
        )
