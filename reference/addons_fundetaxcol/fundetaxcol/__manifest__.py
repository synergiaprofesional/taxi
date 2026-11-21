# -*- coding: utf-8 -*-
{
    'name': "fundetaxcol",
    'summary': """""",
    'description': """""",
    'author': "Synergia Profesional SAS",
    'website': "http://www.synergiaprofesional.com",
    'category': 'Fundetaxcol',
    'version': '2.0',
    'depends': ['bus','base_setup'],
    'application': True,
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        #administracion
        'views/_menu_root.xml',
        'views/_administrador_menu_view.xml',
        'views/app_view.xml',
        'views/bahia_view.xml',
        'views/barrio_view.xml',
        'views/concepto_view.xml',
        'views/conductor_view.xml',
        'views/tarifa_view.xml',
        'views/vehiculo_view.xml',
        #
        'views/sesion_view.xml',
        #modulos
        'views/pago_view.xml',
        
        'views/turno_view.xml',
        'views/ajuste_view.xml',

        #configuracion
        'views/config_view.xml',
        'views/ticket_secuencia_view.xml',
        #templates
        'views/fundetaxcol_templates.xml',
        #reports
        'report/_report_menu.xml',
        'report/sesion_report_template.xml',
        'report/bahia_sesion_report_template.xml',

        'report/report_pago_template.xml',
        'report/report_despacho_template.xml',
        #wizards
        'wizard/ahorro_wizard_view.xml',
        'wizard/report_ruta_xml.xml',
        'wizard/report_ruta_template_xml.xml',

        'wizard/wizard_utilidad_conductor_repetido_view.xml',
        'wizard/wizard_utilidad_clasificar_conceptos.xml',

        'views/ahorro_view.xml',
        'views/transaccion_view.xml',

        'views/credito_view.xml',
        'report/credito_report.xml',

        'wizard/report_temperatura_limpieza.xml',
        # 'wizard/report_cartera.xml',
    ],
    #'qweb': ['static/src/xml/*.xml'],
}
