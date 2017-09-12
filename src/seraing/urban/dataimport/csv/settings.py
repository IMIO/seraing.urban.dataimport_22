# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.importer import CSVDataImporter
from imio.urban.dataimport.csv.interfaces import ICSVImporter
from imio.urban.dataimport.browser.adapter import ImporterFromSettingsForm
from imio.urban.dataimport.browser.import_panel import ImporterSettings

from zope.interface import implements

from imio.urban.dataimport.csv.settings import CSVImporterFromImportSettings


class CSVImporterSettings(ImporterSettings):
    """
    """
    file_type = None


class SeraingCsvImporterFromImportSettings(CSVImporterFromImportSettings):
    """ """

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        CSVImporterSettings.file_type = 'new'
        settings = super(SeraingCsvImporterFromImportSettings, self).get_importer_settings()
        db_settings = {
            'key_column': 'id',
            'csv_filename': 'seraing_lotissements',
        }

        settings.update(db_settings)

        return settings

