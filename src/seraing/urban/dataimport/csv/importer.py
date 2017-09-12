# -*- coding: utf-8 -*-
from seraing.urban.dataimport.csv import objectsmapping
from seraing.urban.dataimport.csv import valuesmapping
from seraing.urban.dataimport.csv.settings import CSVImporterSettings
from imio.urban.dataimport.config import IMPORT_FOLDER_PATH
from imio.urban.dataimport.csv.importer import CSVImportSource, CSVDataExtractor, CSVDataImporter
from imio.urban.dataimport.csv.interfaces import ICSVImportSource, ICSVImporter

from zope.interface import implements

import csv

from imio.urban.dataimport.mapping import ObjectsMapping, ValuesMapping


class SeraingCSVMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        if CSVImporterSettings.file_type == 'old':
            return objectsmapping.OBJECTS_NESTING_OLD
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        if CSVImporterSettings.file_type == 'old':
            return objectsmapping.FIELDS_MAPPINGS_OLD
        return objectsmapping.FIELDS_MAPPINGS


class SeraingCSVValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):

        return valuesmapping.VALUES_MAPS.get(mapping_name, None)
