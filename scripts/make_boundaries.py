from pathlib import Path

import asyncpg
import overpy
import requests
import shapefile
import ujson as json
from minicli import cli, run
from postgis import GeometryCollection, Polygon, LineString, MultiPolygon
from postgis.asyncpg import register

OVERPASS = 'http://overpass-api.de/api/interpreter'
SRC = "/home/ybon/Code/maps/pianoforte/data/boundary234/boundary234"
DEST = "tmp/boundary.json"


async def get_relation(**tags):
    tags = "".join(f'["{k}"="{v}"]' for k, v in tags.items())
    path = Path('tmp') / 'boundary' / tags
    if not path.exists():
        params = {'data': f'relation{tags};(._;>;);out body;'}
        resp = requests.get(OVERPASS, params=params)
        data = resp.content
        with path.open('wb') as f:
            f.write(data)
        data = data.decode()
    else:
        with path.open() as f:
            data = f.read()
    relation = overpy.Result.from_xml(data).relations[0]
    collection = []
    for member in relation.members:
        coords = []
        if member.role != 'outer':
            continue
        way = member.resolve()
        for node in way.nodes:
            coords.append((float(node.lon), float(node.lat)))
        klass = Polygon if coords[0] == coords[-1] else LineString
        collection.append(klass(coords))
    geom = GeometryCollection(collection)
    return geom


async def make_polygon(conn, geom):
    return await conn.fetchval(
        'SELECT ST_MakePolygon(ST_LineMerge('
        'ST_CollectionExtract($1::geometry, 2)))', geom)


async def compute_golan(conn):
    golan = await get_relation(boundary="administrative", admin_level="8",
                               name="מועצה אזורית גולן")
    golan = await make_polygon(conn, golan)
    majdal = await get_relation(boundary="administrative", admin_level="8",
                                name="مجدل شمس")
    majdal = await make_polygon(conn, majdal)
    return await conn.fetchval(
        'SELECT ST_MakePolygon(ST_ExteriorRing(ST_Union($1::geometry, '
        '$2::geometry)))', golan, majdal)


async def compute_west_bank(conn):
    relation = await get_relation(place="region", name="الضفة الغربية")
    return await make_polygon(conn, relation)


async def remove_area(conn, shape, other):
    return await conn.fetchval(
        'SELECT ST_Difference($1::geometry, $2::geometry)', shape, other)


async def add_area(conn, shape, other):
    return await conn.fetchval(
        'SELECT ST_Union($1::geometry, $2::geometry)', shape, other)


def extract_shapes(shape):
    parts = list(shape.parts) + [len(shape.points)]
    shapes = []
    for idx in range(len(parts) - 1):
        shapes.append([shape.points[parts[idx]:parts[idx+1]]])
    return shapes


@cli
async def process():
    conn = await asyncpg.connect(database='pianoforte')
    await register(conn)
    features = []
    golan = await compute_golan(conn)
    reader = shapefile.Reader(SRC)
    fields = [f[0] for f in reader.fields[1:]]
    shapes = reader.shapes()
    records = reader.records()
    for shape, record in zip(shapes, records):
        properties = dict(zip(fields, record))
        if properties['admin_leve'] != '2':
            continue
        shapes = extract_shapes(shape)
        polygon = MultiPolygon(shapes)
        if properties['name_en'] == 'Israel':
            polygon = await remove_area(conn, polygon, golan)
            west_bank = await compute_west_bank(conn)
            polygon = await remove_area(conn, polygon, west_bank)
        if properties['name_en'] == 'Syria':
            polygon = await add_area(conn, polygon, golan)
        features.append({
            'type': 'Feature',
            'geometry': polygon.geojson,
            'properties': properties
        })
    await conn.close()
    with Path(DEST).open('w') as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f)


if __name__ == '__main__':
    run()
