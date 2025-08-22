from clld.web.maps import ParameterMap, Map, Layer, Legend
from clld.web.util.helpers import JS
from clld.web.util.htmllib import HTML, literal
from clldutils.svg import data_url, icon

from tlopo import models


class LanguagesMap(Map):
    def get_legends(self):
        def val(label, ico):
            return HTML.label(
                HTML.img(width=18, src=data_url(icon(ico))),
                literal('&nbsp;'),
                label,
                style='margin-left: 1em; margin-right: 1em;')

        yield Legend(
            self,
            'values',
            [
                val('Oceanic languages', 'cffffff'),
                val('other Austronesian languages', 'tffffff')],
            label='Legend')


class FeatureMap(ParameterMap):
    def get_options(self):
        return {
            'on_init': JS('TLOPO.map_with_taxa_on_init'),
        }


class TaxonMap(Map):
    def get_options(self):
        return {
            'show_labels': True,
            'base_layer': 'OpenTopoMap',
            'on_init': JS('TLOPO.map_with_taxa_on_init'),
        }


class RegionMap(Map):
    def __init__(self, ctx, req, eid='map'):
        self.language = None
        if isinstance(ctx, models.Languoid):
            self.language = ctx
            ctx = ctx.region
        Map.__init__(self, ctx, req, eid)

    def get_layers(self):
        yield Layer(
            self.ctx.id,
            '%s' % self.ctx,
            self.req.route_url('region_alt', id=self.ctx.id, ext='geojson'))

    def get_options(self):
        res = {
            #'show_labels': True,
            'max_zoom': 15,
            'base_layer': 'OpenTopoMap',
        }
        if self.language:
            res['show_labels'] = True
            res['center'] = (self.language.latitude, self.language.longitude)
            res['zoom'] = 9
        return res


class RegionsMap(Map):
    def get_layers(self):
        for region in self.ctx.get_query():
            yield Layer(
                region.id,
                region.name,
                {'type': 'FeatureCollection', 'features': []})

    def get_legends(self):
        return []

    def get_options(self):
        return {
            'on_init': JS('TLOPO.regions_index'),
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('regions', RegionsMap)
    config.register_map('region', RegionMap)
    config.register_map('taxon', TaxonMap)
    config.register_map('parameter', FeatureMap)
