{
    "name": """Chile - Add QBLI Field to invoices """,
    'version': '15.0.0.2',
    'category': 'Localization/Chile',
    'license': 'OPL-1',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'description': """
Adds QBLI to the invoice lines, according to requirements from some customers using SAP
=======================================================================================
//CdgItem/TpoCodigo
//CdgItem/VlrCodigo
    """,
    'website': 'http://bmya.cl',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'views/account_move_view.xml',
        'template/dte_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
