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
from clld.db.models import common, Language, HasSourceNotNullMixin


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------


@implementer(interfaces.ILanguage)
class Languoid(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    group = Column(Unicode)
    icon = Column(Unicode)


@implementer(interfaces.IParameter)
class Cognateset(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    note = Column(Unicode)
    chapter_pk = Column(Integer, ForeignKey('contribution.pk'))
    chapter = relationship(common.Contribution, backref="cognatesets")


@implementer(interfaces.IValue)
class Word(CustomModelMixin, common.Value):
    # name: form
    # description: gloss
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)



class WordSource(Base, HasSourceNotNullMixin):

    """References for a set of values (related to one parameter and one language).

    These references can be interpreted as justifications why a language does not "have"
    certain values for a parameter, too.
    """

    __table_args__ = (UniqueConstraint('value_pk', 'source_pk', 'description'),)

    value_pk = Column(Integer, ForeignKey('value.pk'), nullable=False)
    word = relationship(common.Value, innerjoin=True, backref="references")
