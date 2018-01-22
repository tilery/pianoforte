import:
	env PGHOST=/var/run/postgresql/ imposm3 import -config imposm.conf -diff -read tmp/pbf/egypt-latest.osm.pbf -write -overwritecache -deployproduction
	psql --single-transaction --dbname pianoforte --file tmp/boundary.sql
update:
	env PGHOST=/var/run/postgresql/ imposm3 run -config imposm.conf
boundary:
	python scripts/make_boundaries.py process
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/boundary.sql tmp/boundary.json -select name,'name:en','name:fr','name:ar' -nln itl_boundary
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed --in-place '/BEGIN;/d' tmp/boundary.sql
	sed --in-place '/END;/d' tmp/boundary.sql
	sed --in-place '/COMMIT;/d' tmp/boundary.sql
