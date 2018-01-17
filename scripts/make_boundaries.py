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
    "Andorra",  # Andorra
    "Angola",  # Angola
    "Anguilla",  # Anguilla
    "Antigua and Barbuda",  # Antigua and Barbuda
    "Argentina",  # Argentina
    "Australia",  # Australia
    "Ayiti",  # Haiti
    "Azərbaycan",  # Azerbaijan
    "Barbados",  # Barbados
    "Belau",  # Palau
    "België / Belgique / Belgien",  # Belgium
    "Belize",  # Belize
    "Bermuda",  # Bermuda
    "Bolivia",  # Bolivia
    "Bosna i Hercegovina / Босна и Херцеговина",  # Bosnia and Herzegovina
    "Botswana",  # Botswana
    "Brasil",  # Brazil
    "British Indian Ocean Territory",  # British Indian Ocean Territory
    "British Sovereign Base Areas",  # British Sovereign Base Areas
    "British Virgin Islands",  # British Virgin Islands
    "Brunei Darussalam",  # Brunei
    "Burkina Faso",  # Burkina Faso
    "Burundi",  # Burundi
    "Bénin",  # Benin
    "Cabo Verde",  # Cape Verde
    "Cameroun",  # Cameroon
    "Canada",  # Canada
    "Cayman Islands",  # Cayman Islands
    "Chile",  # Chile
    "Città del Vaticano",  # Vatican City
    "Colombia",  # Colombia
    "Comores Komori جزر القمر",  # Comoros
    "Congo",  # Congo-Brazzaville
    "Kūki 'Āirani",  # Cook Islands
    "Costa Rica",  # Costa Rica
    "Crna Gora / Црна Гора",  # Montenegro
    "Cuba",  # Cuba
    "Côte d’Ivoire",  # Côte d'Ivoire
    "Danmark",  # Denmark
    "Deutschland",  # Germany
    "Djibouti جيبوتي",  # Djibouti
    "Dominica",  # Dominica
    "Ecuador",  # Ecuador
    "Eesti",  # Estonia
    "El Salvador",  # El Salvador
    "España",  # Spain
    "eSwatini Swaziland",  # Swaziland
    "Falkland Islands (Malvinas)",  # Falkland Islands
    "France",  # France
    "Føroyar",  # Faroe Islands
    "Gabon",  # Gabon
    "Gambia",  # Gambia
    "Ghana",  # Ghana
    "Gibraltar",  # Gibraltar
    "Grenada",  # Grenada
    "Guatemala",  # Guatemala
    "Guernsey",  # Guernsey
    "Guinea Ecuatorial",  # Equatorial Guinea
    "Guiné-Bissau",  # Guinea-Bissau
    "Guinée",  # Guinea
    "Guyana",  # Guyana
    "Honduras",  # Honduras
    "Hrvatska",  # Croatia
    "India",  # India
    "Indonesia",  # Indonesia
    "Ireland",  # Ireland
    "Isle of Man",  # Isle of Man
    "Italia",  # Italy
    "Jamaica",  # Jamaica
    "Jersey",  # Jersey
    "Kalaallit Nunaat",  # Greenland
    "Kenya",  # Kenya
    "Kiribati",  # Kiribati
    "Ködörösêse tî Bêafrîka - République Centrafricaine",  # Central African
                                                           # Republic
    "Latvija",  # Latvia
    "Lesotho",  # Lesotho
    "Liberia",  # Liberia
    "Liechtenstein",  # Liechtenstein
    "Lietuva",  # Lithuania
    "Lëtzebuerg",  # Luxembourg
    "Madagasikara",  # Madagascar
    "Magyarország",  # Hungary
    "Malawi",  # Malawi
    "Malaysia",  # Malaysia
    "Mali",  # Mali
    "Malta",  # Malta
    "Maroc ⵍⵎⵖⵔⵉⴱ المغرب",  # Morocco
    "Mauritius",  # Mauritius
    "Micronesia",  # Federated States of Micronesia
    "Moldova",  # Moldova
    "Monaco",  # Monaco
    "Monaco",  # Monaco
    "Montserrat",  # Montserrat
    "Moçambique",  # Mozambique
    "México",  # Mexico
    "M̧ajeļ",  # Marshall Islands
    "Namibia",  # Namibia
    "Naoero",  # Nauru
    "Nederland",  # The Netherlands
    "New Zealand/Aotearoa",  # New Zealand
    "Nicaragua",  # Nicaragua
    "Niger",  # Niger
    "Nigeria",  # Nigeria
    "Niuē",  # Niue
    "Norge",  # Norway
    "Oʻzbekiston",  # Uzbekistan
    "Panamá",  # Panama
    "Papua Niugini",  # Papua New Guinea
    "Paraguay",  # Paraguay
    "Perú",  # Peru
    "Philippines",  # Philippines
    "Pitcairn Islands",  # Pitcairn Islands
    "Polska",  # Poland
    "Portugal",  # Portugal
    "Kosova",  # Kosovo
    "República Dominicana",  # Dominican Republic
    "România",  # Romania
    "Rwanda",  # Rwanda
    "République démocratique du Congo",  # Democratic Republic of the Congo
    "Saint Helena, Ascension and Tristan da Cunha",  # Saint Helena, Ascension
                                                     # and Tristan da Cunha
    "Saint Kitts and Nevis",  # Saint Kitts and Nevis
    "Saint Lucia",  # Saint Lucia
    "Saint Vincent and the Grenadines",  # Saint Vincent and the Grenadines
    "San Marino",  # San Marino
    "Schweiz/Suisse/Svizzera/Svizra",  # Switzerland
    "Sesel",  # Seychelles
    "Shqipëria",  # Albania
    "Sierra Leone",  # Sierra Leone
    "Singapore",  # Singapore
    "Slovenija",  # Slovenia
    "Slovensko",  # Slovakia
    "Solomon Islands",  # Solomon Islands
    "Soomaaliya الصومال",  # Somalia
    "South Africa",  # South Africa
    "South Georgia and South Sandwich Islands",  # South Georgia and the South
                                                 # Sandwich Islands
    "South Sudan",  # South Sudan
    "Suomi",  # Finland
    "Suriname",  # Suriname
    "Sverige",  # Sweden
    "São Tomé e Príncipe",  # São Tomé and Príncipe
    "Sénégal",  # Senegal
    "Sāmoa",  # Samoa
    "Tanzania",  # Tanzania
    "Tchad تشاد",  # Chad
    "The Bahamas",  # The Bahamas
    "Timór Lorosa'e",  # East Timor
    "Togo",  # Togo
    "Tokelau",  # Tokelau
    "Tonga",  # Tonga
    "Trinidad and Tobago",  # Trinidad and Tobago
    "Turks and Caicos Islands",  # Turks and Caicos Islands
    "Tuvalu",  # Tuvalu
    "Türkiye",  # Turkey
    "Türkmenistan",  # Turkmenistan
    "Uganda",  # Uganda
    "United Kingdom",  # United Kingdom
    "United States of America",  # United States of America
    "Uruguay",  # Uruguay
    "Vanuatu",  # Vanuatu
    "Venezuela",  # Venezuela
    "Viti",  # Fiji
    "Việt Nam",  # Vietnam
    "Zambia",  # Zambia
    "Zimbabwe",  # Zimbabwe
    "Ísland",  # Iceland
    "Österreich",  # Austria
    "Česko",  # Czechia
    "Ελλάδα",  # Greece
    "Κύπρος - Kıbrıs",  # Cyprus
    "Беларусь",  # Belarus
    "България",  # Bulgaria
    "Кыргызстан",  # Kyrgyzstan
    "Македонија",  # Macedonia
    "Монгол улс",  # Mongolia
    "Россия",  # Russia
    "Србија",  # Serbia
    "Тоҷикистон",  # Tajikistan
    "Україна",  # Ukraine
    "Қазақстан",  # Kazakhstan
    "Հայաստան",  # Armenia
    "מדינת ישראל",  # Israel
    "افغانستان",  # Afghanistan
    "الأراضي الفلسطينية",  # Palestine
    "الأردن",  # Jordan
    "الإمارات العربيّة المتّحدة",  # United Arab Emirates
    "الجمهورية العربية الصحراوية الديمقراطية‎‎",   # Sahrawi Arab Democratic
                                                 # Republic
    "السعودية",  # Saudi Arabia
    "السودان",  # Sudan
    "العراق",  # Iraq
    "اليمن",  # Yemen
    "تونس",  # Tunisia
    "سوريا",  # Syria
    "عمان",  # Oman
    "لبنان",  # Lebanon
    "مصر",  # Egypt
    "موريتانيا",  # Mauritania
    "ދިވެހިރާއްޖެ",  # Maldives
    "नेपाल",  # Nepal
    "বাংলাদেশ",  # Bangladesh
    "ශ්‍රී ලංකාව இலங்கை",  # Sri Lanka
    "ประเทศไทย",  # Thailand
    "ປະເທດລາວ",  # Laos
    "འབྲུག་ཡུལ་",  # Bhutan
    "မြန်မာ",  # Myanmar
    "საქართველო",  # Georgia
    "ኢትዮጵያ",  # Ethiopia
    "ኤርትራ إرتريا",  # Eritrea
    "ព្រះរាជាណាចក្រ​កម្ពុជា",  # Cambodia
    "‏البحرين‎",  # Bahrain
    "‏الكويت‎",  # Kuwait
    "‏ایران‎",  # Iran
    "‏قطر‎",  # Qatar
    "‏پاکستان‎",  # Pakistan
    "ⵍⵉⴱⵢⴰ ليبيا",  # Libya
    "ⵍⵣⵣⴰⵢⴻⵔ الجزائر",  # Algeria
    "中国",  # China
    "日本",  # Japan
    "臺灣",  # Taiwan
    "대한민국",  # South Korea
    "조선민주주의인민공화국",  # North Korea
]


