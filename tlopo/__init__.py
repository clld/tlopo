import collections

from pyramid.config import Configurator
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement, ILanguage, IUnit, ICtxFactoryQuery
from clld.web.icon import MapMarker
from clld.web.app import CtxFactoryQuery
from clld.db.models import common
from clldutils.svg import pie, icon, data_url
from sqlalchemy.orm import joinedload

# we must make sure custom models are known at database initialization!
from tlopo import models
from tlopo.interfaces import ITaxon

_ = lambda s: s
_('Parameter')
_('Parameters')
_('Contribution')
_('Contributions')
_('Value')
_('Values')
_('Unit')
_('Units')


class TlopoCtxFactoryQuery(CtxFactoryQuery):
    def refined_query(self, query, model, req):
        if model == common.Contribution:
            return query.options(
                joinedload(models.Chapter.contributor_assocs),
                joinedload(models.Chapter.cognatesets))
        return query


class LanguageByGroupMapMarker(MapMarker):
    def __call__(self, ctx, req):
        if IUnit.providedBy(ctx):
            return data_url(icon(ctx.language.icon))

        if ILanguage.providedBy(ctx):
            return data_url(icon(ctx.icon))

        if IValueSet.providedBy(ctx):
            return data_url(icon(ctx.language.icon))

        return super(LanguageByGroupMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    for utility, interface in [
        (TlopoCtxFactoryQuery(), ICtxFactoryQuery),
        (LanguageByGroupMapMarker(), IMapMarker),
    ]:
        config.registry.registerUtility(utility, interface)


    config.register_resource('taxon', models.Taxon, ITaxon, with_index=True)
    config.include('clldmpg')


    return config.make_wsgi_app()
