# -*- coding: utf-8 -*-
import unicodedata

import datetime

from seraing.urban.dataimport.csv.settings import CSVImporterSettings
from seraing.urban.dataimport.csv.utils import get_state_from_licences_dates, get_date_from_licences_dates, \
    load_architects, load_geometers, load_notaries, load_parcellings, get_point_and_digits
from imio.urban.dataimport.config import IMPORT_FOLDER_PATH

from imio.urban.dataimport.exceptions import NoObjectToCreateException

from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.mapper import Mapper, FinalMapper, PostCreationMapper
from imio.urban.dataimport.utils import CadastralReference
from imio.urban.dataimport.utils import cleanAndSplitWord
from imio.urban.dataimport.utils import guess_cadastral_reference
from imio.urban.dataimport.utils import identify_parcel_abbreviations
from imio.urban.dataimport.utils import parse_cadastral_reference

from DateTime import DateTime
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import safe_unicode

from plone import api
from plone.i18n.normalizer import idnormalizer

import re

import os

#
# LICENCE
#

# factory


class ParcellingsFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        path = '%s/urban/%s' % (self.site.absolute_url_path(), 'parcellings')
        return self.site.restrictedTraverse(path)

# mappers


class IdMapper(Mapper):

    def __init__(self, importer, args):
        super(IdMapper, self).__init__(importer, args)
        # load_parcellings()

    def mapId(self, line):
        return normalizeString("parcelling" + self.getData('ID'))


class PortalTypeMapper(Mapper):
    def mapPortal_type(self, line):
        return 'ParcellingTerm'

    def mapFoldercategory(self, line):
        foldercategory = 'uat'
        return foldercategory


class ErrorsMapper(FinalMapper):
    def mapDescription(self, line, plone_object):

        line_number = self.importer.current_line
        errors = self.importer.errors.get(line_number, None)
        description = plone_object.Description()

        error_trace = []
        if errors:
            for error in errors:
                data = error.data
                if 'streets' in error.message:
                    error_trace.append('<p>adresse : %s</p>' % data['address'])
                elif 'notaries' in error.message:
                    error_trace.append('<p>notaire : %s %s %s</p>' % (data['title'], data['firstname'], data['name']))
                elif 'architects' in error.message:
                    error_trace.append('<p>architecte : %s</p>' % data['raw_name'])
                elif 'geometricians' in error.message:
                    error_trace.append('<p>géomètre : %s</p>' % data['raw_name'])
                elif 'parcels' in error.message and CSVImporterSettings.file_type == 'old':
                    error_trace.append('<p>parcels : %s </p>' % data['args'])
                elif 'rubric' in error.message.lower():
                    error_trace.append('<p>Rubrique non trouvée : %s</p>' % (data['rubric']))
                elif 'parcelling' in error.message:
                    if data['search result'] == '0':
                        error_trace.append('<p>lotissement non trouvé : %s </p>' % data['titre'])
                    else:
                        error_trace.append("<p>lotissement trouvé plus d'une fois: %s : %s fois</p>" % (data['titre'], data['search result'] ))
                elif 'article' in error.message.lower():
                    error_trace.append('<p>Articles de l\'enquête : %s</p>' % (data['articles']))
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)

# *** Utils ***

class Utils():
    @staticmethod
    def convertToUnicode(string):

        if isinstance(string, unicode):
            return string

        # convert to unicode if necessary, against iso-8859-1 : iso-8859-15 add € and oe characters
        data = ""
        if string and isinstance(string, str):
            try:
                data = unicodedata.normalize('NFKC', unicode(string, "iso-8859-15"))
            except UnicodeDecodeError:
                import ipdb; ipdb.set_trace() # TODO REMOVE BREAKPOINT
        return data

    @staticmethod
    def createArchitect(name):

        idArchitect = idnormalizer.normalize(name + 'Architect').replace(" ", "")
        containerArchitects = api.content.get(path='/urban/architects')

        if idArchitect not in containerArchitects.objectIds():
            new_id = idArchitect
            new_name1 = name

            if not (new_id in containerArchitects.objectIds()):
                    object_id = containerArchitects.invokeFactory('Architect', id=new_id,
                                                        name1=new_name1)

    @staticmethod
    def createGeometrician(name1, name2):

        idGeometrician = idnormalizer.normalize(name1 + name2 + 'Geometrician').replace(" ", "")
        containerGeometricians = api.content.get(path='/urban/geometricians')

        if idGeometrician not in containerGeometricians.objectIds():
            new_id = idGeometrician
            new_name1 = name1
            new_name2 = name2

            if not (new_id in containerGeometricians.objectIds()):
                    object_id = containerGeometricians.invokeFactory('Geometrician', id=new_id,
                                                        name1=new_name1,
                                                        name2=new_name2)