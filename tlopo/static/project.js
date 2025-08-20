TLOPO = {}

TLOPO.regions_index = function (map) {
    var layers = {};

    function onEachFeature(feature, layer) {
        layer.bindTooltip(feature.properties.title);
        layer.on({click: function () {window.location.href=feature.properties.url}});
        layers[feature.properties.title] = layer;
    }

    layer = L.geoJSON(bboxes, {
        onEachFeature: onEachFeature
    }).addTo(map.map);
    map.map.fitBounds(layer.getBounds());
    L.control.layers(
        {},
        layers,
        {collapsed: false}).addTo(map.map);
}

TLOPO.map_with_taxa_on_init = function (map) {
    var pixel_ratio = parseInt(window.devicePixelRatio) || 1;
    var layers = {};
    var max_zoom = 16;
    var tile_size = 512;
    var index = 0;
    var color = 'classic';
    var url = 'https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}@{r}x.png?taxonKey={t}&style={c}.poly&bin=hex&hexPerTile=50&srs=EPSG%3A3857';

    if (taxa === undefined) {
        return;
    }
    //'classic.poly', 'green.poly'

    for (name in taxa) {
        color = index % 2 === 0 ? 'classic' : 'green'
        tl = L.tileLayer(
            url.replace('{r}', pixel_ratio).replace('{t}', taxa[name]).replace('{c}', color),
            {
                minZoom: 1,
                maxZoom: max_zoom + 1,
                zoomOffset: -1,
                tileSize: tile_size
            }).addTo(map.map);
        layers[name] = tl;
        index += 1;
    }
    L.control.layers(
        {},
        layers,
        {collapsed: false}).addTo(map.map);
}
