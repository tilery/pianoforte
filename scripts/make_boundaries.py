import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import csv
from pathlib import Path

import asyncpg
import overpy
import requests
import ujson as json
from minicli import cli, run
from postgis import LineString, MultiLineString
from postgis.asyncpg import register

OVERPASS = 'http://overpass-api.de/api/interpreter'


async def get_relation(conn, **tags):
    if 'iso' in tags:
        tags['ISO3166-1:alpha2'] = tags.pop('iso')
    tags = "".join(f'["{k}"="{v}"]' for k, v in tags.items())
    path = Path('tmp/boundary')
    path.mkdir(parents=True, exist_ok=True)
    path = path / tags.replace('/', '_')
    if not path.exists():
        params = {'data': f'[out:json];relation{tags};(._;>;);out body;'}
        resp = requests.get(OVERPASS, params=params)
        data = resp.content
        with path.open('wb') as f:
            f.write(data)
        data = data.decode()
    else:
        with path.open() as f:
            data = f.read()
    try:
        relation = overpy.Result.from_json(json.loads(data)).relations[0]
    except IndexError:
        raise ValueError(f'Cannot find relation for {tags}')
    collection = []
    for member in relation.members:
        coords = []
        # Nepal disputed way without outer role:
        # http://www.openstreetmap.org/way/202061325
        if member.role != 'outer' and member.ref != 202061325:
            continue
        way = member.resolve()
        for node in way.nodes:
            coords.append((float(node.lon), float(node.lat)))
        collection.append(LineString(coords))
    shape = await make_polygon(conn, MultiLineString(collection))
    return shape, relation.tags


async def make_polygon(conn, geom):
    return await conn.fetchval(
        'SELECT ST_Multi(ST_Collect(ST_MakePolygon((sub.dump).geom))) FROM '
        '(SELECT ST_Dump(ST_LineMerge($1::geometry)) as dump) AS sub', geom)


async def compute_golan(conn):
    golan, props = await get_relation(conn, boundary="administrative",
                                      admin_level="8", name="מועצה אזורית גולן")
    majdal, _ = await get_relation(conn, boundary="administrative",
                                   admin_level="8", name="مجدل شمس")
    return await conn.fetchval(
        'SELECT ST_MakePolygon(ST_ExteriorRing(ST_Union($1::geometry, '
        '$2::geometry)))', golan, majdal), props


async def compute_doklam(conn):
    # https://en.wikipedia.org/wiki/en:Doklam?uselang=fr
    shape, props = await get_relation(conn, boundary="administrative",
                                      admin_level="3", name="Doklam 洞郎地区")
    other, _ = await get_relation(conn, boundary="administrative",
                                  admin_level="3", name="鲁林地区")
    shape = await add_area(conn, shape, other)
    other, _ = await get_relation(conn, boundary="administrative",
                                  admin_level="3", name="查马普地区")
    shape = await add_area(conn, shape, other)
    other, _ = await get_relation(conn, boundary="administrative",
                                  admin_level="3", name="基伍地区")
    shape = await add_area(conn, shape, other)
    return shape, props


async def remove_area(conn, shape, other):
    return await conn.fetchval(
        'SELECT ST_Difference($1::geometry, $2::geometry)', shape, other)


async def add_area(conn, shape, other):
    return await conn.fetchval(
        'SELECT ST_Union($1::geometry, $2::geometry)', shape, other)


async def load_country(conn, **tags):
    return await get_relation(conn, boundary='administrative', admin_level=2,
                              **tags)


@cli
async def process(itl_path: Path=Path('data/boundary.json'),
                  disputed_path: Path=Path('data/disputed.json')):
    conn = await asyncpg.connect(database='pianoforte')
    await register(conn)
    boundaries = []
    disputed = []

    def add_disputed(polygon, properties):
        disputed.append({
            'type': 'Feature',
            'geometry': polygon.geojson,
            'properties': properties
        })

    # Used more than once.
    golan, props = await compute_golan(conn)
    add_disputed(golan, props)
    doklam, props = await compute_doklam(conn)
    add_disputed(doklam, props)
    bir_tawil, props = await get_relation(conn, type='boundary',
                                          name='بيرطويل (Bir Tawil)')
    add_disputed(bir_tawil, props)
    halaib_triangle, props = await get_relation(conn, type='boundary',
                                                name='مثلث حلايب‎')
    add_disputed(halaib_triangle, props)
    path = Path(__file__).parent.parent / 'data/country.csv'
    with path.open() as f:
        countries = list(csv.DictReader(f))
    for country in countries:
        iso = country['iso']
        polygon, properties = await load_country(conn, iso=iso)
        properties.update(country)
        if properties['name:en'] == 'Sahrawi Arab Democratic Republic':
            continue
        print(f'''"{properties['name']}",  # {properties['name:en']}''')
        if iso == 'IL':
            polygon = await remove_area(conn, polygon, golan)
            west_bank, _ = await get_relation(conn, place="region",
                                              name="الضفة الغربية")
            polygon = await remove_area(conn, polygon, west_bank)
        if iso == 'SY':
            polygon = await add_area(conn, polygon, golan)
        if iso == 'SS':
            sudan, _ = await load_country(conn, iso='SD')  # Sudan
            polygon = await remove_area(conn, polygon, sudan)
        if properties['name:en'] == 'Sudan':
            polygon = await remove_area(conn, polygon, bir_tawil)
        if iso == 'EG':
            polygon = await add_area(conn, polygon, bir_tawil)
        if iso == 'NP':
            claim, props = await get_relation(conn, type="boundary",
                                              name="Extent of Nepal Claim")
            add_disputed(claim, props)
            polygon = await add_area(conn, polygon, claim)
        if iso == 'IN':
            claim, _ = await get_relation(conn, type="boundary",
                                          name="Extent of Nepal Claim")
            polygon = await remove_area(conn, polygon, claim)
        if iso == 'CN':
            polygon = await remove_area(conn, polygon, doklam)
        if iso == 'BH':
            polygon = await add_area(conn, polygon, doklam)
        if iso == 'MA':
            # Western Sahara
            esh, props = await get_relation(conn, boundary="disputed",
                                            name="الصحراء الغربية")
            add_disputed(esh, props)
            polygon = await add_area(conn, polygon, esh)
        boundaries.append({
            'type': 'Feature',
            'geometry': polygon.geojson,
            'properties': properties
        })
    sba, properties = await load_country(conn,
                                         name='British Sovereign Base Areas')
    boundaries.append({
        'type': 'Feature',
        'geometry': sba.geojson,
        'properties': properties
    })
    await conn.close()
    with itl_path.open('w') as f:
        json.dump({'type': 'FeatureCollection', 'features': boundaries}, f)
    with disputed_path.open('w') as f:
        json.dump({'type': 'FeatureCollection', 'features': disputed}, f)


if __name__ == '__main__':
    run()
