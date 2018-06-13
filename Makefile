PBF ?= "africa/egypt-latest.osm.pbf"
all: boundary download import
download:
	wget --show-progress --directory-prefix=tmp/pbf/ --force-directories --no-host-directories http://download.geofabrik.de/$(PBF)
import: import_imposm import_boundary import_city import_country
import_imposm:
	env PGHOST=/var/run/postgresql/ imposm3 import -config imposm.conf -diff -read tmp/pbf/$(PBF) -write -overwritecache -deployproduction
import_boundary:
	wget --show-progress http://nuage.yohanboniface.me/disputed.json -O data/disputed.json
	wget --show-progress http://nuage.yohanboniface.me/boundary.json -O tmp/boundary.json
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/boundary.sql tmp/boundary.json -sql 'SELECT name,"name:en","name:fr","name:ar","name:es","name:de","name:ru","ISO3166-1:alpha2" AS iso FROM boundary' -nln itl_boundary
	psql --dbname pianoforte --file tmp/boundary.sql
import_city:
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/city.sql data/city.csv -select name,'name:en','name:fr','name:ar',capital,type,prio,ldir -nln city -oo X_POSSIBLE_NAMES=Lon* -oo Y_POSSIBLE_NAMES=Lat* -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326
	psql --dbname pianoforte --file tmp/city.sql
import_country:
	wget --show-progress https://raw.githubusercontent.com/tilery/mae-boundaries/master/country.csv -O tmp/country.csv
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/country.sql tmp/country.csv -select name,'name:en','name:fr','name:ar',prio,iso,sov -nln country -oo X_POSSIBLE_NAMES=Lon* -oo Y_POSSIBLE_NAMES=Lat* -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326
	psql --dbname pianoforte --file tmp/country.sql
update:
	env PGHOST=/var/run/postgresql/ imposm3 run -config imposm.conf
