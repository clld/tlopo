from clld.web.maps import ParameterMap, Map
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
            'on_init': JS('TLOPO.map_with_taxa_on_init'),
        }


def includeme(config):
    config.register_map('taxon', TaxonMap)
    config.register_map('parameter', FeatureMap)
