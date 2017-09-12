# -*- coding: utf-8 -*-

from seraing.urban.dataimport.csv.mappers import *
from imio.urban.dataimport.mapper import SimpleMapper

OBJECTS_NESTING = [
    (
        'PARCELLINGS',
        [],
    )
]

FIELDS_MAPPINGS = {
    'PARCELLINGS':
    {
        'factory': [ParcellingsFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': "Libellé",
                    'to': 'label',
                },
                {
                    'from': 'Nom_du_lotisseur',
                    'to': 'subdividerName',
                },
                {
                    'from': 'Date_dautorisation',
                    'to': 'authorizationDate',
                },
                {
                    'from': 'Date_dapprobation',
                    'to': 'approvalDate',
                },
                {
                    'from': 'Nombre_de_lots',
                    'to': 'numberOfParcels',
                },
                {
                    'from': 'Modifications_du_lotissement',
                    'to': 'changesDescription',
                },
            ),

            IdMapper: {
                'from': 'ID',
                'to': 'id',
            },

            PortalTypeMapper: {
                'from': 'Type',
                'to': ('portal_type', 'folderCategory',)
            },

            ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },
}