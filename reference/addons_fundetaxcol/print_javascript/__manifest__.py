# -*- coding: utf-8 -*-
{
    'name': "Impresión Ticketes",
    'summary': """
        Impresión Javascript Desde Servidor
    """,
    'description': """
        Este módulo implementa longpolling para enviar datos al cliente, 
        y éste se encargará de enviar una petición a un servidor local en node el 
        cual imprimirá en impresora térmica
    """,
    'author': "Synergia Profesional SAS",
    'website': "http://www.synergiaprofesional.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'bus'],
    'data': [
        'security/ir.model.access.csv',
        'views/app_view.xml',
        'views/templates.xml',
        'views/impresora_view.xml',
    ],
}