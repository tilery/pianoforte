import:
	env PGHOST=/var/run/postgresql/ imposm3 import -config imposm.conf -diff -read tmp/pbf/egypt-latest.osm.pbf -write -overwritecache -deployproduction
	psql --single-transaction --dbname pianoforte --file tmp/boundary.sql
update:
	env PGHOST=/var/run/postgresql/ imposm3 run -config imposm.conf
boundary:
	python scripts/make_boundaries.py process
	ogr2ogr --config PG_USE_COPY YES -lco GEOMETRY_NAME=geometry -lco DROP_TABLE=IF_EXISTS -f PGDump tmp/boundary.sql data/boundary.json -select name,'name:en','name:fr','name:ar','name:es','name:de','name:ru' -nln itl_boundary
	# Remove transaction management, as it does not cover the DROP TABLE; we'll cover the transaction manually with "psql --single-transaction"
	sed -i.bak '/BEGIN;/d' tmp/boundary.sql
	sed -i.bak '/END;/d' tmp/boundary.sql
	sed -i.bak '/COMMIT;/d' tmp/boundary.sql
	rm tmp/boundary.sql.bak
