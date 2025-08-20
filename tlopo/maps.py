from clld.web.maps import ParameterMap, Map, Layer
from clld.web.util.helpers import JS


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
    def get_options(self):
        return {
            #'show_labels': True,
            'max_zoom': 15,
            'base_layer': 'OpenTopoMap',
        }


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
    config.register_map('regions', RegionsMap)
    config.register_map('region', RegionMap)
    config.register_map('taxon', TaxonMap)
    config.register_map('parameter', FeatureMap)
