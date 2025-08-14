import collections
import itertools

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common, HasSourceNotNullMixin, IdNameDescriptionMixin
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML, literal
from markdown import markdown

from tlopo.interfaces import ITaxon


def md(t):
    res = markdown(t)
    if res.startswith('<p>'):
        res = res[3:]
    if res.endswith('</p>'):
        res = res[:-4]
    return res


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
def htmlify(md):
    return HTML.literal(markdown(md.replace('*', '&ast;')))


@implementer(ITaxon)
class Taxon(Base, IdNameDescriptionMixin):
    # id -> GBIF
    # name -> scientific name
    # description -> english name
    rank = Column(Unicode)
    kingdom = Column(Unicode)
    phylum = Column(Unicode)
    klass = Column(Unicode)
    order = Column(Unicode)
    family = Column(Unicode)
    genus = Column(Unicode)
    genus_eng = Column(Unicode)
    family_eng = Column(Unicode)
    synonyms = Column(Unicode)


@implementer(interfaces.IContribution)
class Chapter(CustomModelMixin, common.Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    volume_num = Column(Integer)
    volume = Column(Unicode)
    next_pk = Column(Integer, ForeignKey('chapter.pk'))
    next = relationship('Chapter', backref=backref('prev', uselist=False), remote_side=[pk], foreign_keys=[next_pk])

    def toc(self):
        def html(i, title, children):
            se = [HTML.a(literal(md(title)), href='#' + i)]
            if children:
                se.append(HTML.ol(*[html('-'.join([i, ii]), c[0], c[1]) for ii, c in children.items()]))
            return HTML.li(*se)

        sections = ('', collections.OrderedDict())
        for level, sid, title in self.jsondata['toc']:
            keys = sid.split('-')
            tk, keys = '-'.join(keys[:2]), keys[2:]
            keys = [tk] + keys
            assert len(keys) == level

            node = sections
            for key in keys[:-1]:
                node = node[1][key]

            node[1][keys[-1]] = (title, collections.OrderedDict())

        return HTML.ol(*[html(i, c[0], c[1]) for i, c in sections[1].items()])


class TaxonChapter(Base):
    #__table_args__ = (UniqueConstraint('unit_pk', 'contribution_pk', 'fragment'),)
    taxon_pk = Column(Integer, ForeignKey('taxon.pk'), nullable=False)
    taxon = relationship(
        Taxon,
        innerjoin=True,
        backref=backref("chapter_assocs", order_by='TaxonChapter.contribution_pk'))
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'), nullable=False)
    chapter = relationship(Chapter, innerjoin=True, backref='taxa')
    fragment = Column(Unicode)

    @property
    def section(self):
        for _, secid, title in self.chapter.jsondata['toc']:
            if secid == self.fragment:
                return HTML.literal(markdown(title))


@implementer(interfaces.ISource)
class Ref(CustomModelMixin, common.Source):
    pk = Column(Integer, ForeignKey('source.pk'), primary_key=True)
    doi = Column(Unicode)
    with_url = Column(Boolean)

    @property
    def grouped_sections(self):
        def key(row):
            return tuple(int(i) for i in row[0].split('-') + row[1].replace('s-', '').split('-'))

        return [
            (cid, [r[1:] for r in rows]) for cid, rows in
            itertools.groupby(sorted(self.jsondata['sections'], key=key), lambda r: r[0])]


@implementer(interfaces.ILanguage)
class Languoid(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    group = Column(Unicode)
    icon = Column(Unicode)
    is_proto = Column(Boolean)

#
# cognatesetreference -> Parameter (with self-referential fk for "full" set)
# cognateset ->          Parameter
#
@implementer(interfaces.IParameter)
class Cognateset(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    note = Column(Unicode)
    chapter_pk = Column(Integer, ForeignKey('contribution.pk'))
    chapter = relationship(common.Contribution, backref="cognatesets")
    fragment = Column(Unicode)

    @property
    def title(self):
        return htmlify(self.name)

    @property
    def shorttitle(self):
        return htmlify(self.name.split("‘")[0].strip())

    def in_chapter_url(self, req):
        return req.route_url('contribution', id=self.chapter.id, _anchor=self.fragment)


class TaxonCognateset(Base):
    #__table_args__ = (UniqueConstraint('unit_pk', 'contribution_pk', 'fragment'),)
    taxon_pk = Column(Integer, ForeignKey('taxon.pk'), nullable=False)
    taxon = relationship(Taxon, innerjoin=True, backref="cognateset_assocs")
    cognateset_pk = Column(Integer, ForeignKey('parameter.pk'), nullable=False)
    cognateset = relationship(Cognateset, innerjoin=True, backref="taxon_assocs")


# FIXME: taxa: a fully new resource!

#
# FIXME: form -> Value
#
@implementer(interfaces.IValue)  # FIXME: Word -> Unit! Gloss -> UnitParameter, row in cldf/glosses.csv -> UnitValue!
class Cognate(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    word_pk = Column(Integer, ForeignKey('unit.pk'))
    word = relationship(common.Unit, backref="cognates")
    ord = Column(Integer)


@implementer(interfaces.IUnit)
class Word(CustomModelMixin, common.Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)
    variants = Column(Unicode)


@implementer(interfaces.IUnitParameter)
class Gloss(CustomModelMixin, common.UnitParameter):
    pk = Column(Integer, ForeignKey('unitparameter.pk'), primary_key=True)


@implementer(interfaces.IUnitValue)
class HasGloss(CustomModelMixin, common.UnitValue):
    pk = Column(Integer, ForeignKey('unitvalue.pk'), primary_key=True)
    pos = Column(Unicode)


class GlossReference(Base, HasSourceNotNullMixin):
    __table_args__ = (UniqueConstraint('unitvalue_pk', 'source_pk', 'description'),)

    unitvalue_pk = Column(Integer, ForeignKey('unitvalue.pk'), nullable=False)
    hasgloss = relationship(HasGloss, innerjoin=True, backref="references")


class WordTaxon(Base):
    #__table_args__ = (UniqueConstraint('unit_pk', 'contribution_pk', 'fragment'),)
    unit_pk = Column(Integer, ForeignKey('unit.pk'), nullable=False)
    word = relationship(Word, innerjoin=True, backref="taxon_assocs")
    taxon_pk = Column(Integer, ForeignKey('taxon.pk'), nullable=False)
    taxon = relationship(Taxon, innerjoin=True, backref="word_assocs")


class WordChapter(Base):
    #__table_args__ = (UniqueConstraint('unit_pk', 'contribution_pk', 'fragment'),)

    unit_pk = Column(Integer, ForeignKey('unit.pk'), nullable=False)
    word = relationship(Word, innerjoin=True, backref="chapter_assocs")

    contribution_pk = Column(Integer, ForeignKey('contribution.pk'), nullable=False)
    chapter = relationship(Chapter, innerjoin=True)

    fragment = Column(Unicode)
    gloss_ids = Column(Unicode)


# cf.csv is only used to infer links from words to chapter texts!
# class WordChapter ? - contribution_pk, fragment,

# Value -> Cognate! with unit_pk!

class WordSource(Base, HasSourceNotNullMixin):

    """References for a set of values (related to one parameter and one language).

    These references can be interpreted as justifications why a language does not "have"
    certain values for a parameter, too.
    """

    __table_args__ = (UniqueConstraint('value_pk', 'source_pk', 'description'),)

    value_pk = Column(Integer, ForeignKey('value.pk'), nullable=False)
    word = relationship(common.Value, innerjoin=True, backref="references")
