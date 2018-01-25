import:
	env PGHOST=/var/run/postgresql/ imposm3 import -config imposm.conf -diff -read tmp/pbf/egypt-latest.osm.pbf -write -overwritecache -deployproduction
	psql --single-transaction --dbname pianoforte --file tmp/boundary.sql
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/city.sql data/city.csv -select name,'name:en','name:fr','name:ar',capital,type -nln city -oo X_POSSIBLE_NAMES=Lon* -oo Y_POSSIBLE_NAMES=Lat* -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed --in-place '/BEGIN;/d' tmp/city.sql
	sed --in-place '/END;/d' tmp/city.sql
	sed --in-place '/COMMIT;/d' tmp/city.sql
	psql --single-transaction --dbname pianoforte --file tmp/city.sql
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/country.sql data/country.csv -select name,'name:en','name:fr','name:ar' -nln country -oo X_POSSIBLE_NAMES=Lon* -oo Y_POSSIBLE_NAMES=Lat* -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed --in-place '/BEGIN;/d' tmp/country.sql
	sed --in-place '/END;/d' tmp/country.sql
	sed --in-place '/COMMIT;/d' tmp/country.sql
	psql --single-transaction --dbname pianoforte --file tmp/country.sql
update:
	env PGHOST=/var/run/postgresql/ imposm3 run -config imposm.conf
boundary:
	python scripts/make_boundaries.py process
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/boundary.sql tmp/boundary.json -select name,'name:en','name:fr','name:ar' -nln itl_boundary
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed --in-place '/BEGIN;/d' tmp/boundary.sql
	sed --in-place '/END;/d' tmp/boundary.sql
	sed --in-place '/COMMIT;/d' tmp/boundary.sql
