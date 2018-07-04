var template = function (str, data) {
    return str.replace(/\{ *([\w_]+) *\}/g, function (str, key) {
        var value = data[key];
        if (value === undefined) value = key
        else if (typeof value === 'function') value = value(data);
        return value;
    });
};

exports.LocalConfig = function (localizer, project) {
    localizer.where('Layer').if({'Datasource.type': 'postgis'}).then({
        'Datasource.dbname': 'tilery',
        'Datasource.password': null,
        'Datasource.user': 'tilery',
        'Datasource.host': '',
    });
    localizer.where('Layer').if({id: 'land'}).then({'Datasource.file': '/srv/tilery/data/land-polygons-split-3857/land_polygons.shp'});
    localizer.where('Layer').if({id: 'land-low'}).then({'Datasource.file': '/srv/tilery/data/simplified-land-polygons-complete-3857/simplified_land_polygons.shp'});
    project.mml.center = [2.1671, 48.9046, 12];
    localizer.where('Layer').if({'Datasource.type': 'postgis'}).then(function (obj) {
        obj.Datasource.table = template(obj.Datasource.table, {lang: process.env.PIANOFORTE_LANG || 'fr'});
        return obj;
    });


};
