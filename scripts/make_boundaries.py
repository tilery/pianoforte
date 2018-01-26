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
    #"DE",  # Germany
    "AD",  # Andorra
    "AO",  # Angola
    "AI",  # Anguilla
    "AG",  # Antigua and Barbuda
    "AR",  # Argentina
    "AU",  # Australia
    "HT",  # Haiti
    "AZ",  # Azerbaijan
    "BB",  # Barbados
    "PW",  # Palau
    "BE",  # Belgium
    "BY",  # Belarus
    "BZ",  # Belize
    "BM",  # Bermuda
    "BO",  # Bolivia
    "BA",  # Bosnia and Herzegovina
    "BW",  # Botswana
    "BR",  # Brazil
    "IO",  # British Indian Ocean Territory
    "British Sovereign Base Areas",  # British Sovereign Base Areas
    "VG",  # British Virgin Islands
    "BN",  # Brunei
    "BF",  # Burkina Faso
    "BI",  # Burundi
    "BJ",  # Benin
    "CV",  # Cape Verde
    "CM",  # Cameroon
    "CA",  # Canada
    "KY",  # Cayman Islands
    "CL",  # Chile
    "CA",  # Vatican City
    "CO",  # Colombia
    "KM",  # Comoros
    "CG",  # Congo-Brazzaville
    "CK",  # Cook Islands
    "CR",  # Costa Rica
    "ME",  # Montenegro
    "CU",  # Cuba
    "CI",  # Côte d'Ivoire
    "DK",  # Denmark
    "DJ",  # Djibouti
    "DM",  # Dominica
    "EC",  # Ecuador
    "EE",  # Estonia
    "SV",  # El Salvador
    "ES",  # Spain
    "SZ",  # Swaziland
    "FK",  # Falkland Islands
    "FR",  # France
    "FO",  # Faroe Islands
    "GA",  # Gabon
    "GM",  # Gambia
    "GH",  # Ghana
    "GI",  # Gibraltar
    "GD",  # Grenada
    "GT",  # Guatemala
    "GG",  # Guernsey
    "GQ",  # Equatorial Guinea
    "GW",  # Guinea-Bissau
    "GN",  # Guinea
    "GY",  # Guyana
    "HN",  # Honduras
    "HR",  # Croatia
    "IN",  # India
    "ID",  # Indonesia
    "IE",  # Ireland
    "IM",  # Isle of Man
    "IT",  # Italy
    "JM",  # Jamaica
    "JE",  # Jersey
    "GL",  # Greenland
    "KE",  # Kenya
    "KI",  # Kiribati
    "CF",  # Central African Republic
    "LV",  # Latvia
    "LS",  # Lesotho
    "LR",  # Liberia
    "LY",  # Liechtenstein
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "MG",  # Madagascar
    "HU",  # Hungary
    "MW",  # Malawi
    "MY",  # Malaysia
    "ML",  # Mali
    "MT",  # Malta
    "MA",  # Morocco
    "MU",  # Mauritius
    "FM",  # Federated States of Micronesia
    "MD",  # Moldova
    "MC",  # Monaco
    "MS",  # Montserrat
    "MZ",  # Mozambique
    "MX",  # Mexico
    "MH",  # Marshall Islands
    "NA",  # Namibia
    "NR",  # Nauru
    "NL",  # The Netherlands
    "NZ",  # New Zealand
    "NI",  # Nicaragua
    "NE",  # Niger
    "NG",  # Nigeria
    "NU",  # Niue
    "NO",  # Norway
    "UZ",  # Uzbekistan
    "PA",  # Panama
    "PG",  # Papua New Guinea
    "PY",  # Paraguay
    "PE",  # Peru
    "PH",  # Philippines
    "PN",  # Pitcairn Islands
    "PL",  # Poland
    "PT",  # Portugal
    "XK",  # Kosovo
    "DO",  # Dominican Republic
    "RO",  # Romania
    "RW",  # Rwanda
    "CD",  # Democratic Republic of the Congo
    "SH",  # Saint Helena, Ascension and Tristan da Cunha
    "KN",  # Saint Kitts and Nevis
    "LC",  # Saint Lucia
    "VC",  # Saint Vincent and the Grenadines
    "SM",  # San Marino
    "CH",  # Switzerland
    "SC",  # Seychelles
    "AL",  # Albania
    "SL",  # Sierra Leone
    "SG",  # Singapore
    "SI",  # Slovenia
    "SK",  # Slovakia
    "SB",  # Solomon Islands
    "SO",  # Somalia
    "ZA",  # South Africa
    "GS",  # South Georgia and the South Sandwich Islands
    "SS",  # South Sudan
    "FI",  # Finland
    "SR",  # Suriname
    "SE",  # Sweden
    "ST",  # São Tomé and Príncipe
    "SN",  # Senegal
    "WS",  # Samoa
    "TZ",  # Tanzania
    "TD",  # Chad
    "BS",  # The Bahamas
    "TL",  # East Timor
    "TG",  # Togo
    "TK",  # Tokelau
    "TO",  # Tonga
    "TT",  # Trinidad and Tobago
    "TC",  # Turks and Caicos Islands
    "TV",  # Tuvalu
    "TR",  # Turkey
    "TM",  # Turkmenistan
    "UA",  # Ukraine
    "UG",  # Uganda
    "GB",  # United Kingdom
    "US",  # United States of America
    "UY",  # Uruguay
    "VU",  # Vanuatu
    "VE",  # Venezuela
    "FJ",  # Fiji
    "VN",  # Vietnam
    "ZM",  # Zambia
    "ZW",  # Zimbabwe
    "IS",  # Iceland
    "AT",  # Austria
    "CZ",  # Czechia
    "GR",  # Greece
    "CY",  # Cyprus
    "BG",  # Bulgaria
    "KG",  # Kyrgyzstan
    "MK",  # Macedonia
    "MN",  # Mongolia
    #"RU",  # Russia
    "RS",  # Serbia
    "TJ",  # Tajikistan
    "KZ",  # Kazakhstan
    "AM",  # Armenia
    "IL",  # Israel
    "AF",  # Afghanistan
    "PS",  # Palestine
    "JO",  # Jordan
    "AE",  # United Arab Emirates
    "الجمهورية العربية الصحراوية الديمقراطية‎‎",  # Western Sahara
    "SA",  # Saudi Arabia
    "SD",  # Sudan
    "IQ",  # Iraq
    "YE",  # Yemen
    "TN",  # Tunisia
    "SY",  # Syria
    "OM",  # Oman
    "LB",  # Lebanon
    "EG",  # Egypt
    "MR",  # Mauritania
    "MV",  # Maldives
    "NP",  # Nepal
    "BD",  # Bangladesh
    "LK",  # Sri Lanka
    "TH",  # Thailand
    "LA",  # Laos
    "BT",  # Bhutan
    "MM",  # Myanmar
    "GE",  # Georgia
    "ET",  # Ethiopia
    "ER",  # Eritrea
    "KH",  # Cambodia
    "BH",  # Bahrain
    "KW",  # Kuwait
    "IR",  # Iran
    "QA",  # Qatar
    "PK",  # Pakistan
    "LY",  # Libya
    "DZ",  # Algeria
    "CN",  # China
    "JP",  # Japan
    "TW",  # Taiwan
    "KR",  # South Korea
    "KP",  # North Korea
]


async def get_relation(conn, **tags):
    tags = "".join(f'["{k.replace("iso","ISO3166-1:alpha2") if (k == "iso" and len(v) == 2) else k.replace("iso","name")}"="{v}"]' for k, v in tags.items())
    dir = Path('tmp/boundary');
    if not dir.is_dir():
        dir.mkdir(parents=True);
    path = Path('tmp') / 'boundary' / tags.replace('/', '_')
    print(tags)
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
