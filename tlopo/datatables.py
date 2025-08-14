from markdown import markdown

from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, IdCol, RefsCol, LinkToMapCol, DataTable, DetailsRowLinkCol
from clld.web.datatables.contribution import ContributorsCol
from clld.web.datatables.source import Sources, TypeCol
from clld.db.models import common
from clld.db.util import icontains, contains, get_distinct_values
from clld.web.util.helpers import map_marker_img, icon, button, link
from clld.web.util.htmllib import HTML


from tlopo import models


class DOICol(Col):
    def format(self, item):
        if item.doi:
            return HTML.a(
                HTML.img(
                    width=25, height=25, src=self.dt.req.static_url('tlopo:static/DOI_logo.svg')),
                href='https://doi.org/' + item.doi)
        return ''


class Refs(Sources):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'd'),
            LinkCol(self, 'name'),
            Col(self, 'author'),
            Col(self, 'year'),
            Col(self, 'description', sTitle='Title', format=lambda i: HTML.span(i.description)),
            DOICol(self, 'doi', model_col=models.Ref.doi),
            Col(self, 'url', model_col=models.Ref.with_url),
            TypeCol(self, 'bibtex_type'),
        ]




class VolCol(Col):
    def order(self):
        return models.Chapter.volume_num

    def search(self, qs):
        return icontains(models.Chapter.volume, qs)

   
class Chapters(datatables.Contributions):
    def get_options(self):
        opts = super(datatables.Contributions, self).get_options()
        opts['aaSorting'] = [[1, 'asc']]
        return opts

    def col_defs(self):
        return [
            VolCol(self, 'vol', model_col=models.Chapter.volume, choices=get_distinct_values(models.Chapter.volume)),
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


class FullGlossCol(Col):
    __kw__ = dict(bSortable=False)

    def search(self, qs):
        return icontains(models.Word.description, qs)

    def format(self, item):
        res = []
        for g in item.word.unitvalues:
            if g.id in item.jsondata['hasglosses']:
                if res:
                    res.append('; ')
                if g.pos:
                    res.append('({}) '.format(g.pos))
                if g.name:
                    res.append(HTML.span(g.name, class_='gloss'))
                i = -1
                for i, ref in enumerate(g.references):
                    if i == 0:
                        res.append(' (')
                    else:
                        res.append(', ')
                    res.append(HTML.a(
                        ref.source.name,
                        title='{}. {}'.format(ref.source.name, ref.source.description),
                        href=self.dt.req.route_url('source', id=ref.key)))
                    if ref.description:
                        res.append(': ')
                        res.append(ref.description)
                if i >= 0:
                    res.append(')')
        return HTML.div(*res)


class Cognates(datatables.Values):
    def base_query(self, query):
        query = query.join(common.ValueSet).options(joinedload(common.Value.valueset))
        query = query.join(common.Unit).options(joinedload(models.Cognate.word))
        query = query.join(models.Languoid)

        if self.parameter:
            query = query.options(joinedload(models.Cognate.word, common.Unit.unitvalues))
            return query.filter(common.ValueSet.parameter_pk == self.parameter.pk)

        return query

    def col_defs(self):
        if self.parameter:
            return [
                # FIXME: GroupCol
                GroupCol(self, 'group', get_object=lambda i: i.word.language),
                LinkCol(self, 'language', model_col=common.Language.name, get_object=lambda i: i.word.language),
                FormCol(self, 'form', get_object=lambda i: i.word),
                FullGlossCol(self, 'gloss'),
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
    __kw__ = dict(
        sDescription="Search for forms by matching substrings. Note that theleading * of "
                     "protoforms is not considered here. You can specify matches at the "
                     "start of a form by prefixing the search term with '^' and matches "
                     "at the end by suffixing with '$'. An underscore '_' can be used as "
                     "one-letter wildcard. So '^t_ma$' will match 'tuma' and 'tama'.")

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


class VariantsCol(Col):
    __kw__ = dict(
        bSortable=False,
        sTitle='Variants',
        sClass="minimal-width",
        sDescription="This column allows searchin for variants of a form in a simple way. "
                     "I.e. '[g,k]opu' can be searched as 'gopu' or 'kopu'. To specify matches "
                     "at the start or end of a form, just append space accordingly.",
    )

    def search(self, qs):
        return contains(models.Word.variants, qs)

    def format(self, item):
        return "←"


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
            VariantsCol(self, 'variant'),
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
    config.register_datatable('sources', Refs)