async def get_relation(conn, **tags):
    tags = "".join(f'["{k}"="{v}"]' for k, v in tags.items())
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
    golan, _ = await get_relation(conn, boundary="administrative",
                                  admin_level="8", name="מועצה אזורית גולן")
    majdal, _ = await get_relation(conn, boundary="administrative",
                                   admin_level="8", name="مجدل شمس")
    return await conn.fetchval(
        'SELECT ST_MakePolygon(ST_ExteriorRing(ST_Union($1::geometry, '
        '$2::geometry)))', golan, majdal)


async def compute_doklam(conn):
    # https://en.wikipedia.org/wiki/en:Doklam?uselang=fr
    shape, _ = await get_relation(conn, boundary="administrative",
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
    return shape


async def remove_area(conn, shape, other):
    return await conn.fetchval(
        'SELECT ST_Difference($1::geometry, $2::geometry)', shape, other)


async def add_area(conn, shape, other):
    return await conn.fetchval(
        'SELECT ST_Union($1::geometry, $2::geometry)', shape, other)


async def load_country(conn, name):
    return await get_relation(conn, boundary='administrative', admin_level=2,
                              name=name)


@cli
async def process(destination: Path):
    conn = await asyncpg.connect(database='pianoforte')
    await register(conn)
    features = []
    # Used more than once.
    golan = await compute_golan(conn)
    doklam = await compute_doklam(conn)
    bir_tawil, _ = await get_relation(conn, type="boundary",
                                      name="بيرطويل (Bir Tawil)")
    for idx, name in enumerate(COUNTRIES):
        polygon, properties = await load_country(conn, name)
        if properties['name:en'] == 'Sahrawi Arab Democratic Republic':
            continue
        print(f'''"{properties['name']}",  # {properties['name:en']}''')
        if properties['name:en'] == 'Israel':
            polygon = await remove_area(conn, polygon, golan)
            west_bank, _ = await get_relation(conn, place="region",
                                              name="الضفة الغربية")
            polygon = await remove_area(conn, polygon, west_bank)
        if properties['name:en'] == 'Syria':
            polygon = await add_area(conn, polygon, golan)
        if properties['name:en'] == 'South Sudan':
            sudan, _ = await load_country(conn, 'السودان')  # Sudan
            polygon = await remove_area(conn, polygon, sudan)
        if properties['name:en'] == 'Sudan':
            polygon = await remove_area(conn, polygon, bir_tawil)
        if properties['name:en'] == 'Egypt':
            polygon = await add_area(conn, polygon, bir_tawil)
        if properties['name:en'] == 'Nepal':
            claim, _ = await get_relation(conn, type="boundary",
                                          name="Extent of Nepal Claim")
            polygon = await add_area(conn, polygon, claim)
        if properties['name:en'] == 'India':
            claim, _ = await get_relation(conn, type="boundary",
                                          name="Extent of Nepal Claim")
            polygon = await remove_area(conn, polygon, claim)
        if properties['name:en'] == 'China':
            polygon = await remove_area(conn, polygon, doklam)
        if properties['name:en'] == 'Bhutan':
            polygon = await add_area(conn, polygon, doklam)
        if properties['name:en'] == 'Morocco':
            # Western Sahara
            esh, props = await get_relation(conn, boundary="disputed",
                                            name="الصحراء الغربية")
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
    with destination.open('w') as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f)


if __name__ == '__main__':
    run()
