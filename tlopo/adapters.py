from sqlalchemy.orm import joinedload

from clld import interfaces
from clld.web.adapters.geojson import GeoJsonParameter, GeoJson
from clld.db.meta import DBSession
from clldutils.svg import data_url, icon

from tlopo import models
from tlopo.interfaces import ITaxon, IRegion


class GeoJsonCognateset(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        label = self.get_language(ctx, req, valueset).name
        forms = ', '.join(v.word.name for v in valueset.values)
        return {
            'values': list(valueset.values),
            'label': '<i>{}</i>'.format(forms)}


class GeoJsonTaxon(GeoJson):
    def featurecollection_properties(self, ctx, req):
        return {'name': ctx.name, 'description': ctx.description}

    def feature_iterator(self, ctx, req):
        return DBSession.query(models.Word) \
            .join(models.WordTaxon) \
            .filter(models.WordTaxon.taxon_pk == ctx.pk) \
            .options(joinedload(models.Word.language))

    def get_language(self, ctx, req, word):
        return word.language

    def feature_properties(self, ctx, req, word):
        return {'label': word.name, 'description': word.description}


class GeoJsonRegion(GeoJson):
    def featurecollection_properties(self, ctx, req):
        return {'name': ctx.name, 'description': ctx.description}

    def feature_iterator(self, ctx, req):
        return ctx.languages

    def feature_properties(self, ctx, req, lang):
        return {'icon': data_url(icon(lang.region_icon))}


def includeme(config):
    config.register_adapter(
        GeoJsonCognateset,
        interfaces.IParameter,
        name=GeoJsonCognateset.mimetype)
    config.register_adapter(
        GeoJsonTaxon,
        ITaxon,
        name=GeoJson.mimetype)
    config.register_adapter(
        GeoJsonRegion,
        IRegion,
        name=GeoJson.mimetype)
