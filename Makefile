import:
	env PGHOST=/var/run/postgresql/ imposm3 import -mapping mapping.yml -read tmp/pbf/lebanon-latest.osm.pbf -connection="postgis:///overcoat" -write -overwritecache -deployproduction
