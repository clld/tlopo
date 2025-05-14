import collections

from pyramid.config import Configurator
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement, ILanguage
from clld.web.icon import MapMarker
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from tlopo import models

_ = lambda s: s
_('Parameter')
_('Parameters')
_('Contribution')
_('Contributions')
_('Value')
_('Values')


class LanguageByGroupMapMarker(MapMarker):
    def __call__(self, ctx, req):
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
    config.registry.registerUtility(LanguageByGroupMapMarker(), IMapMarker)

    config.include('clldmpg')


    return config.make_wsgi_app()
