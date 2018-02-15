PBF=africa/egypt-latest.osm.pbf
all: boundary download import
download:
	wget --show-progress --directory-prefix=tmp/pbf/ --force-directories --no-host-directories http://download.geofabrik.de/$(PBF)
import: import_imposm import_boundary import_city import_country
import_imposm:
	env PGHOST=/var/run/postgresql/ imposm3 import -config imposm.conf -diff -read tmp/pbf/$(PBF) -write -overwritecache -deployproduction
import_boundary:
	psql --single-transaction --dbname pianoforte --file tmp/boundary.sql
import_city:
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/city.sql data/city.csv -select name,'name:en','name:fr','name:ar',capital,type,prio,ldir -nln city -oo X_POSSIBLE_NAMES=Lon* -oo Y_POSSIBLE_NAMES=Lat* -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed -i.bak '/BEGIN;/d' tmp/city.sql
	sed -i.bak '/END;/d' tmp/city.sql
	sed -i.bak '/COMMIT;/d' tmp/city.sql
	rm tmp/city.sql.bak
	psql --single-transaction --dbname pianoforte --file tmp/city.sql
import_country:
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/country.sql data/country.csv -select name,'name:en','name:fr','name:ar',prio -nln country -oo X_POSSIBLE_NAMES=Lon* -oo Y_POSSIBLE_NAMES=Lat* -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed -i.bak '/BEGIN;/d' tmp/country.sql
	sed -i.bak '/END;/d' tmp/country.sql
	sed -i.bak '/COMMIT;/d' tmp/country.sql
	rm tmp/country.sql.bak
	psql --single-transaction --dbname pianoforte --file tmp/country.sql
update:
	env PGHOST=/var/run/postgresql/ imposm3 run -config imposm.conf
boundary:
	python scripts/make_boundaries.py process
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/boundary.sql data/boundary.json -sql 'SELECT name,"name:en","name:fr","name:ar","name:es","name:de","name:ru","ISO3166-1:alpha2" AS iso FROM boundary' -nln itl_boundary
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed -i.bak '/BEGIN;/d' tmp/boundary.sql
	sed -i.bak '/END;/d' tmp/boundary.sql
	sed -i.bak '/COMMIT;/d' tmp/boundary.sql
	rm tmp/boundary.sql.bak
