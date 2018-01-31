from pathlib import Path

import asyncpg
import overpy
import requests
import ujson as json
from minicli import cli, run
from postgis import LineString, MultiLineString
from postgis.asyncpg import register

OVERPASS = 'http://overpass-api.de/api/interpreter'

COUNTRIES = [
    "AD",  # Andorra
    "AE",  # United Arab Emirates
    "AF",  # Afghanistan
    "AO",  # Angola
    "AG",  # Antigua and Barbuda
    "AI",  # Anguilla
    "AL",  # Albania
    "AM",  # Armenia
    "AR",  # Argentina
    "AT",  # Austria
    "AU",  # Australia
    "AZ",  # Azerbaijan
    "BA",  # Bosnia and Herzegovina
    "BB",  # Barbados
    "BD",  # Bangladesh
    "BE",  # Belgium
    "BF",  # Burkina Faso
    "BG",  # Bulgaria
    "BH",  # Bahrain
    "BI",  # Burundi
    "BJ",  # Benin
    "BM",  # Bermuda
    "BN",  # Brunei
    "BO",  # Bolivia
    "BR",  # Brazil
    "British Sovereign Base Areas",  # British Sovereign Base Areas
    "BS",  # The Bahamas
    "BT",  # Bhutan
    "BW",  # Botswana
    "BY",  # Belarus
    "BZ",  # Belize
    "CA",  # Canada
    "CD",  # Democratic Republic of the Congo
    "CF",  # Central African Republic
    "CG",  # Congo-Brazzaville
    "CH",  # Switzerland
    "CI",  # Côte d'Ivoire
    "CK",  # Cook Islands
    "CL",  # Chile
    "CM",  # Cameroon
    "CN",  # CHINA
    "CO",  # Colombia
    "CR",  # Costa Rica
    "CU",  # Cuba
    "CV",  # Cape Verde
    "CY",  # Cyprus
    "CZ",  # Czechia
    "DE",  # Germany
    "DK",  # Denmark
    "DJ",  # Djibouti
    "DM",  # Dominica
    "DO",  # Dominican Republic
    "DZ",  # Algeria
    "EC",  # Ecuador
    "EE",  # Estonia
    "EG",  # Egypt
    "ER",  # Eritrea
    "ES",  # Spain
    "ET",  # Ethiopia
    "FI",  # Finland
    "FJ",  # Fiji
    "FK",  # Falkland Islands
    "FM",  # Federated States of Micronesia
    "FO",  # Faroe Islands
    "FR",  # France
    "GA",  # Gabon
    "GB",  # United Kingdom
    "GD",  # Grenada
    "GE",  # Georgia
    "GG",  # Guernsey
    "GH",  # Ghana
    "GI",  # Gibraltar
    "GL",  # Greenland
    "GM",  # Gambia
    "GN",  # Guinea
    "GQ",  # Equatorial Guinea
    "GR",  # Greece
    "GS",  # South Georgia and the South Sandwich Islands
    "GT",  # Guatemala
    "GW",  # Guinea-Bissau
    "GY",  # Guyana
    "HN",  # Honduras
    "HR",  # Croatia
    "HT",  # Haiti
    "HU",  # Hungary
    "ID",  # Indonesia
    "IE",  # Ireland
    "IL",  # Israel
    "IM",  # Isle of Man
    "IN",  # India
    "IO",  # British Indian Ocean Territory
    "IQ",  # Iraq
    "IR",  # Iran
    "IS",  # Iceland
    "IT",  # Italy
    "JE",  # Jersey
    "JM",  # Jamaica
    "JO",  # Jordan
    "KE",  # Kenya
    "KG",  # Kyrgyzstan
    "KH",  # Cambodia
    "KI",  # Kiribati
    "KM",  # Comoros
    "KN",  # Saint Kitts and Nevis
    "KR",  # South Korea
    "KP",  # North Korea
    "KW",  # Kuwait
    "KY",  # Cayman Islands
    "KZ",  # Kazakhstan
    "LA",  # Laos
    "LB",  # Lebanon
    "LC",  # Saint Lucia
    "LI",  # Liechtenstein
    "LK",  # Sri Lanka
    "LS",  # Lesotho
    "LR",  # Liberia
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "LV",  # Latvia
    "LY",  # Libya
    "MA",  # Morocco
    "MC",  # Monacos
    "MD",  # Moldova
    "ME",  # Montenegro
    "MG",  # Madagascar
    "MH",  # Marshall Islands
    "MK",  # Macedonia
    "ML",  # Mali
    "MM",  # Myanmar
    "MN",  # Mongolia
    "MR",  # Mauritania
    "MS",  # Montserrat
    "MT",  # Malta
    "MU",  # Mauritius
    "MV",  # Maldives
    "MW",  # Malawi
    "MX",  # Mexico
    "MY",  # Malaysia
    "MZ",  # Mozambique
    "NA",  # Namibia
    "NE",  # Niger
    "NG",  # Nigeria
    "NI",  # Nicaragua
    "NL",  # The Netherlands
    "NO",  # Norway
    "NP",  # Nepal
    "NR",  # Nauru
    "NU",  # Niue
    "NZ",  # New Zealand
    "OM",  # Oman
    "PA",  # Panama
    "PE",  # Peru
    "PG",  # Papua New Guinea
    "PH",  # Philippines
    "PK",  # Pakistan
    "PL",  # Poland
    "PN",  # Pitcairn Islands
    "PS",  # Palestine
    "PT",  # Portugal
    "PW",  # Palau
    "PY",  # Paraguay
    "QA",  # Qatar
    "RO",  # Romania
    "RS",  # Serbia
    "RU",  # Russia
    "RW",  # Rwanda
    "SA",  # Saudi Arabia
    "SB",  # Solomon Islands
    "SC",  # Seychelles
    "SD",  # Sudan
    "SE",  # Sweden
    "SG",  # Singapore
    "SH",  # Saint Helena, Ascension and Tristan da Cunha
    "SI",  # Slovenia
    "SK",  # Slovakia
    "SL",  # Sierra Leone
    "SM",  # San Marino
    "SN",  # Senegal
    "SO",  # Somalia
    "SR",  # Suriname
    "SS",  # South Sudan
    "ST",  # São Tomé and Príncipe
    "SV",  # El Salvador
    "SY",  # Syria
    "SZ",  # Swaziland
    "TC",  # Turks and Caicos Islands
    "TD",  # Chad
    "TG",  # Togo
    "TH",  # Thailand
    "TJ",  # Tajikistan
    "TK",  # Tokelau
    "TL",  # East Timor
    "TM",  # Turkmenistan
    "TN",  # Tunisia
    "TO",  # Tonga
    "TR",  # Turkey
    "TT",  # Trinidad and Tobago
    "TV",  # Tuvalu
    "TW",  # Taiwan
    "TZ",  # Tanzania
    "UA",  # Ukraine
    "UG",  # Uganda
    "US",  # United States of America
    "UY",  # Uruguay
    "UZ",  # Uzbekistan
    "VA",  # Vatican City
    "VC",  # Saint Vincent and the Grenadines
    "VE",  # Venezuela
    "VG",  # British Virgin Islands
    "VN",  # Vietnam
    "VU",  # Vanuatu
    "WS",  # Samoa
    "XK",  # Kosovo
    "YE",  # Yemen
    "ZA",  # South Africa
    "ZM",  # Zambia
    "ZW",  # Zimbabwe
    "الجمهورية العربية الصحراوية الديمقراطية‎‎",  # Western Sahara
]

