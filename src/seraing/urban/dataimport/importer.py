# -*- coding: utf-8 -*-

from zope.interface import implements

from imio.urban.dataimport.acropole.importer import AcropoleDataImporter
from seraing.urban.dataimport.interfaces import ISeraingDataImporter


class SeraingDataImporter(AcropoleDataImporter):
    """ """

    implements(ISeraingDataImporter)
