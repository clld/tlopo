from markdown import markdown

from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, IdCol, RefsCol, LinkToMapCol, DataTable, DetailsRowLinkCol
from clld.web.datatables.contribution import ContributorsCol
from clld.db.models import common
from clld.db.util import icontains, get_distinct_values
from clld.web.util.helpers import map_marker_img, icon, button, link
from clld.web.util.htmllib import HTML


from tlopo import models


class VolCol(Col):
    def order(self):
        return models.Chapter.volume_num

    def search(self, qs):
        return icontains(models.Chapter.volume, qs)

   
class Chapters(datatables.Contributions):
    def col_defs(self):
        return [
            VolCol(self, 'vol', model_col=models.Chapter.volume),
            LinkCol(self, 'name'),
            ContributorsCol(self, 'contributor'),
        ]


class LGroupCol(Col):
    def format(self, item):
        return map_marker_img(self.dt.req, item) + item.group


class Languages(datatables.Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            LGroupCol(self, 'group', model_col=models.Languoid.is_proto),
            Col(self, 'proto', model_col=models.Languoid.is_proto),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class CognatesetNameCol(LinkCol):
    def get_attrs(self, item):
        return dict(label=HTML.literal(markdown(item.name)))


class ChapterCol(LinkCol):
    def order(self):
        return common.Contribution.pk


class InChapterLinkCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return button(
            icon('book'),
            title='Go to cognate set in chapter text',
            href=item.in_chapter_url(self.dt.req))


class Cognatesets(datatables.Parameters):
    __constraints__ = [common.Contribution]

    def base_query(self, query):
        query = datatables.Parameters.base_query(self, query)
        query = query.join(common.Contribution).options(joinedload(models.Cognateset.chapter))

        if self.contribution:
            query = query.filter(models.Cognateset.chapter_pk == self.contribution.pk)
        return query

    def col_defs(self):
        if self.contribution:
            return [
                CognatesetNameCol(self, 'reconstruction'),
                DetailsRowLinkCol(self, 'reflexes'),
            ]

        return [
            ChapterCol(self, 'chapter', model_col=common.Contribution.name, get_object=lambda i: i.chapter),
            InChapterLinkCol(self, '#'),
            CognatesetNameCol(self, 'reconstruction', model_col=common.Parameter.name),
            DetailsRowLinkCol(self, 'reflexes', button_text='Reflexes'),
        ]


class GroupCol(Col):
    def format(self, item):
        return map_marker_img(self.dt.req, item.valueset) + item.valueset.language.group

    def order(self):
        return models.Cognate.ord


class Cognates(datatables.Values):
    def base_query(self, query):
        query = query.join(common.ValueSet).options(joinedload(common.Value.valueset))
        query = query.join(models.Word).options(joinedload(models.Cognate.word))
        query = query.join(models.Languoid)

        if self.parameter:
            return query.filter(common.ValueSet.parameter_pk == self.parameter.pk)

        return query

    def col_defs(self):
        if self.parameter:
            return [
                # FIXME: GroupCol
                GroupCol(self, 'group', get_object=lambda i: i.word.language),
                LinkCol(self, 'language', model_col=common.Language.name, get_object=lambda i: i.word.language),
                FormCol(self, 'form', get_object=lambda i: i.word),
                GlossCol(self, 'gloss', model_col=common.Unit.description, get_object=lambda i: i.word),
                LinkToMapCol(self, 'map', get_object=lambda i: i.word.language),
            ]
        return [

        ]


class LanguageCol(LinkCol):
    def order(self):
        return common.Language.name

    def search(self, qs):
        return icontains(common.Language.name, qs)


class ProtoCol(Col):
    def format(self, item):
        return 'yes' if item.language.is_proto else 'no'


class FormCol(LinkCol):
    def get_attrs(self, item):
        item = self.get_obj(item)
        return {'label': HTML.i(('*' if item.language.is_proto else '') + item.name)}


class GlossCol(Col):
    def search(self, qs):
        return icontains(common.Unit.description, qs)

    def format(self, item):
        return markdown(self.get_obj(item).description)


class CognatesetsCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(
                self.dt.req,
                cog.valueset.parameter,
                label=cog.valueset.parameter.shorttitle)) for cog in item.cognates],
            **{'class': 'inline'})


class Words(datatables.Units):
    __constraints__ = [common.Language, models.Taxon]

    def get_options(self):
        opts = super(datatables.Units, self).get_options()
        opts['aaSorting'] = [
            [1, 'asc'], [2, 'asc']]
        return opts

    def base_query(self, query):
        q = datatables.Units.base_query(self, query)
        # if not language or parameter, join and load valueset.language!
        if self.language:
            q = q.join(common.Unit.language)
        if self.taxon:
            q = q.join(models.WordTaxon).filter(models.WordTaxon.taxon_pk == self.taxon.pk)
        return q

    def col_defs(self):
        if self.language:
            return [
                FormCol(self, 'name', sTitle='Form'),
                # LinkCol(self, 'cognateset', get_object=lambda x: x.cognateset),
                GlossCol(self, 'description', sTitle='Gloss'),
                CognatesetsCol(self, 'cogsets'),
                RefsCol(self, 'source'),
            ]
        return [
            ProtoCol(self, 'proto', model_col=models.Languoid.is_proto),
            LanguageCol(self, 'language', get_object=lambda x: x.language),
            FormCol(self, 'name', sTitle='Form'),
            GlossCol(self, 'description', sTitle='Gloss'),
            #LinkCol(self, 'source', get_object=lambda x: x.source),
        ]


class Taxa(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='English name'),
            Col(self, 'rank', choices=get_distinct_values(models.Taxon.rank)),
            Col(self, 'kingdom', choices=get_distinct_values(models.Taxon.kingdom)),
            Col(self, 'family', choices=get_distinct_values(models.Taxon.family)),
        ]


def includeme(config):
    """register custom datatables"""

    config.register_datatable('contributions', Chapters)
    config.register_datatable('values', Cognates)
    config.register_datatable('taxons', Taxa)
    config.register_datatable('units', Words)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Cognatesets)