async def get_relation(conn, **tags):
    tags = "".join(f'["{k.replace("iso","ISO3166-1:alpha2") if (k == "iso" and len(v) == 2) else k.replace("iso","name")}"="{v}"]' for k, v in tags.items())
    dir = Path('tmp/boundary');
    if not dir.is_dir():
        dir.mkdir(parents=True);
    path = Path('tmp') / 'boundary' / tags.replace('/', '_')
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


async def load_country(conn, iso):
    return await get_relation(conn, boundary='administrative', admin_level=2,
                              iso=iso)


@cli
async def process(itl_path: Path=Path('data/boundary.json'),
                  disputed_path: Path=Path('data/disputed.json')):
    conn = await asyncpg.connect(database='pianoforte')
    await register(conn)
    features = []
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
    for idx, name in enumerate(COUNTRIES):
        polygon, properties = await load_country(conn, name)
        if properties['name:en'] == 'Sahrawi Arab Democratic Republic':
            continue
        print(f'''"{properties['name']}",  # {properties['name:en']}''')
        if  'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'IL':
            polygon = await remove_area(conn, polygon, golan)
            west_bank, _ = await get_relation(conn, place="region",
                                              name="الضفة الغربية")
            polygon = await remove_area(conn, polygon, west_bank)
        if  'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'SY':
            polygon = await add_area(conn, polygon, golan)
        if  'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'SS':
            sudan, _ = await load_country(conn, 'SD')  # Sudan
            polygon = await remove_area(conn, polygon, sudan)
        if properties['name:en'] == 'Sudan':
            polygon = await remove_area(conn, polygon, bir_tawil)
        if 'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'EG':
            polygon = await add_area(conn, polygon, bir_tawil)
        if 'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'NP':
            claim, props = await get_relation(conn, type="boundary",
                                              name="Extent of Nepal Claim")
            add_disputed(claim, props)
            polygon = await add_area(conn, polygon, claim)
        if 'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'IN':
            claim, _ = await get_relation(conn, type="boundary",
                                          name="Extent of Nepal Claim")
            polygon = await remove_area(conn, polygon, claim)
        if 'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'CN':
            polygon = await remove_area(conn, polygon, doklam)
        if 'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'BH':
            polygon = await add_area(conn, polygon, doklam)
        if 'ISO3166-1:alpha2' in properties and properties['ISO3166-1:alpha2'] == 'MA':
            # Western Sahara
            esh, props = await get_relation(conn, boundary="disputed",
                                            name="الصحراء الغربية")
            add_disputed(esh, props)
            polygon = await remove_area(conn, polygon, esh)
            features.append({
                'type': 'Feature',
                'geometry': esh.geojson,
                'properties': props
            })
        features.append({
            'type': 'Feature',
            'geometry': polygon.geojson,
            'properties': properties
        })
    await conn.close()
    with itl_path.open('w') as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f)
    with disputed_path.open('w') as f:
        json.dump({'type': 'FeatureCollection', 'features': disputed}, f)


if __name__ == '__main__':
    run()
