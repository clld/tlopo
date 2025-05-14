from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, IdCol, RefsCol, LinkToMapCol, DataTable, DetailsRowLinkCol
from clld.db.models import common
from clld.web.util.helpers import map_marker_img


from tlopo import models

   
class Chapters(datatables.Contributions):
    def col_defs(self):
        return [
            IdCol(self, 'id'),
            LinkCol(self, 'name'),
        ]


class Languages(datatables.Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class Cognatesets(datatables.Parameters):
    __constraints__ = [common.Contribution]

    def base_query(self, query):
        query = datatables.Parameters.base_query(self, query)
        if self.contribution:
            #query.join(models.Cognateset.chapter)
            query = query.filter(models.Cognateset.chapter == self.contribution)
        return query

    def col_defs(self):
        if self.contribution:
            return [
                LinkCol(self, 'reconstruction'),
                DetailsRowLinkCol(self, 'reflexes'),
            ]

        return [
            LinkCol(self, 'reconstruction', model_col=common.Parameter.name),
            LinkCol(self, 'chapter', get_object=lambda i: i.chapter),
            DetailsRowLinkCol(self, 'reflexes'),
            ]


class GroupCol(Col):
    def format(self, item):
        return map_marker_img(self.dt.req, item.valueset) + item.valueset.language.group

    def order(self):
        return models.Languoid.group


class Word(datatables.Values):

    def get_options(self):
        opts = super(datatables.Values, self).get_options()
        if self.parameter:
            opts['aaSorting'] = [
                [0, 'asc'], [1, 'asc']]
        #if self.language:
        #    opts['aaSorting'] = [[0, 'asc'], [2, 'asc']]
        return opts

    def base_query(self, query):
        q = datatables.Values.base_query(self, query)
        # if not language or parameter, join and load valueset.language!
        if self.parameter:
            q = q.join(common.ValueSet.language)
        return q

    def col_defs(self):
        if self.language:
            return [
                LinkCol(self, 'name', sTitle='Form'),
                # LinkCol(self, 'cognateset', get_object=lambda x: x.cognateset),
                Col(self, 'description', sTitle='Gloss'),
                RefsCol(self, 'source'),
            ]
        if self.parameter:
            return [
                GroupCol(self, 'group'),
                LinkCol(self, 'language', get_object=lambda x: x.valueset.language),
                LinkCol(self, 'name', sTitle='Form'),
                Col(self, 'description', sTitle='Gloss'),
                RefsCol(self, 'source'),
            ]

        return [
            LinkCol(self, 'name', sTitle='Form'),
            #LinkCol(self, 'cognateset', get_object=lambda x: x.cognateset),
            Col(self, 'description', sTitle='Gloss'),
            LinkCol(self, 'language', get_object=lambda x: x.valueset.language),
            #LinkCol(self, 'source', get_object=lambda x: x.source),
        ]


def includeme(config):
    """register custom datatables"""

    config.register_datatable('contributions', Chapters)
    config.register_datatable('values', Word)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Cognatesets)
