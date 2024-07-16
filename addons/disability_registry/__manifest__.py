{
    'name': 'Disability Registry',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Registro Único de Personas con Discapacidad',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/disability_support_data.xml',
        'data/disability_therapies_data.xml',
        'data/disability_transport_data.xml',
        'views/disability_registry_views.xml',
    ],
    'installable': True,
    'application': True,
}